# Pristine Pools — Record-Keeping & Water-Testing System

Capstone project (SVSU, CSIS). Developer: Mack. Target completion: **April 2027**.

## How Claude helps on this project
- **Mack writes all the code.** Do not write or edit code files in this repo. Explain the concept, the NiceGUI pieces involved, and what to type and why; Mack types it in the IDE. Small illustrative snippets in chat only when asked. Review Mack's code when asked.
- Exception: restoring or reverting files Claude changed by mistake, and other non-code housekeeping, only when Mack asks.
- Explain what the code does and **why**. Mack wants to understand it, not just receive working output.
- Keep responses concise and structured: method names and architecture reasoning over long prose.
- Don't dump unsolicited code; Mack prefers to iterate in the IDE.
- One NiceGUI concept per step. Mack commits small steps.
- **When Claude needs Mack to decide something, ask with the question popup (AskUserQuestion)**, never a question buried in a reply. It's much more obvious that way.
- This file is committed on purpose so context carries between Mack's desktop and laptop. **Claude keeps it up to date as we go without being asked**: mark steps done and move the current-step marker, record new decisions, preferences, setup changes, and answered open questions.

## Build plan (NiceGUI)
1. `layout.py`: shared `page_layout()` with `ui.header` (☰ `drawer.toggle`, title, search) + `ui.left_drawer` nav, used by every page. **Done.**
2. Split pages into `pages/*.py`, import them in `main.py`. **Done.**
**Decision (2026-10-07): GUI first, functionality later.** Mack wants the whole GUI looking presentable and polished before wiring anything up. Pages use hardcoded placeholder content (a few sample rows written inline) just so layouts can be judged; buttons can be no-ops. Don't steer back toward the database until the GUI phase is done.

### Phase 1: GUI (looks only)
3. Global look: theme colors (`ui.colors`), header/drawer styling, active nav item, fonts/spacing. **← current step.** Decided: **light mode**. Colors: Mack is trying 3 candidates side by side before picking: Pool blue + teal (`#0369a1` / `#0d9488` / `#38bdf8`), Aqua + navy (`#1e3a8a` / `#06b6d4` / `#f59e0b`), Ocean dark (`#0f172a` / `#22d3ee` / `#a78bfa`) as primary / secondary / accent.
4. Home dashboard: Quick Actions cards with icons, summary stat cards (placeholder numbers)
5. Customers page: `ui.table` with placeholder rows, search box, Add/Edit/Delete buttons (no-op)
6. Add/Edit Customer `ui.dialog` form (layout only)
7. Customer detail page (`/customer/{id}`): info card + list of their pools
8. Pool detail page: pool/equipment info, water-test entry form, test history, out-of-range highlight styling
9. Problems & AI Suggestions page (layout for problem entry, suggestion list, chosen solution)
10. Chemical purchases page
11. Maintenance screen (product lists, water-test ranges, backup). Tentative: Mack may drop it later.

### Phase 2: Make it work (later)
- SQLite via built-in `sqlite3`, all data code in `models.py` (pages never write SQL). `init_db()` with `CREATE TABLE IF NOT EXISTS`; CRUD functions (`add_/get_/update_/delete_customer`) with `?` placeholders, `commit()` on writes, `WHERE id = ?` on update/delete; `row_factory = sqlite3.Row` → dicts for `ui.table`. Gitignore `*.db` (customer personal data).
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
- Everything employees need should be reachable from Home in 2–3 clicks (quick-action buttons that open a `ui.dialog`, plus search in the header).

## Client & context
- **Client:** Kara Nominay, owner of Pristine Pools, a new above-ground pool store (not open yet).
- **All client contact goes through Dr. James**, who will also install the system on the client's PC and train the client.
- The store sells hard-sided (steel-wall) and soft-sided above-ground pools, plus chemicals and equipment. **No in-ground pools.**
- **Square** handles pricing, sales, and inventory. This system is **ancillary**: it records what Square doesn't.
- Store staff enter all data while talking with the customer in person. **Customers never use the system.**
- New employees may lack pool-diagnosis experience, so the AI suggestions exist to help them.

## Subsystems (shared database)
1. **Customer Information Management:** name, address, phone.
2. **Pool & Equipment Management:** purchase/install dates, shape, size, manufacturer, model/serial, wall type & liner, floor type, filter, automatic chlorinator, installer. **Calculates total volume in gallons.**
3. **Chemical Purchase Tracking:** list of products carried; per-customer purchases (date, manufacturer, product, quantity, volume).
4. **Water Testing & Reporting:** record chemical panel results and dates, **flag values outside the client's recommended ranges**, print a customer report, show test history per pool.
5. **Problem Tracking & AI Suggestions:** record the problem and date reported, suggest solutions, record the chosen solution so there's a history of what was tried.
6. **Maintenance:** manage lookup lists (chemical products, manufacturers), edit recommended water-test ranges, back up and restore the database.

## Constraints
- Runs on **Windows**, on a single machine. Expect 1–2 concurrent users.
- **The AI must be self-trained or fine-tuned and run locally.** No hosted APIs (no Claude, no ChatGPT). It must be free to run.
- The recommendation feature must be real AI. **A rules-based expert system is ruled out.** Off-the-shelf CRM platforms are also ruled out.
- Limited ML experience so far. Favor approaches that are learnable and well-documented.
- Biggest risk: **training data** for the AI suggestions, and the client's PC hardware (GPU/RAM for a local model).

## Architecture (feasibility study compares three)
1. Web-based: Node.js / Express.js
2. .NET desktop application: C#
3. **NiceGUI (Python), the current lean**, paired with a locally run **Llama** model (e.g., via Ollama), with the app, AI, and database all on one machine.

Final choice is not locked in. Confirm before assuming a stack.

## Open questions
- Exact client PC specs (drives whether a local Llama model is feasible).
- Whether past problem/solution records exist for training data.
- Login/roles: the spec mentions "authorized users" for Maintenance but doesn't define authentication.
- Protection of customer personal data.
