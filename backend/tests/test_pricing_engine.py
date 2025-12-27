"""
Tests for Pricing Engine
Tests cost calculation, multipliers, and invoice generation
"""

import pytest
from decimal import Decimal

from services.pricing_engine import PricingEngine, get_pricing_engine


class TestPricingEngine:
    """Test Pricing Engine functionality"""

    def test_init_pricing_engine(self):
        """Test pricing engine initialization with defaults"""
        engine = PricingEngine()

        assert engine.base_labor_rate == Decimal('150.00')
        assert engine.size_multipliers['small'] == Decimal('1.0')
        assert engine.size_multipliers['medium'] == Decimal('1.5')
        assert engine.size_multipliers['large'] == Decimal('2.0')
        assert engine.size_multipliers['extra_large'] == Decimal('3.0')

        assert engine.workload_multipliers['light'] == Decimal('1.0')
        assert engine.workload_multipliers['moderate'] == Decimal('1.3')
        assert engine.workload_multipliers['heavy'] == Decimal('1.6')
        assert engine.workload_multipliers['extreme'] == Decimal('2.0')

    def test_singleton_pattern(self):
        """Test that get_pricing_engine returns singleton"""
        engine1 = get_pricing_engine()
        engine2 = get_pricing_engine()
        assert engine1 is engine2

    def test_calculate_room_cost_small_light(self):
        """Test calculation: small room, light workload"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('small', 'light')

        # Expected: $150 * 1.0 * 1.0 = $150.00
        assert cost == Decimal('150.00')

    def test_calculate_room_cost_medium_moderate(self):
        """Test calculation: medium room, moderate workload"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('medium', 'moderate')

        # Expected: $150 * 1.5 * 1.3 = $292.50
        assert cost == Decimal('292.50')

    def test_calculate_room_cost_large_heavy(self):
        """Test calculation: large room, heavy workload"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('large', 'heavy')

        # Expected: $150 * 2.0 * 1.6 = $480.00
        assert cost == Decimal('480.00')

    def test_calculate_room_cost_extra_large_extreme(self):
        """Test calculation: extra large room, extreme workload"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('extra_large', 'extreme')

        # Expected: $150 * 3.0 * 2.0 = $900.00
        assert cost == Decimal('900.00')

    def test_calculate_room_cost_with_adjustments(self):
        """Test calculation with adjustments (stairs, etc.)"""
        engine = PricingEngine()

        adjustments = [
            {'type': 'stairs', 'amount': 50.00},
            {'type': 'difficult_access', 'amount': 75.00}
        ]

        cost = engine.calculate_room_cost('medium', 'moderate', adjustments=adjustments)

        # Expected: ($150 * 1.5 * 1.3) + $50 + $75 = $417.50
        assert cost == Decimal('417.50')

    def test_calculate_room_cost_invalid_size_defaults_to_medium(self):
        """Test that invalid size class defaults to medium multiplier"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('invalid_size', 'light')

        # Should use medium (1.5) as default: $150 * 1.5 * 1.0 = $225.00
        assert cost == Decimal('225.00')

    def test_calculate_room_cost_invalid_workload_defaults_to_moderate(self):
        """Test that invalid workload class defaults to moderate multiplier"""
        engine = PricingEngine()
        cost = engine.calculate_room_cost('small', 'invalid_workload')

        # Should use moderate (1.3) as default: $150 * 1.0 * 1.3 = $195.00
        assert cost == Decimal('195.00')

    def test_calculate_job_cost_single_room(self):
        """Test job cost calculation with single room"""
        engine = PricingEngine()

        rooms = [
            {
                'id': 'room-1',
                'name': 'Master Bedroom',
                'size_class': 'large',
                'workload_class': 'heavy'
            }
        ]

        result = engine.calculate_job_cost(rooms)

        assert len(result['room_costs']) == 1
        assert result['room_costs'][0]['name'] == 'Master Bedroom'
        assert result['room_costs'][0]['cost'] == Decimal('480.00')
        assert result['room_total'] == Decimal('480.00')
        assert result['subtotal'] == Decimal('480.00')
        assert result['total'] == Decimal('480.00')

    def test_calculate_job_cost_multiple_rooms(self):
        """Test job cost calculation with multiple rooms"""
        engine = PricingEngine()

        rooms = [
            {
                'id': 'room-1',
                'name': 'Master Bedroom',
                'size_class': 'large',
                'workload_class': 'heavy'
            },
            {
                'id': 'room-2',
                'name': 'Garage',
                'size_class': 'extra_large',
                'workload_class': 'moderate'
            },
            {
                'id': 'room-3',
                'name': 'Bathroom',
                'size_class': 'small',
                'workload_class': 'light'
            }
        ]

        result = engine.calculate_job_cost(rooms)

        # Master Bedroom: $150 * 2.0 * 1.6 = $480.00
        # Garage: $150 * 3.0 * 1.3 = $585.00
        # Bathroom: $150 * 1.0 * 1.0 = $150.00
        # Total: $1,215.00

        assert len(result['room_costs']) == 3
        assert result['room_total'] == Decimal('1215.00')
        assert result['subtotal'] == Decimal('1215.00')
        assert result['total'] == Decimal('1215.00')

    def test_calculate_job_cost_with_job_adjustments(self):
        """Test job cost with job-level adjustments"""
        engine = PricingEngine()

        rooms = [
            {
                'id': 'room-1',
                'name': 'Bedroom',
                'size_class': 'medium',
                'workload_class': 'moderate'
            }
        ]

        job_adjustments = [
            {'type': 'bin_rental', 'description': 'Bin Rental (20 yard)', 'amount': 200.00},
            {'type': 'stairs', 'description': 'Stair Fee (3 flights)', 'amount': 75.00}
        ]

        result = engine.calculate_job_cost(rooms, job_adjustments=job_adjustments)

        # Room: $292.50
        # Adjustments: $275.00
        # Total: $567.50

        assert result['room_total'] == Decimal('292.50')
        assert result['adjustment_total'] == Decimal('275.00')
        assert result['subtotal'] == Decimal('567.50')
        assert result['total'] == Decimal('567.50')
        assert len(result['adjustments']) == 2

    def test_calculate_job_cost_with_room_and_job_adjustments(self):
        """Test job with both room-level and job-level adjustments"""
        engine = PricingEngine()

        rooms = [
            {
                'id': 'room-1',
                'name': 'Attic',
                'size_class': 'large',
                'workload_class': 'heavy',
                'adjustments': [
                    {'type': 'hazmat', 'amount': 150.00}
                ]
            }
        ]

        job_adjustments = [
            {'type': 'bin_rental', 'description': 'Bin Rental', 'amount': 200.00}
        ]

        result = engine.calculate_job_cost(rooms, job_adjustments=job_adjustments)

        # Room base: $480.00
        # Room adjustment (hazmat): $150.00
        # Room total: $630.00
        # Job adjustment (bin): $200.00
        # Total: $830.00

        assert result['room_total'] == Decimal('630.00')
        assert result['adjustment_total'] == Decimal('200.00')
        assert result['subtotal'] == Decimal('830.00')
        assert result['total'] == Decimal('830.00')

    def test_generate_invoice_line_items_no_ai_jargon(self):
        """Test that invoice line items contain no AI jargon"""
        engine = PricingEngine()

        rooms = [
            {
                'id': 'room-1',
                'name': 'Master Bedroom',
                'size_class': 'large',
                'workload_class': 'heavy',
                'ai_confidence': 0.87  # Should NOT appear in invoice
            },
            {
                'id': 'room-2',
                'name': 'Garage',
                'size_class': 'extra_large',
                'workload_class': 'moderate'
            }
        ]

        line_items = engine.generate_invoice_line_items(rooms)

        assert len(line_items) == 2

        # Check first line item
        assert line_items[0]['description'] == 'Master Bedroom Cleanout'
        assert line_items[0]['quantity'] == 1
        assert line_items[0]['unit_price'] == 480.00
        assert line_items[0]['total'] == 480.00

        # Verify NO AI jargon
        assert 'AI' not in line_items[0]['description']
        assert 'confidence' not in str(line_items[0])
        assert 'large' not in line_items[0]['description'].lower()
        assert 'heavy' not in line_items[0]['description'].lower()

    def test_generate_invoice_line_items_with_adjustments(self):
        """Test invoice line items include adjustments"""
        engine = PricingEngine()

        rooms = [
            {
                'name': 'Basement',
                'size_class': 'extra_large',
                'workload_class': 'extreme'
            }
        ]

        job_adjustments = [
            {'type': 'bin_rental', 'description': 'Bin Rental (20 yard)', 'amount': 200.00},
            {'type': 'stairs', 'description': 'Stair Fee (3 flights)', 'amount': 75.00}
        ]

        line_items = engine.generate_invoice_line_items(rooms, job_adjustments)

        assert len(line_items) == 3

        # Room line item
        assert line_items[0]['description'] == 'Basement Cleanout'

        # Adjustment line items
        assert line_items[1]['description'] == 'Bin Rental (20 yard)'
        assert line_items[1]['unit_price'] == 200.00

        assert line_items[2]['description'] == 'Stair Fee (3 flights)'
        assert line_items[2]['unit_price'] == 75.00

    def test_generate_invoice_line_items_unnamed_room(self):
        """Test invoice with unnamed room defaults to 'Room Cleanout'"""
        engine = PricingEngine()

        rooms = [
            {
                'size_class': 'medium',
                'workload_class': 'moderate'
                # No 'name' field
            }
        ]

        line_items = engine.generate_invoice_line_items(rooms)

        assert line_items[0]['description'] == 'Room Cleanout'

    def test_calculate_adjustments_empty_list(self):
        """Test adjustment calculation with empty list"""
        engine = PricingEngine()
        total = engine._calculate_adjustments([])
        assert total == Decimal('0.00')

    def test_calculate_adjustments_multiple_items(self):
        """Test adjustment calculation with multiple items"""
        engine = PricingEngine()

        adjustments = [
            {'amount': 50.00},
            {'amount': 75.25},
            {'amount': 100.00}
        ]

        total = engine._calculate_adjustments(adjustments)
        assert total == Decimal('225.25')

    def test_pricing_consistency_across_methods(self):
        """Test that room cost is consistent across different methods"""
        engine = PricingEngine()

        # Calculate directly
        direct_cost = engine.calculate_room_cost('large', 'heavy')

        # Calculate via job cost
        rooms = [{'size_class': 'large', 'workload_class': 'heavy'}]
        job_result = engine.calculate_job_cost(rooms)

        # Calculate via invoice line items
        line_items = engine.generate_invoice_line_items(rooms)

        assert direct_cost == job_result['room_total']
        assert float(direct_cost) == line_items[0]['unit_price']
