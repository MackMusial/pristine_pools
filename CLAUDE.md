# Pristine Pools — Record-Keeping & Water-Testing System

A record-keeping and water-testing system for Pristine Pools, a new above-ground pool store. Built as an SVSU CSIS capstone (CIS 422) run by Dr. Scott James, with a target completion of April 2027.

## The client
Pristine Pools sells hard-sided and soft-sided above-ground pools, chemicals, and equipment. The owner, Kara Nominay, is non-technical and budget-conscious, so the system has to just work. All client contact goes through Dr. James.

Square handles pricing, sales, and inventory. This system sits alongside it and links purchases to each customer's pool and water-test history.

## How it's used
A customer brings a water sample to the counter. Staff find the customer, enter the test, see which readings are out of range, get help diagnosing any problem, and print a report. Staff use the system while talking to the customer, so it's designed for speed. Newer employees may lack diagnosis experience, which is why it includes AI suggestions.

**Next:**
1. **Multiple bodies (Max, branch `multiple_pools_dropdown`):** the branch is an unfinished start; merge `main` first (`pages/customer.py` conflicts). Known issues: `search_pools()` isn't per customer and collapses bodies of the same type; a customer with one hot tub gets the title "Pool". Plan steps: 2a card fields → `@ui.refreshable pool_details(i)` (defined before the card, called in its `else:`) → 2b dropdown → 2c ✏️ uses selected (`open_edit_pool(i)`) → 2d title. The selector is a dropdown (Max is building it, no ETA yet). Then Add Pool reuses `open_edit_pool` with blank boxes.
2. `refresh_attention()` in `schedule_retest` runs when the dialog is built, not in `save()`, so the drawer doesn't update after scheduling.
3. Refreshable Pool card instead of a page reload (deferrable).
4. Then: "What's off" strip → H polish → I demo run-through.

**Tests** (pytest + NiceGUI `user` fixture; in `main` since PR #2): `pip install -r requirements.txt` then `pytest`. GitHub Actions runs them on PRs to main (job `test`); ruleset `protect-main` requires a PR + 1 approval. In tests always `import rules`, never `from rules import test_colors` (pytest would collect it as a test).

**In progress (2026-11-04), branch `refactor_edit_pool_dialog`:** Edit Pool now uses Max's layout and loads every field; all 14 sample pools have the new keys (`floor_options`, `wall_type_options` in `store.py`). PR #7 (drawer fix + status notes) still needs a review.
- **Left in `open_edit_pool`:** fix `'Rectagle'` typo → hide ✏️ for hot tubs + hot tub TODO → `on_value_change` loop + Rectangle factor (7.5) + `Required` on Length/Width/Wall Height/Volume → `edit_pool`: Width required unless Round, delete old box lines + hot tub branches, `fields` dict + loop, rebuild `wall_liner`/`filter`/`chlorinator`/`installed` for the card → click through → tests (✏️ opens, Save updates) → PR, noting hot tub editing is off.
- **Tell Max:** Add Pool reuses this form, don't connect his Save until then, his dropdown needs the hot tub check on ✏️, Volume stays editable.
- **Later:** merge Add + Edit into one form, hot tub form, card shows new fields, remove old text keys (hot tubs still use `filter` + `installed`).

## Done so far
- **A. Data foundation:** `rules.py` (`BANDS`, `color_for`, `test_colors`), `store.py` sample data + `search_options()`, Contact/Pool cards, Water Tests table, Problem history, open-problem badge, Purchases per customer, empty states, `?tab=problems`.
- **0c–0f. ☰ Needs-attention drawer + retests:** left drawer with red count badge, Retests due + Open problems (live via `@ui.refreshable`), `schedule_retest(days, reason)` dialog, New Test `save_test()` (colors, retest rule, keyboard-first), Save Fix.
- **B. New Customer** dialog (Name + Phone required; Address + Zip saved as `"addr, zip"`) → `store.customers` → search options → navigate.
- **D. Log Purchase** saves (`save_purchase`).
- **F. Settings:** Products + Add Product, Backup (status + Restore… only), Water-test ranges table from `rules.BANDS`.
- **G. AI right drawer** opened by a ✨ fab (`ui.page_sticky` + `z-50`), canned replies; `/` is a "Find a customer" landing.
- **E (partial):** Edit Customer and Edit Pool dialogs save and are built on demand, so Cancel discards edits; ➕ on the Pool card title row.

## Remaining plan
- **E. Edit records:** Pool card selector between bodies (Next #1); edits just overwrite (no change log, decided 2026-10-31; the client spec lists one, so revisit with Kara); New Test "For" select when >1 body. No delete (ask Kara: archive vs delete).
- **C. Retest chip** in the Customer title row: "Retest due Oct 23" (red if overdue) / "No retest" → `schedule_retest` + Clear.
- **H. Polish:** `no-caps` on tabs/buttons, tooltip on Print, Log Purchase date → `ui.date` in a menu. Run `/impeccable critique` on Customer first (findings only).
- **I. Demo run-through:** ☰ overdue → search → Customer → retest chip → New Test (flagged) → Problems → Save Fix → Log Purchase → edit phone → add hot tub → Print → New Customer → AI drawer send → Settings. Run `/impeccable audit` + `clarify` + `/code-review` first.
- **If behind, cut in this order:** + attach → C retest chip → New Test "For" select → if-time items (tab-panel `pt-0` nit, "Log these products?" after Save Fix, theme color pick).
- **Backlog (from design critique):** aria-labels, badge red-9, header search `dark` prop, no-match → New Customer, Send posts typed text.
- **Check every step:** full width, 1920×1080, F12 Console clean, Customer print still fits 1 page.

## What's built
- **Files:** `main.py` (imports pages, `ui.run()`), `layout.py` (`page_layout()`: theme, ☰ left drawer, header with logo→Home, center `ui.select` customer search, New Customer + ⚙ buttons, ✨ AI right drawer, print CSS; returns `refresh_attention`), `pages/home.py` (`/` landing), `pages/customer.py`, `pages/settings.py`, `store.py`, `rules.py`. `models.py` empty until Phase 2.
- **`store.py`:** `TODAY`; `products` (15: name/brand/size); `customers` (16) with name/phone/address/since/bodies/tests/problems/purchases/retest. Display dates are strings; `retest['due']` is a real `date` relative to `TODAY` (overdue: Nick, Jake; today: Marcelino, Mike; tomorrow: Jessica). Open problems: Dave (hot tub foam), Chris (algae), Ryan (liner stains). Hot tubs: Manish + Linda (2nd body), Dave (only body; fields `shell`/`cover`). Empty: Emily (no tests), Megan (no bodies). `test['body']` = index into `bodies`. Pools have `shape` ('Round'/'Oval'/'Rectangle'), `length`, `width` (ft; round → width = length), `wall` (in); gallons = `length × width × wall/12 × factor` (5.9 round/oval, 7.5 rectangle), rounded to 100. Hot tubs keep typed gallons. `search_options()` → `{id: 'Name · phone'}`.
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
- **Readings colored in the table** as solid badges on every reading, labeled in the legend above it (In range `green-9` / Borderline `amber-7` with black text / Out of range `red-9`) for WCAG contrast; off-range readings get a ↑/↓ arrow (`rules.reading_arrows`). `rules.py` keeps the plain color words. Placeholder bands (Kara's real ranges TBD; hot tubs use pool bands for now):

| Reading | green | orange | red |
|---|---|---|---|
| FC / TC | 1–3 | 0.6–0.9 or 3.1–5 (TC also if TC−FC ≥ 0.5) | <0.6 or >5 |
| pH | 7.4–7.6 | 7.2–7.3 / 7.7–7.8 | <7.2 or >7.8 |
| Alk | 80–120 | 60–79 / 121–150 | <60 or >150 |
| Hardness | 200–400 | 150–199 / 401–500 | <150 or >500 |
| CYA | 30–50 | 20–29 / 51–80 | <20 or >80 |
| Phos (ppb) | ≤100 | 101–300 | >300 |

- **Problems:** staff can save a fix without asking for suggestions; the saved fix is what was *actually done* (Phase 2: record matched/edited/ignored AI suggestion = training data). Bodies of water = Pool or Hot tub; equipment edits overwrite the old values (no change log for now).
- **Pool form** (decided 2026-11-04): one shared form for Add + Edit, matching Max's Add Pool for pools: same boxes and options (In-Ground, Rectangle, Water Depth). Pool gallons are calculated from wall height, and staff can type over the result. **Hot tub editing is deferred** (✏️ hidden for hot tubs, TODO in `open_edit_pool`); later they show Size, typed Gallons, Shell, Cover, Manufacturer, Filter, Installation.
- **Purchases:** Square already rings sales; "Log these products?" shortcut after Save Fix if time; Phase 2 idea: Square CSV import.
- **Backups** are automatic (nightly to USB); Settings shows status + Restore… only, no Back Up Now.
- **Printing:** standard Windows print dialog via `window.print()`; we design the handout content only.
- **Desktop/PC only** (decided 2026-11-02): no phone layout. The `md:` classes on the Customer page set column height and inner scrolling on desktop, so leave them.

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
2. **Pools and equipment:** several bodies of water per customer, with equipment details and calculated gallons.
3. **Chemical purchases:** a product list and purchases per customer.
4. **Water testing:** results and dates, out-of-range flags, printed reports, history per pool.
5. **Problems and AI suggestions:** each problem, the suggestions, and the fix that was applied.
6. **Settings:** lookup lists, test ranges, backup and restore.

## Constraints
- Runs on Windows, on 2–3 machines on one LAN, with 1–2 concurrent users.
- Everything stays local, with no internet dependency.
- The AI must be real (not a rules-based expert system), self-trained or fine-tuned, local, and free to run.

## Phases
- **Fall 2026:** a working GUI on in-memory sample data, built with NiceGUI.
- **Spring 2027:** PostgreSQL storage and a local AI model served through Ollama.
