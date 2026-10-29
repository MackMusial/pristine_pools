# Pristine Pools

A record-keeping and water-testing system for Pristine Pools, an above-ground pool store. Staff use it at the counter: look up the customer, enter a water test, see which readings are off, log a problem, get a suggested fix, and print a report for the customer.

Built by Mack Musial for the CIS 422 capstone at Saginaw Valley State University (Dr. Scott James). Target completion: April 2027.

## Status

**Phase 1 (Fall 2026): working interface on sample data.** Every screen runs live in the browser, but records are kept in memory in `store.py` and reset when the app restarts. AI suggestions are placeholder text.

**Phase 2 (Spring 2027):** PostgreSQL database, editable test ranges, gallons calculation, and a locally run, fine-tuned AI model (Llama through Ollama).

## Features

- **Find a customer** by name or phone from any screen
- **Customer screen** with contact and pool / hot tub details, plus three tabs:
  - **Water Tests:** every reading colored green / orange / red, a quick New Test dialog, and a one-page printed report
  - **Problems:** log a problem, pick or edit an AI suggestion, save the fix that was actually applied
  - **Purchases:** chemical and product history per customer
- **Needs Attention drawer (☰):** overdue and due-today retests (with phone numbers to call) and open problems
- **Retests:** scheduled automatically after a red (2 days) or orange (7 days) reading
- **Pool Assistant drawer (✨):** AI chat available on every screen
- **Settings:** product list, backup status and restore, water-test ranges

## Running it

Requires Python 3.12 or newer.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install nicegui
python main.py
```

Then open http://localhost:8080. Always start from `main.py`. Running a page file directly fails with `No module named 'layout'`.

On Windows, if PowerShell blocks the activate script, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Project layout

| File | What it does |
| --- | --- |
| `main.py` | Imports the pages and starts the app |
| `layout.py` | Shared page frame: header, customer search, New Customer dialog, Needs Attention and Pool Assistant drawers, theme, print styles |
| `pages/home.py` | `/` – Find a Customer landing screen |
| `pages/customer.py` | `/customer/{id}` – the main Customer screen and its tabs |
| `pages/settings.py` | `/settings` – Products, Backup, Water-test ranges |
| `rules.py` | Water-test ranges and the green / orange / red coloring |
| `store.py` | Sample customers, tests, problems, purchases and products (Phase 1 only) |
| `models.py` | Placeholder for the Phase 2 database code |

## Sample data

`store.py` holds 16 fictional customers with 555-01xx phone numbers. Records include pools and hot tubs, overdue and upcoming retests, open problems, and customers with no tests or no pool, so every screen and empty state can be demonstrated.

## Planned architecture (Phase 2)

- **Host computer:** one store desktop runs PostgreSQL, Ollama and the app. Other store PCs open it in a browser by that computer's name over the local network.
- **No cloud or internet dependency:** all data and the AI model stay in the store.
- **Backups:** a nightly automatic `pg_dump` to a USB drive. Settings shows the last backup time, and restoring is always a manual, confirmed step.
- **AI:** a small Llama model fine-tuned on expert-checked pool problems and fixes, shrunk to run without a graphics card.
- **Square** keeps handling sales, prices and inventory. This system only records purchase history alongside tests and problems.
