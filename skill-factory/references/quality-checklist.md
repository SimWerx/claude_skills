# Quality Checklist

Validation criteria for production-ready Claude skills.

## Pre-Generation Checklist

Before creating files, ensure:

- [ ] Reviewed CLAUDE.md for repository conventions
- [ ] Folder name is kebab-case (lowercase + hyphens)
- [ ] Use case is clear and specific
- [ ] Decided on folder structure (references/, scripts/, assets/)

---

## SKILL.md Requirements

### YAML Frontmatter

- [ ] Starts and ends with `---`
- [ ] Has `name:` field (kebab-case, lowercase)
- [ ] Has `description:` field (what + when)
- [ ] No angle brackets in description
- [ ] Name matches folder name

### Structure

- [ ] Under 500 lines total
- [ ] "When to use this skill" section with specific scenarios
- [ ] "How to use this skill" with workflow steps
- [ ] "Core principles" with 3-5 bullets
- [ ] "Keywords" section at end
- [ ] References to other files use proper markdown links

### Writing Style

- [ ] Third-person descriptions ("Claude should use...")
- [ ] Imperative instructions ("Load data from..." not "You should load...")
- [ ] No marketing language (cutting-edge, innovative, revolutionary)
- [ ] No emojis in SKILL.md or references
- [ ] Assumes Claude intelligence - only include what Claude doesn't know
- [ ] Concise - every token must justify its cost

---

## sample_prompt.md Requirements

- [ ] File created at `generated-skills/skill-name/sample_prompt.md`
- [ ] Uses casual, inviting language ("Hey Claude!")
- [ ] Exciting language: "surprise me", "blow my mind"
- [ ] Copy-paste ready (zero customization needed)
- [ ] Encourages creative exploration
- [ ] NO formal testing language ("Test case:", "Verify:")
- [ ] NO generic placeholders requiring user fill-in

---

## File System Requirements

- [ ] Created in `generated-skills/skill-name/`
- [ ] ZIP created in `zips/skill-name.zip`
- [ ] ZIP contains skill folder as root
- [ ] All referenced files exist
- [ ] Scripts are executable if included

---

## Multi-Model Testing (Recommended)

- [ ] Tested with Claude Haiku: Does skill provide enough guidance?
- [ ] Tested with Claude Sonnet: Is skill clear and efficient?
- [ ] Tested with Claude Opus: Does skill avoid over-explaining?

---

## Research & Evidence Checklist

If background-research was invoked:

- [ ] Research step executed for time-sensitive skills
- [ ] Web searches included current date (YYYY-MM-DD)
- [ ] Findings synthesized into 3-5 actionable insights
- [ ] Frameworks/tools referenced with temporal context ("as of October 2025")
- [ ] Statistics include source citations: "X% (Source: Publication, Year)"
- [ ] Generic principles omit citations (common knowledge)
- [ ] Each specific claim has attribution
- [ ] Sources match background-research Key Findings
- [ ] Deprecated approaches noted
- [ ] Research confidence level influenced recommendation strength
- [ ] Temporal context appears in description
- [ ] Keywords include contemporary terminology

### Citation Rules

**Citations required for**:
- Specific statistics: "57%", "34.5% CTR drop"
- Specific timeframes: "2-3 days", "1-2 months"
- Performance metrics: "5-10x speedup", "40% time savings"

**Citations NOT required for**:
- General principles: "E-E-A-T signals are important"
- Common knowledge: "Progressive disclosure improves efficiency"
- User-provided specifications

---

## Validation Commands

### Quick validation
```bash
python skill-creator/scripts/quick_validate.py generated-skills/skill-name
```

### Package skill
```bash
python skill-creator/scripts/package_skill.py generated-skills/skill-name
```

### Manual ZIP creation
```bash
cd generated-skills && zip -r ../zips/skill-name.zip skill-name/
```

---

## Common Issues and Fixes

### Validation fails on name
- Ensure name is lowercase with hyphens only
- Name must match directory name exactly

### Description validation fails
- Must include WHAT the skill does AND WHEN to use it
- No angle brackets (< >) allowed

### ZIP already exists
```bash
rm zips/skill-name.zip
```
Then retry ZIP creation.

### Missing required sections
Ensure SKILL.md includes:
- "When to use this skill"
- "How to use this skill"
- "Core principles"
- "Keywords"


