# Licensing Guide

CE-D40 approved licenses, when to use each, and compatibility considerations
for remixed or composed products.

---

## Approved Licenses (CE-D40)

The marketplace accepts exactly 10 license types:

| License | Type | Permissions | Restrictions |
|---------|------|------------|-------------|
| `MIT` | Permissive | Use, modify, distribute, commercial | Attribution required |
| `Apache-2.0` | Permissive | Use, modify, distribute, commercial, patent grant | Attribution + state changes |
| `GPL-3.0` | Copyleft | Use, modify, distribute | Derivatives must also be GPL-3.0 |
| `BSD-3-Clause` | Permissive | Use, modify, distribute, commercial | Attribution, no endorsement |
| `ISC` | Permissive | Use, modify, distribute, commercial | Attribution (simplified MIT) |
| `CC-BY-4.0` | Creative Commons | Share, adapt, commercial | Attribution |
| `CC-BY-SA-4.0` | Creative Commons ShareAlike | Share, adapt, commercial | Attribution + ShareAlike (derivatives same license) |
| `CC0-1.0` | Public Domain | Use freely, no restrictions | None |
| `Proprietary` | Closed | No redistribution | All rights reserved |
| `Custom` | Creator-defined | Defined in LICENSE file | Must be fully specified |

---

## When to Use Each License

### MIT

**Best for:** Skills, agents, and CLAUDE.md configs intended for broad adoption.

**Choose MIT when:**
- You want maximum adoption and don't mind others selling modified versions
- You're building open-source tooling for the Claude Code community
- You want minimal friction for commercial users

**Real-world analogy:** Most popular npm packages (React, Express, Tailwind).

---

### Apache-2.0

**Best for:** Products with business adoption in mind, especially when patents matter.

**Choose Apache-2.0 when:**
- You want the same freedoms as MIT but with an explicit patent grant
- Your product includes novel techniques that might be patentable
- You're building for enterprise adoption where legal teams care about patents

**Difference from MIT:** Includes explicit patent license and requires notice of changes.

---

### GPL-3.0

**Best for:** Products where you want a copyleft guarantee.

**Choose GPL-3.0 when:**
- You want derivatives to remain open source
- You're philosophically committed to free software propagation
- You're building on existing GPL-3.0 licensed work

**Warning:** GPL-3.0 is incompatible with many commercial products. If you want
commercial users to adopt your product, this license will create friction.

---

### CC-BY-4.0

**Best for:** Knowledge-heavy products — prompts, design systems, references.

**Choose CC-BY-4.0 when:**
- The primary value is content (methodologies, frameworks, design tokens), not code
- You want commercial use allowed with attribution
- You're sharing knowledge resources more than software

**Note:** CC licenses are more appropriate for content than for software.
Skills and agents are better served by MIT or Apache-2.0.

---

### CC-BY-SA-4.0

**Best for:** Community knowledge products where you want derivatives to share back.

**Choose CC-BY-SA-4.0 when:**
- You're contributing to a shared knowledge ecosystem (e.g., design system library)
- You want derivatives to be available under the same terms
- You're building on other CC-BY-SA works

---

### CC0-1.0 (Public Domain)

**Best for:** Free tools, starter templates, community resources.

**Choose CC0 when:**
- You want zero friction for any use whatsoever
- You're contributing reference implementations to the community
- Attribution is not important to you

**No restrictions at all.** Anyone can use, modify, sell, or relicense.

---

### Proprietary

**Best for:** Premium products where you want exclusive control.

**Choose Proprietary when:**
- Your product represents significant proprietary methodology
- You do not want others to redistribute or build on your product
- You're monetizing access rather than sharing openly

**What it means:** Buyers get usage rights. They cannot redistribute, modify,
or create derivative products.

---

### Custom

**Best for:** When none of the standard licenses fit your needs.

**Requirements for Custom:**
- Must specify a complete LICENSE file
- Must clearly state what buyers can and cannot do
- Must be reviewed before publishing (takes longer than standard licenses)
- Should reference an existing standard if possible and extend it

---

## Compatibility Considerations for Remixed Products

When you build a product that incorporates or remixes another creator's product:

### Rule: License compatibility

Your product's license must be compatible with all incorporated products' licenses.

| Your target license | Compatible with |
|--------------------|----------------|
| MIT | Any (others may impose restrictions, but MIT is always compatible) |
| Apache-2.0 | MIT, Apache-2.0, BSD-3-Clause, ISC, CC-BY-4.0, CC0 |
| GPL-3.0 | MIT, Apache-2.0, GPL-3.0 (cannot use proprietary components) |
| CC-BY-SA-4.0 | CC-BY-4.0, CC-BY-SA-4.0, CC0 |
| Proprietary | Only can incorporate CC0 and permissive licenses IF terms allow |

**Key incompatibilities:**
- GPL-3.0 + Proprietary = incompatible
- CC-BY-SA-4.0 + MIT code = incompatible (CC-SA doesn't cover code)
- Proprietary + GPL-3.0 component = incompatible

### Attribution requirements

If you incorporate a CC-BY or MIT product:
1. Credit the original creator in your README
2. Link to the original product
3. State what you changed

```markdown
## Attribution

This product incorporates:
- [Original Skill Name] by [@original-creator] — MIT License
  Changes made: Extended the Activation Protocol and added 3 exemplars.
```

---

## License Field in Metadata

The `license` field in product metadata must use the exact SPDX identifier:

```yaml
# Correct SPDX identifiers:
license: "MIT"
license: "Apache-2.0"
license: "GPL-3.0"
license: "BSD-3-Clause"
license: "ISC"
license: "CC-BY-4.0"
license: "CC-BY-SA-4.0"
license: "CC0-1.0"
license: "Proprietary"
license: "Custom"
```

For Custom licenses, also include:
```yaml
license: "Custom"
license_url: "LICENSE"   # Path to your LICENSE file in the product
```

---

## Quick Decision Guide

```
Is it code (skill, agent, CLAUDE.md)?
  └── Want maximum adoption → MIT
  └── Enterprise target + patents → Apache-2.0
  └── Copyleft required → GPL-3.0
  └── Premium / no redistribution → Proprietary

Is it primarily content (prompt, design system, knowledge base)?
  └── Attribution required → CC-BY-4.0
  └── Derivatives must share back → CC-BY-SA-4.0
  └── No restrictions → CC0-1.0
  └── Exclusive rights → Proprietary

Unsure?
  → MIT for most cases. It's the least controversial and the most adopted.
```
