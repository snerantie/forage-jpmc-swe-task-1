# AI Tutor South Africa - Product Requirements Document

## Overview

An AI-powered mathematics tutor for South African learners (Grades 1-12), accessible via WhatsApp and USSD, zero-rated on Vodacom network.

## Problem Statement

- South Africa has a mathematics education crisis
- Learner-to-teacher ratios are high (often 40:1+)
- Private tutoring is expensive (R200-R500/hour)
- Data costs prevent access to online learning platforms
- Language barriers in education

## Solution

An AI tutor that:
1. **Analyzes reasoning** - Not just checking answers, but understanding HOW learners think
2. **Guides discovery** - Uses Socratic method to build problem-solving skills
3. **Is accessible** - Works on any phone via WhatsApp and USSD
4. **Is free to use** - Zero-rated on Vodacom (no data costs)

## Target Users

| Segment | Description | Primary Channel |
|---------|-------------|-----------------|
| Primary (Gr 1-7) | Young learners needing visual support | WhatsApp |
| Senior (Gr 8-9) | Building foundational skills | Both |
| FET (Gr 10-12) | Exam preparation | WhatsApp |

## Core Features

### 1. Reasoning Analysis Engine ⭐ (Key Innovation)

The system doesn't just check if an answer is right or wrong. It analyzes the learner's approach:

```
Learner: "I think I should add 13 and 5 together"
System: Detects "inverse_operation_confusion"
        Provides targeted guidance using balance scale analogy
```

**Misconceptions Detected:**
- Inverse operation confusion
- Sign errors
- Order of operations mistakes
- Equals sign misunderstanding
- Procedural gaps

### 2. Progressive Hint System

Hints are NOT one-size-fits-all:

| Level | Type | Example |
|-------|------|---------|
| 1 | Probing Question | "What do you think is the first step?" |
| 2 | Conceptual Hint | "Think of a balance scale ⚖️" |
| 3 | Procedural Hint | "Try subtracting 5 from both sides" |
| 4 | Worked Example | Shows similar problem solved |

### 3. Progress Tracking

- Problems attempted/solved
- Accuracy by topic
- Improvement areas
- Streak tracking for motivation
- Achievement badges

### 4. Multi-language Support

- English
- IsiZulu
- IsiXhosa
- Afrikaans
- Sepedi
- Setswana
- More planned

### 5. CAPS & IEB Alignment

All content aligned to South African curriculum standards.

## Technical Architecture

```
WhatsApp/USSD → API Gateway → Lambda → AWS Bedrock (Claude)
                                ↓
                            DynamoDB (Progress)
```

### Technology Stack

| Component | Technology |
|-----------|------------|
| AI/LLM | AWS Bedrock (Claude 3.5 Sonnet) |
| Backend | AWS Lambda |
| API | API Gateway |
| Database | DynamoDB |
| Storage | S3 |
| Messaging | WhatsApp Business API |
| USSD | USSD Gateway Provider |
| IaC | AWS CDK |

## Success Metrics

| Metric | Target (6 months) |
|--------|-------------------|
| Active Learners | 10,000 |
| Problems Solved | 100,000 |
| Average Accuracy Improvement | +20% |
| Session Completion Rate | >70% |
| User Satisfaction | >4.0/5.0 |

## MVP Scope (Hackathon Demo)

For the finals presentation:

1. ✅ WhatsApp mock demonstrating reasoning analysis
2. ✅ USSD flow showing basic interaction
3. ✅ Progress tracking display
4. ✅ Architecture documentation

## Future Roadmap

### Phase 1 (Post-Hackathon)
- Production Bedrock integration
- WhatsApp Business API setup
- Vodacom zero-rating partnership

### Phase 2
- Image recognition (snap photo of problem)
- Voice message support
- Parent/guardian reports

### Phase 3
- Expand to Physical Sciences
- Expand to Accounting
- School dashboard for teachers

## Zero-Rating Implementation

To achieve zero-rating with Vodacom:

1. Register as educational service provider
2. Submit API endpoints for whitelisting
3. Implement rate limiting per user
4. Add Vodacom header verification
5. Regular usage reporting

## Cost Estimates

### AWS Costs (Monthly, 10K users)

| Service | Estimated Cost |
|---------|---------------|
| Lambda | $50 |
| API Gateway | $30 |
| DynamoDB | $25 |
| Bedrock | $200 |
| **Total** | **~$305/month** |

### Per-User Cost
~$0.03 per learner per month

---

*Built for South African learners 🇿🇦*
