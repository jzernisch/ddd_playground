from test.factories import BatchFactory, OrderLineFactory


def test_allocate():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.allocate(order_line)
    assert batch.available_quantity == 8

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
