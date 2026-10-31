# Pristine Pools — Record-Keeping & Water-Testing System

SVSU CSIS capstone (CIS 422), run by **Dr. Scott James**. Team project, competing against 2 other groups. Target completion: **April 2027**.

> **Shared file:** this is the team's single source of truth, committed so context carries across everyone's machines. Keep it about the project (status, decisions, rules); personal preferences go in your own gitignored `CLAUDE.local.md`. **Claude keeps it current without being asked** (mark steps done, update status, record decisions) and keeps it **short**: replace finished history with one-line summaries instead of appending. **Claude commits or pushes only when explicitly asked.**

## Working with Claude
- Check the files before claiming what's done (people work on different machines and branches).
- Decisions go in the question popup (AskUserQuestion), not buried in a reply.
- One concept/step at a time; small commits, one git branch per step (`git switch -c <step>` → commit → push → PR to `main`).
- Claude may write sample/placeholder data (realistic pool-store data, 555-01xx phones) and docs.

## ▶ Current status (2026-10-30)
**Phase 1 (Fall 2026):** a GUI that behaves live on fake in-memory data (`store.py`). PostgreSQL + real AI come in Spring 2027.

**In progress, branch `edit_pool_dialog`:** Edit Pool dialog saves: pool Shape toggle + Length/Width/Wall numbers, live `recalc_gallons` via `on_value_change`, Gallons box editable for both types, `validation=` blocks blanks, `size` text rebuilt on save. Add Pool title, `DARK_MODE = False`, Save label done.
✅ Edit Pool dialog is now built on demand by `open_edit_pool(i)` (✏️ → `lambda: open_edit_pool(0)`), so Cancel discards edits.
**Next:**
1. Multiple bodies (own branch, after `edit_pool_dialog` merges). Steps: 2a card fields → `@ui.refreshable pool_details(i)` (defined before the card, called in its `else:`) → 2b toggle → 2c ✏️ uses selected → 2d title. Pool card `ui.toggle` between bodies (only when >1), card body `@ui.refreshable` by index, ✏️ edits the selected body, card title from the selected body. Then Add Pool reuses `open_edit_pool` with blank boxes.
2. Same Cancel bug in Edit Customer (built once at page load). Also: `refresh_attention()` in `schedule_retest` runs at build time, not in `save()`, so the drawer doesn't update after scheduling.
3. Refreshable Pool card instead of a page reload (deferrable).
4. Then: "What's off" strip → H phone pass → I demo run-through.

**Tests** (pytest + NiceGUI `user` fixture; pending PR, not yet in `main`): `pip install -r requirements.txt` then `pytest`. GitHub Actions runs them on PRs to main (job `test`); ruleset `protect-main` requires a PR + 1 approval. In tests always `import rules`, never `from rules import test_colors` (pytest would collect it as a test).

## Done so far
- **A. Data foundation:** `rules.py` (`BANDS`, `color_for`, `test_colors`), `store.py` sample data + `search_options()`, Contact/Pool cards, Water Tests table, Problem history, open-problem badge, Purchases per customer, empty states, `?tab=problems`.
- **0c–0f. ☰ Needs-attention drawer + retests:** left drawer with red count badge, Retests due + Open problems (live via `@ui.refreshable`), `schedule_retest(days, reason)` dialog, New Test `save_test()` (colors, retest rule, keyboard-first), Save Fix.
- **B. New Customer** dialog (Name + Phone required; Address + Zip saved as `"addr, zip"`) → `store.customers` → search options → navigate.
- **D. Log Purchase** saves (`save_purchase`).
- **F. Settings:** Products + Add Product, Backup (status + Restore… only), Water-test ranges table from `rules.BANDS`.
- **G. AI right drawer** opened by a ✨ fab (`ui.page_sticky` + `z-50`), canned replies; `/` is a "Find a customer" landing.
- **E (partial):** ✏️ on Contact + ✏️/➕ on Pool card title rows; Edit/Add Pool dialog (in progress above).

## Remaining plan
- **E. Edit records:** Contact ✏️ dialog (`.set_text` updates); Pool card `ui.toggle` between bodies; edits just overwrite (no change log, decided 2026-10-31; the client spec lists one, so revisit with Kara); New Test "For" select when >1 body. No delete (ask Kara: archive vs delete).
- **C. Retest chip** in the Customer title row: "Retest due Oct 23" (red if overdue) / "No retest" → `schedule_retest` + Clear.
- **H. Phone pass + polish:** `no-caps` on tabs/buttons, tooltip on Print, Log Purchase date → `ui.date` in a menu, `flex-col md:flex-row` on two-column rows, `w-full md:w-1/3`, search `w-full md:w-96`, New Customer icon-only on phones. Run `/impeccable critique` + `adapt` on Customer first (findings only).
- **I. Demo run-through:** ☰ overdue → search → Customer → retest chip → New Test (flagged) → Problems → Save Fix → Log Purchase → edit phone → add hot tub → Print → New Customer → AI drawer send → Settings. Run `/impeccable audit` + `clarify` + `/code-review` first.
- **If behind, cut in this order:** + attach → C retest chip → New Test "For" select → if-time items (tab-panel `pt-0` nit, "Log these products?" after Save Fix, theme color pick).
- **Backlog (from design critique):** aria-labels, badge red-9, header search `dark` prop, no-match → New Customer, Send posts typed text.
- **Check every step:** full width, 1920×1080, phone view, F12 Console clean, Customer print still fits 1 page.

## What's built
- **Files:** `main.py` (imports pages, `ui.run()`), `layout.py` (`page_layout()`: theme, ☰ left drawer, header with logo→Home, center `ui.select` customer search, New Customer + ⚙ buttons, ✨ AI right drawer, print CSS; returns `refresh_attention`), `pages/home.py` (`/` landing), `pages/customer.py`, `pages/settings.py`, `store.py`, `rules.py`. `models.py` empty until Phase 2.
- **`store.py`:** `TODAY`; `products` (15: name/brand/size); `customers` (16) with name/phone/address/since/bodies/tests/problems/purchases/retest. Display dates are strings; `retest['due']` is a real `date` relative to `TODAY` (overdue: Nick, Jake; today: Marcelino, Mike; tomorrow: Jessica). Open problems: Dave (hot tub foam), Chris (algae), Ryan (liner stains). Hot tubs: Manish + Linda (2nd body), Dave (only body; fields `shell`/`cover`). Empty: Emily (no tests), Megan (no bodies). `test['body']` = index into `bodies`. Pools have `shape` ('Round'/'Oval'), `length`, `width` (ft; round → width = length), `wall` (in); gallons = `length × width × wall/12 × 5.9`, rounded to 100. Hot tubs keep typed gallons. `search_options()` → `{id: 'Name · phone'}`.
- **Customer** (`/customer/{customer_id}`): tabs in the title row; left column `w-1/3` Contact + Pool cards (natural height; title buttons `size=sm` + `-my-1`), right tabs column `md:[contain:size] md:overflow-y-auto`. **Water Tests:** latest-test card (Print + New Test), table colored via a `body-cell` slot reading `<field>_color` keys. **Problems:** Log a Problem + Fix card (suggestions radio → editable "Fix applied"; Save Fix), history scrolls inside. **Purchases:** table + Log Purchase dialog. **Print:** `window.print()`, header/tabs `print:hidden`, fits 1 page.

## UI rules & standing decisions
- **Counter workflow:** customer walks in with a sample → search → Customer screen → test → flags → problem / AI help → print. Keyboard-first, smart defaults (today's date), quick adds in `ui.dialog`s. Staff use it; customers never do.
- **Screens:** Customer is the main screen; Settings stays a full page (wide tables, rare admin work); `/` is a simple find-a-customer landing; AI chat is a right drawer available everywhere.
- **AI drawer stays super simple** (greeting, subtitle, chat input; no chips, no chat history). No dashboard cards/tiles on Home: every action starts with a customer, so search *is* the shortcut. "Needs attention" lives in the ☰ drawer.
- **☰ badge** counts retests due today or overdue + open problems. Future retests list with their date but don't count.
- **Retest rules:** one retest per customer (`c['retest']` or None); any saved test clears it; red → +2 days, orange only → +7. A problem is open while `fix is None`.
- **Dates** without zero pad: `f"{d:%b} {d.day}, {d.year}"` → `Oct 5, 2026`.
- **No page scrolling on desktop**; scrolling inside a card/column is fine. No stretched white-space filler. Target 1920×1080; laptop ~1536×740.
- **Light mode** for the client (`DARK_MODE = False` in `layout.py` for demos/printing). Themes `pool`/`aqua`/`ocean` in `THEMES`; color pick deferred to Kara.
- **No `ui.notify` toasts** as placeholders.
- **Readings colored in the table** (green OK / orange watch / red act) as solid `-9` shade badges on every reading (orange gets black text) for WCAG contrast. `rules.py` keeps the plain color words. Placeholder bands (Kara's real ranges TBD; hot tubs use pool bands for now):

| Reading | green | orange | red |
|---|---|---|---|
| FC / TC | 1–3 | 0.6–0.9 or 3.1–5 (TC also if TC−FC ≥ 0.5) | <0.6 or >5 |
| pH | 7.4–7.6 | 7.2–7.3 / 7.7–7.8 | <7.2 or >7.8 |
| Alk | 80–120 | 60–79 / 121–150 | <60 or >150 |
| Hardness | 200–400 | 150–199 / 401–500 | <150 or >500 |
| CYA | 30–50 | 20–29 / 51–80 | <20 or >80 |
| Phos (ppb) | ≤100 | 101–300 | >300 |

- **Problems:** staff can save a fix without asking for suggestions; the saved fix is what was *actually done* (Phase 2: record matched/edited/ignored AI suggestion = training data). Bodies of water = Pool or Hot tub; equipment edits overwrite the old values (no change log for now).
- **Purchases:** Square already rings sales; "Log these products?" shortcut after Save Fix if time; Phase 2 idea: Square CSV import.
- **Backups** are automatic (nightly to USB); Settings shows status + Restore… only, no Back Up Now.
- **Printing:** standard Windows print dialog via `window.print()`; we design the handout content only.
- **Mobile:** must look right on a phone; still runs on the store PC.

## Code style & gotchas
- Click handlers (`save_test`, `save_purchase`, `save_fix`…) live **next to the dialog that uses them**, defined before the button that passes them (`on_click=name`). `schedule_retest` stays near the top since several places call it. Never put a `def` between a `with` line and its body.
- NiceGUI 3.x `ui.table` **copies** `rows`, so insert into BOTH the data list and `table.rows` (newest on top with `.insert(0, row)`), then `table.update()`. Duplicate-key warnings in F12 → rows need a unique `id` + `row_key=`.
- No `#` comments inside Vue template strings (`body-cell` slots); check the F12 Console.
- `.classes()` is Tailwind, `.props()` is Quasar (Tailwind in props is silently ignored).
- `ui.page_sticky` needs `z-50` or the Customer tab panel covers the fab.
- Never assign `ui.icon = ...`; use `icon='...'` on buttons. Windows console shows `·` as `�` (display only).

## Dev setup
- `py -3.12 -m venv .venv` → `.venv\Scripts\Activate.ps1` → `pip install nicegui`; select the `.venv` interpreter in VS Code. (Python 3.13 also works; may need `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.)
- Run `python main.py` → http://localhost:8080. Always launch from `main.py` (a page file alone gives `No module named 'layout'`).
- **Impeccable** design skill (optional): from `~` run `npx --yes impeccable install --providers=claude --scope=global`. Use for review/suggestions.
- `main` history was rewritten on 2026-10-29; if your local main predates that: `git fetch` + `git reset --hard origin/main`.

## Phase 2 (Spring 2027)
- **PostgreSQL**; all data code in `models.py` (pages never write SQL), parameterized queries, rows as dicts. Never commit credentials or dumps.
- Swap `store.py` for DB calls; ranges editable from Settings; local AI via Ollama.

## Client & context
- **Client:** Kara Nominay, owner of Pristine Pools, a new above-ground pool store (not open yet). Non-technical: it must "just work". Budget-conscious.
- **All client contact goes through Dr. James** (he'll also install and train). Send questions as **one organized list**.
- Sells hard-sided and soft-sided above-ground pools, chemicals, equipment. **No in-ground pools.**
- **Square** handles pricing/sales/inventory; this system is **ancillary** (links purchases to pool and test history).
- Staff enter everything while talking to the customer; design for speed. New employees may lack diagnosis experience, hence the AI.

## Subsystems (shared database)
1. **Customers:** name, address, phone.
2. **Pools & equipment** (several bodies of water per customer, Pool or Hot tub; change log): install dates, shape, size, manufacturer, model/serial, wall/liner, floor, filter, chlorinator, installer; **calculates gallons**.
3. **Chemical purchases:** product list; per-customer purchases (date, manufacturer, product, qty, volume).
4. **Water testing:** results + dates, **flag out-of-range values**, print a report, history per pool.
5. **Problems + AI suggestions:** problem + date, suggestions, the chosen fix (history of what was tried).
6. **Maintenance/Settings:** lookup lists, edit test ranges, backup/restore.

## Constraints
- Windows, 2–3 machines on one LAN, 1–2 concurrent users.
- **AI must be self-trained/fine-tuned, local, free to run.** No hosted APIs. Must be real AI (no rules-based expert system); no off-the-shelf CRM.
- Limited ML experience: favor learnable, well-documented approaches.
- Biggest risks: **training data**, and the client PC's hardware.

## Architecture
- Feasibility study compares: (1) Node.js/Express web, (2) C# .NET desktop, (3) **NiceGUI + local Llama via Ollama + PostgreSQL (current lean, not locked in; confirm before assuming)**. Nine objectives: language/platform, desktop vs web, storage/backup, UI + printed report, local AI at no cost, hardware (Appendix M), requirements + tests, failure/recovery, schedule to April 2027.
- **PostgreSQL** (not SQLite: multi-machine writes; not MongoDB: relational, numeric data; not cloud: internet dependency + cost). Everything local.
- **Host:** one desktop runs PostgreSQL + Ollama; clients find it by **computer name**, not IP.
- **Backup:** nightly `pg_dump` (Task Scheduler) to a USB drive; maybe streaming replication. If the DB is unreachable, show a calm message; **no silent auto-restore**.
- **AI:** train on a powerful machine (full fine-tune or LoRA), quantize to 4-bit, run CPU-only via one Ollama on the host. Target ~3B (~2–4 GB RAM); 7–8B possible with 16 GB. Training data = expert-verified problem/solution pairs. Ship the app first, then layer in the model.

## Open questions
- Client PC specs (local model feasibility). Whether past problem/solution records exist. Streaming replication vs nightly dumps. Login/roles for Maintenance. Customer data protection. Final stack confirmation.

## Spec gaps to confirm with Kara (via Dr. James)
- **Hot tubs:** does she service them? Which fields matter? Separate ranges / bromine? Delete vs archive old customers and pools?
- Pool shapes beyond round/oval? Depth entry? Multiple pools per customer?
- Liner info for soft-sided? "Filtering volume" = GPM or sized volume?
- Chemicals: store purchases vs service usage? Price/inventory or history only?
- Water testing: machine export (e.g. LaMotte WaterLink) or typed? Chlorine vs bromine? Dosing on the report? Printed, PDF, or email?
- AI: common problems + usual fixes? Use test history + equipment or just the description? Who picks the applied suggestion?
- Missing must-haves (scheduling, invoicing, reminders)? Opening timeline?
