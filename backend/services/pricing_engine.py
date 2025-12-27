"""
Pricing Engine
Converts AI room classification into dollar estimates
Applies size/workload multipliers and adjustments
"""

from typing import Dict, List, Optional
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class PricingEngine:
    """
    Pricing engine for calculating room cleanout costs

    Uses database pricing rules (size/workload multipliers)
    to convert AI classification into dollar estimates
    """

    # Default pricing (fallback if database unavailable)
    DEFAULT_BASE_LABOR = Decimal('150.00')

    DEFAULT_SIZE_MULTIPLIERS = {
        'small': Decimal('1.0'),
        'medium': Decimal('1.5'),
        'large': Decimal('2.0'),
        'extra_large': Decimal('3.0')
    }

    DEFAULT_WORKLOAD_MULTIPLIERS = {
        'light': Decimal('1.0'),
        'moderate': Decimal('1.3'),
        'heavy': Decimal('1.6'),
        'extreme': Decimal('2.0')
    }

    def __init__(self):
        self.base_labor_rate = self.DEFAULT_BASE_LABOR
        self.size_multipliers = self.DEFAULT_SIZE_MULTIPLIERS.copy()
        self.workload_multipliers = self.DEFAULT_WORKLOAD_MULTIPLIERS.copy()

    def calculate_room_cost(
        self,
        size_class: str,
        workload_class: str,
        adjustments: Optional[List[Dict]] = None
    ) -> Decimal:
        """
        Calculate cost for a single room

        Args:
            size_class: small, medium, large, extra_large
            workload_class: light, moderate, heavy, extreme
            adjustments: List of adjustment dicts (e.g., stairs, access)

        Returns:
            Decimal: Total cost for room
        """
        # Get multipliers
        size_mult = self.size_multipliers.get(size_class, Decimal('1.5'))
        workload_mult = self.workload_multipliers.get(workload_class, Decimal('1.3'))

        # Base calculation: base_rate * size * workload
        room_cost = self.base_labor_rate * size_mult * workload_mult

        # Apply adjustments
        if adjustments:
            adjustment_total = self._calculate_adjustments(adjustments)
            room_cost += adjustment_total

        logger.info(
            f"Room cost calculated: {size_class}/{workload_class} = ${room_cost:.2f}"
        )

        return room_cost

    def calculate_job_cost(
        self,
        rooms: List[Dict],
        job_adjustments: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Calculate total cost for entire job

        Args:
            rooms: List of room dicts with size_class, workload_class
            job_adjustments: Job-level adjustments (bin rental, etc.)

        Returns:
            Dict with breakdown:
            {
                "room_costs": [...],
                "room_total": Decimal,
                "adjustments": [...],
                "adjustment_total": Decimal,
                "subtotal": Decimal,
                "tax_rate": Decimal,
                "tax_amount": Decimal,
                "total": Decimal
            }
        """
        room_costs = []
        room_total = Decimal('0.00')

        # Calculate each room
        for room in rooms:
            cost = self.calculate_room_cost(
                size_class=room.get('size_class', 'medium'),
                workload_class=room.get('workload_class', 'moderate'),
                adjustments=room.get('adjustments')
            )
            room_costs.append({
                'room_id': room.get('id'),
                'name': room.get('name', 'Unnamed Room'),
                'size_class': room.get('size_class'),
                'workload_class': room.get('workload_class'),
                'cost': cost
            })
            room_total += cost

        # Calculate job-level adjustments
        adjustment_details = []
        adjustment_total = Decimal('0.00')

        if job_adjustments:
            for adj in job_adjustments:
                amount = Decimal(str(adj.get('amount', 0)))
                adjustment_details.append({
                    'type': adj.get('type'),
                    'description': adj.get('description', adj.get('type')),
                    'amount': amount
                })
                adjustment_total += amount

        subtotal = room_total + adjustment_total

        # Tax calculation (default 0%, can be configured)
        tax_rate = Decimal('0.00')
        tax_amount = subtotal * tax_rate

        total = subtotal + tax_amount

        return {
            'room_costs': room_costs,
            'room_total': room_total,
            'adjustments': adjustment_details,
            'adjustment_total': adjustment_total,
            'subtotal': subtotal,
            'tax_rate': tax_rate,
            'tax_amount': tax_amount,
            'total': total
        }

    def _calculate_adjustments(self, adjustments: List[Dict]) -> Decimal:
        """Calculate total of adjustments"""
        total = Decimal('0.00')
        for adj in adjustments:
            total += Decimal(str(adj.get('amount', 0)))
        return total

    def generate_invoice_line_items(
        self,
        rooms: List[Dict],
        job_adjustments: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Generate invoice line items (plain language, no AI jargon)

        CRITICAL: "Invoices must be plain and defensible"
        No mention of AI classification, just clear descriptions

        Returns:
            List of line items:
            [
                {
                    "description": "Master Bedroom Cleanout",
                    "quantity": 1,
                    "unit_price": 450.00,
                    "total": 450.00
                },
                ...
            ]
        """
        line_items = []

        # Room line items
        for room in rooms:
            cost = self.calculate_room_cost(
                size_class=room.get('size_class', 'medium'),
                workload_class=room.get('workload_class', 'moderate'),
                adjustments=room.get('adjustments')
            )

            # Create plain description (no AI jargon)
            room_name = room.get('name', 'Room')
            description = f"{room_name} Cleanout"

            line_items.append({
                'description': description,
                'quantity': 1,
                'unit_price': float(cost),
                'total': float(cost)
            })

        # Job-level adjustments
        if job_adjustments:
            for adj in job_adjustments:
                line_items.append({
                    'description': adj.get('description', adj.get('type', 'Adjustment')),
                    'quantity': 1,
                    'unit_price': float(adj.get('amount', 0)),
                    'total': float(adj.get('amount', 0))
                })

        return line_items

    def load_pricing_rules_from_db(self, db_session):
        """
        Load pricing rules from database

        Updates multipliers based on active pricing_rules table
        """
        # TODO: Implement when database models are ready
        pass


# Singleton instance
_pricing_engine = None

def get_pricing_engine() -> PricingEngine:
    """Get pricing engine singleton"""
    global _pricing_engine
    if _pricing_engine is None:
        _pricing_engine = PricingEngine()
    return _pricing_engine
