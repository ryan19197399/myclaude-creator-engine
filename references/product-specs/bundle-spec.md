# Product Spec: Bundles

## Definition

Bundles are curated collections of other MyClaude products, referenced by slug.
A bundle has NO primary content file — `vault.yaml` with `bundle.includes[]` IS the product.
The value is curation: why these products together, for whom, at what price advantage.

A bundle is NOT:
- A product with its own executable content
- A collection of unrelated products
- A discount wrapper with no curation rationale

A bundle IS:
- A thoughtfully curated combination
- A single-install experience for a coherent use case
- A pricing advantage over buying products individually

---

## Canonical File Structure

```
bundle-name/
├── vault.yaml            # Bundle manifest with includes[] (REQUIRED — IS the product)
├── README.md             # Marketplace documentation (REQUIRED)
└── .meta.yaml            # Engine state (auto-generated)
```

---

## Required Files

| File | Purpose | Required For |
|------|---------|-------------|
| `vault.yaml` | Bundle manifest with `bundle.includes[]` array | MCS-1 |
| `README.md` | What's included, why, install instructions | MCS-1 |

---

## Special Validation Rules

### Stage 1 (Structural)
- vault.yaml exists with `bundle.includes[]` field
- `bundle.includes[]` is a non-empty array with **>= 2 products** (a single-product bundle has no curation value)
- README.md exists
- **SKIP** primary file check (bundle has no primary .md file)

### Stage 2 (Integrity)
- All slugs in `bundle.includes[]` are valid product slug strings
- No duplicate slugs
- No self-reference
- Curation rationale field is non-empty

---

## MCS Requirements

### MCS-1: Publishable
- [ ] vault.yaml with valid `bundle.includes[]` array
- [ ] README.md with: what's included, curation rationale, install command, requirements
- [ ] At least 2 products in the bundle
- [ ] No placeholder content

### MCS-2: Quality
- [ ] Clear curation rationale explaining why these products together
- [ ] Pricing strategy documented
- [ ] Anti-patterns section in README
- [ ] Each included product has a one-liner description

---

## DNA Requirements

For the complete DNA pattern applicability matrix, see `product-dna/bundle.yaml`.

**MCS scoring:** `(DNA x 0.50) + (Structural x 0.30) + (Integrity x 0.20)`
