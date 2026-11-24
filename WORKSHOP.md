# Workshop guide: Larkspur weekly operations sync, 2 November 2026

Nine steps for the live session, covering preparation for the 2 November sync, a fact-check of what was said, and the follow-up.

Before you start, follow [Get the lab](README.md#get-the-lab) and open `larkspur-coco-desktop-lab` as a project. Start a **new session** for each step unless the step says otherwise.

| Step | What you do |
|---|---|
| 1 | See what CoCo can work with |
| 2 | Ask the business a question |
| 3 | Review a document and check a source online |
| 4 | Connect a tool |
| 5 | Add custom instructions and install the skills |
| 6 | Fact-check the meeting and automate the follow-up |
| 7 | Build a slide deck and download it as PowerPoint |
| 8 | Publish and share an artifact |
| 9 | Check who used which model, and what data they touched |

## Step 1: See what CoCo can work with

> What documents are in this project, and what company data can you see? One line each.

**What to look for:** eight PDF documents and three sets of company data: adviser queries, energy sites and monthly energy generation. CoCo may use technical names for the data. That's fine.

## Step 2: Ask the business a question

> Which type of adviser query misses its service level most often? Break the worst one down by how it reached us.

Then check one number yourself:

> How did you work out that figure? Explain it in one sentence, without technical terms.

**What to look for:** tax certificates miss their service level in more than half of cases, and every one that came in by email was late.

## Step 3: Review a document and check a source online

> Read @docs/asset-monitoring-report.pdf. Summarise it in five bullets for the investment committee. Then list the three questions the committee is most likely to ask.

Then, in the same session:

> Which of our sites were more than 10% below forecast from August to October? For each one, tell me whether downtime explains it.

**What to look for:** Kestrel Ridge and Saltmarsh are explained by long outages (a gearbox and an inverter). Glen Ardoch isn't: it had almost no downtime, and the operations notes point to grid curtailment.

Now a PDF, in the same session:

> Read @docs/valuation-report-millbrook-yard.pdf. Check the loan against the lending limits in the report. Would you put it to the credit committee as it stands? Answer in three bullets.

**What to look for:** loan to GDV (55.5%) and loan to cost (60.6%) are inside the limits, but developer profit is 8.5% against a 15% minimum, and no ground investigation has been provided for a site next to a former tannery.

Then check what curtailment means using CoCo's browser:

> Open https://en.wikipedia.org/wiki/Curtailment_(electricity) in the browser. In two sentences, explain curtailment to the investment committee and what it means for Glen Ardoch.

**What to look for:** the page opens in a browser tab inside CoCo, and the answer links what the page says to Glen Ardoch's shortfall.

## Step 4: Connect a tool

Draw.io is connected for the whole team, so you don't need to set anything up.

> Find the document in this project that describes how tax certificate requests are handled. Use Draw.io to draw how a request moves from an adviser's email to a resolved query, with the customer portal as a second route, and mark where the delays happen. Then open the diagram in app.diagrams.net in the CoCo browser.

**What to look for:** CoCo finds `docs/tax-certificate-process.pdf` without being told, and the diagram opens in a browser tab inside CoCo, ready to edit. It shows the email route's hand-offs (shared inbox, missing client reference, forward to Tax Operations, print run) marked as the delays found in step 2.

## Step 5: Add custom instructions and install the skills

**Custom instructions.** Open **Customize > Personalization > Custom instructions**, paste the text from [Set how CoCo writes](README.md#set-how-coco-writes), and click **Save**. It applies from your next new session.

**Skills.** Skills are saved tasks you run with `/`. This project ships two in `.snowflake/cortex/skills`. Install them as your own so they work in any project:

> Install every skill in this project's .snowflake/cortex/skills folder as my personal skills, so I can use them in any project. Then explain each one in two lines: what it does and when I'd use it.

Then run one:

> /weekly-ops-brief

Then make it yours:

> Update the weekly-ops-brief skill so it also compares each category with the previous week. Show me the change before you save it.

**What to look for:** `weekly-ops-brief` and `larkspur-deck` appear in **Customize > Skills**, each with a plain explanation, and the change to the brief shows before it's saved.

## Step 6: Fact-check the meeting and automate the follow-up

> Read @docs/meeting-transcript.pdf. Check every claim about our numbers against our data. Give me a table: the claim, right or wrong, and the real number.

**What to look for:** four claims don't hold up. September, not October, was the busiest month. Complaints are concentrated on the EIS Fund. Tax certificates are the worst category for missing service levels. Glen Ardoch's shortfall isn't downtime.

The meeting ends with Marcus agreeing to pull the adviser query numbers by hand every Monday. Schedule it in CoCo:

> Run /weekly-ops-brief every Monday at 8am.

Open **Automations** in the sidebar to see it. Automations run on your computer while CoCo Desktop is open. Delete this one after the lab.

## Step 7: Build a slide deck and download it as PowerPoint

The `larkspur-deck` skill you installed in step 5 writes the slides once and saves two files: an HTML version to review in CoCo and a PowerPoint file.

> /larkspur-deck Build a 5-slide deck for the investment committee from @docs/asset-monitoring-report.pdf: portfolio generation against forecast, the two funds, the sites more than 10% below forecast, and next steps. Save it to my Downloads folder and open the HTML version.

Read the slides, then open your Downloads folder and double-click the `.pptx` file.

**What to look for:** the HTML deck opens in a CoCo tab, the PowerPoint file opens in PowerPoint, Keynote or Google Slides, and the figures match the report (384.5 MW, 6.2% below forecast). If CoCo asks to install `python-pptx`, click **Allow**.

## Step 8: Publish and share an artifact

In the step 6 session:

> Build a one-page fact-check of the 2 November meeting, with the corrected numbers and the corrected action items. Publish it to Artifacts and share it with the workshop team.

Open **Artifacts** and find the page. Then open a colleague's.

**What to look for:** a page you and your colleagues can open, with the same corrected numbers as step 6.

## Step 9: Check who used which model, and what data they touched

This step is for your account administrator. It needs the ACCOUNTADMIN role, so switch to it in CoCo before you start. Usage takes up to an hour to appear, and data-access records up to three hours, so run it at the end of the session or the next day.

> For this workshop session, show usage by user and model, including tokens and estimated spend.

What to look for: a table with one row per user and model, with token and credit totals, built from `SNOWFLAKE.ACCOUNT_USAGE.CORTEX_CODE_DESKTOP_USAGE_HISTORY`. CoCo may load its cost skill to answer.

> Show which users accessed which lab data during the workshop, and when.

What to look for: each user against the `LARKSPUR_LAB.SHARED` tables they queried, with a query count and first and last access times, built from `SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY`.

The same spend is visible without a prompt in Snowsight: **Admin > Cost management > Account Overview**, grouped by **Services** to see Cortex Code Desktop as its own line. That page can lag by up to 72 hours.

## After the session

Run the same steps on your own documents. Suggestions are in [After the lab](README.md#after-the-lab).
