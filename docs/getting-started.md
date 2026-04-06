# Getting Started

Create your first Claude Code product in one sitting — from zero to published on the marketplace.

This guide walks you through every step. You will see exactly what to type, what the engine shows you, and what happens next. By the end, you will have a working product that anyone can install.

**Time:** 15–30 minutes for a simple skill. Longer for deep products like cognitive minds.

---

## Before You Start

You need two things:

1. **[Claude Code](https://claude.ai/download)** — CLI, desktop app, or IDE extension
2. **[MyClaude CLI](https://myclaude.sh)** — `npm i -g @myclaude-cli/cli` (needed for publishing)

If you already have both, skip to Step 1.

---

## Step 1 — Install the Engine
```
○ install → ○ onboard → ○ scout → ○ create → ○ fill → ○ validate → ○ publish
▲
```

```bash
myclaude install studio-engine
```

Or clone manually:

```bash
git clone https://github.com/myclaude-sh/myclaude-creator-engine
cd myclaude-creator-engine && claude
```

When Claude Code starts, the engine loads automatically. You will see a welcome dashboard confirming the version and your setup status.

---

## Step 2 — Set Up Your Profile

```
/onboard
```

The engine asks about your expertise, goals, and how you like to work. This takes about 60 seconds.

**What you will see:**

```
┌─ MyClaude Studio Engine ───────────────────────┐
│                                                 │
│  Welcome. This engine turns your expertise      │
│  into tools anyone can install and use.         │
│                                                 │
│  Let's set up your profile — 60 seconds.        │
│                                                 │
└─────────────────────────────────────────────────┘
```

The engine will ask 2–3 questions, then create your creator profile. Everything downstream — language, vocabulary, guidance depth — adapts based on what you tell it here.

> **Tip:** You can update your profile anytime by running `/onboard` again.

---

## Step 3 — Decide What to Build

You have two paths:

**Path A — You know what you want to build:**
Skip to Step 4 and run `/create [type]` directly.

**Path B — You want the engine to help you decide:**

```
/scout your-domain
```

Replace `your-domain` with your area of expertise — `marketing-strategy`, `kubernetes-security`, `financial-modeling`, anything.

**What the scout does:**
1. Tests what Claude already knows about your domain
2. Identifies gaps — things Claude can't do well alone
3. Scans the marketplace for existing tools
4. Recommends exactly what to build and which product type to use

**Example output:**

```
Scout Report: kubernetes-security
─────────────────────────────────

Claude baseline: 67% coverage (strong on concepts, weak on
operational patterns, attack paths, and compliance mapping)

Gaps found: 11
  - CIS benchmark validation procedures
  - Attack path reasoning from misconfigured RBAC
  - Runtime threat detection workflows
  - Compliance mapping (SOC2, PCI-DSS for K8s)
  ...

Marketplace: 0 existing products in this domain

Recommendation: Create a cognitive mind (depth: cognitive)
  This domain has enough depth for a 5-layer advisor.
  Estimated baseline delta: +33 points vs Claude vanilla.
```

The scout report is saved and automatically feeds into `/create` and `/fill` — so nothing is lost.

---

## Step 4 — Create Your Product
```
● install → ● onboard → ● scout → ○ create → ○ fill → ○ validate → ○ publish
                                   ▲
```

```
/create skill          # for a focused tool
/create minds          # for a knowledge advisor
/create workflow       # for a methodology framework
/create squad          # for a multi-agent team
```

Pick the type that matches what you want to build. Not sure? The engine will ask clarifying questions and suggest the right one.

**What happens:**
The engine generates a complete product structure with guided annotations in every section. These annotations explain what belongs there and why — you will replace them with your content in the next step.

**What you will see:**

```
✦ k8s-security-advisor is born!

  Scaffold ready. 7 sections with guided annotations.
  Your expertise goes in next — run /fill to start.

  ○ scout → ● create → ○ fill → ○ validate → ○ package → ○ publish
                ▲ you are here
```

---

## Step 5 — Fill It With Your Expertise

```
/fill
```

This is where the engine becomes your writing partner. It walks through each section of your product, asking targeted questions about your domain.

**What the conversation looks like:**

```
── Section 1/7: Core Identity ──
What is this product's primary purpose?
What problem does it solve that Claude can't solve alone?
```

You answer in plain language. The engine writes the structured content based on your answers.

```
── Section 3/7: Reasoning Engine ──
Walk me through how you approach a K8s security audit.
What's the first thing you check? What comes next?
```

The engine is not filling in templates — it is asking you domain questions and converting your expertise into structured, activatable content.

**Progress tracking:**

```
Progress: 5/7 sections (71%)
Estimated quality: ~89% (Premium)
```

When all sections are filled, the engine automatically runs a quick quality check and shows your score.

> **Tip:** If you get stuck on a section, say "I'm not sure" — the engine will brainstorm with you, or offer to research the topic with web search.

---

## Step 6 — Validate Quality
```
● install → ● onboard → ● scout → ● create → ● fill → ○ validate → ○ publish
                                                        ▲
```

```
/validate
```

Your product is scored against 20 structural patterns across three tiers:

| Tier | Score | What It Means |
|:-----|:------|:-------------|
| **Verified** | >= 75% | Functional, documented, core patterns present |
| **Premium** | >= 85% | Professional craft — advanced structural patterns |
| **Elite** | >= 92% | State-of-the-art — deep structural quality |

**What you will see if it passes:**

```
READY — 100% (target: 85%)
20/20 structural patterns passing.

  ✦ Elite quality. Craft verified.
```

**What you will see if it needs work:**

```
NEEDS WORK — 72% (target: 85%)
Top 3 fixes:
  1. Anti-patterns: 2 found, need 5
  2. Quality gate: criteria must be verifiable, not aspirational
  3. References: activation protocol must load at least one file

Fix these, then re-run /validate.
```

The engine tells you exactly what to fix, with specific instructions. No guessing.

---

## Step 7 — Test (Premium and Elite products)

```
/test
```

If your product targets Premium or Elite quality, behavioral testing is required. The engine runs three scenarios in an isolated sandbox:

1. **Happy path** — Does it work correctly in normal conditions?
2. **Edge case** — Does it handle unusual inputs gracefully?
3. **Adversarial** — Does it maintain quality under stress?

This step is optional for Verified-tier products.

---

## Step 8 — Package and Publish
```
● install → ● onboard → ● scout → ● create → ● fill → ● validate → ○ publish
                                                                      ▲
```

```
/package
```

The engine strips guided annotations, generates distribution manifests, and prepares everything for publishing.

```
/publish
```

Your product goes live on [myclaude.sh](https://myclaude.sh). Anyone in the world can install it:

```bash
myclaude install your-product-name
```

The engine shows a confirmation with the install command and marketplace URL.

---

## After You Publish

Your product is live. Now what?

**Use it yourself.** The best products are ones the creator uses daily. Install your own product (`myclaude install your-product`) and use it in real work. Notice what feels right and what feels off. That friction is data.

**Check if others are using it.** After a few days, run `myclaude stats your-product` to see install counts and usage data (when available).

**Iterate.** To update a published product: edit the files in `workspace/your-product/`, then re-run `/validate` → `/package` → `/publish`. The engine tracks versions automatically. Users update with `myclaude update your-product`.

---

## What's Next

Now that you have published your first product, here are your options:

- **Use it yourself** — the best products are ones the creator uses daily
- **Run `/scout` on another domain** — discover what else you can build
- **Run `/status`** — see your portfolio dashboard
- **Share the install command** — `myclaude install your-product` is all anyone needs

### Go Deeper

| Guide | What You Will Learn |
|:------|:-------------------|
| **[For Developers](guides/for-developers.md)** | Skills, agents, hooks, squads — technical product types |
| **[For Domain Experts](guides/for-domain-experts.md)** | Package expertise without coding — minds, workflows |
| **[For Teams](guides/for-teams.md)** | Shared standards, multi-agent squads |
| **[Commands Reference](reference/commands.md)** | All 15 commands in detail |
| **[Quality System](reference/quality-system.md)** | How scoring works — tiers, patterns, formulas |
| **[FAQ](../faq.md)** | Common questions answered |

---

## Quick Tips

- **`/status`** anytime — shows where you are and what to do next
- **`/think`** when stuck — brainstorm before committing
- **`/explore`** for inspiration — search the marketplace for existing tools
- **The engine adapts** — a developer sees different language than a consultant
- **Products are yours** — self-contained, no engine dependency after install
