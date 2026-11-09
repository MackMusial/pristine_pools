from unittest.mock import patch

from nicegui import event, ui
from nicegui.testing import User
import store

def customer_id(name):
    return next(cid for cid, c in store.customers.items() if c['name'] == name)

async def open_test_popup(user):
    await user.open(f'/customer/{customer_id("Nick McArdle")}')
    table, listener = next(
        (t, l) for t in user.find(kind=ui.table).elements 
        for l in t._event_listeners if l.type == 'rowClick'
    )
    args = events.GenericEventArguments(sender=table, client=table.client, args=[{}, table.rows[0], 0])
    events.handle_event(listener, args)  #same as clicking the first row of the table, which opens the test popup

async def test_table_column_is_not_collapsed_when_printing(user, User):
    await open_test_popup(user)
    await user.should_see('water test · ')
    assert any('single-page-print' in card.classes for card in user.find(kind=ui.card).elements)
    assert any(button.text == 'Print' for button in user.find(kind=ui.button).elements)

async def test_print_css_is_still_in_place(user: User):
    with patch('layout.ui.add_css') as add_css:
        await user.open('/')
    css = ' '.join(call.args[0] for call in add_css.call_args_list)
    for rule in [
        'body:has(.single-page-print) #app',  # hides the normal page behind the popup
        'body:has(.single-page-print) .q-dialog,',  # unpins the popup's outer layer
        'body:has(.single-page-print) .q-dialog__inner',  # unpins the popup's inner layer
        '@layer quasar_importants',  # needed to unpin the body
        '.q-page, .q-layout',  # stops the blank second page
    ]:
        assert rule in css
    