# SOAR Evaluation Framework — Action Items

**Source**: Synthesized from deep research validation (v0 and v1)  
**Purpose**: Actionable implementation guide for SOAR rubrics, benchmarks, and DII scoring

---

## 1. Implement Hybrid Scoring (Continuous + Binary Gates)

### Validated Finding
Mature evaluation frameworks combine granular numeric scoring for improvement tracking with hard pass/fail gates for safety-critical items. "Numerical averages don't tell you how many individual bad outputs you have" — a high DII score must not mask unacceptable failures.

### Action Items

- [ ] **Classify benchmarks by criticality tier**
  - **Tier 1 (Hard Gate)**: Any failure blocks deployment regardless of DII
    - A-SFT1: Allergy/contraindication detection
    - A-SFT2: Hallucination detection (claims not in transcript)
    - A-NEG1-4: Negation misinterpretation (polarity errors are dangerous)
  - **Tier 2 (Threshold Gate)**: Must meet threshold, but composite can compensate slightly
    - A-FCT: Fact extraction accuracy
    - A-CMP: Completeness
    - A-PRT: Protocol adherence
  - **Tier 3 (Improvement Signal)**: Tracked for improvement, not deployment gates
    - A-FMT: Formatting
    - A-TMP: Temporal ordering

- [ ] **Add `criticality` field to benchmark YAML schema**
  ```yaml
  criticality: hard_gate | threshold_gate | improvement_signal
  ```

- [ ] **Define "never event" criteria**
  - Document specific errors that fail the entire evaluation regardless of other scores
  - Examples: suggesting medication patient is allergic to, fabricating vital signs

- [ ] **Implement gate logic in aggregation code**
  - Before computing DII, check all hard gates pass
  - If any hard gate fails, DII = 0 (or "BLOCKED") regardless of other scores

---

## 2. Validate and Maintain Benchmark Taxonomy

### Validated Finding
20 benchmarks is appropriate granularity for EMS documentation AI — comparable to PDQI-9 (9 attributes) and "Medicine for AI" framework (45 disorders). The hierarchy of 8 rubrics → 20 benchmarks is well-structured. Framework should scale to 50+ benchmarks if needed.

### Action Items

- [ ] **Audit current 20 benchmarks for overlap**
  - If two benchmarks consistently correlate > 0.9, consider consolidation
  - Track which benchmarks never fire (rare errors) — candidates for merge or retirement

- [ ] **Monitor for taxonomy gaps during evaluation**
  - If a new error pattern emerges not covered by existing codes, add benchmark
  - Guiding principle: "iterate until new traces reveal no new failure modes"

- [ ] **Consider A-TPL (Template Compliance) rubric**
  - If template-specific checks (DOA pronouncement, RSI checklist) proliferate
  - Currently under A-CMP and A-PRT, but may warrant own rubric

- [ ] **Document taxonomy evolution process**
  - Who can propose new benchmarks?
  - What evidence threshold triggers a new code?
  - How are deprecated codes handled?

---

## 3. Address Retrospective Documentation Gaps

### Validated Finding
Current framework covers core dimensions (completeness, accuracy, evidence, consistency). Research identifies three potential gaps specific to retrospective documentation AI.

### Action Items

- [ ] **Gap 1: Clarity/Readability**
  - Not critical for automated metrics (LLM output is generally grammatical)
  - Add to SME review rubric (S-pillar) rather than A-pillar
  - Consider A-FMT2 (Readability) LLM-judge only if user complaints emerge

- [ ] **Gap 2: Conciseness**
  - AI-generated notes tend toward verbosity (research confirms this)
  - Monitor word count and redundancy as telemetry
  - Add to O-pillar usability survey: "Is the note too long?"
  - Only add A-pillar metric if verbosity becomes a pattern

- [ ] **Gap 3: Uncertainty Handling**
  - Critical: AI must not hallucinate when data is missing
  - Critical: AI must flag unknowns rather than silently omit
  - **Action**: Create A-UNC (Uncertainty Handling) rubric with benchmarks:
    - A-UNC1: Hallucination on missing data (filled in value not in transcript)
    - A-UNC2: Silent omission (required field blank without clarification prompt)
  - Leverage `unknowns_used` and `data_gaps` artifact tags from synthetic data

- [ ] **Ensure template-specific coverage**
  - RSI: induction agent, ETT confirmation documented
  - DOA: time of death, pronouncement included
  - Airport Transfer: acceptance language, receiving facility
  - Map each template's mandatory fields to A-CMP or A-PRT benchmarks

---

## 4. Prepare for Pydantic Evals Implementation

### Validated Finding
YAML schema captures correct information for Pydantic Evals mapping. Key pattern: Dataset → Cases → Evaluators. Pydantic Evals does not natively handle weights/thresholds — those are post-processing concerns.

### Action Items

- [ ] **Map each benchmark to evaluator type**
  
  | Evaluator Type | When to Use | Examples |
  |----------------|-------------|----------|
  | `EqualsExpected` | Ground truth comparison | Vitals match, patient name match |
  | `Contains` | Substring check | Medication mentioned |
  | `LLMJudge` | Nuanced judgment | Negation interpretation, clinical consistency |
  | `Custom` | Complex logic | Protocol step verification |

- [ ] **Implement inclusion criteria as case filtering**
  - Use transcript frontmatter tags (e.g., `negation_risk: [...]`)
  - Attach evaluators only to relevant cases
  - Example: A-SFT2 (contraindication) only runs on cases with medication + allergy

- [ ] **Design hybrid evaluator chains**
  - Pattern: deterministic check first, LLM judge second (efficiency)
  - Example for A-NEG1:
    1. `Contains(value="denies")` — does case involve negation?
    2. `CustomCheck` — is negated symptom marked present in output?
    3. `LLMJudge(rubric="...")` — confirm negation handling

- [ ] **Plan aggregation layer (separate from Pydantic)**
  - Compute per-benchmark scores (0.0–1.0 or boolean)
  - Apply weights within rubrics
  - Apply rubric weights to compute A-pillar score
  - Check hard gates before computing DII

- [ ] **Create evaluator-to-benchmark mapping table**
  ```yaml
  # evaluators/mapping.yaml
  A-NEG1:
    evaluators:
      - type: Contains
        config: { value: "denies" }
        scope: input
      - type: LLMJudge
        config: { prompt_file: "evaluators/llm-judge/negation_simple_prompt.md" }
    aggregation: all_must_pass
  ```

---

## 5. Establish DII Governance and Evolution

### Validated Finding
A-heavy weighting (45%) in early stages is appropriate — you have synthetic data and automated checks but no real-world outcomes. Plan to increase S, O, R weights as deployment matures.

### Action Items

- [ ] **Document current weight rationale**
  ```
  DII = 0.35·S + 0.15·O + 0.45·A + 0.05·R
  
  Rationale (Phase 1 - Pre-deployment):
  - A (45%): Primary signal — synthetic data allows extensive automated testing
  - S (35%): SME review validates clinical accuracy
  - O (15%): Limited user feedback available
  - R (5%): No real-world outcome data yet
  ```

- [ ] **Define phase transition triggers**
  
  | Phase | Trigger | Weight Adjustment |
  |-------|---------|-------------------|
  | Phase 1 | Pre-deployment | 0.35 S, 0.15 O, 0.45 A, 0.05 R |
  | Phase 2 | Pilot (n=100 cases) | 0.30 S, 0.20 O, 0.40 A, 0.10 R |
  | Phase 3 | Production (1 month) | 0.25 S, 0.20 O, 0.35 A, 0.20 R |
  | Phase 4 | Mature (6 months) | 0.20 S, 0.20 O, 0.30 A, 0.30 R |

- [ ] **Implement hard gates independent of DII**
  - Policy: "DII is meaningful only if all Tier 1 gates pass"
  - DII can be 0.95, but if A-SFT fails, deployment blocked

- [ ] **Plan weight validation using outcome correlation**
  - Once R data exists, correlate with A metrics
  - If A-NEG strongly predicts real-world errors, validate its weight
  - If a metric doesn't correlate with outcomes, reduce weight or retire

- [ ] **Create DII transparency dashboard (future)**
  - Show composite score with drill-down to S/O/A/R
  - Show rubric-level scores under A
  - Show benchmark-level detail for debugging
  - Flag any hard gate failures prominently

---

## 6. Finalize Rubric and Benchmark YAML Schema

### Validated Finding
Current schema captures needed information. Minor additions recommended for implementation clarity.

### Action Items

- [ ] **Add fields to rubric schema**
  ```yaml
  # rubrics/schema-additions.yaml
  code: A-NEG
  label: Negation Handling
  description: ...
  weight: 0.125
  aggregation_method: WEIGHTED_AVERAGE
  passing_threshold: 0.85
  hard_gate: false  # NEW: if true, any failure blocks deployment
  evaluation_guidelines: ...
  benchmarks: [A-NEG1, A-NEG2, ...]
  ```

- [ ] **Add fields to benchmark schema**
  ```yaml
  # benchmarks/schema-additions.yaml
  code: A-NEG1
  parent_rubric: A-NEG
  label: Simple Negation Misinterpretation
  concept: ...
  weight: 0.25
  threshold: 0.90
  criticality: hard_gate | threshold_gate | improvement_signal  # NEW
  evaluator_type: hybrid
  evaluator_config:  # NEW: structured config for Pydantic translation
    deterministic:
      - type: Contains
        config: { value: "denies" }
    llm_judge:
      prompt_file: "evaluators/llm-judge/negation_simple_prompt.md"
  inclusion_criteria: ...
  exclusion_criteria: ...
  examples: ...
  ```

- [ ] **Validate all 20 benchmarks have complete fields**
  - Run schema validation on each file
  - Ensure `criticality` assigned to all
  - Ensure `evaluator_config` present for implementation handoff

---

## 7. Immediate Next Steps (Priority Order)

1. **Add `criticality` field to all benchmarks** — enables gate logic
2. **Create A-UNC rubric for uncertainty handling** — addresses identified gap
3. **Document "never event" criteria** — defines hard gate failure conditions
4. **Map benchmarks to Pydantic evaluator types** — implementation blueprint
5. **Add `evaluator_config` to benchmark schema** — structured implementation spec
6. **Create DII phase transition document** — governance for weight evolution

---

## References

- Evidently AI: "Numerical averages don't tell you how many bad outputs you have"
- PDQI-9: 9-attribute clinical note quality instrument
- Mercor: Domain expert labeling with clear inclusion/exclusion criteria
- Pydantic Evals: Dataset → Cases → Evaluators hierarchy
- Industry consensus: Hybrid approach (continuous scoring + binary gates)

## Terminology

| Term | Definition |
|------|------------|
| **Benchmark** | Atomic measurable test within a rubric (e.g., A-NEG1) |
| **Rubric** | Organizational grouping of related benchmarks (e.g., A-NEG) |
| **DII** | DRAATT Intelligence Index — composite score across S/O/A/R pillars |
| **Hard gate** | Binary pass/fail that blocks deployment regardless of composite score |
| **Threshold** | Minimum acceptable score for a benchmark or rubric |

---

*This document synthesizes validated research findings into actionable implementation tasks. Execute in priority order, updating WORKING.md as tasks complete.*

