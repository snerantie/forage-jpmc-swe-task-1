# AI Tutor South Africa

> An intelligent, reasoning-focused AI tutor for South African learners (Grade 1-12), accessible via WhatsApp and USSD, zero-rated on Vodacom network.

## 🎯 Overview

This AI tutor doesn't just provide answers—it **analyzes how learners think**. It identifies reasoning gaps, provides personalized guidance, and helps learners improve their problem-solving skills over time.

### Key Features

- **Reasoning Analysis**: Identifies *where* and *why* a learner's approach went wrong
- **Multi-language Support**: English, IsiZulu, IsiXhosa, Afrikaans, and more
- **CAPS & IEB Aligned**: Aligned to South African curriculum standards
- **Zero-Rated**: Free data access for Vodacom users
- **Dual Channel**: WhatsApp (rich media) and USSD (basic phones)

## 📚 Subjects

| Subject | Grades | Status |
|---------|--------|--------|
| Mathematics | 1-12 | ✅ Pilot |
| Physical Sciences | 10-12 | 🔜 Planned |
| Accounting | 10-12 | 🔜 Planned |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNER INTERACTION LAYER                     │
├─────────────────────┬───────────────────────────────────────────┤
│   WhatsApp Channel  │              USSD Channel                  │
│   (rich media,      │           (text-only, menu-driven)         │
│   images, voice)    │                                           │
└─────────┬───────────┴─────────────────┬─────────────────────────┘
          │                             │
          ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Zero-Rated Endpoints)            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI TUTOR ENGINE (AWS Lambda)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Reasoning    │  │ Personalized │  │ Progress Tracker     │   │
│  │ Analyzer     │  │ Hints Engine │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AWS BEDROCK                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │ Claude 3.5       │  │ Knowledge Base   │  │ Guardrails   │   │
│  │ Sonnet           │  │ (CAPS/IEB Math)  │  │ (Safety)     │   │
│  └──────────────────┘  └──────────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│  ┌──────────────────┐  ┌──────────────────┐                     │
│  │ DynamoDB         │  │ S3               │                     │
│  │ (Learner Profiles│  │ (Curriculum      │                     │
│  │  & Progress)     │  │  Resources)      │                     │
│  └──────────────────┘  └──────────────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Demo Flow

### WhatsApp Experience
```
Learner: "I'm stuck on this problem: 2x + 5 = 13. Help me solve it."

AI Tutor: "I'd love to help you think through this! 🎓

Before I give you any hints, tell me: what do you think the first step should be?"

Learner: "I think I should add 13 and 5 together"

AI Tutor: "Interesting thinking! Let me help you see this differently.

You have 2x + 5 = 13. The goal is to find x alone.

Think of it like a balance scale ⚖️. On the left you have '2x + 5', 
on the right you have '13'.

If you add 13 and 5, which side of the scale would change?

💡 Hint: We want to get x by itself. What's 'in the way' of x?"
```

### USSD Experience
```
*120*TUTOR# 

Welcome to AI Tutor! 📚
1. Mathematics
2. Help
3. My Progress

> 1

Select your grade:
1. Grade 8
2. Grade 9
3. Grade 10
...

> 3

Today's Topic: Linear Equations
1. Learn
2. Practice
3. Ask Question

> 3

Type your question:
(160 chars max)
```

## 🧠 Reasoning Analysis Engine

The core innovation - analyzing *how* learners think, not just *what* they answer.

```python
# Example: Reasoning Analysis Output
{
  "learner_response": "I think I should add 13 and 5 together",
  "analysis": {
    "misconception_detected": "inverse_operation_confusion",
    "reasoning_gap": "Learner is treating the equation as a left-to-right calculation 
                       rather than maintaining equality balance",
    "severity": "foundational",
    "related_concepts": ["equation_balance", "inverse_operations"]
  },
  "personalized_response": {
    "approach": "socratic_questioning",
    "hint_level": 1,
    "analogy": "balance_scale",
    "next_step": "Ask learner to identify what's 'in the way' of isolating x"
  }
}
```

## 📂 Project Structure

```
ai-tutor-sa/
├── README.md
├── architecture/
│   └── system-architecture.drawio.png
├── backend/
│   ├── lambda/
│   │   ├── reasoning-analyzer/
│   │   ├── hint-engine/
│   │   └── progress-tracker/
│   └── infrastructure/
│       └── cdk/
├── whatsapp/
│   └── webhook-handler/
├── ussd/
│   └── session-handler/
├── curriculum/
│   ├── caps/
│   │   └── mathematics/
│   └── ieb/
│       └── mathematics/
├── demo/
│   ├── scenarios/
│   └── mock-responses/
└── docs/
    ├── PRD.md
    └── demo-script.md
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| AI/LLM | AWS Bedrock (Claude 3.5 Sonnet) |
| Backend | AWS Lambda, API Gateway |
| Database | DynamoDB, S3 |
| WhatsApp | WhatsApp Business API |
| USSD | USSD Gateway Provider |
| Infrastructure | AWS CDK |
| Integrations | n8n (optional) or native AWS |

## 🎬 Demo Presentation

See `docs/demo-script.md` for the full presentation walkthrough.

---

## 🇿🇦 Built for South African Learners

This project is designed to address the unique challenges of education in South Africa:
- Data costs are a barrier → Zero-rated access
- Multiple languages → Multi-language support
- Diverse curricula → CAPS and IEB alignment
- Varying device access → WhatsApp + USSD channels
- Need for quality tutoring → AI-powered personalized learning

---

*Developed for the [Hackathon Name] Finals*
