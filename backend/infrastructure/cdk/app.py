"""
AWS CDK Infrastructure for AI Tutor South Africa
=================================================

This defines the cloud infrastructure for the AI Tutor platform.
Deploy with: cdk deploy

Resources:
- API Gateway (zero-rated endpoints)
- Lambda functions (serverless compute)
- DynamoDB (learner profiles, sessions)
- S3 (curriculum resources)
- AWS Bedrock (AI/LLM)
"""

from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_apigateway as apigw,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_bedrock as bedrock,
    CfnOutput
)
from constructs import Construct


class AITutorStack(Stack):
    """
    Main infrastructure stack for AI Tutor South Africa.
    
    Designed for:
    - Serverless (pay per use, scales automatically)
    - Low latency (API Gateway + Lambda)
    - Zero-rated endpoints (whitelist with Vodacom)
    """
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # ============================================
        # DYNAMODB TABLES
        # ============================================
        
        # Learner profiles table
        self.learners_table = dynamodb.Table(
            self, "LearnersTable",
            table_name="ai-tutor-learners",
            partition_key=dynamodb.Attribute(
                name="phone_number",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # For dev - change for prod
        )
        
        # Add GSI for grade-based queries
        self.learners_table.add_global_secondary_index(
            index_name="by-grade",
            partition_key=dynamodb.Attribute(
                name="grade",
                type=dynamodb.AttributeType.NUMBER
            ),
            sort_key=dynamodb.Attribute(
                name="created_at",
                type=dynamodb.AttributeType.STRING
            )
        )
        
        # Sessions table (for USSD/WhatsApp session management)
        self.sessions_table = dynamodb.Table(
            self, "SessionsTable",
            table_name="ai-tutor-sessions",
            partition_key=dynamodb.Attribute(
                name="session_id",
                type=dynamodb.AttributeType.STRING
            ),
            time_to_live_attribute="ttl",  # Auto-expire sessions
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # Progress tracking table
        self.progress_table = dynamodb.Table(
            self, "ProgressTable",
            table_name="ai-tutor-progress",
            partition_key=dynamodb.Attribute(
                name="learner_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # ============================================
        # S3 BUCKETS
        # ============================================
        
        # Curriculum resources bucket
        self.curriculum_bucket = s3.Bucket(
            self, "CurriculumBucket",
            bucket_name="ai-tutor-curriculum",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
        
        # ============================================
        # LAMBDA FUNCTIONS
        # ============================================
        
        # WhatsApp webhook handler
        self.whatsapp_handler = lambda_.Function(
            self, "WhatsAppHandler",
            function_name="ai-tutor-whatsapp-handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("whatsapp/handler"),
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={
                "LEARNERS_TABLE": self.learners_table.table_name,
                "SESSIONS_TABLE": self.sessions_table.table_name,
                "PROGRESS_TABLE": self.progress_table.table_name
            }
        )
        
        # Grant permissions
        self.learners_table.grant_read_write_data(self.whatsapp_handler)
        self.sessions_table.grant_read_write_data(self.whatsapp_handler)
        self.progress_table.grant_read_write_data(self.whatsapp_handler)
        
        # USSD session handler
        self.ussd_handler = lambda_.Function(
            self, "USSDHandler",
            function_name="ai-tutor-ussd-handler",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("ussd/handler"),
            timeout=Duration.seconds(10),  # USSD needs quick response
            memory_size=128,
            environment={
                "SESSIONS_TABLE": self.sessions_table.table_name,
                "LEARNERS_TABLE": self.learners_table.table_name
            }
        )
        
        self.sessions_table.grant_read_write_data(self.ussd_handler)
        self.learners_table.grant_read_data(self.ussd_handler)
        
        # Reasoning Analyzer (core AI function)
        self.reasoning_analyzer = lambda_.Function(
            self, "ReasoningAnalyzer",
            function_name="ai-tutor-reasoning-analyzer",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("backend/lambda/reasoning-analyzer"),
            timeout=Duration.seconds(60),
            memory_size=512,  # More memory for AI processing
            environment={
                "BEDROCK_MODEL_ID": "anthropic.claude-3-5-sonnet-20241022-v2:0"
            }
        )
        
        # Hint Engine
        self.hint_engine = lambda_.Function(
            self, "HintEngine",
            function_name="ai-tutor-hint-engine",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("backend/lambda/hint-engine"),
            timeout=Duration.seconds(30),
            memory_size=256
        )
        
        # Bedrock client
        self.bedrock_client = lambda_.Function(
            self, "BedrockClient",
            function_name="ai-tutor-bedrock-client",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("backend/lambda/bedrock-client"),
            timeout=Duration.seconds(90),
            memory_size=512,
            environment={
                "BEDROCK_MODEL_ID": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "BEDROCK_REGION": "af-south-1"
            }
        )
        
        # ============================================
        # API GATEWAY
        # ============================================
        
        # Main API (zero-rated endpoint)
        self.api = apigw.RestApi(
            self, "AITutorAPI",
            rest_api_name="AI Tutor API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            ),
            deploy_options=apigw.StageOptions(
                stage_name="v1",
                throttling_rate_limit=100,
                throttling_burst_limit=200
            )
        )
        
        # WhatsApp webhook endpoint
        whatsapp_resource = self.api.root.add_resource("whatsapp")
        whatsapp_resource.add_method(
            "POST",
            apigw.LambdaIntegration(self.whatsapp_handler)
        )
        
        # USSD endpoint
        ussd_resource = self.api.root.add_resource("ussd")
        ussd_resource.add_method(
            "POST",
            apigw.LambdaIntegration(self.ussd_handler)
        )
        
        # Health check endpoint
        health_resource = self.api.root.add_resource("health")
        health_resource.add_method(
            "GET",
            apigw.MockIntegration(
                integration_responses=[{
                    "statusCode": "200",
                    "responseTemplates": {
                        "application/json": '{"status": "healthy", "service": "ai-tutor"}'
                    }
                }],
                request_templates={
                    "application/json": '{"statusCode": 200}'
                }
            )
        )
        
        # ============================================
        # OUTPUTS
        # ============================================
        
        CfnOutput(
            self, "ApiEndpoint",
            value=self.api.url,
            description="API Gateway endpoint URL"
        )
        
        CfnOutput(
            self, "WhatsAppWebhookUrl",
            value=f"{self.api.url}whatsapp",
            description="WhatsApp webhook URL"
        )
        
        CfnOutput(
            self, "USSDEndpointUrl",
            value=f"{self.api.url}ussd",
            description="USSD endpoint URL"
        )
        
        CfnOutput(
            self, "LearnersTableName",
            value=self.learners_table.table_name,
            description="DynamoDB table for learner profiles"
        )
        
        CfnOutput(
            self, "CurriculumBucketName",
            value=self.curriculum_bucket.bucket_name,
            description="S3 bucket for curriculum resources"
        )


# ============================================
# DEPLOYMENT INSTRUCTIONS
# ============================================
"""
To deploy this infrastructure:

1. Prerequisites:
   - AWS CLI configured
   - CDK installed: npm install -g aws-cdk
   - Python dependencies: pip install aws-cdk-lib constructs

2. Bootstrap (first time only):
   cdk bootstrap aws://ACCOUNT-ID/af-south-1

3. Deploy:
   cdk deploy --context region=af-south-1

4. After deployment, note the outputs:
   - API endpoint URL
   - WhatsApp webhook URL
   - USSD endpoint URL

5. Configure WhatsApp Business API:
   - Set webhook URL to: {API_URL}/whatsapp
   - Verify token

6. Configure USSD Gateway:
   - Point USSD code (*120*TUTOR#) to: {API_URL}/ussd
   - Work with Vodacom to zero-rate the endpoint

7. Configure AWS Bedrock:
   - Enable Claude 3.5 Sonnet in af-south-1
   - Set up knowledge base with CAPS/IEB curriculum
   - Configure guardrails for content safety
"""
