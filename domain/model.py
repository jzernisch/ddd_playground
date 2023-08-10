from dataclasses import dataclass, field

@dataclass
class OrderLine:
    ref: str
    sku: str
    qty: int

@dataclass
class Batch:
    ref: str
    sku: str
    qty: int
    allocations: list[OrderLine] = field(default_factory=list)

    @property
    def available_quantity(self):
        return self.qty - sum([order_line.qty for order_line in self.allocations])

    def allocate(self, order_line: OrderLine) -> None:
        if order_line in self.allocations:
            return
        self.allocations.append(order_line)

    def deallocate(self, order_line: OrderLine) -> None:
        if order_line not in self.allocations:
            return
        self.allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.qty >= order_line.qty
