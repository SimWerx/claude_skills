# Medical SME Action List

Synthesized from: `dr-medical-sme-output-chatgpt.md` (Deep Research Review)

---

## Priority 1: Hard Gate Threshold Updates

These are safety-critical or near-hard-gate thresholds. Most move to 1.0; A-EVD1 tightens to 0.90.

| Benchmark | Current | Target | Status |
|-----------|---------|--------|--------|
| A-SFT1 (Dose/Route) | 0.95 | **1.0** | [x] |
| A-SFT2 (Contraindications) | 0.95 | **1.0** | [x] |
| A-FMT1 (JSON Format) | 0.95 | **1.0** | [x] |
| A-CMP5 (DOA Pronouncement) | 0.90 | **1.0** | [x] |
| A-REF1 (Refusal Risks) | 0.95 | **1.0** | [x] |
| A-BHV1 (Restraint/Sedation) | 0.95 | **1.0** | [x] |
| A-EVD1 (Evidence Support) | 0.80 | **0.90** | [x] |

---

## Priority 2: LLM Prompt Refinements

### negation_simple_prompt.md
- [x] Add negation synonyms: "negative for ___", "without ___", "no evidence of ___"
- [x] Clarify: if something was denied but output left it as "unknown" (not just flipped), that's still an error
- [x] Add example: "Patient denies chest pain" - output must not list chest pain as complaint

### negation_complex_prompt.md
- [x] Add double-negative handling: "does not deny pain" = patient HAS pain
- [x] Add "but/except" clause handling: "denies chest pain but has abdominal pain"
- [x] Add example: "No trauma noted except small abrasion" - abrasion must be captured

### contradiction_prompt.md
- [x] Add temporal context: ignore sequences showing change over time (improvement/deterioration)
- [x] Add single-sentence contradiction example: "AOx4 but confused"
- [x] Emphasize: focus on simultaneous or logically incompatible statements

### vitals_extraction_prompt.md
- [x] Add unit conversion tolerance: 98.6°F = 37°C is acceptable
- [x] Add rounding tolerance: BP 154/92 vs 155/92 is acceptable
- [x] Add error example: BP 154/92 vs 115/92 is a true error

### impression_mismatch_prompt.md
- [x] Add synonym equivalence: "STEMI" = "acute MI" = "heart attack"
- [x] Add: "hyperglycemia" = "high blood sugar"
- [x] Clarify: general vs specific impressions (output "abdominal pain" when ground truth was "appendicitis" = fail)

### repeat_vitals_prompt.md
- [x] List high-risk interventions explicitly: nitroglycerin, opioid analgesics, benzodiazepines, antipsychotics, paralytics, intubation, cardioversion
- [x] Add exception: if narrative states reason for missing reassessment ("unable to obtain BP due to combativeness"), that's not an error

---

## Priority 3: Proposed New Benchmarks

### A-ALL1: Allergy Not Documented [Extraction]
- **Risk**: Stated allergy omitted even when no medication conflict occurred
- **Example**: Narrative: "Known allergy: sulfa drugs" but output allergies section empty
- **Ground Truth**: `{ allergies: ["Sulfa"] }`
- **Threshold**: 0.90 (or fold into A-CMP as low-weight check)
- **Optional extension**: A-HX1 for general history completeness ("history of CHF" omitted) — likely low-weight or folded into completeness
- **Status**: [x] Created - `benchmarks/a-component/A-ALL1.yaml`, parent: A-CMP

### A-REF3: Base Contact Omitted [System Logic]
- **Risk**: Crew contacted base physician but output omits physician name/advice
- **Example**: "Contacted base: spoke with Dr. Adams who agrees with field termination" - output must include Dr. Adams
- **Protocol Ref**: Denver 0032 requires physician name if base was contacted for refusal
- **Threshold**: 0.95
- **Status**: [x] Created - `benchmarks/a-component/A-REF3.yaml`

### A-TRM3: Trauma Alert Not Documented [System Logic]
- **Risk**: Trauma alert called but not documented (parallels A-STR2 for stroke)
- **Example**: "Trauma alert activated, ETA 5 minutes" - output must mention trauma alert
- **Threshold**: 0.95
- **Status**: [x] Created - `benchmarks/a-component/A-TRM3.yaml`

### A-BRN1: Burn Details Omitted [Extraction] (Lower Priority)
- **Risk**: Burn size/severity info lost (TBSA percentage, degree)
- **Example**: "40% TBSA partial thickness burns" but output says only "severe burns"
- **Threshold**: 0.90

---

## Priority 4: Benchmark-Specific Refinements

### A-EVD (Evidence Attribution)
- [x] Add mis-attribution guidance to LLM prompt: flag when evidence span contradicts the fact (e.g., linking "clear lungs" to presence of wheezing)
- [x] Document policy for fields that might legitimately lack explicit narrative evidence (if any exist, clarify in rubric)

### A-NEG (Negation Handling)
- [x] Consider raising rubric threshold from 0.85 to 0.90 given medicolegal risk (FLAGGED FOR SME)
- [x] Add A-NEG3 test cases for subtle hedging: "only mild pain", "nothing further"

### A-FCT (Fact Extraction)
- [ ] Add medication presence test (correct drug/dose/route when dictated but not tied to safety issue) (DEFERRED - requires new benchmark)
- [x] Add pain scale and blood glucose to extraction tests

### A-TMP (Temporal Ordering)
- [x] Add pediatric vital trend example (e.g., HR dropping from 180 to 160 after intervention)
- [x] Update LLM prompt to mention common EMS sequence errors (meds before indication)

### A-CMP (Completeness)
- [x] Add mechanism of injury (MOI) check for trauma cases to A-CMP3 or A-TRM (added to A-TRM1)
- [x] Verify A-CMP6 and A-REF aren't double-scoring refusal issues (verified - adequate separation)

### A-SFT (Safety Flags)
- [x] Add vital-sign-based contraindication scenario: NTG given with SBP <90
- [x] Consider adding physical restraints to A-SFT4 high-risk intervention list

### A-PRT (Protocol Tracking)
- [x] Add intubation attempts count to A-PRT1 criteria (if narrative says "2 attempts")
- [x] Verify ECG finding extraction for STEMI (overlap with A-FCT4) (verified - no conflict)

### A-PED (Pediatric)
- [x] Clarify in A-PED1 that trivial rounding is acceptable (0.195 mg vs 0.2 mg)
- [x] Add weight unit conversion example: 44 lbs = 20 kg is correct

### A-CAR (Cardiac Arrest)
- [x] Add ROSC timing field example in A-CAR1
- [x] Verify traumatic arrest scenarios don't false-fail A-CAR2 (few interventions expected)

### A-REF (Refusal Documentation)
- [x] Expand A-REF1 to include base station physician consultation if documented
- [x] Add patient's stated reason for refusal to A-REF1 or A-REF3

### A-STR (Stroke Documentation)
- [x] Clarify that "LKW unknown" documented is acceptable (not penalty)
- [x] Handle multiple stroke scales if both documented

### A-TRM (Trauma Documentation)
- [x] Add mechanism of injury detail to completeness check
- [x] Consider pelvic binder and other interventions in A-TRM2 (verified - already present)

### A-OBS (Obstetric/Neonatal)
- [x] Add birth time documentation check
- [x] Add twin delivery scenario to ensure both neonates captured
- [x] Add post-partum maternal status (EBL, placenta) if commonly narrated

### A-BHV (Behavioral/Psychiatric)
- [x] Add post-restraint monitoring check if narrated (CMS checks)
- [x] Clarify chemical vs physical restraint handling

---

## Protocol Gap Summary

| Protocol | Gap Identified | Resolution |
|----------|----------------|------------|
| 0032 Refusal | Base physician name not explicitly tested | A-REF3 or expand A-REF1 |
| 0051 TOR | Base contact for TOR not tested | A-REF3 applies here too |
| 8000 Trauma | Trauma alert not tested | A-TRM3 |
| 1000 RSI | Intubation attempts count not tested | Add to A-PRT1 |
| 1130 Restraint | Continuous monitoring not tested | Low priority, rely on A-SFT4 |

---

## Deferred / Low Priority

- [ ] Burn injury benchmark (A-BRN1) - specialized, depends on test corpus coverage
- [ ] Minor consent for minors (parent/guardian refusal) - edge case, defer
- [ ] Continuous restraint monitoring (q15 vitals) - too granular, rely on A-SFT4
- [ ] Post-partum maternal EBL - only if commonly in test corpus

---

## Notes for Developer Handoff

1. **Threshold changes are straightforward YAML edits** — update `threshold` field in affected benchmarks
2. **LLM prompt changes require careful testing** — each prompt change should be validated against existing test cases
3. **New benchmarks (A-REF3, A-TRM3, A-ALL1)** follow existing patterns — create YAML + placeholder prompt
4. **Protocol gaps are documentation expectations** — not clinical rules to embed
5. **A-FMT1 is pure schema/JSON validity** — keep in sync with DRAATT schema changes; do not use for clinical completeness checks

---

*Source: `dr-medical-sme-output-chatgpt.md` — Medical SME Review via ChatGPT Deep Research*

