from dataclasses import dataclass, field
import datetime
from typing import NewType


Quantity = NewType("Quantity", str)
SKU = NewType("SKU", str)
BatchRef = NewType("BatchRef", str)
@dataclass(frozen=True)
class OrderLine:
    sku: SKU
    qty: Quantity

@dataclass
class Batch:
    ref: BatchRef
    sku: SKU
    qty: Quantity
    eta: datetime.date = 0
    allocations: list[OrderLine] = field(default_factory=list)

    @property
    def available_quantity(self):
        return self.qty - sum([order_line.qty for order_line in self.allocations])

    def allocate(self, order_line: OrderLine) -> None:
        if not self.can_allocate(order_line):
            raise AllocationException()
        self.allocations.append(order_line)

    def deallocate(self, order_line: OrderLine) -> None:
        if order_line not in self.allocations:
            return
        self.allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.qty >= order_line.qty and order_line not in self.allocations

    def __gt__(self, other):
        return self.eta >= other.eta

class AllocationException(Exception):
    pass

def allocate(order_line: OrderLine, batches: list[Batch]) -> BatchRef:
    for batch in sorted(batches):
        if batch.can_allocate(order_line):
            batch.allocate(order_line)
            return batch.ref
    raise OutOfStock()

class OutOfStock(Exception):
    pass
