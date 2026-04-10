# Structural DNA — Pattern Dependency Graph

> Loaded on-demand by `/validate` for coherence checks (Tier 3 evolution). Not loaded
> at boot. See `structural-dna.md` for the boot-resident layer.

Each pattern declares what it enables and what it requires. This transforms
the DNA from a catalog of isolated checks into a connected language where
patterns reinforce each other.

## Connections

| Pattern | Requires | Enables | Therefore |
|---------|----------|---------|-----------|
| D1 Activation Protocol | — | D3, D7 | "Load context first → disclose progressively and gate execution" |
| D2 Anti-Pattern Guard | — | D11 | "Codified failures → enable genuine self-challenge" |
| D3 Progressive Disclosure | D1 | D20 | "On-demand loading → enables cache-friendly design" |
| D4 Quality Gate | — | D15 | "Verification criteria → enable testability" |
| D5 Question System | D1 | D6 | "Structured questions → enable graduated confidence" |
| D6 Confidence Signaling | D5 | D11 | "Graduated certainty → enables meaningful challenge" |
| D7 Pre-Execution Gate | D1 | D14 | "Precondition checks → enable graceful failure" |
| D8 State Persistence | D7 | D12 | "Session state → enables cross-session memory" |
| D9 Orchestrate Don't Execute | D10 | D18 | "Routing without doing → enables isolated execution" |
| D10 Handoff Specification | D8 | D9 | "Explicit context transfer → enables clean orchestration" |
| D11 Socratic Pressure | D2, D6 | — | "Challenge output → terminal quality improvement" |
| D12 Compound Memory | D8 | — | "Cross-session learning → terminal capability growth" |
| D13 Self-Documentation | — | D16 | "Clear README → enables ecosystem compatibility" |
| D14 Graceful Degradation | D7 | — | "Fail gracefully → terminal trust preservation" |
| D15 Testability | D4 | — | "Test scenarios → terminal quality verification" |
| D16 Composability | D13 | — | "No conflicts → terminal ecosystem compatibility" |
| D17 Hook Integration | — | — | "Lifecycle automation → standalone enhancement" |
| D18 Subagent Isolation | D9, D10 | — | "Context isolation → terminal multi-agent reliability" |
| D19 Attention-Aware | D3 | — | "Critical rules positioned for maximum compliance" |
| D20 Cache-Friendly | D3, D19 | — | "Optimized ambient cost → terminal token efficiency" |

## Reading the Graph

- **Requires** = this pattern needs its prerequisites to deliver full value
- **Enables** = this pattern creates conditions for another to work
- **Therefore** = the generative connection (why this sequence produces quality)
- **Terminal** patterns (no Enables) = leaf nodes delivering final user value
- **Foundation** patterns (no Requires) = D1, D2, D4, D13, D17 — always start here

## Future Validation Implication

/validate could check pattern COHERENCE beyond presence: if D9 (Orchestrate) exists
but D10 (Handoff) is missing, the product has orchestration without handoff contracts.
This is a TIER 3 evolution — not implemented in current /validate.
