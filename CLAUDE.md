# Pristine Pools — Record-Keeping & Water-Testing System

Capstone project (SVSU, CSIS). Developer: Mack. Target completion: **April 2027**.
Run by **Dr. Scott James** (also Mack's CIS 422 professor). Mack's group has 5 people and is competing against 2 other groups.

> **Sync ritual:** this file is the single source of truth, committed so context carries between Mack's desktop and laptop. Carry decisions made in chat/voice sessions into it. **Claude keeps it current without being asked** (mark steps done, move the ▶ marker, record decisions/preferences/answers) and keeps it **short**: replace finished history with one-line summaries instead of appending. **Claude commits or pushes only when Mack explicitly asks**; Mack does git himself to learn it.

## How Claude helps
- **Mack writes ALL the code.** Claude explains the concept, names the NiceGUI pieces and new syntax, Mack types it, Claude reviews. Full snippets only for brand-new syntax or when Mack is stuck and asks. Explain **why**, not just what.
- **If Mack asks Claude to "just write it" (usually when stressed), remind him of this rule and offer a smaller step first.** On 2026-10-21 Claude's written try-out was reverted at his request.
- Claude MAY write: **sample/placeholder data** (realistic pool-store data, 555-01xx phones), pure block-moving restructures when asked, docs, and restoring files Claude broke.
- **Be stern and real** (Mack's ask, 2026-10-24): blunt, no sugarcoating; call out stalling, sloppy code and schedule slips.
- One concept per step; Mack commits small steps. Concise, structured answers; skip basics (running, saving, VS Code clicks).
- **Decisions go in the question popup (AskUserQuestion)**, never buried in a reply.
- Check the files before claiming what's done (Mack also works on his laptop).

## ▶ Current status & PICK UP HERE (2026-10-23)
**⏰ Whole GUI due Tue 2026-10-27, 8:30.** This semester = a GUI that behaves live on fake in-memory data (`store.py`); PostgreSQL + real AI in Spring 2027. Step A done; Friday lost to work, so Sat–Mon are packed (see schedule).

**Step A is ✅ done** (late Thu 10/22 → Fri 10/23 session): Log a Problem fix, "No past problems", Purchases per customer + "No purchases yet", `CUSTOMERS` removed, unknown-customer guard, readable badge colors, `?tab=problems` (`tab: str = ''` → `ui.tab_panels(value=...)`). Mack now works one git branch per step (`git switch -c <step>` → commit → push → switch main → pull → merge → push).

**Next up (Sun 10/25): 0e step 4 keyboard polish (autofocus FC, Enter saves via `.on('keydown.enter', save_test)` → def must move above the grid, `min=0, step=0.1`) → step 5 `@ui.refreshable` drawer** → rest of Sunday's list. 0e steps 1–3 ✅ (branch `test-dialog-refactor`): `inputs` dict built in a loop, `save_test` (blank guard with `all()`, plain test → `c['tests']`, colored copy → `table.rows` + `table.update()`, `latest.set_text`, reset boxes), retest rule (clear, red → +2, orange → +7 via `in` + `elif`). ✅ Chemistry done. ✅ 0d `schedule_retest(days, reason)` (tested: save + reschedule overwrite) (branch `retest-dialog`): nested in `customer()` (sees `c`), dialog built on demand, `ui.date` ISO string in/out (`isoformat` / `date.fromisoformat`), Skip / Schedule → `c['retest']`. (`drawer-badge` ✅ merged.) 0c ✅ done: ☰ red `attention_count` badge (`floating`, hidden at 0) + drawer title row (red icon + `text-lg` title, quiet grey caps section labels). Earlier in 0c (branch `drawer-finish`, 2026-10-24 ~2am): drawer + ☰ toggle, Retests due (sorted, Overdue red + phone / Today / unpadded date), Open problems (links `?tab=problems`), empty stub pages removed. `@ui.refreshable` waits for 0e. Drawer links: Retests due → `/customer/{id}`, Open problems → `/customer/{id}?tab=problems`.

**Day-by-day schedule (re-planned 2026-10-23: Mack works Fri 11am–11pm, so Friday is lost; Mack chose to keep ALL items, no cuts). Within each day, do items in the order listed so anything unfinished is the least important:**
- **Sat 10/24 (re-planned: only the morning, Mack works at 1pm):** finish 0c drawer → 0d `schedule_retest`.
- **Sun 10/25 (free, but chemistry due Sunday: do it FIRST):** chemistry → 0e `save_test` → C retest chip → D Log Purchase saves → 0f Save Fix → B New Customer → E edit records (Contact ✏️ first, then pool/hot tub edit + add, then change history).
- **Mon 10/26 (lots of time):** F Settings (Products + Backup first, Ranges tab last) → G Home chat → "What's off" strip → H phone pass + critique #5 polish → I demo run-through + merge to `main` (PM). **Claude reminds Mack:** `/impeccable critique` + `adapt` on Customer before H (findings only); `/impeccable audit` + `clarify` + `/code-review` before I. Sat if time: `/impeccable onboard` (findings only) on empty states.
- **Tue 10/27 before 8:30:** buffer; finish only what's half-done, no new features.
- **If Sunday night shows we're behind:** fall back to the cut list below (Mack decides; ask via popup).

## Master plan to the deadline (made 2026-10-21; all items are must-haves)
- **A. Data foundation** (Thu 10/22). ✅ `rules.py` (`BANDS`, `color_for`, `test_colors` with blank guard + rounded TC rule). ✅ `store.py` sample data (Claude) + `search_options()` (Mack) feeding the header search. ✅ Contact card, Pool card (Pool vs Hot tub fields, "No pool on file"), Water Tests table (`rows = [{**t, **rules.test_colors(t)} for t in c['tests']]`, "No tests yet"), Problem history (skips open ones), open problem found (`open_p` loop + `break`) → orange "Open · logged …" badge + pre-filled textarea. ⬜ Purchases per customer, cleanups (see above). Later in A: drawer links to `/customer/{id}?tab=problems` (page opens on Problems; query param `tab: str = ''`); New Test ignores an all-blank save.
- **0c–0f. Live ☰ "needs attention" drawer + retests** (Mack builds; Claude's version was reverted):
  - 0c `ui.left_drawer(value=False).props('overlay bordered')` created **before** the header (so ☰ can use `drawer.toggle`); ☰ at the header's far left with a red `floating` count badge (hidden at 0); lists **Retests due** (sorted by date, "Overdue" red + phone line to call, "Today") and **Open problems**; rows → the customer page. `@ui.refreshable` lists + badge so saves update them live.
  - 0d `schedule_retest(cid, days, reason)`: a dialog built on demand with `ui.date` pre-filled to today + days (`timedelta`), Skip / Schedule.
  - 0e New Test `save_test()`: readings in a dict, colors from `test_colors`, new row on top, any saved test clears the due retest; red → retest +2 days, orange only → +7. Keyboard-first: `autofocus` on FC, Enter saves, `ui.number` `min=0`/`step=0.1`. Date strings without a zero pad (`Oct 5, 2026`, not `%d` → `Oct 05`): `f"{d:%b} {d.day}, {d.year}"`.
  - 0f Problems: picking a suggestion must not wipe typed "Fix applied" text (append/confirm). Get Suggestion → open problem; Save Fix → fills `fix`, moves it to history, offers a retest (+2).
  - Rules: one retest per customer (`c['retest']` or None); a problem is open while `fix is None`.
- **B. New Customer** (Fri 10/23, `layout.py`): dialog: Name (`autofocus`, required), Phone, Address, optional first body (`ui.toggle(['Pool','Hot tub'])` + `ui.grid(columns=2)`); Save → add to `store.customers` → `search.set_options(...)` → navigate to the new page.
- **C. Retest chip** in the Customer title row: "Retest due Oct 23" (red if overdue) / "No retest" → `schedule_retest` + Clear; `@ui.refreshable`.
- **D. Log Purchase saves:** brand/size from `store.products` (lookup dict `{p['name']: p for p in store.products}`); give the select/date/qty variables. ⚠ The table **shares** the `c['purchases']` list, so don't append AND `add_row` (doubles it): `c['purchases'].insert(0, row)` (newest on top) then `table.update()`. Same unpadded date format as 0e. "No purchases yet" must hide after a save (`set_visibility` or refreshable). If F12 shows duplicate-key warnings: rows need a unique `id` + `row_key=` (tests table too).
- **E. Edit records** (Sat 10/24): Contact ✏️ dialog (`.set_text` updates); Pool card `ui.toggle` between bodies, ✏️ Edit / ➕ Add pool or hot tub (fields depend on type); edits overwrite + append a change line ("Oct 24, 2026 · Filter: Sand → Cartridge") shown in `ui.expansion('Change history')`; New Test "For" select when >1 body. No delete (ask Kara: archive vs delete).
- **F. Settings** (Sun 10/25 AM, `pages/settings.py`): title "Settings" (remove the stray button); tabs Products (`store.products` + Add dialog; Log Purchase reads it), Water-test ranges (read-only from `rules.BANDS`), Backup (last-backup label, Back Up Now updates it, flat Restore).
- **G. Home chat** (Sun PM, `pages/home.py`): chips post their text + `show_chat`; Send/Enter posts `chat.value` + a canned answer (`ui.markdown` numbered steps inside `with ui.chat_message(...)`); assistant `avatar=`; + → attach-customer dialog → removable chip above the bar.
- **H. Phone pass** (Mon 10/26 AM): critique #5 polish: `no-caps` on tabs/buttons, tooltip on the Print icon, Log Purchase date → `ui.date` in a menu; `flex-col md:flex-row` on two-column rows, `w-full md:w-1/3`, search `w-full md:w-96`, New Customer icon-only on phones.
- **I. Demo run-through + merge to `main`** (Mon PM): ☰ overdue → search → Customer → retest chip → New Test (flagged) → Problems → Save Fix → Log Purchase → edit phone → add hot tub → Print → New Customer → Home chip + send → Settings.
- **If behind, cut in this order:** + attach → change-history expansion → Ranges tab → New Test "For" select → if-time items (tab-panel `pt-0` nit, "Log these products?" shortcut after Save Fix, theme color pick).
- Check every step: full width, 1920×1080, phone view, F12 Console clean, Customer print still fits 1 page.

## What's built (summary)
- **Files:** `main.py` (imports pages, `ui.run()`), `layout.py` (`page_layout()`: theme, header with logo→Home link, center `ui.select` customer search, New Customer + ⚙ buttons; print CSS), `pages/home.py`, `pages/customer.py`, `pages/settings.py` (stub), `store.py`, `rules.py`. `models.py` empty until Phase 2.
- **`store.py` (Claude's sample data):** `TODAY`; `products` (15: name/brand/size); `customers` (16) with name/phone/address/since/bodies/tests/problems/purchases/retest. Display dates are strings; `retest['due']` is a real `date` relative to `TODAY` (overdue: Nick, Jake; today: Marcelino, Mike; tomorrow: Jessica). Open problems: Dave (hot tub foam), Chris (algae), Ryan (liner stains). Hot tubs: Manish + Linda (2nd body), Dave (only body; fields `shell`/`cover`). Empty: Emily (no tests), Megan (no bodies). `test['body']` = index into `bodies`. `search_options()` → `{id: 'Name · phone'}`.
- **Home:** welcome screen (greeting + subtitle + 4 outline chips, vertically centered `min-h-[calc(100vh-10rem)]`), canned chat messages hidden until `show_chat()` (send + chips), Claude.ai-style chat bar in `ui.footer` (`bg-slate-100`, input with +/send slots). Staff bubble `bg-color=primary text-color=white`.
- **Customer** (`/customer/{customer_id}`): tabs in the title row; two-column row (left `w-1/3` Contact + Pool cards, right tabs column `md:[contain:size] md:overflow-y-auto`, row `md:min-h-[calc(100vh-11.5rem)]`). **Water Tests:** latest-test card (Print + New Test dialog), table with every reading colored via a `body-cell` slot reading `<field>_color` keys. **Problems:** Log a Problem (`w-1/3`) + Fix card (`flex-1`; hidden suggestions radio → copies into editable "Fix applied" textarea; Save Fix), history list scrolls inside. **Purchases:** table + Log Purchase dialog (product select, date, qty). **Print:** `window.print()`, header/tabs `print:hidden`, cards side by side on paper, fits 1 page.

## UI rules & standing decisions
- **Counter workflow:** customer walks in with a sample → search → Customer screen → test → flags → problem / AI help → print. Keyboard-first, smart defaults (today's date), quick adds in `ui.dialog`s. Staff use it; customers never do.
- **Three screens** (Home = AI chat, Customer, Settings/"Maintenance"); not a hard ceiling. Pitch: polish + intent; explain *why* three screens.
- **Home stays SUPER SIMPLE** (greeting, subtitle, 4 chips, chat bar). Declined: dashboard cards/tiles (Nick's and teammates' ideas) since every action starts with a customer, so search *is* the shortcut. Don't suggest Home widgets again. "Needs attention" lives in the ☰ drawer instead. Chat history dropped.
- **No page scrolling on desktop; scrolling inside a card/column is fine.** No stretched white-space filler (cards at natural height). Target 1920×1080; laptop ~1536×740.
- **Light mode.** Themes `pool`/`aqua`/`ocean` in `THEMES`; color pick deferred to Kara.
- **No `ui.notify` toasts** as placeholders (Mack dislikes them).
- **Readings colored in the table** (green OK / orange watch / red act), not a badge row. Drawn as solid `-9` shade badges on every reading (orange gets black text) for WCAG contrast; decided 2026-10-23 to keep badges on all readings (not only flagged ones). `rules.py` keeps the plain color words (meanings). Placeholder bands (Kara's real ranges TBD; hot tubs use pool bands for now):

| Reading | green | orange | red |
|---|---|---|---|
| FC / TC | 1–3 | 0.6–0.9 or 3.1–5 (TC also if TC−FC ≥ 0.5) | <0.6 or >5 |
| pH | 7.4–7.6 | 7.2–7.3 / 7.7–7.8 | <7.2 or >7.8 |
| Alk | 80–120 | 60–79 / 121–150 | <60 or >150 |
| Hardness | 200–400 | 150–199 / 401–500 | <150 or >500 |
| CYA | 30–50 | 20–29 / 51–80 | <20 or >80 |
| Phos (ppb) | ≤100 | 101–300 | >300 |

- **Problems:** staff can save a fix without asking for suggestions; the saved fix is what was *actually done* (Phase 2: record matched/edited/ignored AI suggestion = training data). Bodies of water = Pool or Hot tub; equipment edits keep a change log.
- **Purchases:** Square already rings sales; plan a "Log these products?" shortcut after Save Fix (if time); Phase 2 idea: Square CSV import.
- **Printing:** the standard Windows print dialog via `window.print()`; we design the handout content only.
- **Mobile:** must look right on a phone; still runs on the store PC.
- **☰ badge (2026-10-25):** counts retests due **today or overdue** + open problems. Future retests still list in the drawer with their date but don't count.
- **Code style (2026-10-25):** click handlers (`schedule_retest`, `save_test`, later `save_purchase`, `save_fix`…) live **next to the dialog that uses them** (e.g. `save_test` right after the New Test grid, before the button row, at the same indent as `with ui.grid`; `schedule_retest` stays near the top since several places call it). Never put a `def` between a `with` line and its body. They must be defined before the button that passes them (`on_click=name`); names *inside* them are looked up at click time.

## Concepts Mack has learned
`with` nesting (siblings vs children) · `.classes()` (Tailwind) vs `.props()` (Quasar; Tailwind in props is silently ignored) · `flex-1`, `w-full`, `min-h-0`, `justify-*` (along) vs `items-*` (across), `md:`/`print:` prefixes · slots (`add_slot` returns the slot) · `ui.list`/`ui.item` · `ui.select` events (`e.value`) · f-strings · conditional expressions · dicts, nested dicts, `**` unpacking, tuples + unpacking · `for` loops, `break`, `continue`, `is None` · `.split()` · `set_value` / `set_visibility` · `def` vs lambda, late binding (`lambda cid=cid:`) · dialogs · tables + `body-cell` Vue slot (no `#` comments inside template strings; check F12 Console) · `.items()`, comprehensions with `if` filters, `.get()`, `and` short-circuit, float rounding · `import store` (`store.x`) vs `from store import x` · git branches, merge conflicts, `git merge X` merges into the current branch, reverting.

## Dev setup (per machine)
- `py -3.12 -m venv .venv` → `.venv\Scripts\Activate.ps1` → `pip install nicegui`; select the `.venv` interpreter in VS Code.
- Run `python main.py` → http://localhost:8080. Always launch from `main.py` (a page file alone gives `No module named 'layout'`).
- **Which machine?** Claude runs `hostname` at the start: laptop = `MacksWaterFountain`, desktop = `Mack`.
- Laptop: Python 3.13 only (`python -m venv .venv`; needed `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`).
- **Impeccable** design skill (global, installed 2026-10-23 on desktop): from `~` run `npx --yes impeccable install --providers=claude --scope=global` (`/plugin` doesn't work in the VS Code panel). Use for **review/suggestions only** (H/I polish); Mack still writes the code.
- Short terminal prompt (per machine, done on desktop 2026-10-25): `$PROFILE` defines `function prompt` showing `folder (branch)> ` via `Split-Path -Leaf (Get-Location)` + `git branch --show-current`.
- Windows console shows `·` as `�` (display only). Never assign `ui.icon = ...`; use `icon='...'` on buttons.

## Phase 2 (Spring 2027)
- **PostgreSQL**; all data code in `models.py` (pages never write SQL), parameterized queries, rows as dicts. Never commit credentials or dumps.
- Swap `store.py` for DB calls; ranges from Settings; gallons calc; local AI via Ollama.

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
- **Backup:** nightly `pg_dump` (Task Scheduler) to a USB drive + a Back Up Now button; maybe streaming replication. If the DB is unreachable, show a calm message; **no silent auto-restore**.
- **AI:** train on a powerful machine (full fine-tune or LoRA), quantize to 4-bit, run CPU-only via one Ollama on the host. Target ~3B (~2–4 GB RAM); 7–8B possible with 16 GB. Training data = expert-verified problem/solution pairs. Ship the app first, then layer in the model.

## Open questions
- Client PC specs (local model feasibility). Whether past problem/solution records exist. Streaming replication vs nightly dumps. Login/roles for Maintenance. Customer data protection. Final stack confirmation.

## Spec gaps to confirm with Kara (via Dr. James)
- **Hot tubs:** does she service them? Which fields matter? Separate ranges / bromine? Delete vs archive old customers and pools?
- Pool shapes beyond round/rectangular? Depth entry? Multiple pools per customer?
- Liner info for soft-sided? "Filtering volume" = GPM or sized volume?
- Chemicals: store purchases vs service usage? Price/inventory or history only?
- Water testing: machine export (e.g. LaMotte WaterLink) or typed? Chlorine vs bromine? Dosing on the report? Printed, PDF, or email?
- AI: common problems + usual fixes? Use test history + equipment or just the description? Who picks the applied suggestion?
- Missing must-haves (scheduling, invoicing, reminders)? Opening timeline?
