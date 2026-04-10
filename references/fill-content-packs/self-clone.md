# SELF-CLONE Content Pack for /fill

> **Consumer:** `/fill` skill walker when `.meta.yaml.type == "minds" AND .meta.yaml.minds_sub_type == "self"`.
> **Source architecture:** `references/self-clone-forge.md` (canonical substrate).
> **Purpose:** Replace the generic section walk with the SELF-CLONE protocol. This file contains the walker instructions, the ordered question sequences, the distillation procedures, the typology mirror, and the dimensional routing — everything `/fill` needs to run SELF-CLONE without loading the full canonical substrate.

---

## §1 — Walker Entry Point

When `/fill` detects `sub_type=self`, it skips the standard Discovery, Extraction Mode, and generic Section Walk phases. Instead:

1. **Mode selection.** Compute corpus density: count the creator's published or sealed artifacts and their total tokens.
   - `corpus_tokens >= 20_000 AND artifact_count >= 3` → **distillation mode**
   - Otherwise → **elicitation mode**
   - Record `self_clone_mode` in `.meta.yaml`

2. **Distillation pass (distillation mode only).** For each of the eight dimensional targets, run the distillation procedure from §3 below. Present the first-draft populated dimension to the creator for confirm / refine / reject per entry.

3. **Gap identification.** After distillation (or immediately in elicitation mode), identify dimensions with confidence < 0.7. These dimensions enter the elicitation sequence.

4. **Elicitation sequence.** For each dimension requiring elicitation, walk the ordered question sequence from §2 below. Respect the three-phase ordering (Instances → Pattern → Counter-proof) and the mode tags (DIST / ELIC / BOTH).

5. **Dimensional routing.** As features are elicited, tag each with primary + up to two secondary dimensions using the routing rules from §4 below.

6. **Typology mirror.** After all eight dimensions are populated, run the three-step typology probe from §5 below.

7. **Coherence diff.** Generate the diff between distillation drafts and creator responses. Write to `workspace/{slug}/self-clone-diff.md`.

8. **Honesty floor.** Run gates 1, 4, 5 inline during elicitation (counter-proofs, signed incaptable list, uncapturable decisions). Gates 2 and 3 (three-day delay, adversarial reader) run post-elicitation. Write the manifest to `workspace/{slug}/self-clone-manifest.md`.

9. **Write mind files.** Populate the cognitive mind layer files using the standard `/fill` write discipline: `AGENT.md`, `cognitive-core.md`, `personality.md`, `knowledge-base.md`, `reasoning-engine.md`, `examples/examples.md`.

10. **Completion.** Promote product state to "content". Run auto-validate at the structural level.

---

## §2 — Ordered Question Sequences

### §2.1 — Ordering rule

Every dimension follows three phases:

- **Phase I — Instances**: "List the last N times X happened." Concrete, timestamped where possible.
- **Phase II — Pattern**: "What holds across what you just named?" Creator abstracts from their own data.
- **Phase III — Counter-proof**: "Name a situation where this pattern would fail to predict your behavior." Honesty floor gate 1 integrated.

### §2.2 — Questions per dimensional target

The question set below covers Tier Functional (3 per dimension) through Tier High (7-9 per dimension). Each question carries a mode tag and behavioral manifestation binding where applicable.

**Target 1: distinctive_terms** (foundation, ≥50)

| # | Phase | Mode | Question |
|---|---|---|---|
| 1.1 | I | BOTH | List fifteen words or short phrases you use that a reader could recognize as yours with no byline. Point to one paragraph where each term carries your meaning, not a dictionary meaning. |
| 1.2 | I | ELIC | Name three words you consciously refuse to use. For each, name the substitution and what it protects. |
| 1.3 | II | ELIC | Among the confirmed terms, which five would a reader use to identify your authorship? Rank them. |
| 1.4 | II | DIST | Cluster confirmed terms by semantic domain (conceptual, operational, metaphoric, relational, temporal). Note the dominant domain. |
| 1.5 | III | ELIC | Describe a situation where you deliberately suppressed your distinctive vocabulary. What did you lose? What did you gain? |

**Target 2: recurring_metaphors** (foundation, ≥20)

| # | Phase | Mode | Question |
|---|---|---|---|
| 2.1 | I | BOTH | List five images or comparisons you reach for when explaining something difficult. State the source domain for each. |
| 2.2 | I | DIST | Extract cross-domain analogies from the creator's corpus. Group by source domain. Retain domains appearing in ≥2 documents. |
| 2.3 | II | ELIC | Which two or three source domains are load-bearing — if you stopped using one, your explanatory range would shrink? |
| 2.4 | II | ELIC | When you encounter a new problem, which source domain do you reach for first? Does first-reach differ from most-effective? |
| 2.5 | III | ELIC | Tell a case where a load-bearing metaphor produced a misleading analogy. What revealed the mismatch? |

**Target 3: master_mental_models** (critical, 3-5)

| # | Phase | Mode | Question |
|---|---|---|---|
| 3.1 | I | ELIC | Take a decision you felt unusually confident about this month. What did you see that a competent outsider would have missed? |
| 3.2 | I | DIST | From creator artifacts, identify decision points where the same structural frame was applied across ≥3 situations in ≥2 domains. |
| 3.3 | II | ELIC | Name the lens that made the difference. State in one sentence. Declare: what does it make visible? What does it render invisible? |
| 3.4 | II | ELIC | For each lens, declare the trade-off: what it gains and what it sacrifices. |
| 3.5 | III | ELIC | Describe a situation where this lens would have produced the wrong answer. What signal should tell you the lens is wrong here? |

**Target 4: inviolable_values** (critical, 5-7, floor 0.90)

| # | Phase | Mode | Question |
|---|---|---|---|
| 4.1 | I | BOTH | Name five commitments you have refused to compromise even when the cost of refusal was high. Describe each refusal with a concrete situation and verifiable timestamp. |
| 4.2 | I | DIST | From creator decisions, extract cases where visible cost was paid to honor a commitment. Retain principles appearing ≥3 times. |
| 4.3 | II | ELIC | For each value, write the "would do X, would not do Y" pair. Both sides concrete, not abstract. |
| 4.4 | II | ELIC | Rank these five when two conflict. Is the order stable or situational? |
| 4.5 | III | ELIC | For each value, write the inversion: "the version of me that breaks this does what exactly, and justifies it how?" If inversion is absurd, the value is structural. If merely regrettable, it is a preference — downgrade. |

**Target 5: core_obsessions** (critical, 3-5)

| # | Phase | Mode | Question |
|---|---|---|---|
| 5.1 | I | BOTH | List 3-5 questions you cannot stop thinking about across contexts. Name the earliest documented moment each appeared. |
| 5.2 | I | DIST | Extract question-shaped constructions repeating across ≥3 documents over ≥6 months. |
| 5.3 | II | ELIC | What would your life lose if the question dissolved? A question you would willingly surrender is not an obsession. |
| 5.4 | II | ELIC | For each obsession, name a partial answer you have reached. |
| 5.5 | III | ELIC | Describe a case where pursuing the obsession led somewhere wrong. What signal should have told you to set it aside? |

**Target 6: productive_paradoxes** (critical, 3-5, floor 0.80)

| # | Phase | Mode | Question |
|---|---|---|---|
| 6.1 | I | BOTH | Name three tensions where both poles are true and you hold them together rather than resolving. What collapses when either pole is sacrificed? |
| 6.2 | I | DIST | From creator artifacts, identify passages holding two claims in tension without resolution. Retain tensions in ≥3 passages. |
| 6.3 | II | ELIC | For each paradox: "I know I am operating this well when I catch myself about to _____, and I stop." Name the anti-pattern it protects from. |
| 6.4 | II | ELIC | Name the wrong way the tension usually resolves when people try to collapse it. What do they lose? |
| 6.5 | III | ELIC | Describe a case where the paradox should have been collapsed — holding both poles was the wrong move. What made that case different? |

**Target 7: unique_sensors** (foundation, ≥10)

| # | Phase | Mode | Question |
|---|---|---|---|
| 7.1 | I | BOTH | List ten things you notice in your domain that most competent practitioners overlook. Describe the signal and what you infer. |
| 7.2 | I | DIST | From creator artifacts, extract observations flagged as important that were not flagged by peers. Extract cue-to-inference mapping. |
| 7.3 | II | ELIC | Which three sensors would you lose most painfully? What would you become worse at? |
| 7.4 | II | ELIC | For each sensor, name the signal category (structural, relational, behavioral, temporal, energetic, linguistic, absence-of-expected). |
| 7.5 | III | ELIC | Tell the last time something felt wrong before you could articulate why. Reconstruct the smallest cue. If unarticulable after reconstruction → route to the uncapturable section. |

**Target 8: decision_signatures** (critical, ≥5)

| # | Phase | Mode | Question |
|---|---|---|---|
| 8.1 | I | BOTH | Describe five decision patterns: "when X occurs, I do Y rather than the competent alternative Z, and the trade-off I accept is W." |
| 8.2 | I | DIST | Extract decision patterns repeating across ≥3 situations. Reconstruct the implicit trade-off. |
| 8.3 | II | ELIC | For each signature, name the alternative you did not take and why it would have been wrong for your trade-off. The alternative must be competent. |
| 8.4 | II | ELIC | Name the decision you would regret most if your successor took it in your name. |
| 8.5 | III | ELIC | Describe a situation where your pattern would have been wrong — where alternative Z was correct. What signal should tell you to deviate? |

---

## §3 — Distillation Procedures (Distillation Mode)

For each dimensional target, the walker reads the creator's corpus and produces a first-draft populated dimension. The procedures are summarized here; full algorithmic detail is in `references/self-clone-forge.md` §6.2.

| Target | Procedure summary | Confidence threshold |
|---|---|---|
| distinctive_terms | Frequency analysis against baseline English, ≥5x ratio | ≥0.8 when ≥50 terms |
| recurring_metaphors | Cross-domain analogy scan, group by source domain | ≥0.8 when ≥20 in ≥4 domains |
| master_mental_models | Reasoning chain abstraction, cluster by structural frame | ≥0.7 when 3-5 frames |
| inviolable_values | Cost-paid decision scan, cluster principles | ≥0.7 when ≥5 principles |
| core_obsessions | Question-shaped construction scan, 6-month persistence | ≥0.7 when 3-5 questions |
| productive_paradoxes | Tension-without-resolution scan | ≥0.7 when ≥3 tensions |
| unique_sensors | Creator-specific observation extraction | ≥0.7 when ≥10 observations |
| decision_signatures | Named-alternative decision scan | ≥0.7 when ≥5 patterns |

After each distillation, present the draft. Creator confirms / refines / rejects per entry. Rejected entries trigger elicitation gap-filling.

---

## §4 — Dimensional Routing Rules

**Primary tag:** assigned to the dimension where the feature's behavioral manifestation is most directly observable.

**Secondary tags:** up to two additional dimensions the feature partially populates. Weight: 0.5 each.

**Composite test:** if a feature could be primary in ≥3 dimensions, split into separate features.

**Critical-layer rule:** stopping rules for critical dimensions (values, paradoxes) count only primary tags. Secondary contributions do not satisfy the critical-layer floor.

---

## §5 — Typology Mirror (Post-Elicitation)

After all eight dimensions are populated:

1. **Surface pattern** — synthesize a paragraph in the creator's own vocabulary summarizing the dimensional cluster. No typology language.
2. **Offer vocabulary** — "Some creators recognize this pattern in typology languages (DISC, Enneagram, MBTI). Would you like to see the closest match?" Three options: yes / no / unfamiliar.
3. **Record signal** — recognition, refusal, or unfamiliarity is stored as `typology_recognition` in the manifest. All three responses are data.

---

## §6 — Honesty Floor Integration

### Gate 1 (inline): Removal test inverted
Every Phase III question is the counter-proof gate. Dimensions without counter-proofs → `speculative`.

### Gate 2 (post-elicitation): Three-day delay
Re-ask the 3 most critical entries with different framing after delay. Discrepancy >30% → `unstable`. Single-session variant: same-session reframing, tagged `same_session_reframe`.

### Gate 3 (post-elicitation): Adversarial reader
A second Claude reads the clone, predicts 3 decisions, cross-checks. Contradictions → gate fails. Non-skippable.

### Gate 4 (inline): Signed incaptable list
Before manifest seal, creator writes in first person: "this clone does not capture: X, Y, Z."

### Gate 5 (inline): Uncapturable decisions
Creator names 3 recent decisions they cannot justify in writing. Stored as `uncapturable: true`.

---

## §7 — Output Files

| File | Content | Stripped from .publish/ |
|---|---|---|
| Mind layer files | Populated cognitive architecture | No |
| `self-clone-diff.md` | Coherence diff (distillation vs self-report) | Yes (default) |
| `self-clone-manifest.md` | Five gates output + typology recognition | Yes (default) |

---

*Content pack for the SELF-CLONE protocol. Loaded by /fill when sub_type=self. All question sequences, distillation procedures, routing rules, typology mirror, and honesty floor integration in one consumable document.*
