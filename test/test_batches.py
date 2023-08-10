from test.factories import BatchFactory, OrderLineFactory


def test_allocate():
    batch = BatchFactory(qty=10)
    order_line = OrderLineFactory(qty=2)

    batch.allocate(order_line)
    assert batch.available_quantity == 8
