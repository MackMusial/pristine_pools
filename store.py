from datetime import date

# ---------- Shared in-memory data ----------
# Module-level lists: every page shares them while the server runs (lost on restart).
# Use them as store.retests_due (not "from store import ...") so every page sees the same list.
# Phase 2: these become PostgreSQL tables.

retests_due = [  # one retest per customer
    {'cid': 1,  'due': date(2026, 10, 17), 'reason': 'green water'},
    {'cid': 7,  'due': date(2026, 10, 20), 'reason': 'cloudy water'},
    {'cid': 12, 'due': date(2026, 10, 23), 'reason': 'low chlorine'},
]
open_problems = [  # logged, no fix saved yet
    {'cid': 4, 'logged': date(2026, 10, 19), 'text': 'white flakes in water'},
    {'cid': 9, 'logged': date(2026, 10, 21), 'text': 'stains on liner'},
]


def has_open_problem(cid):
    return any(p['cid'] == cid for p in open_problems)


def add_open_problem(cid, text):
    if not has_open_problem(cid):
        open_problems.append({'cid': cid, 'logged': date.today(), 'text': text})


def close_problem(cid):
    open_problems[:] = [p for p in open_problems if p['cid'] != cid]  # [:] changes the list in place, so every page sees it


def set_retest(cid, due, reason):
    clear_retest(cid)  # only one retest per customer
    retests_due.append({'cid': cid, 'due': due, 'reason': reason})


def clear_retest(cid):
    retests_due[:] = [r for r in retests_due if r['cid'] != cid]
