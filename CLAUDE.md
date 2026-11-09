# Pristine Pools — Record-Keeping & Water-Testing System

A record-keeping and water-testing system for Pristine Pools, a new above-ground pool store. Built as an SVSU CSIS capstone (CIS 422) run by Dr. Scott James, with a target completion of April 2027.

## The client
Pristine Pools sells hard-sided and soft-sided above-ground pools, chemicals, and equipment. The owner, Kara Nominay, is non-technical and budget-conscious, so the system has to just work. All client contact goes through Dr. James.

Square handles pricing, sales, and inventory. This system sits alongside it and links purchases to each customer's pool and water-test history.

## How it's used
A customer brings a water sample to the counter. Staff find the customer, enter the test, see which readings are out of range, get help diagnosing any problem, and print a report. Staff use the system while talking to the customer, so it's designed for speed. Newer employees may lack diagnosis experience, which is why it includes AI suggestions.

## What it covers
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
