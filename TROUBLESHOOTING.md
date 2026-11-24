# Troubleshooting

Fixes for common problems in this lab. For anything not covered here, ask your facilitator or see the [CoCo Desktop documentation](https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-desktop).

## Getting the lab

**CoCo can't download the lab**
Your network may block the download. Open https://github.com/sfc-gh-ldeleyritz/larkspur-coco-desktop-lab in your browser, click **Code > Download ZIP**, unzip it into Documents, and open the folder as a project.

**`@` doesn't find the documents**
Open the whole `larkspur-coco-desktop-lab` folder as a project, not a single file.

## Answers and data

**CoCo won't answer, or no models show up**
Check the connection menu at the top: it should show the workshop connection your facilitator set up. If it doesn't, ask your facilitator.

**CoCo says it can't find the company data**
Make sure you started the session inside the Larkspur project. The project tells CoCo where the company data is.

**"No active warehouse"**
CoCo needs compute to answer questions about the data. Click your connection name in the top bar, choose **Default Warehouse**, and pick the one your facilitator named.

## Connectors and skills

**Draw.io doesn't appear in Customize > MCP**
Your facilitator needs to turn it on for the team. After they do, start a new session.

**I can't find a skill**
Check **Customize > Skills > Local Skills**, inside the Larkspur project. If it isn't there, ask your facilitator.

## Still stuck?

Ask your facilitator. They can collect CoCo Desktop's logs for Snowflake Support if needed.

## The deck step can't build the PowerPoint file

The `larkspur-deck` skill needs the Python package `python-pptx`. Ask CoCo: "Install python-pptx for me, then rebuild the deck." If your laptop blocks installs, ask for the HTML version only and print it to PDF from the browser.

## Step 9 returns "insufficient privileges" on ACCOUNT_USAGE

Step 9 runs as ACCOUNTADMIN. Switch to that role and run the prompts again. To give the check to another role later, such as an auditor, an admin can grant:

```sql
GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE <role>;
GRANT DATABASE ROLE SNOWFLAKE.GOVERNANCE_VIEWER TO ROLE <role>;
GRANT APPLICATION ROLE SNOWFLAKE.APP_USAGE_VIEWER TO ROLE <role>;
```

The first covers model usage, the second covers data access, the third the Cost management page.
