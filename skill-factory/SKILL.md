---
name: skill-factory
description: Generate complete, production-ready Claude skills directly to the filesystem. Claude should use this skill when creating new skills, extending Claude's capabilities, or helping users build custom skill packages.
---

## When to use this skill

Use this skill when users request:
- Creating new Claude skills from scratch
- Generating skill packages with proper structure
- Building skills for specific workflows or domains
- Packaging skills for deployment (Claude.ai, Claude Code, API)

**This factory's approach**: Beyond Anthropic's basic skill patterns, this factory emphasizes **research-grounded generation**. For domains where accuracy matters (e.g., medical documentation, compliance, technical standards), skills should be built on current evidence rather than Claude's training data. The `background-research` skill gathers real-time findings with source citations.

## How to use this skill

1. **Validate request** - Confirm skill name (kebab-case), verify use case clarity, ask for clarification if needed

2. **Research current standards** - Invoke the `background-research` skill with current date to gather evidence-based findings. This ensures skills reflect current best practices rather than relying on potentially outdated training data. See [references/generation-workflow.md](references/generation-workflow.md) Step 2 for the decision tree on research depth.

3. **Plan the skill** - Using research findings, determine folder structure, decide if scripts are necessary, plan references/ organization.

4. **Generate files** - Create SKILL.md, sample_prompt.md, and any needed references/scripts/assets using patterns in [references/patterns.md](references/patterns.md). Integrate research citations where appropriate.

5. **Validate and package** - Run `python scripts/quick_validate.py`, then `python scripts/package_skill.py` to create ZIP. See [references/quality-checklist.md](references/quality-checklist.md) for all requirements

## Core principles

1. **Research-grounded** - Do not rely on Claude's training data for evolving domains; gather current evidence first
2. **Progressive disclosure** - SKILL.md under 500 lines; move detailed content to references/
3. **Evaluation-first** - Build evaluations before extensive documentation when possible
4. **Concise instructions** - Only include what Claude doesn't already know
5. **Third-person voice** - "Claude should use this skill when..." not "You should..."
6. **Pragmatic language** - No marketing speak, emojis, or buzzwords

## File system organization

```
skill-name/
├── SKILL.md                    # Required: Under 500 lines, concise navigation
├── sample_prompt.md            # Required: Copy-paste ready user invocations
├── references/                 # Optional: Detailed templates, workflows
├── scripts/                    # Optional: Executable Python scripts
└── assets/                     # Optional: Test data, templates
```

**Output locations**:
- Generated skills: `generated-skills/skill-name/`
- ZIP files: `zips/skill-name.zip`

## SKILL.md template

```yaml
---
name: skill-name
description: What this skill does and when to use it. Claude should use this skill when [triggers].
---

## When to use this skill
[Specific scenarios and file types]

## How to use this skill
1. **Step 1** - [Action]
2. **Step 2** - [Action with reference: "REQUIRED READING: Before X, you MUST read references/file.md"]
3. **Step 3** - [Action]
4. **Step 4** - [Action]

## Core principles
1. **[Name]** - [Brief explanation]
2. **[Name]** - [Brief explanation]
3. **[Name]** - [Brief explanation]

## Keywords
[keyword], [keyword], [keyword]
```

## Reference documentation

- **[references/generation-workflow.md](references/generation-workflow.md)** - Complete 8-step generation process
- **[references/patterns.md](references/patterns.md)** - Skill patterns, writing style, script templates
- **[references/quality-checklist.md](references/quality-checklist.md)** - Validation criteria and checklists
- **[references/advanced.md](references/advanced.md)** - Research integration, Claude A/B testing, multi-model testing

## Keywords

skill generation, skill factory, skill creation, Claude skills, skill packaging, skill templates, progressive disclosure

---

<!-- 
AUTHOR MAINTENANCE NOTES (not runtime instructions):

This factory aligns with Anthropic Agent Skills Spec v1.0 (October 16, 2025).
Repository structure was updated December 1, 2025.

Key spec requirements:
- SKILL.md required with YAML frontmatter (name + description)
- Optional frontmatter: license, allowed-tools, metadata
- Under 500 lines for optimal performance

For spec updates, periodically check: https://github.com/anthropics/skills/tree/main/spec
Last reviewed: December 2025
-->
