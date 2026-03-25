# System Exemplar: Research Intelligence System

**MCS Level:** 3 (State-of-the-Art)
**Composition:** 2 skills + 1 agent + 1 workflow
**Demonstrates:** SYSTEM.md with routing layer, manifest.yaml, shared knowledge base,
user journey documentation, component independence, CE-D36 question system integration.

---

## File: `SYSTEM.md`

```markdown
# Research Intelligence System

**Purpose:** Transforms research requests into structured intelligence reports by
combining deep search, synthesis, and validation into a cohesive pipeline.

**Version:** 1.1.0
**Components:** 4 components — 2 skills, 1 agent, 1 workflow
**Entry Point:** Describe a research question or topic
**Complexity:** COGNITIVE
**Author:** @researchcraft

---

## What This System Does

The Research Intelligence System handles the full research lifecycle: from raw question
to structured, sourced, and validated report. Individual components — a search skill,
a synthesis skill, a fact-checking agent, and an assembly workflow — are coordinated
by the routing layer into a coherent whole.

The emergent capability: **automated research pipeline with built-in validity checking**.
No individual component provides this — it requires the system.

**Primary use cases:**
1. Deep-dive research on complex topics requiring synthesis of multiple sources
2. Fact-checking and evidence quality assessment for existing claims
3. Competitive intelligence gathering with structured output

---

## Architecture

```
[User Research Question]
          │
          ▼
[Routing Layer — intent detection]
          │
          ├── "find sources" ──────────────► [search-skill]
          │                                        │
          │                                        ▼
          ├── "synthesize" ◄─────────────── [synthesis-skill]
          │                                        │
          │                                        ▼
          └── "validate" ───────────────► [fact-checker-agent]
                                                   │
                                                   ▼
                                         [report-assembly-workflow]
                                                   │
                                                   ▼
                                       [Structured Intelligence Report]
```

**Full pipeline (default path):**
1. User provides research question
2. Routing detects intent: `full-research` (most common)
3. `search-skill` retrieves and structures relevant sources
4. `synthesis-skill` synthesizes sources into a structured brief
5. `fact-checker-agent` validates key claims and assesses evidence quality
6. `report-assembly-workflow` assembles and formats the final report

---

## Component Inventory

| Name | Type | Location | MCS Level | Purpose |
|------|------|----------|-----------|---------|
| `search-skill` | Skill | `skills/search-skill/` | MCS-2 | Source discovery and structuring |
| `synthesis-skill` | Skill | `skills/synthesis-skill/` | MCS-2 | Multi-source synthesis and brief creation |
| `fact-checker-agent` | Agent | `agents/fact-checker-agent.md` | MCS-2 | Claim validation and evidence quality scoring |
| `report-assembly-workflow` | Workflow | `workflows/report-assembly/` | MCS-2 | Final report formatting and delivery |

---

## Routing Logic

See `config/routing.yaml` for machine-readable routing rules.

| User Intent | Routes To | Notes |
|-------------|----------|-------|
| `full-research` | `search-skill` → `synthesis-skill` → `fact-checker-agent` → `report-assembly-workflow` | Default path |
| `find-sources-only` | `search-skill` | Returns source list without synthesis |
| `synthesize-existing` | `synthesis-skill` → `fact-checker-agent` | User provides sources |
| `fact-check-only` | `fact-checker-agent` | User provides claims to validate |
| `format-existing` | `report-assembly-workflow` | User provides brief, needs formatting |
| Ambiguous | System asks clarification | "Are you starting fresh or have sources?" |

**Intent detection rules:**
- Contains "research" or "find out about" → `full-research`
- Contains "here are my sources" or "I have these links" → `synthesize-existing`
- Contains "is it true that" or "verify this claim" → `fact-check-only`
- Provides a brief and says "format this" → `format-existing`
- Unclear → Ask one question before routing

---

## Shared Knowledge Base

All components reference the shared knowledge base in `references/`:

| File | Contents | Used By |
|------|---------|---------|
| `references/source-quality-rubric.md` | 5-tier evidence quality scoring (T1-T5) | search-skill, fact-checker-agent |
| `references/report-templates.md` | 3 report format templates | synthesis-skill, report-assembly-workflow |
| `references/domain-routing-hints.md` | Domain-specific source authority lists | search-skill |

The shared knowledge base is what makes the system's outputs consistent across components.
All components use the same evidence quality rubric — T3 evidence means the same thing
to the search skill and the fact-checker agent.

---

## User Journey

### Journey 1: Full Research from Question

**Scenario:** User wants a complete report on a topic they know little about.

```
1. User: "Research the current state of small modular reactor deployment globally"

2. System routing detects: full-research
   → Routes to search-skill

3. search-skill (Activation Protocol):
   - Loads source-quality-rubric.md
   - Question system: "What depth? Academic sources only or include industry?"
   - User: "Include industry reports, 2022 onwards"
   - Retrieves and structures 8-12 sources with T1-T5 quality scores

4. synthesis-skill receives: structured source list
   - Synthesizes across sources
   - Produces: key claims with source attribution

5. fact-checker-agent receives: key claims + sources
   - Validates top 5 claims against T1-T2 evidence threshold
   - Scores overall evidence quality: 73/100
   - Flags: 2 claims with only T4 evidence

6. report-assembly-workflow receives: brief + validation report
   - Selects template: "strategic-intelligence" from report-templates.md
   - Assembles final report with inline citations and evidence quality notes
   - Delivers: report.md (structured, cited, validated)

Final output: 1,200-word intelligence report with 9 cited sources,
evidence quality score 73/100, 2 flagged claims that need verification.
```

### Journey 2: Fact-Check Only (Single Component)

**Scenario:** User has a specific claim and wants evidence assessment.

```
1. User: "Fact-check: Nuclear energy produces less lifecycle CO2 than solar PV"

2. System routing detects: fact-check-only
   → Routes directly to fact-checker-agent

3. fact-checker-agent:
   - Loads source-quality-rubric.md
   - Searches for T1-T2 evidence on lifecycle emissions comparisons
   - Finds: IPCC AR6 data (T1), NREL lifecycle analysis (T1)
   - Result: SUPPORTED (T1 evidence, 89% confidence)
   - Notes: Range matters — varies by energy mix and panel type

4. Returns: Evidence assessment, not a full report
```

### Journey 3: Ambiguous Input → Clarification

**Scenario:** Input could be any of 3 routing paths.

```
1. User: "I need something on climate finance"

2. Routing: Cannot determine intent.

3. System asks ONE question:
   "Are you starting a fresh research task (I'll find sources and synthesize),
   or do you have sources/a brief you'd like me to work with?"

4. User: "Fresh research"

5. Routes to: full-research path
```

---

## Configuration

See `config/manifest.yaml` and `config/routing.yaml`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `evidence_threshold` | `T3` | Minimum evidence quality for inclusion |
| `source_count_target` | `8-12` | Target number of sources per research task |
| `report_format` | `strategic-intelligence` | Default report template |
| `fact_check_top_n` | `5` | Number of top claims to validate per research task |

### Enabling/Disabling Components

When a component is disabled in `manifest.yaml`, the system skips that step:
- `fact-checker-agent: enabled: false` — skips validation, produces unvalidated synthesis
- `report-assembly-workflow: enabled: false` — returns raw brief without formatted report

---

## Component Independence

Each component works standalone:

| Component | Standalone Usage | Notes |
|-----------|----------------|-------|
| `search-skill` | `/search-skill` | Source discovery for any use case |
| `synthesis-skill` | `/synthesis-skill` | Synthesis from any provided sources |
| `fact-checker-agent` | `@fact-checker-agent` | Claim validation for any domain |
| `report-assembly-workflow` | See `workflows/report-assembly/README.md` | Format any brief |
```

---

## File: `config/manifest.yaml`

```yaml
# Research Intelligence System — Manifest v1.1.0
system:
  name: "research-intelligence"
  version: "1.1.0"
  entry_point: "SYSTEM.md"
  complexity: "COGNITIVE"

components:
  skills:
    - name: "search-skill"
      path: "skills/search-skill/"
      mcs_level: 2
      enabled: true
      handles: ["source-discovery", "literature-search"]

    - name: "synthesis-skill"
      path: "skills/synthesis-skill/"
      mcs_level: 2
      enabled: true
      handles: ["multi-source-synthesis", "brief-creation"]

  agents:
    - name: "fact-checker-agent"
      path: "agents/fact-checker-agent.md"
      mcs_level: 2
      enabled: true
      handles: ["claim-validation", "evidence-scoring"]

  workflows:
    - name: "report-assembly-workflow"
      path: "workflows/report-assembly/"
      mcs_level: 2
      enabled: true
      triggers: ["synthesis-complete", "validation-complete"]

  shared_references:
    - "references/source-quality-rubric.md"
    - "references/report-templates.md"
    - "references/domain-routing-hints.md"

routing:
  config: "config/routing.yaml"
  default_path: "full-research"
  fallback: "ask-clarification"
```

---

## File: `references/source-quality-rubric.md` (excerpt)

```markdown
# Source Quality Rubric

## Evidence Tiers (T1-T5)

| Tier | Name | Description | Examples |
|------|------|-------------|---------|
| T1 | Primary evidence | Peer-reviewed, IPCC, government statistics, direct measurement | IPCC reports, NREL data, census data |
| T2 | High-quality secondary | Well-sourced synthesis by domain experts | Nature News, major research institute reports |
| T3 | Credible analysis | Analytical pieces with cited evidence | Quality journalism with sources, industry analyst reports |
| T4 | Informed opinion | Expert opinion without primary citation | Expert blog posts, unverified industry claims |
| T5 | Unverified | No attribution, marketing content, unknown provenance | Company press releases, Wikipedia (as primary) |

## Usage Rules

- All key claims in reports must have T1-T3 evidence minimum
- T4 and T5 evidence may be included as context but must be flagged
- Evidence quality score formula: (T1×5 + T2×4 + T3×3 + T4×1 + T5×0) / (count × 5) × 100
```

---

## Quality Verification

This exemplar demonstrates:

- [x] SYSTEM.md with all required sections
- [x] Architecture diagram showing component interaction
- [x] Component inventory with MCS levels
- [x] Routing logic table + intent detection rules
- [x] Shared knowledge base: files, contents, and which components use each
- [x] 3 user journeys including ambiguous case with clarification
- [x] Component independence table
- [x] `config/manifest.yaml` with full specification
- [x] Shared knowledge base demonstrates CE-D36 question system integration (search-skill asks clarifying question in Journey 1)
- [x] MCS-3 criteria met
