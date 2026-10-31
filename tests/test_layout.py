import layout
import store


def test_retests_are_sorted_oldest_first():
    due, _ = layout.needs_attention()
    dates = [c['retest']['due'] for cid, c in due]
    assert dates == sorted(dates)
    assert len(due) == sum(1 for c in store.customers.values() if c['retest'] is not None)


def test_open_problems_are_the_ones_without_a_fix():
    _, open_list = layout.needs_attention()
    for cid, c, p in open_list:
        assert p['fix'] is None
        assert store.customers[cid] is c
    names = {c['name'] for cid, c, p in open_list}
    assert {'Dave Thompson', 'Chris Patel'} <= names


def test_customer_with_two_open_problems_is_listed_once(monkeypatch):
    c = {'retest': None, 'problems': [
        {'title': 'A', 'fix': None},
        {'title': 'B', 'fix': None},
    ]}
    monkeypatch.setattr(store, 'customers', {1: c})  # swapped back after the test
    due, open_list = layout.needs_attention()
    assert due == []
    assert open_list == [(1, c, c['problems'][0])]


def test_nothing_needs_attention(monkeypatch):
    monkeypatch.setattr(store, 'customers', {1: {'retest': None, 'problems': [{'fix': 'Done'}]}})
    assert layout.needs_attention() == ([], [])
