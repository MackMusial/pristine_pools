# Pristine Pools — Record-Keeping & Water-Testing System

Capstone project (SVSU, CSIS). Developer: Mack. Target completion: **April 2027**.

## How Claude helps on this project
- **Mack writes all the code.** Do not write or edit code files in this repo. Explain the concept, the NiceGUI pieces involved, and what to type and why; Mack types it in the IDE. Small illustrative snippets in chat only when asked. Review Mack's code when asked.
- Exception: restoring or reverting files Claude changed by mistake, and other non-code housekeeping, only when Mack asks.
- Explain what the code does and **why**. Mack wants to understand it, not just receive working output.
- Keep responses concise and structured: method names and architecture reasoning over long prose.
- Don't dump unsolicited code; Mack prefers to iterate in the IDE.
- One NiceGUI concept per step. Mack commits small steps.
- This file is committed on purpose so context carries between Mack's desktop and laptop. Update the build progress below when a step is finished.

## Build plan (NiceGUI)
1. `layout.py`: shared `page_layout()` with `ui.header` + `ui.left_drawer`, used by every page. **← current step (Mack is doing it)**
2. Split pages into `pages/*.py`, import them in `main.py`
3. Customers page: `ui.table` of fake data, wire up the search box
4. Add Customer: `ui.dialog` form
5. Customer detail via `/customer/{id}`
6. Pool detail: info, gallons calc, water-test form with out-of-range flags (range checks in `rules.py`)
7. Swap fake data for SQLite
8. Ask AI page UI, Ollama later

## Dev setup (per machine)
- `py -3.12 -m venv .venv`, then `.venv\Scripts\Activate.ps1`, then `pip install nicegui`
- In VS Code: Python: Select Interpreter, pick `.venv`
- Run: `python main.py`, open http://localhost:8080
- `.venv/` and `__pycache__/` are gitignored

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
