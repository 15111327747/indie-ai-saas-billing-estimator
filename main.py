from dataclasses import dataclass, field
from typing import List

@dataclass
class Usage:
    name: str
    units: int
    unit_price: float
    free_units: int = 0

    def cost(self) -> float:
        billable = max(0, self.units - self.free_units)
        return round(billable * self.unit_price, 2)

@dataclass
class Plan:
    name: str
    base_fee: float
    usages: List[Usage] = field(default_factory=list)

    def subtotal(self) -> float:
        return round(self.base_fee + sum(u.cost() for u in self.usages), 2)

def estimate(plan: Plan, tax_rate: float = 0.0) -> dict:
    subtotal = plan.subtotal()
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    lines = []
    for u in plan.usages:
        lines.append({
            'item': u.name,
            'units': u.units,
            'free_units': u.free_units,
            'cost_usd': u.cost()
        })
    return {
        'plan': plan.name,
        'base_fee_usd': plan.base_fee,
        'usage_lines': lines,
        'subtotal_usd': subtotal,
        'tax_usd': tax,
        'total_usd': total
    }

if __name__ == '__main__':
    plan = Plan('Indie AI Starter', 20.0, [
        Usage('LLM tokens (1K)', 1200, 0.002, 100),
        Usage('Image generations', 300, 0.04, 50),
        Usage('Vector DB reads (1K)', 800, 0.0015, 200)
    ])
    invoice = estimate(plan, tax_rate=0.08)
    for key, value in invoice.items():
        if key != 'usage_lines':
            print(f'{key}: {value}')
    print('usage_lines:')
    for line in invoice['usage_lines']:
        print('  ', line)