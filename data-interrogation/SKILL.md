---
name: data-interrogation
description: Analyze CSV and tabular data to extract executive-level insights, identify patterns and anomalies, and create actionable recommendations. Claude should use this skill when analyzing spreadsheets, CSV files, or tabular data requiring summary statistics and business insights.
---

## When to use this skill

Use this skill to analyze:
- CSV files and spreadsheets
- Sales data, customer metrics, operational data
- Survey results and response data
- Any tabular data requiring pattern analysis
- Data requiring executive-level insights

## Analysis process

1. **Data inspection** - Structure, completeness, quality check
2. **Exploratory analysis** - Summary statistics, patterns, outliers
3. **Insight generation** - Business-relevant findings
4. **Output creation** - Executive-ready format with recommendations

## Output format

```markdown
# Data Analysis: [Dataset Name]

## Dataset Overview
- **Rows**: [count]
- **Columns**: [count]  
- **Date Range**: [if applicable]
- **Quality**: [assessment]

## Key Findings

### Finding 1: [Title]
[Pattern/insight with supporting numbers]

### Finding 2: [Title]
[Pattern/insight with supporting numbers]

## Summary Statistics

| Metric | Value |
|--------|-------|
| [Metric] | [Value] |

## Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

## Data Quality Notes
[Issues, limitations, caveats]
```

## Analysis techniques

- **Summary stats**: count, mean, median, min, max, percentiles
- **Pattern detection**: sorting, grouping, time-series trends, outliers
- **Comparisons**: period-over-period, category analysis, correlations
- **Quality checks**: missing values, duplicates, range validation

## Key principles

1. **Executive lens** - Focus on decision-useful insights, not just statistics
2. **Flag issues** - Call out data quality problems clearly
3. **Show methodology** - Explain calculations for reproducibility
4. **Context matters** - Ask for clarification if data context unclear
5. **Appropriate depth** - Match detail level to data complexity

## For large datasets

When analyzing >10,000 rows, focus on summary statistics and patterns rather than row-by-row review.

## Keywords

data analysis, CSV analysis, spreadsheet analysis, data interrogation, business intelligence, metrics analysis, statistical summary, trend analysis

