# AI Tool Adoption Tracking - Quick Start Guide

## Overview

Track and analyze AI tool adoption across the Penang team to:
- Measure adoption rates by tool and role
- Identify training needs
- Quantify time saved and ROI
- Track trends over time

---

## Setup (One-Time)

### Step 1: Create Tracking Template

```python
from ai_tool_adoption_tracker import create_tracking_template

# Creates Excel file with 4 weeks of tracking rows
create_tracking_template('ai_tool_usage_tracker.xlsx')
```

**Output**: `ai_tool_usage_tracker.xlsx` with 4 sheets:
- **Weekly Tracking**: Main data entry sheet
- **Team Members**: Team roster (AMs + MGS)
- **AI Tools Reference**: List of tracked tools
- **Instructions**: How to use the tracker

---

## Weekly Process

### Step 2: Fill in Usage Data

**Every Monday**, fill in the previous week's data:

1. Open `ai_tool_usage_tracker.xlsx`
2. Go to **Weekly Tracking** sheet
3. For each team member + tool combination:
   - **Usage Frequency**: Select from dropdown
     - Daily
     - 3-4x per week
     - 1-2x per week
     - Few times per month
     - Rarely/Never
   - **Primary Use Case**: Brief description
     - Examples: "SQL queries", "Report writing", "Code debugging", "Data analysis"
   - **Time Saved**: Estimate hours saved per week
   - **Notes**: Optional context

**Example Entry:**
| Week | Team Member | AI Tool | Usage Frequency | Primary Use Case | Time Saved |
|------|-------------|---------|------------------|------------------|------------|
| Week 1 | Darren | Cursor | Daily | Code generation, SQL queries | 5 |

---

### Step 3: Run Analysis

```python
from ai_tool_adoption_tracker import analyze_adoption

# Generates adoption report
metrics = analyze_adoption(
    tracker_file='ai_tool_usage_tracker.xlsx',
    report_file='ai_tool_adoption_report.md'
)
```

**Output**: `ai_tool_adoption_report.md` with:
- Executive summary
- Tool adoption rates
- Usage frequency analysis
- Time saved metrics
- Individual adoption status
- Weekly trends
- Recommendations

---

## Metrics Tracked

### 1. Tool Adoption Rate
- % of team using each tool
- Users vs. total team size

### 2. Usage Frequency
- Average frequency score per tool
- Frequency distribution

### 3. Role-Based Adoption
- AM vs. MGS adoption patterns
- Tool coverage by role

### 4. Time Saved
- Hours saved per tool
- Total time saved per week
- Individual time saved

### 5. Use Case Distribution
- Most common use cases
- Tool-to-use-case mapping

### 6. Individual Adoption
- Tools used per person
- Time saved per person
- Average frequency per person

### 7. Weekly Trends
- Adoption growth over time
- Active users trend
- Tools used trend

---

## Reporting to Leadership

### Monthly Summary Format

**Title**: AI Tool Adoption - Penang Team (Month YYYY)

**Key Metrics**:
- Adoption Rate: X% of team using AI tools
- Top Tool: [Tool Name] (X% adoption)
- Time Saved: X hours/week
- ROI: [Calculate if tool costs available]

**Insights**:
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

**Recommendations**:
- [Action item 1]
- [Action item 2]

---

## Team Members Tracked

### Account Managers (AM)
- Chia Yee
- Darren
- Suki

### Merchant Growth Specialists (MGS)
- Teoh Jun Ling
- Lee Sook Chin
- Low Jia Ying
- Hon Yi Ni

**Total**: 7 team members

---

## AI Tools Tracked

1. **Cursor** - Code editor with AI
2. **ChatGPT** - General AI assistant
3. **Claude (Anthropic)** - AI assistant
4. **GitHub Copilot** - Code completion
5. **Microsoft Copilot** - Office AI
6. **Perplexity** - AI search
7. **Notion AI** - Note-taking AI
8. **Other** - Custom tools

---

## Troubleshooting

### "No usage data found"
- Ensure "Usage Frequency" column is filled in
- Check that data is in the correct sheet ("Weekly Tracking")

### "Could not load data"
- Verify file path is correct
- Ensure Excel file is not open in another program
- Check file permissions

### Missing team members
- Update `PENANG_TEAM` dictionary in `ai_tool_adoption_tracker.py`
- Re-run `create_tracking_template()`

---

## Next Steps

1. **Week 1**: Create template, share with team
2. **Week 2**: Collect first week of data
3. **Week 3**: Run analysis, share initial insights
4. **Week 4**: Identify gaps, plan training
5. **Monthly**: Generate leadership report

---

## Questions?

Contact: Benjamin Liang (Commercial Manager, Penang)

