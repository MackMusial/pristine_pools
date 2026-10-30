import pytest
from nicegui.testing import User
import store

# Each test opens a page in NiceGUI's fake browser. If a page throws an error
# while it's being built, the test fails, so a broken page can't reach main.


def customer_id(name):
    return next(cid for cid, c in store.customers.items() if c['name'] == name)


async def test_home_page(user: User):
    await user.open('/')
    await user.should_see('Find a customer')


async def test_settings_page(user: User):
    await user.open('/settings')
    await user.should_see('Settings')
    await user.should_see('Products')


@pytest.mark.parametrize('name', [c['name'] for c in store.customers.values()])
async def test_every_customer_page_loads(user: User, name):
    await user.open(f'/customer/{customer_id(name)}')
    await user.should_see(name)
    await user.should_see('Water Tests')


async def test_customer_page_opens_on_problems(user: User):
    await user.open(f'/customer/{customer_id("Chris Patel")}?tab=problems')
    await user.should_see('Log a Problem')


async def test_unknown_customer(user: User):
    await user.open('/customer/9999')
    await user.should_see('Customer does not exist')


async def test_customer_without_a_pool(user: User):
    await user.open(f'/customer/{customer_id("Megan Fischer")}')
    await user.should_see('No pool on file')
