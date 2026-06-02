# AI Tutor South Africa - Visual Aids for Presentation

## ARCHITECTURE DIAGRAM (Text-Based)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                         AI TUTOR SOUTH AFRICA                              ║
║                   System Architecture Overview                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                          LEARNER INTERACTION LAYER                          │
│                                                                             │
│    ┌─────────────────────────────┐      ┌─────────────────────────────┐    │
│    │      📱 WHATSAPP            │      │       📞 USSD               │    │
│    │                             │      │                             │    │
│    │  • Rich media support       │      │  • Works on ANY phone       │    │
│    │  • Images & voice notes     │      │  • Text-only (160 chars)    │    │
│    │  • Interactive sessions     │      │  • Menu-driven navigation   │    │
│    │  • Smartphones only         │      │  • Basic phones supported   │    │
│    │                             │      │                             │    │
│    │  Vodacom Zero-Rated ✅      │      │  Vodacom Zero-Rated ✅      │    │
│    └──────────────┬──────────────┘      └──────────────┬──────────────┘    │
│                   │                                     │                   │
└───────────────────┼─────────────────────────────────────┼───────────────────┘
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API GATEWAY (AWS)                                   │
│                                                                             │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │  Endpoint: https://api.aitutor.co.za                              │   │
│    │  • Zero-rated endpoints whitelisted by Vodacom                    │   │
│    │  • Rate limiting: 100 requests/second                             │   │
│    │  • CORS enabled for cross-origin requests                         │   │
│    │  • Authentication via WhatsApp signature verification             │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI TUTOR ENGINE (AWS Lambda)                          │
│                                                                             │
│    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│    │   🧠            │  │   💡            │  │   📊            │          │
│    │   REASONING     │  │   HINT          │  │   PROGRESS      │          │
│    │   ANALYZER      │  │   ENGINE        │  │   TRACKER       │          │
│    │                 │  │                 │  │                 │          │
│    │  Detects        │  │  Progressive    │  │  Learner        │          │
│    │  misconceptions │  │  hints (1-4)    │  │  profiles       │          │
│    │  & reasoning    │  │  tailored to    │  │  & progress     │          │
│    │  gaps           │  │  learner level  │  │  tracking       │          │
│    └────────┬────────┘  └────────┬────────┘  └────────┬────────┘          │
│             │                    │                    │                   │
└─────────────┼────────────────────┼────────────────────┼───────────────────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AWS BEDROCK                                        │
│                                                                             │
│    ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐  │
│    │   🤖 CLAUDE 3.5     │  │   📚 KNOWLEDGE      │  │   🛡️ GUARDRAILS │  │
│    │   SONNET            │  │   BASE              │  │                 │  │
│    │                     │  │                     │  │                 │  │
│    │  • Primary AI model │  │  • CAPS curriculum  │  │  • Content      │  │
│    │  • Socratic method  │  │  • IEB curriculum   │  │    safety       │  │
│    │  • Multi-language   │  │  • Grade 1-12       │  │  • Age-         │  │
│    │  • Reasoning        │  │  • Mathematics      │  │    appropriate  │  │
│    │                     │  │  • Physics          │  │  • No harmful   │  │
│    │                     │  │  • Accounting       │  │    content      │  │
│    └─────────────────────┘  └─────────────────────┘  └─────────────────┘  │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                       │
│                                                                             │
│    ┌─────────────────────────────────┐  ┌─────────────────────────────┐    │
│    │   📊 DYNAMODB                   │  │   📁 S3                     │    │
│    │                                 │  │                             │    │
│    │   Tables:                       │  │   Buckets:                  │    │
│    │   • learners (profiles)         │  │   • curriculum-resources    │    │
│    │   • sessions (active)           │  │   • caps-mathematics        │    │
│    │   • progress (tracking)         │  │   • ieb-mathematics         │    │
│    │   • achievements (badges)       │  │   • problem-sets            │    │
│    │                                 │  │                             │    │
│    │   Features:                     │  │   Features:                 │    │
│    │   • Auto-scaling                │  │   • Versioning              │    │
│    │   • TTL for sessions            │  │   • Encrypted at rest       │    │
│    │   • Global indexes              │  │   • CDN for speed           │    │
│    └─────────────────────────────────┘  └─────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## REASONING ANALYSIS FLOW

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                   REASONING ANALYSIS ENGINE                                ║
║            The Core Innovation of AI Tutor South Africa                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    PROBLEM: 2x + 5 = 13                                                     │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    LEARNER SAYS:                                                            │
│    "I think I should add 13 and 5 together"                                │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │                    🧠 REASONING ANALYZER                          │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│    DETECTED:                                                                │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │  Misconception: inverse_operation_confusion                       │   │
│    │  Reasoning Gap:  Treating equation as left-to-right calculation   │   │
│    │                   instead of maintaining equality balance          │   │
│    │  Severity:       foundational                                     │   │
│    │  Confidence:     85%                                              │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │                    💡 HINT ENGINE                                 │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│    GENERATES RESPONSE (Socratic Method):                                    │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │  "Interesting thinking! Let me help you see this differently.     │   │
│    │   Think of it like a balance scale ⚖️. You have 2x+5 on the      │   │
│    │   left, 13 on the right. What's 'in the way' of x?"              │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│    WHY THIS WORKS:                                                          │
│    ┌───────────────────────────────────────────────────────────────────┐   │
│    │  ✅ Acknowledges learner's thinking (builds confidence)           │   │
│    │  ✅ Uses analogy (balance scale) to visualize concept             │   │
│    │  ✅ Asks question to guide discovery                              │   │
│    │  ✅ NEVER gives the answer directly                               │   │
│    └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## PROGRESSIVE HINT SYSTEM

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    PROGRESSIVE HINT SYSTEM                                 ║
║         Hints Get More Specific as Learner Needs More Help                ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    LEVEL 1: PROBING QUESTION                                               │
│    ══════════════════════════                                               │
│    "What do you think is the first step?"                                  │
│                                                                             │
│    🎯 Goal: Understand learner's thinking                                  │
│    💡 Approach: Open-ended question                                        │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ Still stuck?
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    LEVEL 2: CONCEPTUAL HINT                                                │
│    ══════════════════════════                                               │
│    "Think of a balance scale ⚖️. What's 'in the way' of x?"               │
│                                                                             │
│    🎯 Goal: Provide mental model                                           │
│    💡 Approach: Analogy or concept explanation                             │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ Still stuck?
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    LEVEL 3: PROCEDURAL HINT                                                │
│    ══════════════════════════                                               │
│    "Try subtracting 5 from BOTH sides. What do you get?"                   │
│                                                                             │
│    🎯 Goal: Guide specific action                                          │
│    💡 Approach: Step-by-step suggestion                                    │
│                                                                             │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │ Still stuck?
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    LEVEL 4: WORKED EXAMPLE                                                 │
│    ══════════════════════════                                               │
│    "Let me show you a similar problem:                                     │
│     3x + 7 = 19                                                            │
│     Step 1: Subtract 7 from both sides... "                                │
│                                                                             │
│    🎯 Goal: Show complete worked solution                                  │
│    💡 Approach: Model problem-solving process                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

  KEY PRINCIPLE: Learners EARN the answer through guided discovery
  
═══════════════════════════════════════════════════════════════════════════════
```

---

## WHATSAPP VS USSD COMPARISON

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                 DUAL CHANNEL ACCESS STRATEGY                               ║
║        Reaching Every South African Learner, Regardless of Device         ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┐  ┌─────────────────────────────────────┐
│         📱 WHATSAPP                 │  │         📞 USSD                     │
├─────────────────────────────────────┤  ├─────────────────────────────────────┤
│                                     │  │                                     │
│  DEVICES:                           │  │  DEVICES:                           │
│  • Smartphones only                 │  │  • ANY phone (even Nokia 3310)      │
│  • Requires app installation        │  │  • No app needed                    │
│                                     │  │  • Built into phone                 │
│  FEATURES:                          │  │                                     │
│  • Rich media (images, voice)       │  │  FEATURES:                          │
│  • Long messages                    │  │  • Text only (160 chars/screen)     │
│  • Interactive buttons              │  │  • Menu-driven navigation           │
│  • Message history                  │  │  • Session-based (3 min timeout)    │
│                                     │  │                                     │
│  USER EXPERIENCE:                   │  │  USER EXPERIENCE:                   │
│  • Conversational                   │  │  • Structured menus                 │
│  • Visual learning aids             │  │  • Quick interactions               │
│  • Problem photos                   │  │  • Multiple choice                  │
│                                     │  │                                     │
│  BEST FOR:                          │  │  BEST FOR:                          │
│  • Complex problems                 │  │  • Quick practice                   │
│  • Visual explanations              │  │  • Basic phones                     │
│  • Learners with smartphones        │  │  • Rural areas                      │
│                                     │  │                                     │
│  COST:                              │  │  COST:                              │
│  🆓 Zero-rated on Vodacom           │  │  🆓 Zero-rated on Vodacom           │
│                                     │  │                                     │
└─────────────────────────────────────┘  └─────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

  📊 SOUTH AFRICA MOBILE LANDSCAPE:
  
  • 90%+ mobile penetration
  • ~60% smartphone users (growing)
  • ~40% basic/feature phones
  • WhatsApp: Most used messaging app
  
  🎯 OUR STRATEGY: Both channels to reach EVERY learner

═══════════════════════════════════════════════════════════════════════════════
```

---

## COMPETITIVE COMPARISON

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                    COMPETITIVE ADVANTAGE                                   ║
║         Why AI Tutor South Africa is Different                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

┌────────────────┬────────────────────┬────────────────────┐
│   FEATURE      │  TRADITIONAL AI    │   AI TUTOR SA      │
│                │     TUTORS         │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  REASONING     │  ❌ Checks answer  │  ✅ Analyzes WHY   │
│  ANALYSIS      │     only           │     learner thinks │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  TEACHING      │  ❌ Gives answers  │  ✅ Socratic       │
│  METHOD        │     directly       │     method         │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  ACCESS        │  ❌ Requires       │  ✅ Zero-rated     │
│                │     data/internet  │     on Vodacom     │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  DEVICES       │  ❌ Smartphone     │  ✅ ANY phone      │
│                │     only           │     (USSD)         │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  LANGUAGE      │  ❌ English only   │  ✅ 11 official    │
│                │                    │     SA languages   │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  CURRICULUM    │  ❌ Generic/US     │  ✅ CAPS & IEB     │
│                │     curriculum     │     aligned        │
│                │                    │                    │
├────────────────┼────────────────────┼────────────────────┤
│                │                    │                    │
│  CONTEXT       │  ❌ Generic        │  ✅ South African  │
│                │     examples       │     context        │
│                │                    │     (taxis, etc.)  │
│                │                    │                    │
└────────────────┴────────────────────┴────────────────────┘

═══════════════════════════════════════════════════════════════════════════════

  🏆 OUR UNIQUE VALUE PROPOSITION:
  
  "Traditional AI tutors give answers. We build thinkers."
  
  This is how we create independent problem-solvers who can tackle
  ANY problem, not just the ones they've seen before.

═══════════════════════════════════════════════════════════════════════════════
```
