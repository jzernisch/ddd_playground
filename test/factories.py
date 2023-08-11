import factory
from domain import model

class BatchFactory(factory.Factory):
    class Meta:
        model = model.Batch

    ref = factory.Sequence(lambda n: f"batch_{n}")
    sku = factory.Sequence(lambda n: f"product_{n}")
    qty = 10


class OrderLineFactory(factory.Factory):
    class Meta:
        model = model.OrderLine

    sku = factory.Sequence(lambda n: f"product_{n}")
    qty = 2
