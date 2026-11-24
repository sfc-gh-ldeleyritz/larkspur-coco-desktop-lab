# Larkspur Group lab: context for CoCo

This project is a hands-on lab for Larkspur Group, a fictional UK investment group. All data and documents are synthetic.

## Where the data lives

The company data is already in Snowflake, in database `LARKSPUR_LAB`, schema `SHARED`. Use it whenever the user asks about the business. Never ask the user for table or schema names.

| Table | What it holds |
|---|---|
| `LARKSPUR_LAB.SHARED.ADVISER_QUERIES` | 360 service queries from financial advisers and their clients, August to October 2026: product, category, channel, status, service level (`SLA_HOURS`), time to resolve (`HOURS_TO_RESOLVE`) and the adviser's comment (`FEEDBACK_TEXT`). A query breaches its service level when `HOURS_TO_RESOLVE` is greater than `SLA_HOURS`. |
| `LARKSPUR_LAB.SHARED.ENERGY_SITES` | 24 solar, wind and battery storage sites across two funds |
| `LARKSPUR_LAB.SHARED.ENERGY_GENERATION_MONTHLY` | Forecast and actual generation, downtime hours and operations notes per site, January to October 2026 |

Documents are in `docs/`.

## How to work with this team

- The people using this project are business leaders, not engineers. Answer in plain business language.
- Don't show SQL unless asked. Say which data you used in one short line at the end.
- Read only. Never create, change or delete anything in Snowflake unless the user explicitly asks.
- Lead with the answer, then the numbers behind it. UK English.
