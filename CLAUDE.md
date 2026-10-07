# Pristine Pools — Record-Keeping & Water-Testing System

Capstone project (SVSU, CSIS). Developer: Mack. Target completion: **April 2027**.

## How Claude helps on this project
- **Mack writes all the code.** Do not write or edit code files in this repo. Explain the concept, the NiceGUI pieces involved, and what to type and why; Mack types it in the IDE. Small illustrative snippets in chat only when asked. Review Mack's code when asked.
- Exception: restoring or reverting files Claude changed by mistake, and other non-code housekeeping, only when Mack asks.
- Explain what the code does and **why**. Mack wants to understand it, not just receive working output.
- Keep responses concise and structured: method names and architecture reasoning over long prose.
- Don't dump unsolicited code; Mack prefers to iterate in the IDE.
- One NiceGUI concept per step. Mack commits small steps.
- This file is committed on purpose so context carries between Mack's desktop and laptop. **Claude keeps it up to date as we go without being asked**: mark steps done and move the current-step marker, record new decisions, preferences, setup changes, and answered open questions.

## Build plan (NiceGUI)
1. `layout.py`: shared `page_layout()` with `ui.header` + `ui.left_drawer`, used by every page. **← current step.** Part A (move `header()` into `layout.py` as `page_layout()`) done; Part B (`ui.left_drawer` nav in `page_layout()`, per-page nav buttons removed) done; next Part C (hamburger: `ui.left_drawer() as drawer`, `ui.button(icon='menu', on_click=drawer.toggle)`). An older laptop attempt at B + C is in `git stash` for reference only.
2. Split pages into `pages/*.py`, import them in `main.py`
3. Customers page: `ui.table` of fake data, wire up the search box
4. Add Customer: `ui.dialog` form
5. Customer detail via `/customer/{id}`
6. Pool detail: info, gallons calc, water-test form with out-of-range flags (range checks in `rules.py`)
7. Swap fake data for SQLite
8. Ask AI page UI, Ollama later
9. Maintenance screen (product lists, water-test ranges, backup). Tentative: Mack may drop it later.

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
