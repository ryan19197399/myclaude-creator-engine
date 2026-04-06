# UX Vocabulary — Translating Engine to Human

**Purpose:** Every term that touches a user must speak human, not engineer. This document is the Rosetta Stone between builder language and buyer experience.

**Rule:** If a term requires explanation, it shouldn't face the user. The magic is that it WORKS, not that it was VALIDATED.

---

## Quality Tiers (user-facing)

| Internal | User-Facing | Badge | Description for Marketplace |
|----------|------------|-------|-----------------------------|
| MCS-1 (>=75%) | **Verified** | `verified.svg` | "Tested and working. Meets quality standards." |
| MCS-2 (>=85%) | **Premium** | `premium.svg` | "Deep expertise. Genuine knowledge you won't find in a generic prompt." |
| MCS-3 (>=92%) | **Elite** | `elite.svg` | "Best in class. Extensively validated, research-backed." |

**In README badges:** Use "Premium Quality" not "MCS-2".
**In marketplace listings:** Show stars (3/4/5) not percentages.
**In /validate output:** Builder sees MCS scores. User never does.

---

## Product Types (user-facing)

| Internal | User-Facing | One-liner |
|----------|------------|-----------|
| skill | **Tool** | "Adds a new capability to Claude Code" |
| minds (advisory) | **Quick Advisor** | "An expert you can ask questions" |
| minds (cognitive) | **Deep Intelligence** | "A specialist mind that reasons about your problems" |
| agent | **Autonomous Agent** | "Works independently on complex tasks" |
| squad | **Team** | "Multiple agents working together" |
| workflow | **Guided Process** | "Step-by-step automation" |
| system | **Complete Setup** | "Full working environment" |
| claude-md | **Project Rules** | "Smart defaults for your project type" |
| hooks | **Auto-Actions** | "Things that happen automatically" |
| statusline | **Status Bar** | "Live info at the bottom of your screen" |
| design-system | **Design Kit** | "Visual design language and components" |
| bundle | **Collection** | "Curated set of tools that work together" |
| output-style | **Response Style** | "Changes how Claude communicates" |

---

## Technical Terms (never expose)

| Internal Term | If user asks | Translate to |
|--------------|-------------|-------------|
| DNA patterns D1-D20 | "How was this validated?" | "We check 20 quality dimensions including how it handles errors, how it loads information, and how it protects your files." |
| Substance score | "Is this real expertise?" | "This tool fills [N] knowledge gaps that Claude doesn't cover on its own." |
| VALUE_SCORE | Never shown | Pricing signal only — user sees the price, not the formula |
| Baseline delta | "How much does this add?" | "Claude knows the basics. This adds [N] areas of deep expertise on top." |
| Cognitive fidelity | Never shown | Internal quality metric for minds |
| Pitfalls G001-G016 | Never shown | Internal institutional memory |
| Anti-patterns | "What can go wrong?" | "What it won't do" (user section name) |
| Quality Gate | Never shown | Internal verification checklist |
| Activation Protocol | "How does it start?" | "What it loads" or just let it happen invisibly |
| Progressive Disclosure | Never shown | Architecture pattern — user just experiences it as "fast" |

---

## Safety Language

| Internal | User-Facing |
|----------|------------|
| `denied-tools: [Write, Edit, Bash, NotebookEdit]` | "Safe mode — this tool will never touch your files or run commands" |
| Advisory only | "Thinks alongside you, never acts on your behalf" |
| Agent tool bypass (G016) | "Note: Claude Code's architecture means this tool could theoretically delegate to other agents. Its instructions explicitly prohibit this." |

---

## Experience Principles

1. **First 10 seconds define retention.** The first response must demonstrate value, not explain architecture.
2. **Show, don't tell.** Instead of "I use a 4-step cognitive flow," just USE it. The user sees the result, not the method.
3. **Confidence is trust.** "I'm 70% confident because..." builds more trust than "Here's the answer."
4. **Admit boundaries.** "I don't know cloud IAM — that's outside my expertise" is more credible than silence.
5. **One insight per interaction.** Don't dump everything. Give the most impactful insight, then offer to go deeper.
6. **Not everyone is a developer.** Many Claude Code users are writers, marketers, consultants, researchers, entrepreneurs. Never use dev jargon in user-facing output unless the creator's profile.type is "developer". Say "your product" not "scaffold". Say "launch" not "deploy". Say "ready to share" not "packaged".

---

## Where This Vocabulary Applies

| Touchpoint | Language | Example |
|-----------|---------|---------|
| Marketplace listing | User-facing only | "Deep Intelligence for Kubernetes Security" |
| README | User-facing + tips | "Premium Quality" badge, "What it won't do" |
| First conversation | Natural, no jargon | "I think in attack paths, not checklists" |
| /validate output | Builder language | "MCS-2 100%, D1-D6 PASS, substance 70/100" |
| /status dashboard | Builder language | "15 products, 13 published, 2 packaged" |
| Error messages | Human + fix | "This tool needs to be tested first. Run /test." |

---

*This document is loaded by /package, /publish, and /fill when generating user-facing content. Builder-facing skills (/validate, /status) use internal terminology.*
