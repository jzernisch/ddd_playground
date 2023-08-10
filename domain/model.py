from dataclasses import dataclass

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

    @property
    def available_quantity(self):
        return self.qty

    def allocate(self, order_line: OrderLine) -> None:
        self.qty -= order_line.qty

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.qty >= order_line.qty
