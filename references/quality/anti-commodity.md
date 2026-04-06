# Anti-Commodity Mechanism

**CE-D25:** Three-layer defense against marketplace flooding with generic products.

---

## Purpose

The anti-commodity mechanism ensures the marketplace remains a curated collection of
valuable, differentiated products — not a flood of AI-generated templates that all
do the same thing slightly differently.

The mechanism is **coaching, not gatekeeping** (CE-D26). A product that fails
differentiation checks receives specific, actionable feedback to improve.
It is never silently rejected.

---

## Layer 1: MCS Quality Bar

The first filter eliminates structurally broken products before they reach quality review.

**What MCS-1 eliminates:**
- Products with broken or incomplete structure
- Products with placeholder content
- Products without documentation
- Products with security issues

**Effect:** Reduces commodity flooding by raising the effort bar. AI-generated outputs
often fail structural checks because they produce plausible content without correct structure.

---

## Layer 2: Anti-Commodity Gate (CE-D9)

Applied before publishing at MCS-2 or MCS-3. Checks differentiation — not just quality.

### Uniqueness Score

Computed by the quality-reviewer agent. Three dimensions:

| Dimension | What it Measures | Scoring |
|-----------|----------------|---------|
| **Domain expertise depth** | Is there knowledge that required human expertise to encode? Could an AI generate this without domain-specific input? | 0-40 points |
| **Specificity** | Does this solve a narrow, well-defined problem or a vague, broad one? "Security audit for Node.js APIs" vs. "general security helper" | 0-30 points |
| **Methodology originality** | Does this have a unique approach, framework, or perspective? Not "different" for its own sake — meaningfully differentiated. | 0-30 points |

**Total:** 0-100 points
**Threshold:** Products scoring below 40 receive feedback before proceeding.

### The Three Gate Questions

Before publishing any MCS-2 or MCS-3 product, the Engine asks:

**Question 1:** "What domain expertise did the creator inject that AI alone couldn't generate?"

*Strong answer:* "The skill encodes my 8 years of penetration testing methodology — specifically the threat modeling approach I developed for microservices architectures that isn't documented anywhere."

*Weak answer:* "I wrote good instructions for the AI to follow."

---

**Question 2:** "If we removed all AI-generated content, what would remain?"

*Strong answer:* "The `references/` knowledge base, the threat model taxonomy, and the decision trees in `config/routing-table.md` — those represent my domain thinking."

*Weak answer:* "The file structure and maybe the README."

---

**Question 3:** "Does this product solve a specific problem that fewer than 5 other products address?"

*Strong answer:* "I checked the marketplace — there are 3 generic security audit prompts but none targeting microservices threat modeling specifically."

*Weak answer:* "It's a general-purpose skill, anyone could use it."

### Gate Scoring

| Score | Domain Expertise | Specificity | Methodology | Gate Result |
|-------|----------------|-------------|-------------|------------|
| ≥70 | Strong | Narrow | Original | Pass — differentiated |
| 40-69 | Moderate | Semi-specific | Partial | Pass with feedback |
| 20-39 | Weak | Broad | Generic | Feedback required |
| <20 | None | Very broad | None | Strong feedback + coaching |

**Threshold:** Products below 40 get feedback, NOT rejection (CE-D26).

### Feedback Template (When Score is Low)

```
Your product [NAME] is structurally sound (MCS-[level] checks passed).

Uniqueness Score: [X]/100
- Domain expertise: [score]/40 — [specific finding]
- Specificity: [score]/30 — [specific finding]
- Methodology: [score]/30 — [specific finding]

Your product is currently similar to [N] existing marketplace products:
[list 2-3 most similar]

To differentiate, consider:
1. [Specific suggestion based on creator's expertise from creator.yaml]
2. [Specific suggestion based on gap in marketplace]
3. [Specific suggestion based on underserved use case]

You can publish now at this differentiation level, but your product
may have lower visibility than more differentiated products.
Would you like to improve it before publishing?
```

---

## Layer 3: Creator Reputation

Long-term quality signal that weights products in search and recommendation.

### Reputation Signals

| Signal | How It Builds | Effect |
|--------|--------------|--------|
| **MCS level consistency** | Publishing multiple MCS-3 products | Featured placement in category |
| **Quality stability** | No downgrade after review | Trust badge |
| **Review-verified quality** | Buyer reviews confirm claims | Social proof, search ranking |
| **Upgrade trajectory** | Products improving over versions | "Rising creator" badge |

### Featured Placement Criteria

Creators earn featured placement when:
1. Average MCS level ≥ 2.5 across all products
2. At least 1 MCS-3 product published
3. No MCS-1 violations in last 90 days
4. At least 1 verified buyer review per product

### Trust Badges

| Badge | Criteria |
|-------|---------|
| **Verified Creator** | Identity verified + payment method linked |
| **Quality Publisher** | 3+ products at MCS-2+ |
| **Expert Tier** | 1+ MCS-3 product + 5+ positive reviews |
| **Domain Authority** | 3+ MCS-3 products in same category |

---

## CE-D26: The Engine Helps, Not Blocks

The anti-commodity mechanism is coaching, not gatekeeping. If a product is generic:

> "Your skill is structurally sound but similar to 3 existing products.
> Here are 3 ways to make it stand out: [specific, actionable suggestions]"

The Engine never says "this product is rejected." It says "this product would benefit
from differentiation, and here's specifically how."

**Rationale:** Creators who receive helpful, specific feedback improve and stay in the
ecosystem. Creators who receive rejections leave and create elsewhere. The marketplace
benefits from creators who improve, not from gatekeeping that loses them.

---

## For Creators: How to Pass the Gate

### High-differentiation strategies:

1. **Encode proprietary methodology:** Your product should express YOUR way of approaching
   the problem — not the most common AI-generated approach.

2. **Target narrow use cases:** "Marketing analytics prompts" is a category.
   "Marketing attribution analysis for B2B SaaS with multi-touch models" is a product.

3. **Build a knowledge base:** The `references/` directory is where your expertise lives.
   A product with a deep, domain-specific knowledge base almost always passes the gate.

4. **Document your decision-making:** The cognitive architecture section (why you designed
   it this way) is itself a differentiation signal — it shows domain thinking.

5. **Test against real problems:** Products created from real problems score higher than
   products created from "what would be useful." Publish the product you actually needed.
