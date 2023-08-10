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


    def allocate(self, order_line: OrderLine):
        self.qty -= order_line.qty
