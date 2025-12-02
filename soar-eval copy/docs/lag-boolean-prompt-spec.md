# Medic Copilot – LLM-as-a-Judge Boolean Prompt Spec  
Version: 2025‑11‑28

0. PURPOSE & SCOPE
------------------
This document defines a best‑in‑class pattern for using LLMs as binary judges in the Medic Copilot evaluation harness.

Goals:
- Evaluate Medic Copilot outputs against ground truth using LLM judges.
- Use strictly binary decisions per behavior (pass / fail).
- Align with Pydantic AI / Pydantic Evals so evaluators can be dropped into that framework with minimal adaptation.

This spec covers:
- Prompt structure.
- Behavior‑level rubric design.
- Exception and edge‑case handling.
- Output schema and Pydantic integration.
- A worked example for medication extraction accuracy.


1. CORE DESIGN PRINCIPLES
-------------------------
1. Single behavior per judge  
   - Each judge answers exactly one yes/no question (for example, “Were active medications extracted correctly?”).  
   - If you want to evaluate multiple aspects (accuracy, completeness, tone), define separate judges.

2. Binary verdict, optional low‑precision score  
   - The canonical outcome is a boolean `pass`.  
   - A numeric `score` (0.0 or 1.0, or a small discrete scale) is optional and used only for reporting or dashboards.

3. Rubric‑first, criteria as numbered list  
   - For each behavior, write a short behavior description followed by a numbered list of pass conditions.  
   - The numbered list is interpreted as strict AND logic: all conditions must be satisfied to pass.

4. Explicit pass/fail logic  
   - Always state explicitly how to map criteria to the final boolean:
     - “Set `pass = true` only if all conditions 1–N hold.”  
     - “Otherwise set `pass = false`.”

5. Explicit edge cases and acceptable variations  
   - For each behavior, capture “automatic fail” triggers and “acceptable variations” that should still count as pass.  
   - Keep these separate from the main pass conditions to avoid clutter.

6. Grounded evaluation only  
   - Judges must base decisions solely on the supplied ground truth, source narrative, and candidate output.  
   - Judges must not invent facts or rely on external medical knowledge to fill gaps.

7. Reason‑before‑verdict pattern via rationale field  
   - Judges are instructed to identify evidence and reasons before finalizing the verdict.  
   - The explanation is captured in a short `reason` (or `rationale`) string.

8. Strict structured output  
   - Judges return a small, fixed JSON object: no extra text, no headings, no markdown.  
   - All downstream metric logic relies on this schema.

9. Deterministic inference settings  
   - Evaluation calls use temperature=0 (or as close as the model allows) and a fixed system prompt.  
   - This minimizes variance across runs and makes regressions easier to spot.

10. Alignment by example where needed  
    - If a behavior is hard for the judge, add one or two few‑shot examples (clear pass / clear fail) in the prompt.  
    - Examples are short, domain‑specific, and reuse the same JSON schema.


2. CANONICAL JUDGE OUTPUT SCHEMA
--------------------------------
At the prompt level, the standard JSON schema is:

Required fields:
- `pass`: boolean  
  - `true` if the behavior is satisfied under the rubric.  
  - `false` otherwise (including “cannot determine” cases).
- `reason`: string  
  - One or two short sentences (roughly 50–200 characters).  
  - Must reference the key evidence for the decision (for example, which medication is missing or incorrect).

Optional fields:
- `score`: number  
  - Default mapping: 1.0 if `pass` is true, 0.0 if `pass` is false.  
  - Can be extended to a small discrete scale (for example, 0.0–3.0) if needed.
- `confidence`: string  
  - One of `"high"`, `"medium"`, `"low"`.  
  - `"low"` is used when the judge cannot decide cleanly from the evidence.
- `uncertain`: boolean  
  - `true` if the judge believes the case is ambiguous or underspecified.  
  - For automation, `uncertain = true` still implies `pass = false`, but can route to human review.

Example JSON (single line):

    {"pass": true, "reason": "All ground-truth meds present with correct dose/route; no extra meds.", "score": 1.0}

In Pydantic Evals, this aligns with the default `LLMJudge` expectation:

- `pass` maps to the built‑in pass/fail flag.  
- `reason` maps to the explanation string.  
- `score` can be used or ignored depending on configuration.

If your existing harness expects a behavior‑specific key (for example, `medications_extracted_correct`), map from `pass` to that key at the aggregation/logging layer.


3. BEHAVIOR SPEC TEMPLATE
-------------------------
Each behavior evaluated by Medic Copilot is defined by a structured spec that is independent of any particular framework. This spec can be rendered into prompts for Pydantic Evals or direct API calls.

Recommended behavior metadata (YAML‑style sketch):

    behavior_id: medications_extracted_correct
    field_name: medications_extracted_correct         # Used in dashboards / logs
    description: >
      Checks whether the AI correctly extracts all active medications administered
      during the encounter, with accurate name, dose, and route.
    category: extraction
    severity: high

    ground_truth_source:
      - structured_medications_section

    input_context:
      include:
        - source clinical note or transcript for the encounter
        - structured ground-truth medications for the same encounter
      ignore:
        - non-clinical metadata
        - formatting-only differences (lists vs paragraphs, casing)

    automatic_fail:
      - Any administered medication in the ground truth is completely missing from the candidate output.
      - A medication appears with a clearly incorrect dose (for example, wrong magnitude or units).
      - A medication is invented that has no support in the ground truth or note.

    pass_conditions:
      - Every administered medication in the ground truth appears in the candidate output.
      - For each medication, name, dose, and route match the ground truth
        (allowing minor spelling and abbreviation differences that preserve meaning).
      - No extra medications are added that are not grounded in the ground truth or source note.

    acceptable_variations:
      - Brand vs generic names with the same active ingredient.
      - Abbreviations vs expanded forms (for example, "PO" vs "by mouth", "ASA" vs "aspirin").
      - Minor differences in formatting or word order.

    uncertainty_policy: fail_and_flag

    examples:
      - name: simple_pass
        ground_truth: ["Aspirin 324mg PO", "Nitroglycerin 0.4mg SL"]
        narrative: "Gave ASA 324mg by mouth and NTG 0.4mg sublingual."
        candidate: ["ASA 324mg PO", "NTG 0.4mg SL"]
        expected_pass: true
        expected_reason: "Both ground-truth meds present with equivalent abbreviations and correct dosing."
      - name: simple_fail_missing_med
        ground_truth: ["Aspirin 324mg PO", "Nitroglycerin 0.4mg SL"]
        narrative: "Gave ASA 324mg PO and NTG 0.4mg SL."
        candidate: ["ASA 324mg PO"]
        expected_pass: false
        expected_reason: "Nitroglycerin is missing from the extracted list."

All behaviors in the evaluation harness should follow this pattern:

- One `behavior_id` per judge.  
- A small list of `automatic_fail` rules.  
- A small list of AND‑ed `pass_conditions`.  
- A small list of `acceptable_variations`.  
- Optional illustrative `examples` for calibration and regression testing.


4. GENERIC PROMPT TEMPLATE (DIRECT LLM CALL)
--------------------------------------------
This section defines the canonical prompt structure when you call an LLM directly (without relying on Pydantic’s implicit system prompt).

4.1 System message template

    You are a neutral medical documentation evaluator.
    You evaluate one behavior at a time.
    For each case, you are given:
    - Ground-truth structured data
    - The source clinical documentation
    - An AI-generated candidate output

    Your job is to decide whether a single evaluation behavior is satisfied, using the rubric provided.
    Be strict and literal about the rubric.
    If you cannot tell from the evidence whether all conditions are met, treat the behavior as NOT satisfied.

    Use only the information in the provided inputs.
    Do not invent clinical details or use outside knowledge to fill gaps.

    Respond only with a single JSON object with fields:
      - pass: boolean
      - reason: short explanation (<= 200 characters)
      - score: numeric score (1.0 if pass is true, 0.0 if pass is false)

    Do not include any text before or after the JSON.

4.2 User message template (behavior‑specific)

The harness fills this template with behavior metadata and concrete inputs.

    BEHAVIOR ID:
    {behavior_id}

    BEHAVIOR DESCRIPTION:
    {behavior_description}

    EVALUATION SCOPE:
    - Include:
      {bullet list from input_context.include}
    - Ignore:
      {bullet list from input_context.ignore}

    RUBRIC

    Automatic fail if any of the following are true:
    {numbered list from automatic_fail}

    Pass conditions (all must be satisfied):
    1. {pass_conditions[0]}
    2. {pass_conditions[1]}
    3. {pass_conditions[2]}
    ...

    Acceptable variations (still treated as pass):
    - {acceptable_variations[0]}
    - {acceptable_variations[1]}
    ...

    Uncertainty policy:
    - If the information is ambiguous or incomplete, set pass = false and
      explain that the case is uncertain in the reason.

    INPUTS

    GROUND_TRUTH:
    {rendered ground truth for this case}

    SOURCE_NARRATIVE:
    {rendered clinical note or transcript}

    CANDIDATE_OUTPUT:
    {rendered Medic Copilot output for this case}

Because the system message already defines the output format, no additional instructions are needed at the end of the user message.


5. PYDANTIC EVALS INTEGRATION
-----------------------------
When using Pydantic Evals, the primary surface you control is the `LLMJudge` `rubric` string. Pydantic supplies its own system and output‑format instructions.

5.1 Canonical Pydantic `LLMJudge` usage

Python sketch:

    from pydantic_evals.evaluators import LLMJudge

    MEDS_EXTRACTED_CORRECT_RUBRIC = """
    Behavior: medications_extracted_correct

    Goal:
    Check whether the AI output correctly extracts all active medications
    administered during the encounter.

    Automatic fail if:
    - Any administered medication in the ground truth is missing from the AI output.
    - A medication in the AI output has a clearly incorrect dose (wrong magnitude or units).
    - The AI output adds a medication that does not appear in either the ground truth or narrative.

    Pass conditions (all must hold):
    1. Every administered medication in the ground truth appears in the AI output.
    2. For each medication, name, dose, and route match the ground truth,
       allowing minor spelling differences and standard abbreviations.
    3. The AI output does not add medications that are not present in the ground truth or note.

    Acceptable variations:
    - Brand vs generic names for the same active ingredient.
    - Common abbreviations (ASA for aspirin, NTG for nitroglycerin, NS for normal saline).
    - Formatting differences such as order or line breaks.

    Evaluation instructions:
    - Use only the supplied ground truth and candidate output.
    - Treat the ground truth as canonical when it conflicts with the narrative.
    - If you cannot determine whether all conditions are met, treat this as a failure
      and explain briefly why the case is uncertain in the reason.
    """

    meds_extracted_correct_judge = LLMJudge(
        rubric=MEDS_EXTRACTED_CORRECT_RUBRIC,
        include_input=True,            # include source input (for example, note)
        include_expected_output=True,  # include ground truth where applicable
        assertion={"evaluation_name": "medications_extracted_correct"},
        # Use temperature ~0.0 via model_settings for evaluations.
    )

Pydantic’s `LLMJudge` will prompt the model with this rubric and instruct it to return JSON with `pass` / `reason` / `score`.  
The `evaluation_name` `"medications_extracted_correct"` is the metric name used in aggregated reports.

5.2 Mapping to the canonical JSON schema

- The `pass` field in Pydantic Evals maps directly to `pass` in this spec.  
- The `reason` field maps to `reason`.  
- The `score` field can be set to 1.0 for pass and 0.0 for fail, or to a more nuanced value if you later extend the rubric.

If your existing harness uses a per‑behavior key (for example, `medications_extracted_correct`), map from `pass` to that key when logging or storing evaluation results:

    result.medications_extracted_correct = judge_output.pass


6. EXAMPLE: MEDICATION EXTRACTION ACCURACY
------------------------------------------
Below is a concrete example of applying this spec to the `medications_extracted_correct` behavior.

6.1 Behavior spec (summary)

    behavior_id: medications_extracted_correct
    field_name: medications_extracted_correct
    description: >
      Verifies that the AI output lists all active medications administered during the encounter
      with correct name, dose, and route, without adding unsupported medications.
    category: extraction
    severity: high

    automatic_fail:
      - Any administered medication in the ground truth is missing from the AI output.
      - A medication in the AI output has a clearly incorrect dose (wrong magnitude or units).
      - The AI output adds a medication that does not appear in either the ground truth or narrative.

    pass_conditions:
      - Every administered medication in ground truth appears in the AI output.
      - For each medication, name, dose, and route match ground truth, allowing minor spelling differences and standard abbreviations.
      - No extra medications are present beyond those supported by ground truth or narrative.

    acceptable_variations:
      - Brand vs generic names for the same active ingredient.
      - Abbreviations such as ASA/aspirin, NTG/nitroglycerin, NS/normal saline.
      - Differences in ordering or formatting.

    uncertainty_policy: fail_and_flag

6.2 Direct LLM prompt instance (user message body)

Given:

- Ground truth:

    ["Aspirin 324mg PO", "Nitroglycerin 0.4mg SL", "Normal Saline 500mL IV"]

- Source narrative:

    "58 y/o male with chest pain. Administered ASA 324mg by mouth, NTG 0.4mg sublingual,
     and NS 500mL IV bolus."

- Candidate output:

    ["ASA 324mg PO", "NTG 0.4mg SL", "NS 500mL IV"]

User message:

    BEHAVIOR ID:
    medications_extracted_correct

    BEHAVIOR DESCRIPTION:
    Verifies that the AI output lists all active medications administered during the encounter
    with correct name, dose, and route, without adding unsupported medications.

    EVALUATION SCOPE:
    - Include:
      - Medications administered during the documented encounter.
      - Doses and routes for those medications.
    - Ignore:
      - Home medications not administered during this encounter.
      - Formatting-only differences and casing.

    RUBRIC

    Automatic fail if any of the following are true:
    - Any administered medication in the ground truth is missing from the AI output.
    - A medication in the AI output has a clearly incorrect dose (wrong magnitude or units).
    - The AI output adds a medication that does not appear in either the ground truth or narrative.

    Pass conditions (all must be satisfied):
    1. Every administered medication in the ground truth appears in the AI output.
    2. For each medication, name, dose, and route match ground truth, allowing minor spelling differences and standard abbreviations.
    3. No extra medications are present beyond those supported by the ground truth or narrative.

    Acceptable variations (still treated as pass):
    - Brand vs generic names for the same active ingredient.
    - Abbreviations such as ASA/aspirin, NTG/nitroglycerin, NS/normal saline.
    - Differences in ordering or line breaks.

    Uncertainty policy:
    - If the information is ambiguous or incomplete, set pass = false and explain that the case is uncertain in the reason.

    INPUTS

    GROUND_TRUTH:
    ["Aspirin 324mg PO", "Nitroglycerin 0.4mg SL", "Normal Saline 500mL IV"]

    SOURCE_NARRATIVE:
    "58 y/o male with chest pain. Administered ASA 324mg by mouth, NTG 0.4mg sublingual,
     and NS 500mL IV bolus."

    CANDIDATE_OUTPUT:
    ["ASA 324mg PO", "NTG 0.4mg SL", "NS 500mL IV"]

Expected JSON response from the judge:

    {"pass": true,
     "reason": "All three ground-truth meds present with equivalent abbreviations and correct doses/routes; no extras.",
     "score": 1.0}


7. OPERATIONAL GUIDELINES
-------------------------
1. Temperature and sampling  
   - Use temperature=0.0 for all judge calls.  
   - Set `top_p=1.0` and do not enable creative decoding strategies for evaluations.

2. Max tokens and rationale length  
   - Cap `max_tokens` so the judge cannot produce long essays.  
   - With a tight cap, the `reason` field stays naturally under roughly 200 characters.

3. Single model per evaluation lane  
   - For a given evaluation run, use a single model configuration for all cases.  
   - This avoids configuration‑induced variance across test cases.

4. Optional multi‑judge ensembles  
   - For high‑risk behaviors (for example, safety‑critical checks), you may run multiple judges and aggregate:
     - Majority vote on `pass`.  
     - Mean or median of `score`.  
   - The prompt structure and behavior spec stay the same; only aggregation changes.

5. Golden sets and regression tests  
   - Maintain a small, curated set of human‑labeled examples per behavior.  
   - Regularly compare judge outputs against this golden set to detect drift when you change prompts, models, or behavior definitions.

This file is intended to be dropped directly into your repo as the source of truth for LLM‑as‑a‑judge boolean prompt design for Medic Copilot.
