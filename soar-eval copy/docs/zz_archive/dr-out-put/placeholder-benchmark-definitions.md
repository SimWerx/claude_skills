# Medical SME Review: Placeholder Benchmark Definitions

## Executive Summary

This review defines seven placeholder benchmarks in the SOAR evaluation framework, focusing on extraction fidelity and completeness in Medic Copilot's output. Each benchmark targets a specific failure mode (e.g., missing section content, evidence misalignment, format errors, temporal logic mistakes) without duplicating existing checks. We also assess a proposed **A-UNC (Uncertainty Handling)** rubric to address how the AI handles absent data, and cross-reference Denver EMS protocols to ensure critical documentation elements (refusals, pronouncements, RSI, behavioral cases) are covered by current benchmarks. Overall, the new definitions emphasize **preservation of stated information** over clinical decision-making, aligning with the eval harness scope[\[1\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L9-L17)[\[2\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L15-L19).

## Placeholder Benchmark Definitions

### A-CMP2: Response Section Incomplete

**Concept**:

Medic Copilot's output fails to include key **Response** section details (unit response and crew information) that were present in the narrative. This covers missing response mode (e.g., emergent vs non-emergent), crew identifiers, or notable delays/hazards en route[\[3\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L95-L101).

**Inclusion Criteria**:

Apply to scenarios where the narrative clearly describes response details (dispatch mode, units responding, crew names, any response delays or scene hazards) but the structured output's response section omits one or more of these elements. For example, if the transcript states "Medic 5 responded code 3 with two paramedics, no delays" and draatt_json lacks the response mode or crew info, flag this benchmark.

**Exclusion Criteria**:

Do not apply if the scenario template intentionally omits a separate response section (e.g. certain overlays or abbreviated templates). Also exclude cases where the narrative itself provides no response details-no penalty for absence of information not dictated.

**Examples**:  
\- _"Dispatched emergent, Medic 42 and Engine 15 responding, no traffic delays"_ - but the output does not list the responding units or indicates an incorrect mode.  
\- _Narrative describes a_ _scene hazard_ _("downed power lines on approach delayed arrival by 5 minutes") not captured in the output's response section._

**Threshold**: 0.80 | **Criticality**: threshold_gate (partial credit allowed; ≥80% of expected fields should be present to pass)  
**Evaluator Type**: code (deterministic check for presence of required keys/values in response section)

### A-CMP3: Arrival Section Incomplete

**Concept**:

Medic Copilot's output omits critical **Arrival** details that the narrative provides, such as patient position/location on arrival, scene context, or arrival time[\[3\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L95-L101). This benchmark catches missing content in the arrival section of DRAATT.

**Inclusion Criteria**:

Apply when the narrative describes how the patient was found and initial scene observations-e.g., _"arrived at 08:46 to find patient lying on the bedroom floor, scene secure with police on scene"_-but the output's arrival documentation lacks one or more of those details (arrival timestamp, patient location/position, scene safety findings, immediate patient presentation).

**Exclusion Criteria**:

Exclude scenarios that have no on-scene component (e.g., interfacility transfers where an arrival narrative is not expected). Also do not flag if the template legitimately merges arrival info into another section or if the narrative itself is missing these details.

**Examples**:  
\- Narrative: _"Arrived on scene at 14:30, found patient seated in a recliner complaining of chest pain, scene calm."_ Output: no mention of patient's found position or the scene environment in the arrival section.  
\- Narrative notes _"patient found unresponsive on bathroom floor, agonal respirations"_ but the output arrival section fails to mention patient's initial condition or location.

**Threshold**: 0.80 | **Criticality**: threshold_gate (≥80% of expected arrival fields present)  
**Evaluator Type**: code (checks for presence of arrival timestamp, patient location, and immediate scene findings in output)

### A-CMP4: Assessment Section Incomplete

**Concept**:

Medic Copilot's output is missing significant **Assessment** findings that were documented in the narrative. This benchmark targets omissions in the physical exam and primary/secondary survey details within the assessment section[\[4\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L96-L101).

**Inclusion Criteria**:

Apply when the narrative provides a thorough patient assessment (e.g., vital signs, Glasgow Coma Scale, head-to-toe exam findings across systems) and the output fails to capture one or more critical components. For instance, if the transcript includes a neurological exam and GCS but the output assessment lacks any neuro status or GCS field, this benchmark should flag it.

**Exclusion Criteria**:

Do not use if the scenario's narrative itself is limited (e.g., focused exam only) and those details are not present to extract. Also exclude if the missing content pertains to a different rubric (e.g., omission of treatment details belongs in completeness of treatment, not assessment).

**Examples**:  
\- The narrative lists **vital signs and a 12-system exam** (HEENT, chest, abdomen, etc.), but the output's assessment section contains only vitals and omits entire system exams (e.g., no neurological or no abdominal findings recorded).  
\- Narrative: _"GCS 15, pupils equal and reactive, lungs clear bilaterally, no neurologic deficits"_. Output: no GCS documented and no mention of neuro exam findings in assessment.

**Threshold**: 0.80 | **Criticality**: threshold_gate (missing more than ~20% of major assessment elements triggers failure)  
**Evaluator Type**: code (checks for presence of expected assessment sub-sections or fields like GCS if applicable, vitals, and at least a minimal exam across required systems)

### A-EVD3: Evidence Span Misalignment

**Concept**:

The evidence text linked to an extracted fact **does not accurately support the fact**, even if a span is provided. In these cases, Medic Copilot's cited narrative span is incomplete, tangential, or misleading relative to the output claim[\[5\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L109-L113).

**Inclusion Criteria**:

Apply when an output fact or value has an evidence span attached, but that span either fails to include the key detail of the fact or includes content that doesn't directly substantiate the fact. For example, if the output states a medication dose and the cited span is a portion of the transcript that _lacks the dose value_, this misalignment should be flagged.

**Exclusion Criteria**:

Do not apply if evidence spans are simply longer than necessary but still contain the relevant information (extra context is acceptable[\[6\]\[6\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/A-EVD.yaml#L20-L28)). Also exclude cases where the evidence is entirely missing or clearly wrong - those are handled by A-EVD1 (unsupported/absent evidence)[\[7\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-EVD1.yaml#L9-L17)[\[8\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-EVD1.yaml#L27-L35).

**Examples**:  
\- Output documents _"Pain score 9/10"_ but the attached evidence span only shows _"patient reports chest pain"_ without the numeric severity. The evidence is present but doesn't capture the **9/10** value, failing to fully support the structured data.  
\- Output records _"administered 0.4mg nitroglycerin"_ and links a span, but the span text corresponds to a different medication or dose (e.g., quotes an aspirin administration) - the span exists but is for the wrong fact.

**Threshold**: 0.90 | **Criticality**: threshold_gate (high bar for evidence accuracy; up to 10% minor span errors tolerated, but systematic misalignments fail)  
**Evaluator Type**: hybrid (automatic checking of span content with LLM validation to ensure the span contains the fact; likely uses an LLM prompt to judge support[\[5\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L109-L113))

### A-FMT2: Schema Compliance Error

**Concept**:

The structured DRAATT output is **schema-valid JSON** (passes A-FMT1) but violates field-level format specifications. This includes using values or keys outside the allowed schema (e.g., wrong data types, non-standard enumerations, or extra fields not defined)[\[9\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L103-L107).

**Inclusion Criteria**:

Apply when the output JSON contains all required structure yet still has format issues such as: - **Invalid enumerations**: Using values not in the expected set (e.g., a yes/no field populated with "Y" or "unknown" instead of allowed "Yes"/"No").  
\- **Type mismatches**: Numeric fields given as strings or with units (e.g., "heart_rate": "eighty" or "80 bpm" instead of an integer).  
\- **Extraneous keys**: Fields that are not part of the DRAATT schema appear in the JSON (for instance, a stray "scene_safety": ... field that isn't specified).  
\- **Missing required sub-fields** within an included section (e.g., a vitals object present but missing a required key like blood pressure).

**Exclusion Criteria**:

Do not apply if the only issues are top-level JSON parsing failures or completely missing sections (those are handled by A-FMT1[\[10\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-FMT1.yaml#L26-L34)). Also exclude trivial format deviations that do not break schema interpretation (e.g., acceptable nulls for optional fields, or additional context fields that are explicitly allowed as extensions).

**Examples**:  
\- Output JSON uses "transport_mode": "by ambulance" when the schema expects a coded value (e.g., "transport_mode": "ground" or a boolean for lights/sirens).  
\- The draatt_json includes "patientAge": 45 where the schema expects "patient_age" (wrong key name), or includes an undeclared field like "weather": "clear" that is not in the standard schema.  
\- A numeric field is provided with units embedded (_"temperature": "98.6 F"_), violating the expected numeric format.

**Threshold**: 0.95 | **Criticality**: threshold_gate (nearly strict compliance required; minor allowable deviations under 5%)  
**Evaluator Type**: code (structured schema validation against expected keys and allowed values/types)

### A-TMP3: Protocol Step Misordering

**Concept**:

Medic Copilot's output preserves events chronologically but **violates protocol-specific time/order logic**. This catches cases where time-sensitive protocol steps are documented out of order or without regard to timing constraints (e.g., ignoring an eligibility timeframe)[\[11\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L90-L93).

**Inclusion Criteria**:

Apply when the scenario involves a time-critical protocol or ordered steps, and the output's sequencing contradicts those rules. For example: - **Stroke care**: Narrative indicates symptom onset was beyond the thrombolytic window (e.g., last known well 6 hours ago), but the output still documents a _stroke alert or tPA consideration_ as if timing were normal[\[11\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L90-L93).  
\- **Protocol prerequisites**: Narrative has an intervention that should occur only after a certain step (e.g., intubation after sedative given), and the output lists the actions in a reversed or impossible order (sedative missing or noted after the intubation).  
\- **Termination of efforts**: In a cardiac arrest, if narrative notes downtime exceeding protocol criteria for termination, but output fails to mark the resuscitation as terminated (implying a protocol step was missed in documentation timing).

**Exclusion Criteria**:

Exclude if the narrative does not clearly provide the timing context or sequence trigger (we only flag misordering when ground truth makes it evident). Also exclude minor reordering that doesn't break protocol logic (e.g., documenting two simultaneous interventions in either order is acceptable as long as causality isn't broken[\[12\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/A-TMP.yaml#L20-L28)).

**Examples**:  
\- _Stroke Example_: Narrative: _"Last known well 07:00 (now 13:30)"_. Medic Copilot output **still lists** _"Stroke alert called, preparing for tPA"_ without any note of the elapsed 6.5 hours. The AI failed to respect the thrombolysis time exclusion indicated by the narrative timeline.  
\- _RSI Example_: Narrative: _"Patient sedated with etomidate, then intubated with a 7.5 ETT"_. Output inverts this order or omits the sedative, effectively documenting intubation without the required prior sedation - a protocol sequence error (intubation prerequisites not properly ordered).

**Threshold**: 0.85 | **Criticality**: threshold_gate (allows small timing/order oversights, but significant protocol sequence errors cause failure)  
**Evaluator Type**: hybrid (combination of rule-based checks for known sequence patterns and an LLM to interpret protocol timing context, e.g. using clinical prompts for stroke time logic)

### A-TMP4: Trend Direction Misinterpreted

**Concept**:

Medic Copilot misrepresents the **overall trend of the patient's condition**. Despite correct ordering of events, the output's description of improvement vs. deterioration is opposite to what the narrative data indicates (or the output fails to note a significant trend)[\[11\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-framework/soar-graphs.mm#L90-L93).

**Inclusion Criteria**:

Apply when multiple data points over time clearly show the patient either improving or worsening, and the output gets this qualitative trend wrong. This often involves vital sign trajectories or repeated assessments: - If the patient's serial vitals indicate decline (e.g., dropping blood pressure _and_ rising heart rate), but the output summation implies the patient was _"stable"_ or _"improving,"_ flag this.  
\- Conversely, if the patient improved after interventions (pain level, vital signs, mental status) and the output does not reflect any improvement or incorrectly states the patient worsened, this benchmark applies.  
\- Also include if the output ignores a documented trend altogether (omitting the trend insight), such as failing to mention that a second set of vitals showed improvement after treatment when the narrative emphasized it.

**Exclusion Criteria**:

Do not use for single pre/post comparisons already covered by A-TMP2 (that benchmark handles discrete paired trend errors[\[13\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-TMP2.yaml#L9-L17)[\[14\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-TMP2.yaml#L27-L35)). Also exclude cases where changes are minimal or ambiguous such that a trend is not clinically apparent (e.g., vitals fluctuate within normal range without a clear direction).

**Examples**:  
\- Narrative: _"BP 90/50 → 70/40, HR 120 → 140, patient increasingly pale and lethargic"_. Output summary says, _"patient remained hemodynamically stable"_ or fails to mention the deterioration. The AI incorrectly portrays a worsening shock trend as stability - a trend direction error.  
\- Narrative: _"Pain 9/10 down to 5/10 after morphine, patient less distressed"_. Output does not indicate any improvement (or worse, labels pain as "worsened"), missing the positive trend in patient response.

**Threshold**: 0.85 | **Criticality**: threshold_gate (some leeway for subtle trends, but a major misinterpretation of trend fails below 85%)  
**Evaluator Type**: llm_judge (subjective evaluation by an LLM of whether the output's description of patient course aligns with the series of data points; uses a prompt focusing on clinical trend reasoning)

## A-UNC Rubric Assessment

**Recommendation**: _Create a standalone A-UNC rubric_ for uncertainty handling, rather than folding it into existing rubrics.

**Rationale**:

Handling of **absent data** is a distinct quality dimension. Existing rubrics like A-EVD and A-CMP focus on facts present in output vs. input - they catch hallucinations (unsupported facts)[\[7\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-EVD1.yaml#L9-L17) and completeness of documented facts[\[15\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CMP1.yaml#L9-L17), respectively. However, neither explicitly addresses how the AI should behave when the source narrative lacks information. A-UNC would target errors of _commission_ (hallucinating a value that was never provided) and _omission_ (failing to flag a notably missing piece of documentation). This is distinct from evidence linkage - it's about the AI's approach to unknowns. By making it a standalone rubric, we can assign it specific weight and thresholds to treat certain uncertainty issues as "never events" (e.g., inventing critical data) without conflating them with general evidence or completeness scores.

**If creating A-UNC**:  
\- **A-UNC1 Concept**: _Hallucinated Data for Missing Input_. If the narrative provides no evidence for a required field but Medic Copilot supplies one anyway, it's a hallucination due to uncertainty. For example, adding a blood glucose reading or an exact patient weight that was never mentioned. This benchmark would fire on any **value fabrication** in lieu of admitting uncertainty.  
\- **A-UNC2 Concept**: _Silent Omission of Critical Field_. When an important documentation field is entirely absent in the narrative, the AI output leaves it blank or omits it without acknowledgment. In other words, the AI neither provides the data (appropriately, since it's unknown) **nor flags that it's missing**. For instance, a patient refusal scenario where the narrative never states that risks were explained, and the output simply doesn't include any mention of risk explanation - effectively creating a documentation gap without alerting the user.

**Threshold**: For A-UNC1 (hallucination), threshold = **1.0** with hard_gate - any hallucination of missing info is unacceptable (this mirrors how safety-critical hallucinations are handled, zero tolerance). For A-UNC2 (omission), threshold ~ **0.90** with threshold_gate - we allow a small margin since not every missing piece can be flagged, but frequent unacknowledged omissions would fail.

**Weight**: Assign A-UNC a moderate weight (e.g., 0.10-0.15 of the A-component score) so that it is significant but does not overshadow factual accuracy rubrics. This ensures a chart can't pass with high marks on other rubrics if it repeatedly fabricates or ignores unknowns, while one or two minor omissions won't sink the entire score if everything else is excellent.

**Examples triggering A-UNC**:  
\- _A-UNC1_: Narrative never mentions an allergies status, but the output populates "allergies": "NKDA" by assumption - a hallucinated entry for a field that was truly unknown.  
\- _A-UNC1_: No second set of vitals in narrative, yet output JSON includes a full set of "reassessment vitals" that were not actually documented (the AI made them up to fill the template).  
\- _A-UNC2_: Narrative does not include whether risks of refusal were explained to a patient who refused care. The output has no risks_explained field or note - effectively a blank, without even an "unknown" or comment. In a high-liability category like refusal, the AI should at least signal this absence.  
\- _A-UNC2_: For a DOA case, if the narrative never stated the **pronouncement time**, and Medic Copilot leaves that field null without any note, this omission might be flagged (though one could argue it overlaps with completeness - here it's because the input lacked it entirely).

## Denver Protocol Coverage Analysis

Using the **Denver Metro EMS Protocols (July 2025)** as a reference, we verify that current benchmarks cover the required documentation elements for key high-risk scenarios:

| Protocol (Section) | Documentation Requirement | Current Coverage in Benchmarks | Gap/Action |
| --- | --- | --- | --- |
| **0032 - Patient Refusal** | Document decision-making **capacity**, that **risks** of refusal were explained, patient's **understanding** and reason, and obtain refusal **signature/witness**[\[16\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L184-L193)[\[17\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L200-L204). | **A-REF1** checks that risk explanation is documented[\[18\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L186-L194). **A-REF2** checks for refusal signature/witness presence[\[18\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L186-L194)[\[17\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L200-L204). The rubric also highlights capacity assessment as a focus[\[16\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md#L184-L193). | _Minor Gap:_ Capacity documentation isn't a standalone automated check in A-REF (capacity is emphasized but not its own benchmark). However, **A-BHV2** (Behavioral) covers capacity missing[\[19\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/WORKING.md#L2-L5). We may apply A-BHV2 in refusal cases or introduce an A-REF3 for capacity if needed. |
| **0050 - Field Pronouncement (DOA)** | If patient found obviously dead: document criteria (signs of obvious death), **pronouncement time**, pronouncing **physician** or protocol (standing order), and agency involvement (coroner, medical control)[\[20\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CMP5.yaml#L10-L18)[\[21\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CMP5.yaml#L27-L35). | **A-CMP5** specifically ensures all four pronouncement elements are present in DOA cases[\[20\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CMP5.yaml#L10-L18)[\[21\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CMP5.yaml#L27-L35): method (standing order vs base call), physician name, time, and agency notification. **A-CAR1** further ensures the outcome (field termination) is documented if mentioned[\[22\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR1.yaml#L8-L16)[\[23\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR1.yaml#L27-L35). | _OK:_ No significant gap. Obvious death physical findings would fall under general assessment completeness (the narrative's mention of rigor or lividity should be captured as exam findings; any miss there would be caught by A-CMP4 or A-FCT). The critical pronouncement details are covered by A-CMP5. |
| **0051 - Termination of Resuscitation** | For cardiac arrest cessation: document that **ROSC or termination** outcome was reached (or not), including time of cessation and by whose authority (protocol criteria vs physician order). Ensure initial rhythm, interventions, and timeline of resus are recorded for QA[\[24\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/A-CAR.yaml#L16-L25)[\[25\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/rubrics/A-CAR.yaml#L18-L26). | **A-CAR1** (hard gate) verifies ROSC or field termination is documented if the narrative states an outcome[\[22\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR1.yaml#L8-L16)[\[23\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR1.yaml#L27-L35). **A-CAR2** ensures CPR event details (initial rhythm, shocks, meds, airway) are not omitted[\[26\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR2.yaml#L8-L16)[\[27\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-CAR2.yaml#L27-L35). Together these cover the key termination documentation (outcome + sequence of resus). Pronouncement time/physician falls under DOA case (A-CMP5) if applicable. | _OK:_ No gap. The combination of A-CAR1 and A-CAR2 addresses protocol 0051's documentation needs. If medical control contact is required for termination, it would be documented in narrative; absence in output would be caught by evidence/completeness. |
| **1000 - RSI (Intubation)** | Document **indication** for RSI, **drugs** used (sedative and paralytic with doses), ETT **size/position**, confirmation methods (e.g., **EtCO₂** value), and post-intubation management (sedation, securing tube). Also note number of attempts or difficulties per protocol. | **A-PRT1** covers critical RSI fields[\[28\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-PRT1.yaml#L10-L18)[\[29\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-PRT1.yaml#L29-L37): it flags if **sedative or paralytic** (or their doses) are missing, if **ETT size/depth** or numeric **EtCO₂** confirmation is not documented, or if confirmation methods are insufficient. It even checks for post-intubation sedation if mentioned[\[28\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/benchmarks/a-component/A-PRT1.yaml#L10-L18). These align well with protocol requirements. | _Mostly OK:_ The main RSI elements are covered by A-PRT1. One minor area not explicitly covered is the number of intubation **attempts** (if the narrative notes multiple attempts and output doesn't, it's an omission). This could be considered under general assessment completeness or included in a future RSI-related benchmark, but it's a corner case. |
| **6000 - Behavioral**&lt;br&gt;_(Patient Restraint & Capacity)_ | If restraining patient (physical or chemical), document **why**, what was done (type of restraint or medication and dose), patient response, and ongoing **monitoring**. Document **decision-making capacity** (or lack thereof) especially if patient refuses care or has altered mental status[\[30\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/WORKING.md#L116-L120). | **A-BHV1** (hard gate) ensures any use of **restraints or chemical sedation** mentioned in narrative is documented in output[\[19\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/WORKING.md#L2-L5). **A-BHV2** ensures a **capacity assessment** appears if the situation demands it (e.g., behavioral patient or one refusing treatment)[\[19\]](https://github.com/SimWerx/synthetic-data-epcr-narrative/blob/3504cf46ccaae80b4d05f379137945e3a01f7257/zy_experimental/soar-pydantic-eval/WORKING.md#L2-L5). These align with protocol's emphasis on restraint documentation and decisional capacity. | _OK:_ No gap. The eval harness explicitly covers restraint documentation and capacity. Continuous monitoring after sedation (vitals) would be caught by A-SFT or A-PRT2 if not documented (e.g., missing reassessment), so the patient safety aspect is indirectly covered. |

## Summary Table

| Benchmark | Label | Evaluator | Threshold | Criticality |
| --- | --- | --- | --- | --- |
| **A-CMP2** | Response Section Incomplete | code | 0.80 | threshold_gate |
| **A-CMP3** | Arrival Section Incomplete | code | 0.80 | threshold_gate |
| **A-CMP4** | Assessment Section Incomplete | code | 0.80 | threshold_gate |
| **A-EVD3** | Evidence Span Misalignment | hybrid | 0.90 | threshold_gate |
| **A-FMT2** | Schema Compliance Error | code | 0.95 | threshold_gate |
| **A-TMP3** | Protocol Step Misordering | hybrid | 0.85 | threshold_gate |
| **A-TMP4** | Trend Direction Misinterpreted | llm_judge | 0.85 | threshold_gate |

