from datetime import date, timedelta
import pytest
from test.factories import BatchFactory, OrderLineFactory
from domain.model import AllocationException, allocate, OutOfStock


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

def test_orderline_is_compares_by_value():
    order_line_1 = OrderLineFactory()
    order_line_2 = OrderLineFactory(qty=order_line_1.qty, sku=order_line_1.sku)
    assert order_line_1 == order_line_2
    assert len({order_line_1, order_line_2}) == 1

def test_allocate():
    sku = "sku"
    order_line = OrderLineFactory(sku=sku, qty=5)
    batch = BatchFactory(sku=sku, qty=10)
    allocate(order_line, [batch])
    assert batch.available_quantity == 5

def test_allocate_prefers_earlier_batches():
    sku = "sku"
    order_line = OrderLineFactory(sku=sku, qty=5)
    earlier = date.today()
    later = date.today() + timedelta(days=1)
    batch_1 = BatchFactory(sku=sku, qty=10, eta=later)
    batch_2 = BatchFactory(sku=sku, qty=10, eta=earlier)
    allocate(order_line, [batch_1, batch_2])
    assert batch_1.available_quantity == 10
    assert batch_2.available_quantity == 5

def test_allocate_raises_out_of_stock():
    sku = "sku"
    order_line = OrderLineFactory(sku=sku, qty=5)
    earlier = date.today()
    later = date.today() + timedelta(days=1)
    batch_1 = BatchFactory(sku=sku, qty=2, eta=later)
    batch_2 = BatchFactory(sku=sku, qty=2, eta=earlier)
    with pytest.raises(OutOfStock):
        allocate(order_line, [batch_1, batch_2])

def test_allocate_returns_allocated_batch_ref():
    sku = "sku"
    order_line = OrderLineFactory(sku=sku, qty=5)
    earlier = date.today()
    later = date.today() + timedelta(days=1)
    batch_1 = BatchFactory(sku=sku, qty=10, eta=later)
    batch_2 = BatchFactory(sku=sku, qty=10, eta=earlier)
    assert allocate(order_line, [batch_1, batch_2]) == batch_2.ref
