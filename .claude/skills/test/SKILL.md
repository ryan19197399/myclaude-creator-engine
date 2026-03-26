---
name: test
description: >-
  Sandbox test a product against sample inputs before publishing. Generates 3 test cases
  (happy path, edge case, adversarial) and runs the product against each. Reports behavior
  quality without modifying any files. Use when the creator wants to "test this",
  "try it out", "does it work", or "sandbox test".
argument-hint: "[product-path]"
---

# Test

Sandbox test a product against realistic inputs. Non-destructive — never modifies files.

## Protocol (CE-D35)

1. **Detect product** — Read `.engine-meta.yaml` for category and entry file.

2. **Generate 3 test cases** appropriate for the product type:

   | Test | Purpose | Input Character |
   |------|---------|-----------------|
   | Happy path | Clear, well-formed request | Standard use case the product is designed for |
   | Edge case | Ambiguous or underspecified | Valid but unusual — boundary of stated scope |
   | Adversarial | Off-topic or confusing | Designed to break or confuse the product |

3. **Run each test** — Invoke the product's entry file with the test input. Observe behavior.

4. **Report per test:**
   - Did the product handle it correctly?
   - Did it fail gracefully (if applicable)?
   - Output quality assessment (1-5 scale)
   - Specific observations

## Output Format

```
TEST REPORT — {product-name}

Test 1: Happy Path
  Input: "{test input}"
  Result: PASS | PARTIAL | FAIL
  Quality: {1-5}/5
  Notes: {observation}

Test 2: Edge Case
  Input: "{test input}"
  Result: PASS | PARTIAL | FAIL
  Quality: {1-5}/5
  Notes: {observation}

Test 3: Adversarial
  Input: "{test input}"
  Result: PASS | PARTIAL | FAIL
  Quality: {1-5}/5
  Notes: {observation}

Overall: {summary} — {recommendation}
```
