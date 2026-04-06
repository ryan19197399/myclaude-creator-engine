# Package Your Expertise as an Installable Advisor

You don't need to write code. You need expertise worth sharing.

The frameworks you've built, the decision-making patterns you've refined over years, the things you explain to every new client — those belong in a tool that anyone can install and use. This guide shows you exactly how to build it.

---

## Understand What You're Creating

The product you'll build is called a **mind** — an installable knowledge advisor.

When someone installs your mind, Claude Code gains your expertise. Your frameworks. Your mental models. Your pattern recognition. They ask Claude a question in your domain, and it responds the way you would — with your approach, your nuance, your depth.

Think of it as the difference between a generalist consultant and a specialist you trust completely. Claude is already a capable generalist. Your mind turns it into the specialist.

**What minds look like in practice:**

- A brand strategist builds a positioning advisor. Her clients install it, describe their company, and get positioning guidance that sounds like her — because it draws on her methodology.
- A business coach packages his six-step growth framework. His community installs it and works through the framework with Claude as the guide.
- A UX researcher creates an advisor that applies her evaluation rubric. Her team uses it on every project without scheduling time with her.

You don't need technical knowledge to build any of these. The engine asks the questions; you answer them.

---

## Choose Your Depth Before You Start

Minds come in two forms. The engine will recommend one based on your domain, but it helps to understand the difference.

| Depth | What It Is | Best For |
|:------|:-----------|:---------|
| **Advisory** | Focused guidance in one area, clear and direct | A single methodology, a specific framework, a defined process |
| **Cognitive** | Deep, layered expertise with multiple reasoning patterns | A full professional discipline, a complex domain with many facets |

If this is your first advisor, start with Advisory. A focused, well-built advisor is more valuable than an ambitious one that tries to cover everything.

---

## Build Your First Advisor — A Complete Walkthrough

This example follows Sofia, a brand positioning strategist, building her first advisor. Your steps are identical — only the content changes.

### Step 1: Research what Claude already knows

```
/scout brand-positioning
```

This takes two minutes and tells you something valuable: where Claude is already competent in your domain, and where it falls short. You're building where it falls short.

Sofia's scout result looks like this:

```
Scout Report: brand-positioning
What Claude handles well: general brand definitions, copywriting frameworks,
                          competitor analysis basics.
Where it struggles: differentiation in crowded markets, emotional positioning
                    for B2B, repositioning existing brands without losing
                    existing customers.
Gap Score: 41% — strong opportunity for a specialist advisor.
Recommendation: Advisory mind (focused on differentiation and repositioning).
```

That 41% gap is exactly where Sofia's ten years of experience lives.

### Step 2: Create your advisor

```
/create minds
```

The engine asks you three discovery questions. No jargon, no technical setup — just conversation.

- "What's the area of expertise this advisor covers?"
- "Who will use it? What do they typically need help with?"
- "What makes your approach different from the standard advice in this space?"

Sofia answers in plain language. The engine generates a complete structure — a skeleton with clearly labeled sections, each one waiting for her thinking.

### Step 3: Fill it with your knowledge

```
/fill
```

This is the heart of the process. The engine becomes an interviewer. It walks through each section of your advisor and asks you targeted questions about your actual thinking.

For Sofia's positioning advisor, the questions sound like this:

- "Walk me through how you diagnose a positioning problem. What do you look for first?"
- "What are the three most common mistakes brands make when trying to differentiate in a crowded market?"
- "Describe a repositioning situation where the obvious move was wrong. What did you do instead?"
- "When a client pushes back on a positioning recommendation, how do you handle it?"

Sofia talks. The engine writes. She reviews, adjusts, adds details. The sections fill up with her actual methodology.

If she gets stuck on a section, she says so. The engine can brainstorm with her, or it can search for current thinking in that area and show her what it finds before she decides what to include.

A completed section looks like this:

```
## Diagnosing a Positioning Problem

Start by asking who the brand is currently positioned for — not who they say
their audience is, but who actually buys from them and why. There's almost
always a gap.

The three warning signs that positioning needs work:
1. The sales team describes the product differently than marketing does
2. Customers use the product in ways the brand didn't intend or anticipate
3. The brand wins on price more than on preference

When you see all three, you're not dealing with a messaging problem.
You're dealing with an identity problem, and messaging fixes will make it worse.
```

That's Sofia's voice. That's her framework. That's what gets installed.

### Step 4: Check the quality

```
/validate
```

The engine scores your advisor and shows you what it found. You don't need to understand the technical scoring — the output is plain language.

```
Your advisor scores 84% — close to Premium (85%).

Strong areas:
  Your methodology section is detailed and specific.
  Your anti-patterns are the best part — keep them.

One gap:
  The "Getting Started" section is thin. Users don't know how to
  begin a conversation with your advisor. Add 2-3 example prompts
  that show them how to engage it.

Fix that one section and you'll cross Premium.
```

Sofia adds three example prompts. She re-runs `/validate`. Score: 87%. Premium.

### Step 5: Share your work

```
/publish
```

The engine packages everything and publishes it to the marketplace. From this point, anyone can install Sofia's advisor with one command:

```
myclaude install sofia-brand-positioning
```

When they install it, they get exactly what Sofia built — her frameworks, her patterns, her anti-patterns, her examples. Claude becomes a version of her domain expertise, available any time, as many times as needed.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  ✦ sofia-brand-positioning is live                  │
│                                                     │
│  research → draft → refine → verify → launch        │
│                                          ●          │
│                                                     │
│  Baseline delta: +41 points vs Claude vanilla       │
│  Quality: Premium (87%)                             │
│  Install: myclaude install sofia-brand-positioning   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## What "Premium Quality" Means in Plain Terms

Quality tiers sound technical. Here's what they actually measure.

| Quality Level | What It Means |
|:--------------|:--------------|
| **Verified (75%+)** | Your advisor is complete and works as intended. Good for personal use and sharing with people who know your work. |
| **Premium (85%+)** | Your advisor is thorough, well-structured, and clear enough that strangers can use it without needing to ask you questions. |
| **Elite (92%+)** | Your advisor is deep, nuanced, and validated against real behavioral scenarios. The standard for professional distribution. |

Most first advisors land at Verified naturally. With one or two focused improvements, Premium is within reach in the same session.

---

## Tips That Make the Difference

**Start with what you teach, not what you know.**
If you explain the same framework to every client at the start of an engagement, that framework is your first advisor. It's already structured in your head. The engine just captures it.

**Focused beats comprehensive.**
An advisor that does one thing exceptionally well is more useful — and easier to build — than one that tries to cover an entire profession. Sofia's advisor doesn't cover all of brand strategy. It covers the specific problem she's best at solving.

**Your anti-patterns are your secret weapon.**
The things you tell clients NOT to do, the mistakes you've seen over and over — those are uniquely yours. General advice is available everywhere. Hard-won warnings are not. Fill this section generously.

**Use the scout results to guide you.**
If the scout found that Claude already handles an area well, spend less time on it. Pour your depth into the gaps. That's where your advisor creates real value.

---

**Next:** [Getting Started](../getting-started.md) · [Frequently Asked Questions](../faq.md) · [All Commands](../reference/commands.md)
