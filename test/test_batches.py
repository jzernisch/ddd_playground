import pytest
from test.factories import BatchFactory, OrderLineFactory
from domain.model import AllocationException


def test_allocate_reduces_available_quantity():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.allocate(order_line)
    assert batch.available_quantity == 8

def test_deallocate_increases_available_quantity():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 10

def test_deallocate_is_idempotent_for_same_order_line():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.allocate(order_line)
    batch.deallocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 10

def test_deallocate_has_no_effect_if_not_allocated():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.deallocate(order_line)
    assert batch.available_quantity == 10

def test_can_allocate_depending_on_sku():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2, sku=batch.sku)
    order_line_with_different_sku = OrderLineFactory(qty=2, sku=batch.sku + "x")

    assert batch.can_allocate(order_line)
    assert not batch.can_allocate(order_line_with_different_sku)

def test_can_only_allocate_depending_on_qty():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2, sku=batch.sku)
    order_line_higher_qty = OrderLineFactory(qty=20, sku=batch.sku)
    order_line_same_qty = OrderLineFactory(qty=10, sku=batch.sku)

    assert batch.can_allocate(order_line)
    assert batch.can_allocate(order_line_same_qty)
    assert not batch.can_allocate(order_line_higher_qty)

def test_allocate_raises_exception_when_cannot_allocate():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=12, sku=batch.sku)

    with pytest.raises(AllocationException):
        batch.allocate(order_line)
