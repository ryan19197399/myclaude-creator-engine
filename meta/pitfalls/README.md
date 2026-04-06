# Pitfall Memory

Institutional memory for the MyClaude Creator Studio Engine. Records recurring validation failures so the system learns from its own operation.

## How It Works

1. **/validate** runs and detects failures
2. If the same failure pattern appears 3+ times across different products, it becomes a pitfall
3. **/fill** reads the registry before filling sections — warns creators about known pitfalls
4. **/status** shows pitfall count and most common issue
5. Confidence **decays 0.05/month** without recurrence — stale pitfalls evict below 0.2

## Schema

Each pitfall has:
- `type[]` — which product types this affects
- `section` — which product section is involved
- `description` — human-readable problem statement
- `fix` — actionable remediation
- `confidence` — 0.0-1.0 (boosted by recurrence, decayed by time)
- `occurrences` — total count
- `source` — where it came from (validate-failures, friction-reports, manual)

## Feeding the Registry

The registry is currently maintained manually (seeded from 89 internal sessions). Future automation:
- /validate could auto-propose new pitfalls when a failure pattern repeats 3+ times
- Hook on PostToolUse for /validate could capture failure patterns automatically

## Relationship to Frictions

Pitfalls are TACTICAL (specific validation failures). Frictions (`meta/frictions/`) are STRATEGIC (systemic issues requiring architecture changes). A pitfall might become a friction if it reveals a deeper structural problem.
