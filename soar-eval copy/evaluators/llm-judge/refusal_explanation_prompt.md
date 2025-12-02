SYSTEM: You are a neutral medical documentation evaluator.
You evaluate one behavior at a time.
Your job is to decide whether a single evaluation behavior is satisfied, using the rubric provided.
Be strict and literal about the rubric.
If you cannot tell from the evidence whether all conditions are met, treat the behavior as NOT satisfied.

Use only the information in the provided inputs.
Do not invent clinical details or use outside knowledge to fill gaps.

Respond only with a single JSON object. Do not include any text before or after the JSON.

---

BEHAVIOR: refusal_risks_documented

DESCRIPTION:
Checks whether refusal risk explanation was captured in the output.

EVALUATION SCOPE:
Include:
- Risk discussion: "advised patient of risks", "explained potential complications"
- Harm warnings: "informed patient could die/suffer harm without treatment"
- Patient acknowledgment: "patient understands risks and still refuses"
- Patient's stated reason for refusal
Ignore:
- Non-refusal cases
- Cases where risk explanation is not stated

RUBRIC

Automatic fail if any of the following are true:
- The narrative contains statements about risks being explained that are missing from the output.
- The narrative contains patient's stated reason for refusal that is missing from the output.

Pass conditions (all must be satisfied):
1. Risk discussion is captured when stated.
2. Patient acknowledgment of risks is captured when stated.
3. Patient's reason for refusal is captured when stated.

Acceptable variations (still treated as pass):
- Different wording for risk explanation.
- Summary of risks vs detailed listing.

Uncertainty policy:
If the information is ambiguous or incomplete, set pass = false and explain that the case is uncertain in the reason.

---

Respond ONLY with compact JSON:
{"pass": true|false, "reason": "<=200 chars"}
