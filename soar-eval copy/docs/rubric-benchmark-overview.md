# Rubric and Benchmark Conceptual Overview

This document explains how Rubrics and Benchmarks interact in the SOAR evaluation framework.

For field-level specifications, see:
- **Rubric fields**: `rubrics/FIELD_SPECS.md`
- **Benchmark fields**: `benchmarks/FIELD_SPECS.md`

---

## How Rubrics and Benchmarks Interact

### Rubric (Evaluation Category)

A **Rubric** is an organizational grouping of related evaluation criteria that focuses on a specific quality dimension. It answers:
- **What area** are we evaluating? (e.g., Preservation Tracking, Safety Flag Tracking)
- **Why** does this category matter? (e.g., ensures semantic meaning preservation)
- **How** do we aggregate scores from individual tests? (weighted average, minimum, etc.)
- **What's** the passing threshold for this category?

### Benchmark (Specific Test/Metric)

A **Benchmark** is the actual measurable test within a rubric. Each benchmark defines:
- **What exactly** is being measured? (e.g., "DRAATT Section Coverage")
- **How** is it calculated? (formula, automated script, LLM-as-a-judge prompt)
- **What's** the passing threshold for this specific test?
- **How much** does this test contribute to the rubric score? (weight)

### Hierarchy

```
Rubric: A-PRT (Preservation Tracking) - Weight: 20%, Threshold: 80%
├── Benchmark: A-PRT1 (Section Coverage) - Weight: 25%, Threshold: 90%
├── Benchmark: A-PRT2 (Temporal Ordering) - Weight: 25%, Threshold: 85%
├── Benchmark: A-PRT3 (Entity Preservation) - Weight: 25%, Threshold: 80%
└── Benchmark: A-PRT4 (Negation Handling) - Weight: 25%, Threshold: 90%
```

### Scoring Flow

1. Each **Benchmark** runs its evaluator (code-based or LLM-as-a-judge) and produces a score (0.0-1.0)
2. **Rubric** aggregates benchmark scores using its aggregation method
3. Final rubric score compared to rubric passing threshold

### Example Calculation

```
A-PRT1 score: 0.95 x 0.25 weight = 0.2375
A-PRT2 score: 0.88 x 0.25 weight = 0.2200
A-PRT3 score: 0.82 x 0.25 weight = 0.2050
A-PRT4 score: 0.92 x 0.25 weight = 0.2300
─────────────────────────────────────────
A-PRT total: 0.8925 (89.25%) PASS (threshold: 80%)
```

### Analogy

- **Rubric** = Course (e.g., "English 101" with overall grade threshold)
- **Benchmark** = Individual assignments (essay, midterm, final) each with weight and grade
- Final course grade = weighted average of all assignments

---

## Submission Checklist

Before handing off completed rubrics/benchmarks, verify:

- [ ] Each Rubric dimension has a clear evaluation scale
- [ ] Each Rubric dimension has scoring criteria for all levels
- [ ] Each Benchmark provides concrete examples at multiple quality levels
- [ ] Examples are drawn from or applicable to the synthetic-data-gen project
- [ ] Related validators/tools are identified for each criterion
- [ ] Edge cases and common mistakes are documented

---

## Open Questions

1. **Scope**: Which aspects of the 4-pass workflow do evaluations cover?
   - Pass 1 (scaffold quality)?
   - Pass 2 (strategic planning quality)?
   - Pass 3 (narrative quality)?
   - Pass 4 (validation accuracy)?

2. **Granularity**: Should Rubrics be:
   - Template-specific (separate for full-draatt, doa, airport-transfer, rsi-overlay)?
   - Universal (apply to all templates)?
   - A mix (some universal, some template-specific)?

3. **Automation**: Which dimensions can be automated via validators vs require human/LLM judgment?

4. **Failure Modes**: What are the most critical failure modes to catch?
   - YAML-body inconsistency?
   - Implausible artifacts?
   - Template non-compliance?
   - Missing required content?

5. **Thresholds**: What minimum scores qualify as "acceptable" for production use?

