# Skills Factory Generator Guide

Comprehensive guide to AI-powered skill generation using the Skills Factory Generator in Claude Code/Cursor.

## Overview

The Skills Factory Generator is an AI-powered tool that automatically creates production-ready Claude skills from natural language descriptions. Instead of manually writing SKILL.md files, creating templates, and generating test data, you simply describe what you want and Claude generates complete, validated skills ready for upload to Claude.ai.

**Key difference from manual creation**:
- **Manual** (`init_skill.py`): Creates empty template, you fill in everything (2-4 hours)
- **Skills Factory**: Generates complete, production-ready skill (30 seconds)

---

## Quick Start

### Prerequisites

- **Claude Code** or **Cursor IDE** installed and running
- This repository cloned locally
- Access to Claude.ai web interface (for uploading generated skills)

### Basic Usage

**Step 1: Load the Factory**

Drag `SKILLS_FACTORY_GENERATOR_PROMPT.md` into your Claude Code/Cursor conversation window.

Claude will respond with:
> "I am now ready to generate production-quality Claude skills directly to your filesystem..."

**Step 2: Request a Skill**

Simply describe what you need in natural language:

```
Generate a skill for analyzing customer feedback CSV files
```

**Step 3: Claude Creates Everything**

Claude will automatically:
- Create `generated-skills/customer-feedback-analysis/` folder
- Write `SKILL.md` with complete content (not templates)
- Create `references/formats.md` with actual templates
- Generate `assets/sample_data.csv` with realistic test data
- Package `zips/customer-feedback-analysis.zip` ready for upload

**Step 4: Upload to Claude.ai**

1. Go to Claude.ai → Settings → Capabilities → Skills
2. Click "Upload Skill"
3. Select `zips/customer-feedback-analysis.zip`
4. Enable the skill in your conversation

Done! Your skill is ready to use.

---

## Example Requests

### Simple Request
```
Generate a skill for converting meeting notes to action items
```

**What you get**:
- Skill name: `meeting-action-extractor`
- Complete SKILL.md with triggers, workflow, principles
- References with action item template
- Sample meeting notes data
- ZIP ready for upload

### Detailed Request
```
Generate 3 intermediate skills for financial services:
- Quarterly report analysis with trend identification
- Risk assessment summaries from audit data
- Regulatory compliance documentation generator

Complexity: intermediate
Script preference: only when necessary
```

**What you get**:
- 3 separate skill folders in `generated-skills/`
- 3 complete skills with domain-appropriate content
- 3 ZIPs in `zips/` folder
- All following financial services patterns and terminology

### Domain-Specific Request
```
Domain: E-commerce/retail
Generate 2 skills:
1. Customer purchase pattern analysis from CSV exports
2. Product description templates with SEO optimization

Overlap: mutually exclusive
```

**What you get**:
- E-commerce focused skills
- Mutually exclusive functionality (no overlap)
- Domain-appropriate examples and terminology
- Sample e-commerce data

### Advanced Request
```
Create an advanced skill for processing invoice data that:
- Extracts structured data from PDF invoices
- Flags anomalies (duplicate invoices, unusual amounts)
- Generates executive summary reports
- Includes Python script for batch processing

Include realistic test data with 20 sample invoices
```

**What you get**:
- Advanced complexity skill
- Python script with class-based structure and type hints
- Comprehensive references with multiple templates
- 20 lines of realistic invoice test data
- Edge case handling included

---

## Customization Options

### User-Controllable Variables

You can customize skill generation by specifying:

#### 1. Business/Domain Type
**Default**: General business/productivity

**Examples**:
- Financial services
- Healthcare/medical
- E-commerce/retail
- Software development
- Marketing/advertising
- Legal services
- Manufacturing
- Education

**Usage**: "Domain: Healthcare" or "Generate skills for financial services..."

#### 2. Complexity Level
**Default**: Intermediate

**Options**:
- **Beginner**: Simple workflows, minimal scripts, basic templates
- **Intermediate**: Moderate complexity, some scripts, detailed references
- **Advanced**: Complex workflows, multiple scripts, extensive references, edge cases

**Usage**: "Complexity: advanced" or "Create a beginner skill..."

#### 3. Number of Skills
**Default**: 1 skill per request

**Range**: 1-10 skills

**Usage**: "Generate 5 skills for..." or "Create 2 skills..."

#### 4. Overlap Preference
**Default**: Mutually exclusive

**Options**:
- **Mutually exclusive**: Each skill has distinct, non-overlapping functionality
- **Overlapping**: Skills may have complementary or overlapping capabilities
- **Workflow-chained**: Skills designed to work together in sequence

**Usage**: "Overlap: workflow-chained" or "Create skills that work together..."

#### 5. Script Preference
**Default**: Only when necessary

**Options**:
- **Only when necessary**: Scripts only for fragile/deterministic operations
- **Prefer scripts**: Include scripts when they add reliability
- **Minimal scripts**: Text instructions preferred, scripts as last resort

**Usage**: "Script preference: prefer scripts" or "Include Python scripts for..."

---

## Understanding Generated Skills

### Skill Patterns

The Factory automatically selects from 4 proven patterns based on your use case:

#### Pattern 1: Analysis Skills
**Triggers**: Data analysis, CSV processing, metrics, reports

**Example skills**: data-interrogation, customer-feedback-analysis

**Structure**:
- SKILL.md: Overview, triggers, 4-step workflow, core principles
- references/formats.md: Analysis report templates, comparative formats
- assets/sample_data.csv: Realistic tabular data

**Key principles**:
- Executive lens (decision-useful insights)
- Flag data quality issues
- Show methodology for reproducibility

#### Pattern 2: Document Creation Skills
**Triggers**: Writing, creating documents, memos, reports

**Example skills**: executive-memo, status-reports

**Structure**:
- SKILL.md: Document types, workflow, quality checklist
- references/formats.md: Full templates for each document type

**Key principles**:
- Answer-first structure
- Evidence-based claims
- Professional tone for target audience

#### Pattern 3: Technical Skills
**Triggers**: Technical documentation, README, API docs, code

**Example skills**: technical-docs, api-documentation

**Structure**:
- SKILL.md: Conventions, document types, quality checklist
- references/templates.md: README, API docs, changelog templates

**Key principles**:
- Proper syntax (language tags, headers)
- Runnable code examples
- Consistent formatting

#### Pattern 4: Data Processing Skills
**Triggers**: Processing, transformation, extraction, batch operations

**Example skills**: invoice-processor, pdf-extractor

**Structure**:
- SKILL.md: Operations, workflow, script usage
- scripts/processor.py: Class-based processor with type hints
- references/api_reference.md: Detailed processing options
- assets/sample_input.json: Test data

**Key principles**:
- Scripts for reliability
- Clear error messages
- Deterministic output

---

## Quality Standards

Every generated skill follows these standards automatically:

### SKILL.md Format
- ✅ 30-50 lines (overview only, details in references/)
- ✅ Exact YAML frontmatter format
- ✅ "When to use this skill" section with specific triggers
- ✅ "How to use this skill" with exactly 4 steps
- ✅ Core principles (3-5 bullets)
- ✅ Keywords section for discoverability
- ✅ Links to references/ files

### Writing Style
- ✅ Third-person descriptions ("Claude should use...")
- ✅ Imperative instructions ("Load data from CSV")
- ✅ No marketing language (no "cutting-edge", "innovative", etc.)
- ✅ No emojis in SKILL.md
- ✅ Direct, pragmatic, technical language

### Progressive Disclosure
- ✅ SKILL.md: Navigation and overview (30-50 lines)
- ✅ references/: Detailed templates (50-200 lines each)
- ✅ scripts/: Executable code (only when necessary)
- ✅ assets/: Test data (10-20 lines, minimal but realistic)

### Code Quality (when scripts included)
- ✅ Class-based structure
- ✅ Type hints (Python 3.7+)
- ✅ Docstrings for all classes and methods
- ✅ Clear error messages
- ✅ Executable with proper shebang

---

## Comparison: Manual vs. Factory

| Aspect | init_skill.py (Manual) | Skills Factory (AI-Powered) |
|--------|------------------------|------------------------------|
| **Input** | Command line with skill name | Natural language description |
| **SKILL.md** | TODO placeholders | Complete content |
| **Description** | You write it | Auto-generated from use case |
| **Workflow** | You design it | 4-step workflow created |
| **Principles** | You define them | 3-5 principles auto-generated |
| **Keywords** | You add them | Auto-generated |
| **references/** | Empty examples | Complete templates |
| **scripts/** | Placeholder | Functional code (when needed) |
| **Test data** | You create it | Realistic data included |
| **ZIP creation** | Manual (`package_skill.py`) | Automatic |
| **Multiple skills** | Run script N times | Generate N skills at once |
| **Validation** | Separate step | Built-in |
| **Time to production** | 2-4 hours | 30 seconds |
| **Manual work required** | 2-4 hours fill templates | Minimal: upload + test only |
| **Quality guarantee** | Manual adherence | Automatically enforced |

---

## File System Organization

The Factory creates this structure:

```
claude_skills/
├── generated-skills/              # Auto-created skills
│   ├── skill-name-1/
│   │   ├── SKILL.md              # Complete, production-ready
│   │   ├── references/
│   │   │   └── formats.md        # Actual templates
│   │   ├── scripts/              # (if needed)
│   │   │   └── helper.py         # Functional code
│   │   └── assets/               # (if needed)
│   │       └── sample_data.csv   # Realistic test data
│   └── skill-name-2/
│       └── SKILL.md
└── zips/                          # Ready for upload
    ├── skill-name-1.zip
    └── skill-name-2.zip
```

### ZIP Structure

Each ZIP contains the skill folder as root (Claude.ai requirement):

```
skill-name.zip
└── skill-name/
    ├── SKILL.md
    ├── references/
    ├── scripts/
    └── assets/
```

---

## Advanced Usage

### Iterating on Generated Skills

You can refine skills in the same conversation:

```
# Initial request
Generate a skill for customer feedback analysis

# Refinement
Can you add sentiment scoring to this skill?

# Further refinement
Include a Python script that processes CSV files in batches
```

### Generating Skill Families

Create related skills that work together:

```
Generate 4 workflow-chained skills for product management:
1. User story parser (converts text to structured format)
2. Technical spec generator (from parsed user stories)
3. Acceptance criteria creator (from specs)
4. Test plan generator (from acceptance criteria)

Overlap: workflow-chained
Complexity: intermediate
```

### Domain-Specific Customization

```
Domain: Healthcare/Medical
Generate 3 skills following HIPAA compliance guidelines:
- Patient data anonymizer
- Medical record summarizer
- Treatment plan formatter

Include disclaimers about regulatory compliance in all skills
Complexity: advanced
```

### Testing Generated Skills

After generating a skill, test it in Claude.ai:

**Basic test**:
```
I just added the 'customer-feedback-analysis' skill. Can you analyze this feedback data?
[attach sample CSV]
```

**Complex test**:
```
Use the customer-feedback-analysis skill to:
1. Identify the top 5 customer pain points
2. Group feedback by sentiment (positive/negative/neutral)
3. Generate an executive summary with actionable recommendations
```

---

## Troubleshooting

### Issue: ZIP Already Exists

**Error message**: `⚠️ zips/skill-name.zip already exists, skipping`

**Solution**:
- Delete the existing ZIP if you want to regenerate it
- Or rename your skill to avoid conflicts

**Command**:
```bash
rm zips/skill-name.zip
# Then request regeneration
```

### Issue: Generated Skill Doesn't Match Expectations

**Solution**: Provide more specific details in your request

**Instead of**:
```
Generate a data analysis skill
```

**Try**:
```
Generate a skill for analyzing quarterly sales data that:
- Identifies revenue trends by region
- Flags unusual sales patterns
- Compares performance to previous quarters
- Generates executive summary with visualizations

Include sample data with 50 sales transactions
Complexity: intermediate
```

### Issue: Need to Modify Generated Skill

**Options**:

1. **Regenerate with more specific instructions**:
   ```
   Regenerate customer-feedback-analysis but add:
   - NPS score calculation
   - Customer segmentation by feedback type
   - Monthly trend analysis
   ```

2. **Manually edit files**:
   - Edit `generated-skills/skill-name/SKILL.md`
   - Modify `references/formats.md`
   - Recreate ZIP manually:
     ```bash
     cd generated-skills
     zip -r ../zips/skill-name.zip skill-name/
     ```

3. **Request incremental changes**:
   ```
   Add a Python script to the customer-feedback-analysis skill
   that calculates NPS scores from rating data
   ```

### Issue: Upload to Claude.ai Fails

**Common causes**:
1. ZIP structure incorrect (folder not at root)
2. SKILL.md missing or malformed
3. ZIP file corrupted

**Solution**: Validate the skill first

```bash
# Check ZIP contents
unzip -l zips/skill-name.zip

# Should show:
# skill-name/SKILL.md
# skill-name/references/...

# Validate SKILL.md
python skill-creator/scripts/quick_validate.py generated-skills/skill-name
```

---

## Best Practices

### 1. Be Specific About Use Cases

**Good**:
```
Generate a skill for analyzing customer support tickets that:
- Categorizes tickets by issue type (billing, technical, feature request)
- Calculates average resolution time
- Identifies repeat issues
- Generates weekly summary reports
```

**Avoid**:
```
Generate a customer support skill
```

### 2. Specify Domain Context

Always include domain if not general business:

```
Domain: Healthcare
Generate a skill for medical record summarization
```

This ensures appropriate terminology, examples, and compliance considerations.

### 3. Start Simple, Then Iterate

Begin with basic version, then enhance:

```
# Initial
Generate a beginner skill for meeting notes to action items

# After testing
Add deadline extraction and priority assignment to the meeting-action-extractor skill

# Further enhancement
Include a script that sends action items to a task management system
```

### 4. Request Multiple Related Skills Simultaneously

When skills work together, generate them in one batch:

```
Generate 3 workflow-chained skills:
1. Data collector (CSV import and validation)
2. Data analyzer (statistical analysis and insights)
3. Report generator (executive summary creation)
```

This ensures consistency and compatibility.

### 5. Test Generated Skills Before Deployment

Always test with sample data before using in production:
- Verify output format matches expectations
- Check edge case handling
- Confirm quality of generated content

---

## Examples Gallery

### Example 1: Financial Analysis Skill

**Request**:
```
Generate an intermediate skill for quarterly financial report analysis
```

**Generated files**:
- `generated-skills/quarterly-financial-analysis/SKILL.md`
- `generated-skills/quarterly-financial-analysis/references/formats.md`
- `generated-skills/quarterly-financial-analysis/assets/sample_financials.csv`
- `zips/quarterly-financial-analysis.zip`

**SKILL.md excerpt**:
```yaml
---
name: quarterly-financial-analysis
description: Analyze quarterly financial reports to identify revenue trends, expense patterns, and key performance metrics. Claude should use this skill when analyzing financial statements, earnings reports, or quarterly business results.
---

## When to use this skill

Use for quarterly earnings reports, financial statements, P&L analysis, budget vs. actual comparisons, or any structured financial data requiring executive-level insights.

## How to use this skill

1. **Inspect financial data** - Review structure, completeness, identify key metrics
2. **Analyze patterns** - Revenue trends, expense analysis, margin calculations
3. **Generate insights** - YoY comparisons, quarter-over-quarter trends, anomalies
4. **Create output** - Use executive summary format from references/formats.md
...
```

### Example 2: Multiple Skills for Project Management

**Request**:
```
Generate 3 workflow-chained skills for project management:
- Sprint planning assistant
- Daily standup summarizer
- Sprint retrospective analyzer

Complexity: intermediate
```

**Generated**:
- 3 skills in `generated-skills/`
- 3 ZIPs ready for upload
- Each with complete templates and workflows
- Designed to work together in project management workflow

### Example 3: Technical Documentation Skill

**Request**:
```
Create a skill for API documentation generation that:
- Converts code comments to markdown docs
- Includes parameter tables
- Generates example requests/responses
- Creates changelog entries

Include a Python script for parsing code files
Complexity: advanced
```

**Generated**:
- Complete SKILL.md with API doc conventions
- `scripts/api_doc_generator.py` with class-based parser
- `references/templates.md` with API doc templates
- `assets/sample_api_code.py` for testing

---

## Reference

### Related Documentation

- [skill-format-spec.md](skill-format-spec.md) - SKILL.md format requirements
- [skill-authoring-guide.md](skill-authoring-guide.md) - Manual skill creation best practices
- [CLAUDE.md](../CLAUDE.md) - Repository guide for Claude Code

### External Resources

- [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

### Tool Location

- **Factory Prompt**: `SKILLS_FACTORY_GENERATOR_PROMPT.md` (repository root)
- **Generated Skills**: `generated-skills/` folder
- **ZIPs**: `zips/` folder
- **Manual Tools**: `skill-creator/scripts/` folder

---

## FAQ

**Q: Can I modify generated skills manually?**
A: Yes! Edit files in `generated-skills/skill-name/`, then recreate the ZIP:
```bash
cd generated-skills && zip -r ../zips/skill-name.zip skill-name/
```

**Q: How many skills can I generate at once?**
A: Up to 10 skills per request. For more, make multiple requests.

**Q: Can I use this for skills other than business/productivity?**
A: Yes! Specify any domain: gaming, education, creative writing, research, etc.

**Q: Do I need to validate generated skills?**
A: No, validation is automatic. But you can double-check:
```bash
python skill-creator/scripts/quick_validate.py generated-skills/skill-name
```

**Q: Can I generate skills for the Claude API (not Claude.ai web)?**
A: Yes! The generated skills work with Claude API, Claude.ai web, and Claude Code.

**Q: What if I don't like the generated skill name?**
A: Just specify the name in your request:
```
Generate a skill called 'financial-wizard' for quarterly report analysis
```

**Q: Can I see examples before generating?**
A: Yes! Look at existing skills in the repository:
- `research-synthesis/` - Analysis pattern
- `executive-memo/` - Document creation pattern
- `technical-docs/` - Technical pattern
- `data-interrogation/` - Data processing pattern

**Q: Is there a cost to generating skills?**
A: No additional cost beyond your normal Claude usage (Claude Code/Cursor subscription).

---

**Last Updated**: October 2024
