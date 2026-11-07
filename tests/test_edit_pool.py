import copy
import pytest
from nicegui import ui
from nicegui.testing import User
import store


def customer_id(name):
    return next(cid for cid, c in store.customers.items() if c['name'] == name)


@pytest.fixture(autouse=True)
def restore_store():
    saved = copy.deepcopy(store.customers)
    yield
    store.customers.clear()
    store.customers.update(saved)


async def open_dialog(user, name):
    await user.open(f'/customer/{customer_id(name)}')
    user.find(marker='edit-pool').click()


def box(user, label):
    return next(iter(user.find(kind=ui.number, content=label).elements))


def nicks_pool():
    return store.customers[customer_id('Nick McArdle')]['bodies'][0]


async def test_edit_button_opens_dialog(user: User):
    await open_dialog(user, 'Nick McArdle')
    await user.should_see('Edit Pool')


async def test_dialog_loads_the_saved_pool(user: User):
    await open_dialog(user, 'Nick McArdle')
    await user.should_see('Doughboy')
    assert box(user, 'Length (ft)').value == 24


async def test_changing_length_recalculates_volume(user: User):
    await open_dialog(user, 'Nick McArdle')
    box(user, 'Length (ft)').value = 30
    assert box(user, 'Volume (gal)').value == 23000


async def test_save_updates_the_pool(user: User):
    await open_dialog(user, 'Nick McArdle')
    box(user, 'Length (ft)').value = 30
    user.find(marker='save-pool').click()
    assert nicks_pool()['length'] == 30
    assert nicks_pool()['size'].startswith('30 ft round')
    assert nicks_pool()['gallons'] == 23000


async def test_save_keeps_a_typed_over_volume(user: User):
    await open_dialog(user, 'Nick McArdle')
    box(user, 'Volume (gal)').value = 15000
    user.find(marker='save-pool').click()
    assert nicks_pool()['gallons'] == 15000


async def test_rectangle_saves_its_size_and_gallons(user: User):
    await open_dialog(user, 'Nick McArdle')
    next(iter(user.find(marker='pool-shape').elements)).value = 'Rectangle'
    box(user, 'Width (ft)').value = 12
    user.find(marker='save-pool').click()
    assert nicks_pool()['size'].startswith('12 x 24 ft rectangle')
    assert nicks_pool()['gallons'] == 9400  # 24 x 12 x (52 / 12) x 7.5, to the nearest 100


async def test_save_keeps_a_floating_chlorinator_on_the_card(user: User):
    await open_dialog(user, 'Manish Shrestha')
    user.find(marker='save-pool').click()
    assert store.customers[customer_id('Manish Shrestha')]['bodies'][0]['chlorinator'] == 'Pool Time'


async def test_cancel_discards_changes(user: User):
    await open_dialog(user, 'Nick McArdle')
    box(user, 'Length (ft)').value = 30
    user.find(kind=ui.button, content='Cancel').click()
    assert nicks_pool()['length'] == 24


async def test_blank_length_blocks_save(user: User):
    await open_dialog(user, 'Nick McArdle')
    box(user, 'Length (ft)').value = None
    user.find(marker='save-pool').click()
    assert nicks_pool()['length'] == 24


async def test_hot_tub_has_no_edit_button(user: User):
    await user.open(f'/customer/{customer_id("Dave Thompson")}')
    await user.should_not_see(marker='edit-pool')
