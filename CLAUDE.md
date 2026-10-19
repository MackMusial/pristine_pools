# Pristine Pools — Record-Keeping & Water-Testing System

Capstone project (SVSU, CSIS). Developer: Mack. Target completion: **April 2027**.
Run by **Dr. Scott James** (also Mack's CIS 422 professor). Mack's group has 5 people and is competing against 2 other groups.

> **Sync ritual:** this file is the single source of truth. When a decision is made in a chat or voice session, carry it into this file. When one is made in Claude Code, update this file and commit it.

## How Claude helps on this project
- **Mack writes all the code.** Do not write or edit code files in this repo. Explain the concept, the NiceGUI pieces involved, and what to type and why; Mack types it in the IDE. Small illustrative snippets in chat only when asked. Review Mack's code when asked.
- Exception: restoring or reverting files Claude changed by mistake, and other non-code housekeeping, only when Mack asks.
- Explain what the code does and **why**. Mack wants to understand it, not just receive working output.
- Keep responses concise and structured: method names and architecture reasoning over long prose.
- Don't dump unsolicited code; Mack prefers to iterate in the IDE.
- One NiceGUI concept per step. Mack commits small steps.
- **Preferred pattern (2026-10-18): Claude describes what's needed (the pieces, the element names, any new syntax), Mack writes it, then Claude reviews.** Give full snippets only for brand-new syntax or when asked.
- **Sample/placeholder data is OK for Claude to write** (fake customers, canned AI suggestions, test readings). Mack pastes it in. It's not the learning part. Keep it realistic for a pool store (use 555-01xx phone numbers).
- **Focus on syntax and the NiceGUI pieces.** That's where Mack needs help. Skip the basics: running the app, saving, where to click in VS Code, "press Enter".
- **When Claude needs Mack to decide something, ask with the question popup (AskUserQuestion)**, never a question buried in a reply. It's much more obvious that way.
- This file is committed on purpose so context carries between Mack's desktop and laptop. **Claude keeps it up to date as we go without being asked**: mark steps done and move the current-step marker, record new decisions, preferences, setup changes, and answered open questions.

## Build plan (NiceGUI)
1. `layout.py`: shared `page_layout()` with `ui.header` (☰ `drawer.toggle`, title, search) + `ui.left_drawer` nav, used by every page. **Done.**
2. Split pages into `pages/*.py`, import them in `main.py`. **Done.**
**Decision (2026-10-07): GUI first, functionality later.** Mack wants the whole GUI looking presentable and polished before wiring anything up. Pages use hardcoded placeholder content (a few sample rows written inline) just so layouts can be judged; buttons can be no-ops. Don't steer back toward the database until the GUI phase is done.

### Phase 1: GUI (looks only)
3. Global look: theme colors (`ui.colors`), header/drawer styling, active nav item, fonts/spacing. Decided: **light mode**. Theme switcher is built in `layout.py` (`THEMES` dict: `pool` / `aqua` / `ocean`, `CURRENT_THEME`, `ui.colors(**THEMES[CURRENT_THEME])`). **Color pick deferred** until more of the GUI exists to judge against; header/drawer polish also comes back later.
**App structure (decided 2026-10-07), built around the counter workflow:** customer walks in with a water sample → find customer → pick pool → enter test → see flags → log problem / AI help → print report. Modeled on real pool-store test software (LaMotte WaterLink, BioGuard ALEX, AccuBlue). Pools, tests, problems and purchases live *inside* a customer (see the three-screen decision below). Efficiency rules: keyboard-first (Enter submits, sensible Tab order, autofocus), smart defaults (today's date, auto-select a customer's only pool), flag out-of-range values live while typing, quick adds in `ui.dialog`s.

**Decision (2026-10-12): chat-style layout (like ChatGPT/Claude).** Replaces the search-first Home design. Mack's sketch: header across the top, a column down each side, a long chat bar with a **+** pinned at the bottom center.
   - **Middle:** Home = the AI chat (messages stack in the middle, bar at the bottom). The Customer and Maintenance screens are normal pages that open in the middle area.
   - **Left (`ui.left_drawer`):** navigation (Home, Maintenance) + chat history / recent customers.
   - **Right (`ui.right_drawer`):** the selected customer/pool's details + latest test, as context next to the chat.
   - **Header:** the other buttons go here (e.g. New Water Test, Add Customer). Quick actions now live in the header, not on Home.
   - **+ on the chat bar:** attach a customer/pool, so the AI answer uses that pool's size, equipment and tests (like attaching a file). Canned AI replies in Phase 1.
   - **Chat bar (decided 2026-10-12): look like Claude.ai's.** Use `ui.footer()` to pin it to the bottom, but make the bar invisible (`bg-slate-100`, the same as the body). Inside it goes a centered column (`w-full max-w-3xl mx-auto`) holding an `outlined rounded` input, with + / send in the input's `prepend` / `append` slots (`chat = ui.input(...)`, then `with chat.add_slot(...)`). Optionally, a small row under the box like Claude's.
   - Old Home content: the stat cards and the big search bar are probably dropped or moved (recent customers → left drawer). Decide while building.
4. Home = chat screen. **Done (2026-10-16).** Order: (a) chat bar → (b) clear the old Home content out of the middle → (c) chat messages in the middle (`ui.chat_message`, canned conversation) → (d) right drawer (customer/pool context) → (e) header action buttons → (f) left drawer recent customers.
   - (a) progress: footer `bg-slate-100`; a centered row (`w-full max-w-3xl mx-auto justify-center items-center`) holds the chat input (`chat = ui.input(...)`, `flex-1`, `outlined rounded`) with + / send in its `prepend` / `append` slots (`flat round dense`). Committed in `04680a7`. Learned: `justify-*` = along the row, `items-*` = across it; an invisible container can be centered while its contents sit at its left edge; `.add_slot()` returns the slot, not the element, so nothing can be chained after it.
   - (a) **Done** (the crash bug was fixed in `f8cec2a`, and the page loads). (b) **Done**: the old Home content is commented out in `home.py` (also in `3a7f295`). (c) **Done** (the canned staff + Pool Assistant messages). (d) **Done**: the right drawer has Customer / Pool / Latest test sections split by `ui.separator()`, with heading / main / detail label styles and `ui.badge(text, color=...)` flags in a row (`text-gray-500` fixed). (e) **Done**: a second `ui.row()` in the header (a sibling of the title row) with New Water Test / Add Customer (`flat color=white`), pushed right by `justify-between`. (f) **Done**: the left drawer (`layout.py`) has Home / Settings buttons, `ui.separator()`, a small uppercase "Recent customers" label, and a `ui.list().props('dense')` of 4 sibling `ui.item(on_click=lambda: None)` rows (name + `caption` details). Learned: `ui.header` is the page's top bar (keyword-only args, one per page), not a text heading; headings are styled `ui.label`s. (d) means `ui.right_drawer()` in `home.py` (only the chat page), showing the attached customer/pool context. For reference, (c) was a centered message column (`w-full max-w-3xl mx-auto`) with `ui.chat_message(...)` bubbles; `sent=True` = staff (right side), `sent=False` = AI (left side). **Voice:** an employee asks the AI on a customer's behalf ("Customer's pool...", with test numbers), and the AI suggests what the employee should recommend to the customer.
   - Previous search-first Home (search bar, stat cards, Quick Actions, Recent Customers card) is **finished and committed** (`3a7f295`) and can be referenced or reused.
   - Concepts Mack has learned so far: `with` nesting/indentation (siblings vs children), `.classes()` (Tailwind) vs `.props()` (Quasar), `flex-1` + `w-full`, slots, `ui.list`/`ui.item`/`item_section`/`item_label`, nested dicts + `**` unpacking.
   - Run tip: always launch from `main.py` (running a page file directly gives `No module named 'layout'`); a launch.json pointing at `${workspaceFolder}/main.py` fixes F5.
**Decision (2026-10-15): three screens** (see "Screens" under Architecture decisions). This replaces the earlier separate Customers-list / Customer / Pool / Settings pages.
5. **Done (2026-10-16).** Built: `CUSTOMERS` dict in `layout.py` (id → `'Name · phone'`, 16 sample customers with 555-01xx numbers); `search = ui.select(CUSTOMERS, with_input=True, label='Find customer', on_change=lambda e: ui.navigate.to(f'/customer/{e.value}'))` with `dense dark standout clearable`, `w-96`, 🔍 in the prepend slot. Mack disliked `ui.notify` toasts, so don't use them as placeholders. The ✕ clear guard (`... if e.value else None`) is done (`42489a4`). Learned: flat dict vs nested, event object `e` / `e.value`, f-strings, conditional expressions.
   - **Customer search on Home:** a search bar with a dropdown of matches (`ui.select` with `with_input` or `ui.input` + autocomplete). Picking a customer opens their Customer screen. It replaces the separate Customers-list page and `ui.table`. Placement decided 2026-10-16: **header, center** (in `layout.py`, between the logo row and the action-button row, so it's on every page).
6. **← current step.** **▶ PICK UP HERE (end of session 2026-10-17):**
   - **State of `pages/customer.py`:** page column `max-w-screen-2xl`; title row; a two-column row (`w-full no-wrap gap-6 items-start`). Left `w-1/3` column = Contact + Pool cards (label-above-value; the `ui.grid` lines are left commented out). Right `flex-1` column = tabs. Water Tests tab done (latest-test card + history table). Problems tab = Log a Problem card + Suggestions card (radio → `fix_box` via `set_value`, clearable, Save Fix row), still **stacked**. Purchases = placeholder.
   - **Decision (2026-10-18, clarified): on desktop/POS-size screens the PAGE never scrolls like a website, but scrolling INSIDE a card or column is fine** for long data (history, long lists). Phones may scroll normally. Technique (`md:` and up only): page column `md:h-[calc(100vh-4rem)]` (tweak the rem to the real header height) → two-column row `md:flex-1 md:min-h-0` → each column `md:h-full md:overflow-y-auto`. Still keep content tight (Problems cards side by side; optional `ui.expansion` for less-used pool details; `pagination=` on long tables) so inner scrolling is only needed for genuinely long data. Target: a 1920×1080 store monitor (assumed; the client's PC specs are still open).
   - **Fit-to-screen done (2026-10-18):** page column `md:h-[calc(100vh-7rem)]`, row `md:flex-1 md:min-h-0`, left info column `md:h-full` (no scroll; both cards `gap-1`), tabs column `md:h-full md:overflow-y-auto`. Checked on the laptop (~1536×740 usable at 125% scaling) and at 1920×1080. Learned: NiceGUI adds ~1rem of padding around page content; Tailwind silently ignores misspelled classes; each class needs its own `md:`.
   - **Problems cards side by side done (2026-10-18)**: one row (`w-full no-wrap gap-4 items-start`) holding both cards as siblings. To avoid inner scroll: Mack rejected `dense` on the radio (too cramped) and short labels (he wants the full suggestion text visible). **Decided: Log a Problem card `w-1/3`, Suggestions card `flex-1`** (wider, so the text wraps less). Textareas use `autogrow` (it only works on textareas, not the radio), and that removed the last inner scroll. The radio is NOT `dense`.
   - **Paused here (2026-10-18, 1am).** Next: the remaining Problems nits (Get Suggestion button *below* the textarea in a `w-full justify-end` row; "customers" → "customer's"; drop `.classes('justify-end')` from the Save Fix button and add `icon='check'`), then Step 4, problem history.
   - **Decision (2026-10-19): New Water Test moves off the header to the Customer screen's Water Tests panel**, as a filled `New Test` button (`icon='add'`) in a `w-full justify-end` row at the top of the panel. Reason: a test always belongs to one pool, so start it where the pool is already in context (search → customer → Water Tests → New Test). The header keeps Add Customer + ⚙. Later it opens a `ui.dialog` test-entry form with live out-of-range flags.
   - Step 4 (problem history) in progress: the `history` list of `(problem, fix)` tuples is in place; next is `with ui.list()` → `for problem, fix in history:` → item/section/two labels (fix = `caption`). Learned: tuples, `for` loops with tuple unpacking.
   - **Next, in order:**
     1. ~~**Step 3:** Problems cards side by side.~~ **Done 2026-10-18.** In `ui.tab_panel(problems_tab)`, wrap both cards in `ui.row().classes('w-full no-wrap gap-4 items-start')`, cards `w-full` → `flex-1`; move the `suggestions = [...]` list inside the problems panel (it currently sits between panels).
     2. Small nits in the Problems cards: move Get Suggestion *below* the textarea in a `w-full justify-end` row; "customers" → "customer's"; merge `.props('outlined').props('clearable')` → `.props('outlined clearable')`; drop `.classes('justify-end')` from the Save Fix button and add `icon='check'`.
     3. **Step 4:** Problem history card, full width under the row (`ui.list` / `ui.item`: date + problem main line, fix as `caption`). Claude writes the sample entries.
     4. **Step 5:** responsive stacking for phones (`flex-col md:flex-row` on the two-column rows).
     5. Then: the Purchases tab, the Add Customer `ui.dialog`, the Print Report button (`window.print()`). (The header logo → Home click-target row is already done in `layout.py`.)
   - Full history of this step below. Started 2026-10-16: `pages/customer.py` exists with `@ui.page('/customer/{customer_id}')` + `def customer(customer_id: int)` (path parameter, `int` type hint converts the URL text), shows `CUSTOMERS[customer_id]` as the title; imported in `main.py`. Tabs skeleton **done** (`ui.tabs() as tabs` with `test_tab` / `problems_tab` / `purchases_tab`; `ui.tab_panels(tabs, value=test_tab)`, one `ui.tab_panel` per tab). Water Tests tab: a latest-test card is **done** (a `w-full` card → a header row `w-full items-center justify-between` with title + print button, then a badge row). Learned: `justify-between` needs a **row** (a card stacks like a column) that is `w-full`. Contact + Pool info cards: **decided 2026-10-18 to stack them vertically** (Mack compared stacked vs. side by side). Cards sit directly in the page column with `w-full`, with no wrapping row. Problems tab: "Log a Problem" card **done** (`a061a3e`: `w-full` card, heading, `problem_description = ui.textarea(...)` outlined `w-full`, Get Suggestion button). Nits: move the button *below* the textarea (right-aligned), fix the placeholder typo "customers" → "customer's". **Pick up (2026-10-17): canned suggestions to pick from → problem history.** Suggestions card: `suggestions` list (3 canned fixes for the green-pool example; pH first, then shock, then algaecide + backwash) → `selection = ui.radio(suggestions)`. **Decision (2026-10-17): an editable "Fix applied" box.** Picking a radio option copies its text into a `ui.textarea` labeled "Fix applied". The employee can save it as-is, edit it (e.g. a different dose), or ignore the suggestions and type their own, so the history logs what was *actually done*. A right-aligned **Save fix** button (`ui.row().classes('w-full justify-end')`). Phase 2: record whether the saved fix matched, edited, or ignored the AI suggestion. Those cases are the most valuable training data. **Suggestions card done (2026-10-17)**: `ui.radio(suggestions, on_change=lambda e: fix_box.set_value(e.value))`, `fix_box` textarea (outlined clearable), and Save Fix in a `justify-end` row. Learned: `.set_value()` (no `=` assignment allowed in a lambda), `clearable` is a `.props()` not a `.classes()`, `justify-*` goes on the parent row. **Next: problem history** (past problems: date, problem, fix applied) below the Suggestions card.
   - **Decision (2026-10-17, Claude's call at Mack's request): no scrolling for the essentials. Two-column Customer screen**, which supersedes the stacked Contact/Pool cards. Left column (~⅓, `w-1/3`): Contact + Pool cards, compacted with `ui.grid(columns=2)` label/value pairs on one line. Right column (`flex-1`): the tabs (the work area). Inside Problems: Log a Problem and Suggestions **side by side**, history underneath (only history lists may scroll). Outer row: `w-full no-wrap`, stacking on phones via `flex-col md:flex-row`. Rationale: who / what pool / what's wrong / what to do all visible at once at the counter; CRM-style record layout (HubSpot/Salesforce). Order: (1) two-column row **done 2026-10-17** (Claude did this restructure once at Mack's explicit request because it was pure block-moving; the default is still that Mack writes the code), (2) `ui.grid` compact cards: tried, then **reverted by Mack (2026-10-17): too compacted**. Keep the label-above-value stacking in the Contact/Pool cards (Mack prefers the spread-out look). The `ui.grid(columns='auto 1fr')` syntax was still learned. Page width: `max-w-8xl` isn't a real Tailwind class (named widths stop at `7xl`); use `max-w-screen-2xl` or no cap. **← next:** (3) side-by-side Problems cards, (4) problem history, (5) responsive `md:` stacking. Test history `ui.table` **done** (below the card; `columns` = `{'name','label','field'}` dicts, `rows` = dicts keyed by `field`). **Next:** then the contact info + pool section above the tabs; then the Problems and Purchases tabs.
   **Customer screen** (`/customer/{id}`): contact info, their **pools** (cards or a selector), equipment + gallons, and **tabs/panels** for **Water Tests** (latest + history, out-of-range values color-coded, New Test form, Print via the Windows print dialog), **Problems** (describe → canned AI suggestions → choose one → history), and **Purchases** (subsystem 3). Add Customer = a `ui.dialog` form (layout only).
   - Reminder: put icons on buttons with `icon='...'`; never assign `ui.icon = ...`, because that overwrites NiceGUI's function for every page.
7. **Settings screen** (named "Settings" in the app as of 2026-10-16: `pages/settings.py`, route `/settings`, renamed from the old `customers.py`; it's the "Maintenance" screen / subsystem 6 in the docs): lookup lists (products, manufacturers), the "Back Up Now" button, and possibly water-test ranges. Rarely used.
8. **Decision (2026-10-16): keep the ☰ drawer, slimmed down.** The logo (🏊 Pristine Pools) becomes the link to Home; Settings moves to a ⚙ icon button in the header's right group. The drawer then holds only **Recent customers + (later) chat history**, like ChatGPT's sidebar, and it stays the mobile menu spot. (Supersedes the nav buttons below.)
   Previously: Left drawer: Home / Settings nav + chat history / recent customers; highlight the active page. Drawer **starts closed** (`ui.left_drawer(value=False)`), and ☰ opens it.
- Three is the target, not a ceiling: Reports or a test-range Settings screen can be added later if Kara wants them.

### Phase 2: Make it work (later)
- **PostgreSQL** (see Architecture decisions; this replaces the earlier SQLite plan). All data code in `models.py` (pages never write SQL). `init_db()` with `CREATE TABLE IF NOT EXISTS`; CRUD functions (`add_/get_/update_/delete_customer`) with parameterized queries (never string-formatted SQL), commit on writes, `WHERE id = ...` on update/delete; return rows as dicts for `ui.table`. Never commit DB credentials or dumps (customer personal data).
- Swap placeholder rows for DB calls, wire buttons/dialogs/search, gallons calc, range checks in `rules.py`
- Extend DB to pools, water tests, problems, chemical purchases
- Ask AI via local Ollama

## Dev setup (per machine)
- `py -3.12 -m venv .venv`, then `.venv\Scripts\Activate.ps1`, then `pip install nicegui`
- In VS Code: Python: Select Interpreter, pick `.venv`
- Run: `python main.py`, open http://localhost:8080
- `.venv/` and `__pycache__/` are gitignored
- Laptop: only Python 3.13 is installed, so the venv there was made with `python -m venv .venv`. The first activation needed `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Optional: view the app in VS Code's Simple Browser (Ctrl+Shift+P, "Simple Browser: Show"). `ui.left_drawer` auto-hides when the window is narrow.

## Decisions
- **This semester (Fall 2026) = GUI only:** a semi-functional front end to present to the professor. Navigation, dialogs and forms work on hard-coded fake data. The AI shows canned answers. The real database and AI come in Spring 2027.
- **Mobile:** the GUI must *look* right on a phone (responsive layout, ☰ menu for the drawer). The app still runs on the store PC; no field or remote use.
- Everything employees need should be reachable from Home in 2–3 clicks (header action buttons that open a `ui.dialog`, plus search).
- **Chat-style layout (2026-10-12):** see build plan step 4.
- **Printing (decided in planning; recorded 2026-10-16): use the standard Windows print dialog. We are NOT building our own print screen.** A "Print Report" button on the Customer screen's Water Tests tab opens the browser's print, which shows the normal Windows print dialog (printer choice, copies, Save as PDF), using `ui.run_javascript('window.print()')`. What we **do** design is the *content*: a print-friendly customer handout (customer, pool, test date, each reading with its range and flag, recommended actions), shown on screen and hidden from the app's header/drawers when printing (CSS `@media print` / Tailwind `print:hidden`). Still to confirm with Kara: printed vs. PDF vs. email, and whether dosing amounts go on the handout (see Spec gaps).
- **Project files (cleaned up 2026-10-16):** `main.py`, `layout.py`, `pages/home.py`, `pages/customer.py`, `pages/settings.py`. `models.py` and `rules.py` stay empty until Phase 2. The unused `ask_ai.py`, `customer_detail.py` and `pool_detail.py` were removed (the AI lives on Home, and the pool lives on the Customer screen).

## Client & context
- **Client:** Kara Nominay, owner of Pristine Pools, a new above-ground pool store (not open yet; with no software, records would be on paper). She's non-technical, so the system must "just work" with no babysitting and no expert on site. She's budget-conscious about hardware and ongoing costs.
- **All client contact goes through Dr. James**, who will also install the system on the client's PC and train the client. Send client questions as **one organized list**.
- The store sells hard-sided (steel-wall) and soft-sided above-ground pools, plus chemicals and equipment. **No in-ground pools.**
- **Square** handles pricing, sales, and inventory. This system is **ancillary**: it records what Square doesn't, and links purchases to pool and water-test history, which Square can't.
- Store staff enter all data while talking with the customer in person. **Customers never use the system.** Design for employee efficiency (speed, few clicks), not customer learnability.
- New employees may lack pool-diagnosis experience, so the AI suggestions exist to help them.

## Subsystems (shared database)
1. **Customer Information Management:** name, address, phone.
2. **Pool & Equipment Management:** purchase/install dates, shape, size, manufacturer, model/serial, wall type & liner, floor type, filter, automatic chlorinator, installer. **Calculates total volume in gallons.**
3. **Chemical Purchase Tracking:** list of products carried; per-customer purchases (date, manufacturer, product, quantity, volume).
4. **Water Testing & Reporting:** record chemical panel results and dates, **flag values outside the client's recommended ranges**, print a customer report, show test history per pool.
5. **Problem Tracking & AI Suggestions:** record the problem and date reported, suggest solutions, record the chosen solution so there's a history of what was tried.
6. **Maintenance:** manage lookup lists (chemical products, manufacturers), edit recommended water-test ranges, back up and restore the database.

## Constraints
- Runs on **Windows**, on about **2–3 machines on the same local network**, with 1–2 concurrent users.
- **The AI must be self-trained or fine-tuned and run locally.** No hosted APIs (no Claude, no ChatGPT). It must be free to run.
- The recommendation feature must be real AI. **A rules-based expert system is ruled out.** Off-the-shelf CRM platforms are also ruled out.
- Limited ML experience so far. Favor approaches that are learnable and well-documented.
- Biggest risk: **training data** for the AI suggestions, and the client's PC hardware (GPU/RAM for a local model).

## Architecture (feasibility study compares three)
1. Web-based: Node.js / Express.js
2. .NET desktop application: C#
3. **NiceGUI (Python), the current lean**, paired with a locally run **Llama** model via Ollama and a **PostgreSQL** database. NiceGUI can run as a web app or as a native desktop window.

Final choice is not locked in. Confirm before assuming a stack.

An earlier draft compared five alternatives (also an ML.NET classifier, an Access split DB, and a joke "seagull" option), since narrowed to the three above.

**Feasibility study, nine objectives:** (1) language and platform, (2) desktop vs. web, (3) data storage, backup and recovery, (4) user interaction: data-entry screen layout and the printed customer report, (5) how the AI is provided and whether it can run locally with no ongoing cost, (6) hardware for the system and the AI (Appendix M), (7) system requirements and how each is tested, (8) failure scenarios and recovery, (9) how the project gets done by April 2027.

## Architecture decisions (from planning sessions)
### Database: PostgreSQL (not SQLite, MongoDB, or cloud)
- **SQLite dropped:** it's a single-file DB and unreliable with several machines writing at once.
- **PostgreSQL chosen:** free forever, handles concurrent connections from 2–3 machines cleanly, and runs on hardware the client is already buying, so no server purchase.
- **MongoDB rejected:** the data is strongly relational (customer → pools → tests / equipment / purchases / problems) with a fixed, known shape, and water tests are numeric data to query and trend. Relational + SQL fits.
- **Cloud DB rejected** (Supabase / Neon / AWS): it adds internet dependency (the store stops if the internet drops), recurring cost, and reliance on outside services. **Decision: everything local and self-contained.**

### Host discovery
- One desktop is the **host**: it runs PostgreSQL, holds the data, and hosts Ollama. The other machines are clients that run only the app.
- Clients find the host by **computer name**, not a hard-coded IP, so it works on any local network with no static-IP setup. That's preferred over router IP reservation or a manual static IP, which don't travel when the machine moves to the store.

### Backup: fully local, no cloud
- Automated nightly **`pg_dump`** via Windows Task Scheduler to an external USB drive. Staff never touch it, and there's no command line.
- A **"Back Up Now"** button on the Maintenance screen runs `pg_dump` behind the scenes.
- Under consideration: **PostgreSQL streaming replication**, where the second desktop keeps a live copy, so a dead host drive loses no data. It takes more setup up front but stays self-contained.
- On startup, if the app can't reach the DB, show a calm, plain-English message. **No silent auto-restore**, because a misread hiccup could overwrite good data.

### AI / inference
- Separate training from inference. **Train** on a high-powered machine (a full server rack is available), either a full fine-tune or the lighter **LoRA**. Then **quantize to 4-bit** and **run** on a generic CPU-only Windows box via Ollama.
- Sizing: target a **3B** model by default (~2–4 GB RAM at Q4). A 7–8B model is usable with 16 GB RAM but slower on CPU. Rule of thumb: ~0.6 GB RAM per billion parameters at Q4. No GPU needed for inference; aim for 16 GB RAM.
- Run **one** Ollama on the host, not one per machine.
- **Training data is make-or-break:** problem/solution pairs (symptom readings → correct action). Sources: client and staff expertise, published pool-care references, water-chemistry charts. A big model *may* help generate or format pairs during development (the constraint only applies to what ships). Have an expert verify the pairs.
- Strategy: ship a working app first, then layer the trained model in once the data is solid.

### Screens (from planning session): three, deliberately minimal for employee efficiency
1. **Home:** AI chat + chat history + a customer search bar with a dropdown of matches.
2. **Customer:** customer info, pools, equipment; water-test entry as a tab or panel; print via the standard Windows print dialog (not a separate screen).
3. **Maintenance:** lookup lists (products, manufacturers) + the backup button.
- Three is the target, **not a hard ceiling**. A Reports view or a Settings screen (test-range thresholds) may earn its own space later. Let Kara's reactions decide.
- Pitch framing: the edge over the other groups is polish and intent. Explain **why** three screens (employee efficiency), not how many.
- **Adopted into the build plan on 2026-10-15** (steps 5–8).

## Open questions
- Exact client PC specs (drives whether the local model is feasible). Biggest hardware risk.
- Whether past problem/solution records exist for training data. Biggest AI risk, since the store is brand new and historical records may not exist.
- Streaming replication vs. nightly dumps only.
- Login/roles: the spec mentions "authorized users" for Maintenance but doesn't define authentication.
- Protection of customer personal data.
- Final confirmation of the stack in the feasibility study.

## Spec gaps to confirm with the client (via Dr. James)
- Pool shapes beyond round/rectangular? How is depth entered? Can a customer own more than one pool?
- Should soft-sided pools carry liner info? What does "filtering volume" mean (GPM or sized volume)?
- Chemicals: store purchases vs. service-call usage? Track price and inventory, or only history?
- Water testing: export from a testing machine (e.g. LaMotte WaterLink), or typed in? Chlorine vs. bromine per pool? Dosing amounts on the report, or only flags? Printed, PDF, or email?
- AI: the most common problems and their usual fixes? Should it use test history + equipment, or just the description? Who picks the applied suggestion?
- Scope: any must-haves missing (scheduling, invoicing, reminders)? Opening timeline?
