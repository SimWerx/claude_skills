# Skill Generation Workflow

Complete step-by-step process for generating production-ready Claude skills.

## Step 0: Evaluation-Driven Development (Recommended)

**Build evaluations BEFORE writing extensive documentation.** This ensures skills solve real problems rather than documenting imagined ones.

**When to use this step**:
- Creating skills for complex or critical workflows
- Skills that need to improve Claude's baseline performance measurably
- When the user can test with representative tasks

**Skip this step when**:
- User needs a quick skill for a well-understood task
- Time constraints prevent evaluation cycles
- The skill is simple and low-risk

**Evaluation workflow**:

1. **Identify gaps**: Run Claude on representative tasks WITHOUT a skill. Document specific failures, missing context, or suboptimal outputs.

2. **Create 3 evaluation scenarios**: Build concrete test cases that expose the gaps.

   **Evaluation structure**:
   ```json
   {
     "skills": ["skill-name"],
     "query": "The actual user request to test",
     "files": ["test-files/sample-input.csv"],
     "expected_behavior": [
       "Successfully identifies X pattern in the data",
       "Produces output in the specified format",
       "Handles edge case Y appropriately"
     ]
   }
   ```

3. **Establish baseline**: Note Claude's current performance without the skill.

4. **Write minimal instructions**: Create just enough skill content to address the gaps.

5. **Iterate**: Execute evaluations, compare against baseline, refine the skill.

---

## Step 1: Validate Request

- Confirm skill name (convert to kebab-case if needed)
- Verify use case clarity
- Ask for clarification if needed

---

## Step 2: Research & Contextualize (Conditional)

**Determine if research needed**:

**Invoke research for**:
- Frameworks or methodologies (copywriting patterns, analysis workflows)
- Tools or technologies (libraries, platforms, APIs)
- Best practices that evolve over time (SEO/AEO, social media)
- Industry standards or conventions

**Skip research for**:
- Evergreen tasks with timeless workflows
- Fixed specifications (file format schemas)
- User has provided complete, current specification

**Decision tree**:

| Skill Type | Research? | Rationale |
|------------|-----------|-----------|
| "Social media optimization 2025" | YES | Temporal + evolving |
| "Project management methodologies" | YES | Frameworks evolve |
| "Python CSV parsing" | YES | Libraries have versions |
| "Meeting notes to action items" | NO | Timeless workflow |
| "PDF file format specification" | NO | Fixed standard |

**When uncertain**: Default to YES (standard depth).

**If research needed**:

1. **Invoke background-research skill**:
   ```
   Topic: [skill domain]
   Current Date: [YYYY-MM-DD]
   Focus Areas: [frameworks/tools/templates]
   Research Depth: standard
   ```

2. **Use findings to enrich skill**:
   - Core Principles: Incorporate evidence-based rules
   - references/: Include current frameworks and templates
   - Keywords: Add contemporary terminology
   - Description: Add temporal context
   - Citations: Preserve source citations for statistics

3. **Archive research**:
   ```bash
   mkdir -p research-archive
   ```
   Filename format: `research-archive/YYYY-MM-DD-HHMM-topic-kebab.md`

**If research skipped**: Add HTML comment after YAML frontmatter:
```html
<!--
Generated without temporal research on [YYYY-MM-DD].
Skill based on existing knowledge. Consider periodic review if domain evolves.
-->
```

---

## Step 3: Plan the Skill

- Determine folder structure needed
- Decide if scripts are necessary
- Plan references/ organization
- Identify test data needs

---

## Step 4: Create Directories

```bash
mkdir -p generated-skills/skill-name/{references,scripts,assets}
mkdir -p zips
```

---

## Step 5: Generate Files

Use `Write` tool to create:
- `generated-skills/skill-name/SKILL.md`
- `generated-skills/skill-name/sample_prompt.md` (ALWAYS required)
- `generated-skills/skill-name/references/formats.md` (if needed)
- `generated-skills/skill-name/scripts/helper.py` (if needed)
- `generated-skills/skill-name/assets/sample_data.csv` (if needed)

**SKILL.md structure**:

1. **YAML frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: What this does and when to use it...
   ---
   ```

2. **HTML comment for research** (conditional):
   ```html
   <!--
   Generated with research on YYYY-MM-DD HH:MM.
   Research archive: research-archive/YYYY-MM-DD-HHMM-topic-name.md
   -->
   ```

3. **Markdown sections** (required): "When to use", "How to use", "Core principles", "Keywords"

**If research conducted**, create `references/research-findings.md`:
```markdown
# Research Findings

This research was conducted on [YYYY-MM-DD HH:MM] to inform this skill's development.

**Archive location**: research-archive/[YYYY-MM-DD-HHMM-topic-name].md

---

[COMPLETE RESEARCH OUTPUT]
```

---

## Step 6: Validate Generated Skill

```bash
python skill-creator/scripts/quick_validate.py generated-skills/skill-name

if [ $? -eq 0 ]; then
  echo "Skill validation passed"
else
  echo "Skill validation failed - fix errors before creating ZIP"
  exit 1
fi
```

**Validation confirms**:
- SKILL.md exists with valid YAML frontmatter
- Name field matches directory name
- Description includes what + when
- Required sections present

**Citation validation** (if research invoked):
- Verify source citations present for statistics
- Format: "[claim] (Source: [Publication], [Year])"

**If validation fails**: Stop immediately, show errors, do NOT create ZIP

---

## Step 7: Create ZIP

```bash
mkdir -p generated-skills zips

if [ ! -d "generated-skills/skill-name" ]; then
  echo "Error: generated-skills/skill-name/ not found"
  exit 1
fi

if [ -f "zips/skill-name.zip" ]; then
  echo "zips/skill-name.zip already exists - delete first or rename skill"
  exit 1
fi

cd generated-skills
zip -r ../zips/skill-name.zip skill-name/
cd ..

FILE_SIZE=$(du -h zips/skill-name.zip | cut -f1)
echo "Created zips/skill-name.zip (${FILE_SIZE})"
```

**Batch ZIP creation**:
```bash
for skill in skill-1 skill-2 skill-3; do
  if [ ! -f "zips/${skill}.zip" ]; then
    cd generated-skills && zip -r "../zips/${skill}.zip" "${skill}/" && cd ..
    echo "${skill}.zip created"
  fi
done
```

---

## Step 8: Confirm Completion

```
Skill Generation Complete: skill-name

Created files:
- generated-skills/skill-name/SKILL.md
- generated-skills/skill-name/sample_prompt.md
- generated-skills/skill-name/references/formats.md
- zips/skill-name.zip (ready for upload)

Deployment Options:

**Claude.ai (ZIP Upload)**:
1. Go to Claude.ai → Settings → Capabilities → Skills
2. Click "Upload Skill" and select zips/skill-name.zip
3. Enable the skill in your conversation

**Claude Code - Personal**:
mkdir -p ~/.claude/skills/
unzip zips/skill-name.zip -d ~/.claude/skills/

**Claude Code - Project** (team-shared):
mkdir -p .claude/skills/
unzip zips/skill-name.zip -d .claude/skills/
git add .claude/skills/skill-name/
git commit -m "Add skill-name skill"

**Claude API**:
Upload via /v1/skills endpoint
```

