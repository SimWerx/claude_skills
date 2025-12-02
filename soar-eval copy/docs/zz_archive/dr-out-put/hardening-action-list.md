## Hardening Action List

> **Source of truth**: This document is the authoritative, implementation-ready
> action list for clinical hardening. When implementing, use the existing
> rubrics/benchmarks and other files in this repo as your clinical and
> behavioral specification. Do **not** introduce new protocol rules,
> web-sourced guidance, or training-time medical knowledge. The goal is to
> encode existing SME decisions, not extend the research.
>
> **Historical reference**: This list was derived from
> `docs/backlog/clinical-hardening.md`, which may be consulted for additional
> context if needed.
>
> **Last reconciled**: 2025-11-29 — Status checkboxes verified against codebase state.

### Critical Priority

- [x] **Implement A-FCT2 Medication Extraction benchmark**
  - **Goal**: Ensure every medication explicitly stated in narrative (name, dose, route) appears correctly in structured output.
  - **Scope**: All call types; focus on analgesics, antiemetics, cardiac meds, sedation, RSI adjuncts.
  - **Files**: `rubrics/A-FCT.yaml`, `benchmarks/a-component/A-FCT2.yaml` (new), associated LLM-judge prompt if needed.

- [x] **Implement A-FCT3 Procedure Extraction benchmark**
  - **Goal**: Ensure non-medication procedures (IV/IO starts, 12-leads, oxygen therapy, basic procedures not already covered by trauma/RSI rubrics) are preserved from narrative into structured output.
  - **Scope**: Common non-critical interventions whose omission impacts QA/billing and clinical clarity.
  - **Files**: `rubrics/A-FCT.yaml`, `benchmarks/a-component/A-FCT3.yaml` (new), prompts if applicable.

- [x] **Enhance A-TMP3 – Protocol Step Ordering**
  - **Goal**: Verify that within protocol-driven sequences (e.g., RSI, STEMI, arrest loops, stroke timelines), documented events appear in clinically plausible order.
  - **Examples**: Sedation before paralytic in RSI; defibrillation before epinephrine in VF; stroke alert after LKW assessment.
  - **Files**: `rubrics/A-TMP.yaml`, `benchmarks/a-component/A-TMP3.yaml` (enhance existing).

- [x] **Repurpose A-TMP4 for Explicit Timing Consistency; preserve Trend Direction as A-TMP5**
  - **Goal**: Check that explicit times and intervals (departure/arrival times, ROSC time, field delivery time) are sequential and consistent with narrative.
  - **Scope**: Scenarios where narrative provides specific timestamps or durations.
  - **Note**: Current A-TMP4 ("Trend Direction Misinterpreted") is a valid concept and must be preserved as A-TMP5 before repurposing A-TMP4.
  - **Files**: 
    - `benchmarks/a-component/A-TMP5.yaml` (new – copy current A-TMP4 content, relabel as Trend Direction)
    - `benchmarks/a-component/A-TMP4.yaml` (replace content with Explicit Timing Consistency)
    - `rubrics/A-TMP.yaml` (add A-TMP5 to benchmark list)
    - `evaluators/llm-judge/timing_consistency_prompt.md` (new prompt for A-TMP4)
    - Keep `evaluators/llm-judge/trend_direction_prompt.md` (now referenced by A-TMP5)

- [x] **Define A-CMP2 / A-CMP3 / A-CMP4 section-level completeness benchmarks**
  - **Goal**: Enforce completeness for `Response`, `Arrival/Scene`, and `Assessment` sections when narrative contains content for those areas.
  - **Examples**:
    - A-CMP2: Response delays or upgrades mentioned in narrative must appear in structured response section.
    - A-CMP3: Scene/arrival details (mechanism, bystander info, hazards) must not be dropped.
    - A-CMP4: Major exam systems described (neuro, respiratory, cardiovascular) must appear in Assessment.
  - **Files**: `rubrics/A-CMP.yaml`, `benchmarks/a-component/A-CMP2.yaml`, `A-CMP3.yaml`, `A-CMP4.yaml`.
  - **Status**: Implemented. Benchmarks exist with full `inclusion_criteria`, `exclusion_criteria`, and examples.

- [x] **Define A-EVD3 – Evidence Contradiction / Irrelevance**
  - **Goal**: Ensure evidence spans used to justify structured facts do not contradict the fact and are semantically relevant.
  - **Examples**: Evidence span "denies chest pain" mapped to `chest_pain: true`; span describing unrelated complaint mapped to primary impression.
  - **Files**: `rubrics/A-EVD.yaml`, `benchmarks/a-component/A-EVD3.yaml`.
  - **Status**: Implemented as "Evidence Span Misalignment" with hybrid evaluator and LLM prompt.

- [x] **Enforce explicit capacity documentation in refusals**
  - **Goal**: Make refusal documentation fail if patient decision-making capacity is not clearly documented when applicable.
  - **Mechanics**:
    - Tighten A-REF1 to treat absence of a capacity statement (when narrative supports it) as a failure.
    - Ensure A-UNC2 marks capacity as a critical field that must be flagged `unknown` if truly unavailable.
  - **Files**: `rubrics/A-REF.yaml`, `benchmarks/a-component/A-REF1.yaml`, `benchmarks/a-component/A-UNC2.yaml`.
  - **Status**: Implemented. A-REF1 concept/inclusion_criteria/examples updated; A-UNC2 concept strengthened; A-REF rubric critical_requirements updated.

### High Priority

- [x] **Restraint/sedation documentation details (RASS + de-escalation)**
  - **Goal**: When narrative includes IMC-RASS scores and de-escalation attempts prior to restraint/sedation, ensure they are preserved in output.
  - **Actions**:
    - Update A-BHV1 concept/criteria to explicitly mention capturing RASS and de-escalation efforts if present.
    - Ensure LLM-judge prompt for A-BHV1 checks for these details when applicable.
  - **Files**: `rubrics/A-BHV.yaml`, `benchmarks/a-component/A-BHV1.yaml`, `evaluators/llm-judge/*behavioral*_prompt.md`.
  - **Status**: Implemented. A-BHV1 concept/inclusion_criteria/examples updated; restraint_sedation_prompt.md updated with RASS and de-escalation conditions.

- [x] **Twin / multi-newborn delivery handling**
  - **Goal**: Guarantee that each neonate in a multi-birth scenario is documented with distinct APGARs and status.
  - **Actions**:
    - Confirm A-OBS1 examples and criteria explicitly require separate documentation for each baby.
    - Add or tag benchmark cases that exercise twin/multiple deliveries.
  - **Files**: `rubrics/A-OBS.yaml`, `benchmarks/a-component/A-OBS1.yaml`, relevant benchmark YAMLs.
  - **Status**: Implemented. A-OBS1 concept/examples updated; neonatal_apgar_prompt.md updated with multi-birth handling conditions.

- [x] **Medication contraindication override rationale**
  - **Goal**: Treat documented protocol overrides (e.g., giving contraindicated med with base approval) as acceptable when rationale appears in output.
  - **Actions**:
    - Refine A-SFT2 acceptable-deviation criteria to explicitly permit contraindicated administration if override rationale is present.
    - Adjust LLM-judge prompt to distinguish unflagged unsafe behavior from documented, physician-directed exceptions.
  - **Files**: `rubrics/A-SFT.yaml`, `benchmarks/a-component/A-SFT2.yaml`, `evaluators/llm-judge/*safety*_prompt.md`.
  - **Status**: Implemented. A-SFT2 evaluator_type changed to hybrid, new example added, contraindication_detection_prompt.md created with pass conditions for documented override rationale.

- [x] **Evidence-contradiction hardening**
  - **Goal**: Tie A-EVD3 into the evaluation harness to specifically test narrative vs structured contradictions using evidence spans.
  - **Actions**:
    - Design A-EVD3 benchmark cases where the evidence span plainly contradicts the field value.
    - Ensure scoring and prompts penalize contradictions even when extraction is otherwise "complete."
  - **Files**: `benchmarks/a-component/A-EVD3.yaml`, `evaluators/llm-judge/evidence_misalignment_prompt.md`.
  - **Status**: A-EVD3 implemented; `evidence_misalignment_prompt.md` exists. Example quality review remains in "Example-quality" section.

### Medium Priority

- [x] **General section completeness (Dispatch/Response/Arrival/Assessment)**
  - **Goal**: Use A-CMP2-4 to catch missing but clinically relevant content within sections when narrative provides it.
  - **Actions**:
    - Define inclusion/exclusion rules so extraction errors (missing individual facts) are owned by A-FCT/A-NEG, while completely empty or skeletal sections are owned by A-CMP2-4.
    - Add 1–2 realistic scenarios per section type.
  - **Files**: `rubrics/A-CMP.yaml`, `benchmarks/a-component/A-CMP2.yaml`–`A-CMP4.yaml`.
  - **Status**: Benchmark definitions complete. Additional scenario/example work tracked in "Example-quality" section.

- [x] **Pediatric documentation clarifications (A-PED / A-OBS interplay)**
  - **Goal**: Clarify division of responsibility between pediatric and OB rubrics and ensure Broselow-based weight documentation is exercised.
  - **Actions**:
    - Decide whether APGAR omissions are primarily owned by A-OBS1 vs A-PED2 and reflect that in rubric text.
    - Add at least one Broselow tape example (color/estimated weight) to A-PED2 and ensure extraction is required when present in narrative.
  - **Files**: `rubrics/A-PED.yaml`, `benchmarks/a-component/A-PED2.yaml`, `benchmarks/a-component/A-OBS1.yaml`.
  - **Status**: Implemented. APGAR ownership clarified (A-OBS1 for deliveries, A-PED2 for pediatric patients). Broselow tape examples added to A-PED2.

- [x] **Sepsis/shock protocol documentation (if scenarios exist)**
  - **Goal**: Ensure any explicit sepsis or shock alerts and key documentation elements (e.g., lactate, sepsis alert activation) in narrative are preserved.
  - **Actions**:
    - Decide whether to extend existing rubrics (e.g., A-CMP, A-PRT) or introduce a focused benchmark for sepsis/shock if synthetic scenarios include them.
    - Draft at least one representative benchmark if warranted.
  - **Files**: Candidate new benchmark in `benchmarks/a-component/`, rubric notes in `rubrics/*.yaml`.
  - **Status**: Implemented. Created new A-SEP rubric with A-SEP1 (sepsis alert activation) and A-SEP2 (key sepsis elements) benchmarks, plus sepsis_documentation_prompt.md.

- [x] **Trauma assessment thoroughness**
  - **Goal**: Encourage documentation of all major injuries described in narrative, not just the "worst" one.
  - **Actions**:
    - Consider adding LLM-judge guidance under A-TRM1 to check that all named injuries are reflected.
    - Keep focus on clinically significant injuries to avoid over-penalizing minor omissions.
  - **Files**: `rubrics/A-TRM.yaml`, `benchmarks/a-component/A-TRM1.yaml`, associated prompts.
  - **Status**: Implemented. A-TRM1 concept/inclusion_criteria updated to include injury completeness; trauma_gcs_prompt.md updated with pass conditions for named injuries.

- [x] **Refusal high-risk scenario coverage**
  - **Goal**: Ensure at least one refusal benchmark covers a high-risk post-intervention refusal (e.g., post-naloxone, post-hypoglycemia).
  - **Actions**:
    - Add or adapt an A-REF test case where base contact, risks, capacity, and signature/witness all interact.
  - **Files**: `benchmarks/a-component/A-REF1.yaml`–`A-REF3.yaml`.
  - **Status**: Implemented. Added high-risk post-naloxone and post-hypoglycemia refusal examples to A-REF1, A-REF2, and A-REF3 benchmarks.

### Low Priority / Future Consideration

- [x] **NKDA and allergy niceties**
  - **Goal**: Optionally warn when narrative explicitly says "no known drug allergies" but output leaves allergy field blank instead of NKDA, while still treating this as low-risk.
  - **Actions**:
    - Clarify in A-ALL1 acceptable deviations how NKDA should be represented.
    - Consider adding a soft LLM-judge note rather than a hard failure.
  - **Files**: `benchmarks/a-component/A-ALL1.yaml`, `rubrics/A-CMP.yaml` (if needed).
  - **Status**: Implemented. Updated A-ALL1 exclusion_criteria and allergy_extraction_prompt.md to explicitly accept blank allergy fields as semantically equivalent to "NKDA".

- [x] **Other future enhancements (polish-only checks)**
  - **Goal**: Track low-impact ideas such as image/OCR robustness, spelling/abbreviation consistency, holistic narrative-vs-structured alignment, timeline plausibility, and demographic misdocumentation checks.
  - **Actions**:
    - Record candidate future checks (e.g., OCR-based inputs, A-FMT2 spelling/abbreviation extensions, global contradiction scan, on-scene/transport duration plausibility, age/sex mismatch flags) in `WORKING.md` or a separate design doc.
  - **Files**: `WORKING.md`, potential future rubric skeletons.
  - **Status**: Implemented. Added OCR robustness, spelling/abbreviation consistency, timeline plausibility, and demographic mismatch flags to WORKING.md Future Enhancements table.

### Threshold & Example Updates

- [x] **Threshold adjustments**
  - **A-NEG rubric**: Raise rubric-level threshold from 0.85 → 0.90 to tighten tolerance for negation errors.
    - Files: `rubrics/A-NEG.yaml`.
  - **A-REF2 (signature)**: Raise benchmark threshold from 0.85 → 0.95 to reflect legal importance of refusal signatures/witnesses.
    - Files: `benchmarks/a-component/A-REF2.yaml`.
  - **A-SFT4 (reassessments)**: Set threshold to 1.0 for consistency with A-SFT rubric MIN/1.0 semantics.
    - Files: `benchmarks/a-component/A-SFT4.yaml`, `rubrics/A-SFT.yaml` (commentary).
  - **A-CMP rubric**: Bump rubric-level threshold from 0.80 → 0.85 to slightly tighten completeness expectations.
    - Files: `rubrics/A-CMP.yaml`.
  - **Status**: Implemented. All four threshold adjustments applied.

- [x] **Example-quality and criteria clarifications**
  - **Negation, evidence & impressions**: Add examples for partial denial, contradictory evidence spans, and clear acceptable vs unacceptable impression mappings.
    - Files: `benchmarks/a-component/A-NEG3.yaml`, `A-EVD1.yaml`, `A-EVD3.yaml`, `A-FCT4.yaml`.
  - **Temporal, completeness & arrest**: Add or refine examples for protocol-sensitive ordering, section conflation, DOA field nuances, and explicit ROSC/termination time requirements.
    - Files: `benchmarks/a-component/A-TMP1.yaml`, `A-CMP1.yaml`, `A-CMP5.yaml`, `A-CAR1.yaml`.
  - **Refusal & stroke**: Incorporate examples that jointly exercise risk explanation and capacity (A-REF1/3) and clarify acceptable handling of unknown vs known LKW and stroke alerts (A-STR1/2).
    - Files: `benchmarks/a-component/A-REF1.yaml`, `A-REF3.yaml`, `A-STR1.yaml`, `A-STR2.yaml`.
  - **Trauma & OB**: Broaden A-TRM2/3 examples to include pelvic binder/cricothyrotomy and trauma alert variants; ensure A-OBS1/2 examples clearly cover twin deliveries, delivery time, and placenta/EBL.
    - Files: `benchmarks/a-component/A-TRM2.yaml`, `A-TRM3.yaml`, `A-OBS1.yaml`, `A-OBS2.yaml`.
  - **Behavioral & uncertainty**: Clarify A-BHV1 expectations around RASS, de-escalation, and monitoring examples; ensure A-BHV2 has capacity/implied-consent examples; add a positive A-UNC2 example showing correct "unknown" handling.
    - Files: `benchmarks/a-component/A-BHV1.yaml`, `A-BHV2.yaml`, `A-UNC2.yaml`, relevant prompts.
  - **Status**: Implemented. Examples added/refined across 15 benchmarks.


### Rubric-by-Rubric Recommended Changes (Summary)

This section condenses the per-rubric “Recommended Changes” from `clinical-hardening.md` into implementation checkpoints. Use it alongside the priority sections above.

#### A-NEG (Negation Handling)

- Tighten rubric threshold (see Threshold adjustments) and emphasize “no negated finding is charted as present” as an explicit critical requirement in `rubrics/A-NEG.yaml`.
- Add at least one **partial denial** example to A-NEG3 (e.g., “denies chest pain, just mild soreness”) and ensure evaluation treats this nuance correctly.
- Update A-NEG4 so that **contradictions must be explicitly flagged or resolved**, not just detected silently.

#### A-FCT (Fact Extraction)

- Ensure A-FCT1 test cases explicitly exercise **temperature and EtCO2** and treat them as first-class vitals.
- ~~Implement A-FCT2 and A-FCT3 (see Critical Priority) for medications and procedures.~~ — DONE
- For A-FCT4, retain current synonym handling but be explicit about **LLM judgment boundaries**; avoid adding new clinical rules, only enforce fidelity to scenario ground truth.

#### A-TMP (Temporal Ordering)

- ~~Enhance A-TMP3 (existing) for protocol-step ordering; repurpose A-TMP4 for explicit timing consistency while preserving "Trend Direction Misinterpreted" as new A-TMP5 (see Critical Priority).~~ — DONE
- Include at least one **time-critical stroke timeline** example (LKW vs arrival vs alert) when designing A-TMP3/4 benchmark cases.

#### A-EVD (Evidence Attribution)

- ~~Implement A-EVD3 (see Critical Priority) focused on **contradictory or irrelevant evidence spans**.~~ — DONE
- Add an explicit **contradictory evidence example** (e.g., evidence span "no wheezing" mapped to wheezing: true) and document expected failure behavior.
- Optionally nudge rubric threshold slightly upward (already captured in Threshold adjustments) to reflect importance of evidence mapping, without changing existing hallucination rules.

#### A-CMP (Completeness)

- ~~Define A-CMP2–4 for Response/Arrival/Assessment completeness (see Critical Priority / Medium Priority).~~ — DONE
- Document the **boundary between extraction and completeness**: missing stated facts belong to A-FCT/A-NEG, while near-empty or section-level omissions belong to A-CMP2–4.
- Enhance A-CMP6 (and A-CMP6-airport) examples to highlight **handoff and condition-on-arrival documentation** as key transport completeness elements.

#### A-SFT (Safety Flags)

- Keep A-SFT rubric at MIN/1.0 and set A-SFT4 threshold to 1.0 (Threshold adjustments).
- Decide whether A-SFT3 remains unused or is reserved for a future safety scenario; document this explicitly in `rubrics/A-SFT.yaml` to avoid confusion.
- Expand A-SFT1/2/4 examples with fuller narrative snippets, and include at least one **documented override** scenario where a contraindicated med is given with clear rationale (tied to the “contraindication override rationale” High Priority item).

#### A-PRT (Protocol Tracking)

- Confirm A-PRT1 (RSI) and A-PRT2 (STEMI) remain the only protocol benchmarks here (other protocol checks live under their own rubrics).
- In A-PRT1, ensure examples include an explicit **attempt count** when present in narrative, and verify that output is required to preserve it.
- Optionally add commentary in the rubric about why other protocols (e.g., stroke, trauma) are covered under separate rubrics rather than A-PRT.

#### A-PED (Pediatric Documentation)

- Keep A-PED1/A-PED2 thresholds as-is (peds dosing strict, completeness slightly more forgiving).
- Clarify in A-PED vs A-OBS rubrics **who owns APGAR** for newborns, while still allowing overlap where needed (see Pediatric documentation clarifications).
- Add a concrete **Broselow example** to A-PED2 (color + approximate weight) and require extraction when present.

#### A-CAR (Cardiac Arrest Documentation)

- In A-CAR1, explicitly require **ROSC or termination time** in critical requirements, not just in examples.
- Ensure at least one scenario tests **field termination with base contact**, with both outcome (A-CAR1) and pronouncement fields (A-CMP5) expected to pass.

#### A-REF (Refusal Documentation)

- Raise A-REF2 threshold to 0.95 (Threshold adjustments) and treat missing signature/witness as nearly as critical as missing risk explanation.
- Add at least one **high-risk refusal** scenario (e.g., post-naloxone or post-hypoglycemia) that exercises A-REF1/2/3 plus A-UNC2 capacity handling.
- In A-REF1, ensure capacity documentation is treated as part of the same critical block as risk explanation when narrative supports it.

#### A-STR (Stroke Documentation)

- Keep A-STR thresholds as-is, but ensure examples clearly separate what is **required** (scale, LKW, alert) from what is acceptable to omit.
- Add an explicit **“LKW unknown” acceptable example**, where output must mark LKW as unknown rather than hallucinating a time.

#### A-TRM (Trauma Documentation)

- In A-TRM2, explicitly list **cricothyrotomy** among critical interventions that must be documented if performed.
- Ensure at least one example includes **tourniquet time** and that tests require capturing it when narrated.
- In A-TRM3, keep focus on trauma alert activation, with examples that show level/tier and explicit alert calls.

#### A-OBS (Obstetric & Neonatal Documentation)

- Clarify how A-OBS and A-PED interact for neonatal APGAR (see Pediatric documentation clarifications).
- Ensure examples cover **twin deliveries** with separate neonate entries and that missing data for either neonate is treated as a failure.
- Emphasize placenta status and EBL as required when narrated in postpartum scenarios.

#### A-BHV (Behavioral/Psychiatric Documentation)

- In A-BHV1, explicitly note that **RASS scores and de-escalation attempts**, if present in narrative, should be documented, while maintaining strict stance on restraint/sedation presence.
- In A-BHV2, ensure examples clearly cover **implied consent due to incapacity** (e.g., intoxication/psychosis) and legal hold status.
- Optionally note law-enforcement-applied restraints (e.g., handcuffs) as documentation points when narratively salient, even if EMS did not apply them.

#### A-UNC (Uncertainty Handling)

- In A-UNC2, clearly define what counts as **flagging** (e.g., explicit “unknown/not documented” vs silent nulls) and ensure examples show both failure and success cases.
- Add at least one **positive example** where a missing critical field is correctly marked unknown (e.g., pronouncement time unknown but acknowledged).
- Keep the critical-field list focused on high-liability items (refusal risks, pronouncement time, capacity/consent, key protocol fields) and update only if new critical fields are added elsewhere in the corpus.


### Denver Protocol Gap Analysis (Reference)

The table below summarizes how current benchmarks map to key Denver protocols and where actions above close gaps. It is adapted from `clinical-hardening.md` for implementation reference (no new protocol logic should be added beyond what is already reflected here and in existing YAMLs).

| Protocol | Key Documentation Requirement | Current Coverage in Eval | Gap? | Priority | Action Recommendation |
| --- | --- | --- | --- | --- | --- |
| **0032 - Refusal** | - Risks explained to patient<br>- Patient capacity confirmed<br>- Base contact physician name if required<br>- Signed refusal or witness name | **Covered:** A-REF1 (risks), capacity indirectly via A-UNC2, A-REF3 (base MD), A-REF2 (signature). | **No major gap** (capacity not standalone) | High | Ensure capacity is explicitly documented (tie into A-REF1/A-UNC2); raise A-REF2 threshold so signature omission is never acceptable. |
| **0050 - Field Pronouncement** | - Pronouncement time<br>- Pronouncing physician name<br>- Pronouncement method (base order vs protocol)<br>- Agency notified (coroner) | **Covered:** A-CMP5 checks time, physician, method, agency all present. Base contact aspect also by A-REF3 if applicable. | **No gap** | High | Keep A-CMP5 threshold 1.0; clarify “method” includes standing order vs base order in rubric/docs. |
| **0051 - Termination of Resusc.** | - Base contact for termination (unless criteria met)<br>- Time of termination<br>- Family informed (often) | **Covered:** Outcome/time via A-CAR1 and A-CMP5; base contact via A-CMP5 (method/MD). | **Minor gap:** no explicit check on documenting family informed | Medium | Optionally add narrative guidance or manual SME check for family notification; ensure termination scenarios are evaluated by both A-CAR1 and A-CMP5. |
| **1000 - RSI (Intubation: Oral)** | - Indication for RSI<br>- Pre-oxygenation performed<br>- Sedative drug and dose<br>- Paralytic drug and dose<br>- ETT size and depth<br>- Confirmation methods (EtCO₂ required)<br>- # of attempts<br>- Post-intubation sedation/management | **Covered:** A-PRT1 hits all except explicit scoring of indication; it conceptually expects indication/preoxygenation and checks sedative, paralytic, ETT size/depth, EtCO₂, attempts, post-intubation meds. | **No major gap** | High | Ensure scenarios narrate indication and pre-oxygenation; A-PRT1 must preserve attempts and confirmation details. Threshold 0.90 remains acceptable. |
| **3000 - Cardiac Arrest (ALS)** | - Initial rhythm<br>- All interventions with times (shocks, meds, airway)<br>- ROSC occurrence and time or termination<br>- CPR times (no-flow) often device-driven<br>- Handoff if terminated on scene | **Covered:** Initial rhythm, shock count, meds via A-CAR2; ROSC/time via A-CAR1; termination time via A-CMP5; agency notified via A-CMP5. | **Minor gap:** No explicit eval of CPR quality/timing | Low | Accept CPR quality/timing as out-of-scope; ensure interventions and outcomes are documented via A-CAR1/2 and A-CMP5. |
| **3010 - STEMI (ACS)** | - 12-lead ECG performed/interpreted<br>- ASA 324 mg given (if no allergy)<br>- NTG given if appropriate or contraindication documented<br>- IV access, O₂ as needed<br>- STEMI Alert called with ETA | **Covered:** A-PRT2 checks ASA, 12-lead, STEMI alert, nitro, with contraindication exclusions. IV/O₂ not separately evaluated. | **No major gap** | Medium | Keep IV/O₂ as narrative-only; A-PRT2 already enforces major elements and respects contraindications. |
| **4030 - Stroke (Acute CVA)** | - Stroke scale findings (CPSS/FAST/LAMS)<br>- Last Known Well time<br>- Blood glucose checked<br>- Stroke Alert to hospital if indicated | **Covered:** A-STR1 (scale & neuro findings), A-STR2 (LKW & stroke alert); glucose via A-FCT1. | **No gap** | High | Ensure scenarios always include LKW (or explicit unknown) and stroke alert when applicable; require unknown to be flagged, not invented. |
| **6000 - Psychiatric/Behavioral (General)** | - Mental status/capacity<br>- Mental health hold status and authorizer<br>- Law enforcement involvement if relevant<br>- Implied consent when no capacity | **Covered:** A-BHV2 covers capacity/hold status; PD involvement may be narratively present but not explicitly tested unless tied to restraints. | **Minor gap:** LE-applied restraints not explicitly checked | Low | Optionally add guidance/examples noting handcuffs/LE presence; primary focus remains on EMS-applied restraints and capacity. |
| **6010 - Agitated/Combative** | - De-escalation attempts<br>- IMC-RASS score before restraint/sedation<br>- Medication given for sedation (dose/route)<br>- Physical restraint (type/position)<br>- Reassessment q5–15 min (vitals, limb circulation) | **Covered:** A-BHV1 ensures restraints/sedation documented, with Q15 monitoring if narrated; RASS and de-escalation not strictly enforced; A-SFT4 checks post-intervention reassessments. | **Minor gap:** RASS value and de-escalation attempts not explicitly enforced | Medium | Incorporate RASS and de-escalation into A-BHV1 expectations and prompts while keeping main focus on restraint/sedation presence and monitoring. |
| **6015 - Post-Sedation** | - Continued monitoring (airway, SpO₂, ECG, BP)<br>- Effect of sedation (e.g., calmer) | **Covered:** A-SFT4 checks for repeat vitals after sedation; qualitative effect not explicitly scored. | **No major gap** | Low | Rely on A-SFT4 and A-BHV1; treat behavioral description as nice-to-have rather than a scored requirement. |
| **7000 - Childbirth/OB Emergencies** | - Gravidity/para (GxPx)<br>- Multiple gestation<br>- OB complications (preeclampsia, bleeding)<br>- If delivery: time of birth, gender, APGAR at 1 & 5 min, neonatal interventions<br>- Placenta delivered and EBL | **Covered:** A-OBS2 handles G/P, multiples, complications, EBL; A-OBS1 covers delivery time, APGARs, neonatal status and interventions. | **No gap** | High | Ensure scenarios cover both undelivered OB emergencies and field deliveries; use A-OBS1/2 benchmarks to enforce required fields. |
| **8000 - Trauma General** | - Mechanism of Injury<br>- GCS or mental status<br>- Vital trends<br>- Major exam findings (e.g., distal neuro status) | **Covered:** Mechanism & GCS via A-TRM1; vitals and trends via A-FCT1/A-TMP2; major findings indirectly via trauma/other rubrics. | **Minor gap:** No explicit requirement to document every injury | Low | Accept that minor injuries may be summarized; rely on A-TRM1 and trauma-specific rubrics to enforce critical details. |
| **8010 - Traumatic Arrest** | - Justification for termination in non-survivable injury<br>- If resuscitation, follow 3000 plus mechanism<br>- Transport vs field pronouncement and time | **Covered:** Outcome via A-CAR1; mechanism via A-TRM1; pronouncement via A-CMP5. | **Minor gap:** No explicit check that obvious death signs are documented | Low | Optional future scenario to ensure obvious death signs, if narrated, appear; main enforcement remains outcome and pronouncement completeness. |
| **8110 - Trauma in Pregnancy** | - Pregnancy and gestational age whenever applicable<br>- Pregnancy-specific care actions (tilting, etc.)<br>- Fetal movement if known | **Covered:** Pregnancy/EGA via A-OBS2; trauma details via A-TRM1. | **No gap** | High | Ensure pregnant trauma scenarios are evaluated under both OB and trauma rubrics so pregnancy is not lost in trauma documentation. |


### Completed During Implementation (Not in Original Scope)

The following work was completed during implementation to ensure evaluation quality:

- [x] **LLM Judge Prompt Spec Alignment** (35 prompts)
  - Migrated all prompts in `evaluators/llm-judge/` to canonical structure defined in `PROMPT_SPECS.md`
  - Standardized output schema (`pass`, `reason`, `score`) across all prompts
  - Fixed AND/OR logic errors in compound failure conditions (`silent_omission_prompt.md`, `hallucination_missing_prompt.md`, `contradiction_prompt.md`)
  - Created validation tools: `tools/validate_prompt_structure.py`, `tools/flag_compound_logic.py`
  - Updated `evaluators/llm-judge/AGENTS.md` with delta-style guidance

- [x] **Benchmark `inclusion_criteria` Format Alignment** (40 benchmarks)
  - Standardized to two-part structure: "Apply when [TRIGGER]. Flag if [FAILURE]."
  - See `benchmarks/FIELD_SPECS.md` for spec and `benchmarks/AGENTS.md` for guidance

- [x] **Rubric Housekeeping**
  - Updated stale `[TBD]` comments in `rubrics/A-CMP.yaml` to reflect actual benchmark labels

### Summary Statistics & Scope

For planning and scoping:

- **Benchmarks reviewed**: 51 (all `benchmarks/a-component/*.yaml`).
- **Rubrics**: 17 (including new A-SEP rubric).
- **LLM prompts**: 37.
- **Benchmarks with no changes** (sound as-is): ~30.
- **Minor refinements suggested** (thresholds, examples, clarity): ~10.
- **Significant changes / new content** (status as of 2025-11-29):
  - ~~Enhance existing: A-TMP3 (protocol step ordering)~~ — DONE
  - ~~Repurpose with preservation: A-TMP4 → Explicit Timing Consistency; A-TMP5 (Trend Direction)~~ — DONE
  - ~~Placeholder definitions: A-CMP2–4, A-EVD3~~ — DONE
  - ~~New benchmarks: A-FCT2 (medications), A-FCT3 (procedures), A-TMP5~~ — DONE
  - ~~New rubric: A-SEP (sepsis/shock) with A-SEP1, A-SEP2 benchmarks~~ — DONE
  - ~~Pediatric/OB interplay clarification (A-PED, A-OBS)~~ — DONE
  - ~~Trauma injury completeness (A-TRM1)~~ — DONE
  - ~~High-risk refusal examples (A-REF1–3)~~ — DONE
- **Remaining work**: Threshold adjustments, example quality improvements (see unchecked items above).
- **Overall assessment**: Framework is ~97% complete for clinically relevant documentation fidelity. Remaining items are threshold tuning and example quality refinements.


