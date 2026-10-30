from datetime import date
import rules
import store

# Phase 2 swaps store.py for the database. These checks keep the sample data
# in the shape the pages expect, so a typo in store.py fails here, not on demo day.

CUSTOMER_KEYS = {'name', 'phone', 'address', 'since', 'bodies', 'tests', 'problems', 'purchases', 'retest'}


def test_every_customer_has_every_key():
    for cid, c in store.customers.items():
        assert CUSTOMER_KEYS <= c.keys(), f'customer {cid} is missing {CUSTOMER_KEYS - c.keys()}'


def test_customer_ids_are_whole_numbers():
    assert all(isinstance(cid, int) for cid in store.customers)


def test_name_and_phone_are_filled_in():
    for cid, c in store.customers.items():
        assert c['name'].strip(), cid
        assert c['phone'].strip(), cid


def test_bodies_are_pool_or_hot_tub():
    for cid, c in store.customers.items():
        for b in c['bodies']:
            assert b['type'] in ('Pool', 'Hot tub'), cid


def test_every_test_points_at_a_real_body():
    for cid, c in store.customers.items():
        for t in c['tests']:
            assert 0 <= t['body'] < len(c['bodies']), f'customer {cid}, test on {t["date"]}'


def test_every_sample_test_can_be_colored():
    for c in store.customers.values():
        for t in c['tests']:
            rules.test_colors(t)  # would raise if a reading had a bad type


def test_retest_is_none_or_a_real_date():
    for cid, c in store.customers.items():
        r = c['retest']
        if r is not None:
            assert isinstance(r['due'], date), cid
            assert r['reason'], cid


def test_problems_have_a_fix_or_are_open():
    for cid, c in store.customers.items():
        for p in c['problems']:
            assert p['fix'] is None or isinstance(p['fix'], str), cid


def test_products_have_name_brand_size():
    names = [p['name'] for p in store.products]
    assert len(names) == len(set(names)), 'two products share a name'  # Settings uses name as the row key
    for p in store.products:
        assert p['name'] and p['brand'] and p['size']


def test_search_options_lists_every_customer():
    options = store.search_options()
    assert options.keys() == store.customers.keys()
    nick = next(cid for cid, c in store.customers.items() if c['name'] == 'Nick McArdle')
    assert options[nick] == 'Nick McArdle · (989) 555-0142'
