---
name: weekly-ops-brief
description: Produce a one-page weekly operations brief from Larkspur's adviser queries. Use when the user asks for the weekly ops brief, service level performance, backlog, or top service issues.
---

# Weekly operations brief

Produce a one-page brief from `LARKSPUR_LAB.SHARED.ADVISER_QUERIES`. Read only; never change data.

## Steps

1. **Pick the week.** Use the most recent full week in the data unless the user names one. Say which week you used.
2. **Service levels.** For resolved queries, a query is late when `HOURS_TO_RESOLVE` is greater than `SLA_HOURS`. Show the late rate by category, worst first.
3. **Backlog.** Count queries that are Open or In progress, by priority.
4. **Top 3 issues.** The three categories or products with the most late queries or complaints, each with one line of evidence and a number.
5. **Write it up.** Lead with one sentence on the most important point. Then three short sections: service levels, backlog, issues. Under one page, plain business language, UK English. No SQL in the brief.
