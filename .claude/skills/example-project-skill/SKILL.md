---
name: example-project-skill
description: Example project skill showing team-shared skill pattern for Claude Code. Claude should use this as a reference when creating project skills that will be checked into git and shared with the team.
---

## When to use this skill

This is an **example project skill** demonstrating the `.claude/skills/` pattern for Claude Code.

**Project skills** are:
- Stored in `.claude/skills/` within the project repository
- Checked into git and shared with the entire team
- Auto-discovered when teammates clone or pull the repository
- Perfect for project-specific conventions, workflows, and shared expertise

## How to use this skill

1. **Create directory** - `mkdir -p .claude/skills/your-skill-name`
2. **Add SKILL.md** - Include YAML frontmatter and markdown content
3. **Commit to git** - `git add .claude/skills/ && git commit -m "Add team skill"`
4. **Share with team** - Teammates get the skill automatically when they pull

## Core principles

1. **Team-shared** - Available to all project contributors, not just one developer
2. **Version controlled** - Changes tracked in git, can be reviewed in PRs
3. **Auto-discovered** - No manual installation required for team members
4. **Project-specific** - Contains workflows and conventions unique to this codebase

## Example use cases

- API integration patterns specific to this project
- Database query conventions your team follows
- Code review checklists for this codebase
- Deployment workflows for this application
- Testing strategies unique to your stack

## Keywords

project skill, team skill, claude code, git, shared workflow, team conventions
