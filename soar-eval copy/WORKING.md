# WORKING - SOAR Pydantic Eval

## Active Work

No active tasks. Project is in review/handoff state.

---

## Backlog

### Future Enhancements

| Item | Rubric | Notes |
|------|--------|-------|
| Intubation attempts count | A-PRT1 | If narrative states "2 attempts" and output omits, could be added to A-PRT1 inclusion criteria |
| Capacity in refusals | A-REF | Currently handled by A-BHV2; consider explicit A-REF benchmark if recurring issue |
| OCR robustness testing | N/A | Test extraction from OCR-based inputs (handwritten notes, scanned forms) |
| Spelling/abbreviation consistency | A-FMT | Extend A-FMT2 to flag inconsistent abbreviations within same document |
| Timeline plausibility | A-TMP | Check that scene/transport durations are realistic (not negative, not impossibly long) |
| Demographic mismatch flags | A-FCT | Flag when extracted age/sex contradicts contextual clues in narrative |

---

## Open Questions

- **Rubric weight rebalancing**: With 16 rubrics, should weights be reassessed?
- Should rubrics be template-specific or universal?
- What minimum DII score qualifies as "production ready"?

---

## Recently Completed (Summary)

| Phase | Summary | Date |
|-------|---------|------|
| Phase 1 | Threshold updates (A-SFT, A-FMT, A-CMP5, A-EVD1 → hard gates) | 2025-11 |
| Phase 2 | LLM prompt refinements (6 prompts) | 2025-11 |
| Phase 3 | New rubrics (A-PED, A-CAR, A-REF, A-STR, A-TRM, A-OBS, A-BHV) | 2025-11 |
| Phase 4 | Existing benchmark enhancements | 2025-11 |
| Phase 5 | Scope boundary clarification, FIELD_SPECS consolidation | 2025-11 |
| Phase 6 | A-UNC rubric + benchmarks (A-UNC1, A-UNC2) for uncertainty handling | 2025-11 |
| Phase 7 | Placeholder benchmark definitions (A-CMP2-4, A-EVD3, A-FMT2, A-TMP3-4) | 2025-11 |

For full details, see git history or `docs/archive/`.

---

## Current State (Validated)

```
Rubrics:    16
Benchmarks: 46
Prompts:    32
Issues:     0
```

Run `python3 tools/validate_consistency.py` to verify.

---

## Reference

- **Placeholder definitions source**: `docs/placeholder-benchmark-definitions.md`
- **Parent SOAR framework**: `zy_experimental/soar-framework/soar-overview.md`
- **Rubric field specs**: `rubrics/FIELD_SPECS.md`
- **Benchmark field specs**: `benchmarks/FIELD_SPECS.md`
