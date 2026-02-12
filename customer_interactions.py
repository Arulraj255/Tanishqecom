"""
Customer Interactions Tracking and Summary Module for Tanishq E-Commerce Website

This module tracks and summarizes customer interactions on the Tanishq e-commerce platform.
It captures various types of customer activities and generates comprehensive summaries.
"""

from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict, Counter
import json


class CustomerInteraction:
    """Represents a single customer interaction on the website"""
    
    def __init__(self, customer_id: str, interaction_type: str, 
                 timestamp: datetime, details: Dict[str, Any] = None):
        """
        Initialize a customer interaction
        
        Args:
            customer_id: Unique identifier for the customer
            interaction_type: Type of interaction (e.g., 'page_view', 'product_view', 
                            'add_to_cart', 'purchase', 'search', 'review', 'contact')
            timestamp: When the interaction occurred
            details: Additional details about the interaction
        """
        self.customer_id = customer_id
        self.interaction_type = interaction_type
        self.timestamp = timestamp
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert interaction to dictionary"""
        return {
            'customer_id': self.customer_id,
            'interaction_type': self.interaction_type,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details
        }


class InteractionTracker:
    """Tracks and manages customer interactions"""
    
    def __init__(self):
        self.interactions: List[CustomerInteraction] = []
    
    def add_interaction(self, interaction: CustomerInteraction):
        """Add a new interaction to the tracker"""
        self.interactions.append(interaction)
    
    def add_bulk_interactions(self, interactions: List[CustomerInteraction]):
        """Add multiple interactions at once"""
        self.interactions.extend(interactions)
    
    def get_interactions_by_customer(self, customer_id: str) -> List[CustomerInteraction]:
        """Get all interactions for a specific customer"""
        return [i for i in self.interactions if i.customer_id == customer_id]
    
    def get_interactions_by_type(self, interaction_type: str) -> List[CustomerInteraction]:
        """Get all interactions of a specific type"""
        return [i for i in self.interactions if i.interaction_type == interaction_type]
    
    def get_interactions_in_period(self, start_date: datetime, 
                                   end_date: datetime) -> List[CustomerInteraction]:
        """Get all interactions within a time period"""
        return [i for i in self.interactions 
                if start_date <= i.timestamp <= end_date]


class InteractionSummary:
    """Generates comprehensive summaries of customer interactions"""
    
    def __init__(self, tracker: InteractionTracker):
        self.tracker = tracker
    
    def generate_overall_summary(self) -> Dict[str, Any]:
        """Generate an overall summary of all customer interactions"""
        interactions = self.tracker.interactions
        
        if not interactions:
            return {
                'total_interactions': 0,
                'unique_customers': 0,
                'interaction_breakdown': {},
                'message': 'No interactions recorded yet'
            }
        
        # Basic statistics
        total_interactions = len(interactions)
        unique_customers = len(set(i.customer_id for i in interactions))
        
        # Interaction type breakdown
        interaction_types = Counter(i.interaction_type for i in interactions)
        
        # Customer engagement levels
        customer_interaction_counts = defaultdict(int)
        for interaction in interactions:
            customer_interaction_counts[interaction.customer_id] += 1
        
        # Categorize customers by engagement
        engagement_levels = {
            'high': 0,  # 10+ interactions
            'medium': 0,  # 5-9 interactions
            'low': 0  # 1-4 interactions
        }
        
        for count in customer_interaction_counts.values():
            if count >= 10:
                engagement_levels['high'] += 1
            elif count >= 5:
                engagement_levels['medium'] += 1
            else:
                engagement_levels['low'] += 1
        
        # Time-based analysis
        timestamps = [i.timestamp for i in interactions]
        earliest_interaction = min(timestamps)
        latest_interaction = max(timestamps)
        
        return {
            'summary_generated_at': datetime.now().isoformat(),
            'total_interactions': total_interactions,
            'unique_customers': unique_customers,
            'date_range': {
                'earliest': earliest_interaction.isoformat(),
                'latest': latest_interaction.isoformat()
            },
            'interaction_breakdown': dict(interaction_types),
            'customer_engagement_levels': engagement_levels,
            'average_interactions_per_customer': round(
                total_interactions / unique_customers, 2
            ) if unique_customers > 0 else 0
        }
    
    def generate_customer_summary(self, customer_id: str) -> Dict[str, Any]:
        """Generate a summary for a specific customer"""
        interactions = self.tracker.get_interactions_by_customer(customer_id)
        
        if not interactions:
            return {
                'customer_id': customer_id,
                'total_interactions': 0,
                'message': 'No interactions found for this customer'
            }
        
        interaction_types = Counter(i.interaction_type for i in interactions)
        timestamps = [i.timestamp for i in interactions]
        
        # Extract product views if available
        products_viewed = []
        items_purchased = []
        searches = []
        
        for interaction in interactions:
            if interaction.interaction_type == 'product_view' and 'product_id' in interaction.details:
                products_viewed.append(interaction.details['product_id'])
            elif interaction.interaction_type == 'purchase' and 'items' in interaction.details:
                items_purchased.extend(interaction.details['items'])
            elif interaction.interaction_type == 'search' and 'query' in interaction.details:
                searches.append(interaction.details['query'])
        
        return {
            'customer_id': customer_id,
            'total_interactions': len(interactions),
            'interaction_breakdown': dict(interaction_types),
            'first_interaction': min(timestamps).isoformat(),
            'last_interaction': max(timestamps).isoformat(),
            'products_viewed_count': len(products_viewed),
            'unique_products_viewed': len(set(products_viewed)),
            'total_purchases': len([i for i in interactions if i.interaction_type == 'purchase']),
            'total_items_purchased': len(items_purchased),
            'search_queries_count': len(searches),
            'engagement_level': self._determine_engagement_level(len(interactions))
        }
    
    def generate_interaction_type_summary(self, interaction_type: str) -> Dict[str, Any]:
        """Generate a summary for a specific type of interaction"""
        interactions = self.tracker.get_interactions_by_type(interaction_type)
        
        if not interactions:
            return {
                'interaction_type': interaction_type,
                'total_count': 0,
                'message': f'No {interaction_type} interactions found'
            }
        
        unique_customers = len(set(i.customer_id for i in interactions))
        
        return {
            'interaction_type': interaction_type,
            'total_count': len(interactions),
            'unique_customers': unique_customers,
            'average_per_customer': round(len(interactions) / unique_customers, 2)
        }
    
    def generate_period_summary(self, start_date: datetime, 
                               end_date: datetime) -> Dict[str, Any]:
        """Generate a summary for a specific time period"""
        interactions = self.tracker.get_interactions_in_period(start_date, end_date)
        
        if not interactions:
            return {
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'total_interactions': 0,
                'message': 'No interactions in this period'
            }
        
        unique_customers = len(set(i.customer_id for i in interactions))
        interaction_types = Counter(i.interaction_type for i in interactions)
        
        return {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_interactions': len(interactions),
            'unique_customers': unique_customers,
            'interaction_breakdown': dict(interaction_types)
        }
    
    def _determine_engagement_level(self, interaction_count: int) -> str:
        """Determine customer engagement level based on interaction count"""
        if interaction_count >= 10:
            return 'high'
        elif interaction_count >= 5:
            return 'medium'
        else:
            return 'low'
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print a formatted summary"""
        print(json.dumps(summary, indent=2))


def create_sample_interactions() -> List[CustomerInteraction]:
    """Create sample customer interactions for demonstration"""
    from datetime import timedelta
    
    base_time = datetime.now()
    interactions = []
    
    # Customer 1: Active shopper
    interactions.extend([
        CustomerInteraction(
            'CUST001', 'page_view', 
            base_time - timedelta(days=5),
            {'page': 'home'}
        ),
        CustomerInteraction(
            'CUST001', 'search',
            base_time - timedelta(days=5),
            {'query': 'gold necklace'}
        ),
        CustomerInteraction(
            'CUST001', 'product_view',
            base_time - timedelta(days=5),
            {'product_id': 'PROD101', 'product_name': 'Gold Chain Necklace'}
        ),
        CustomerInteraction(
            'CUST001', 'product_view',
            base_time - timedelta(days=4),
            {'product_id': 'PROD102', 'product_name': 'Diamond Pendant'}
        ),
        CustomerInteraction(
            'CUST001', 'add_to_cart',
            base_time - timedelta(days=4),
            {'product_id': 'PROD101', 'quantity': 1}
        ),
        CustomerInteraction(
            'CUST001', 'purchase',
            base_time - timedelta(days=3),
            {'items': ['PROD101'], 'total_amount': 45000}
        ),
        CustomerInteraction(
            'CUST001', 'review',
            base_time - timedelta(days=1),
            {'product_id': 'PROD101', 'rating': 5, 'comment': 'Excellent quality'}
        ),
    ])
    
    # Customer 2: Browser
    interactions.extend([
        CustomerInteraction(
            'CUST002', 'page_view',
            base_time - timedelta(days=3),
            {'page': 'collections'}
        ),
        CustomerInteraction(
            'CUST002', 'product_view',
            base_time - timedelta(days=3),
            {'product_id': 'PROD103', 'product_name': 'Silver Bracelet'}
        ),
        CustomerInteraction(
            'CUST002', 'product_view',
            base_time - timedelta(days=2),
            {'product_id': 'PROD104', 'product_name': 'Gold Earrings'}
        ),
    ])
    
    # Customer 3: Frequent visitor
    interactions.extend([
        CustomerInteraction(
            'CUST003', 'page_view',
            base_time - timedelta(days=7),
            {'page': 'home'}
        ),
        CustomerInteraction(
            'CUST003', 'search',
            base_time - timedelta(days=7),
            {'query': 'engagement rings'}
        ),
        CustomerInteraction(
            'CUST003', 'product_view',
            base_time - timedelta(days=6),
            {'product_id': 'PROD105', 'product_name': 'Diamond Ring'}
        ),
        CustomerInteraction(
            'CUST003', 'add_to_cart',
            base_time - timedelta(days=6),
            {'product_id': 'PROD105', 'quantity': 1}
        ),
        CustomerInteraction(
            'CUST003', 'product_view',
            base_time - timedelta(days=5),
            {'product_id': 'PROD106', 'product_name': 'Platinum Band'}
        ),
        CustomerInteraction(
            'CUST003', 'add_to_cart',
            base_time - timedelta(days=5),
            {'product_id': 'PROD106', 'quantity': 1}
        ),
        CustomerInteraction(
            'CUST003', 'purchase',
            base_time - timedelta(days=4),
            {'items': ['PROD105', 'PROD106'], 'total_amount': 125000}
        ),
        CustomerInteraction(
            'CUST003', 'contact',
            base_time - timedelta(days=2),
            {'subject': 'Product inquiry', 'type': 'email'}
        ),
        CustomerInteraction(
            'CUST003', 'page_view',
            base_time - timedelta(hours=12),
            {'page': 'new_arrivals'}
        ),
        CustomerInteraction(
            'CUST003', 'product_view',
            base_time - timedelta(hours=12),
            {'product_id': 'PROD107', 'product_name': 'Gold Bangle'}
        ),
    ])
    
    # Customer 4: Cart abandoner
    interactions.extend([
        CustomerInteraction(
            'CUST004', 'search',
            base_time - timedelta(days=2),
            {'query': 'silver anklets'}
        ),
        CustomerInteraction(
            'CUST004', 'product_view',
            base_time - timedelta(days=2),
            {'product_id': 'PROD108', 'product_name': 'Silver Anklet'}
        ),
        CustomerInteraction(
            'CUST004', 'add_to_cart',
            base_time - timedelta(days=2),
            {'product_id': 'PROD108', 'quantity': 2}
        ),
    ])
    
    # Customer 5: Researcher
    interactions.extend([
        CustomerInteraction(
            'CUST005', 'search',
            base_time - timedelta(days=1),
            {'query': 'kundan jewelry'}
        ),
        CustomerInteraction(
            'CUST005', 'product_view',
            base_time - timedelta(days=1),
            {'product_id': 'PROD109', 'product_name': 'Kundan Necklace Set'}
        ),
        CustomerInteraction(
            'CUST005', 'product_view',
            base_time - timedelta(days=1),
            {'product_id': 'PROD110', 'product_name': 'Kundan Earrings'}
        ),
        CustomerInteraction(
            'CUST005', 'product_view',
            base_time - timedelta(hours=6),
            {'product_id': 'PROD111', 'product_name': 'Traditional Maang Tikka'}
        ),
        CustomerInteraction(
            'CUST005', 'contact',
            base_time - timedelta(hours=6),
            {'subject': 'Customization query', 'type': 'chat'}
        ),
    ])
    
    return interactions


if __name__ == '__main__':
    # Demonstration of the customer interaction summary system
    print("=" * 80)
    print("TANISHQ E-COMMERCE - Customer Interactions Summary")
    print("=" * 80)
    print()
    
    # Initialize tracker and add sample data
    tracker = InteractionTracker()
    sample_interactions = create_sample_interactions()
    tracker.add_bulk_interactions(sample_interactions)
    
    # Create summary generator
    summary_gen = InteractionSummary(tracker)
    
    # Generate and display overall summary
    print("\n" + "=" * 80)
    print("OVERALL INTERACTION SUMMARY")
    print("=" * 80)
    overall_summary = summary_gen.generate_overall_summary()
    summary_gen.print_summary(overall_summary)
    
    # Generate customer-specific summaries
    print("\n" + "=" * 80)
    print("INDIVIDUAL CUSTOMER SUMMARIES")
    print("=" * 80)
    for customer_id in ['CUST001', 'CUST002', 'CUST003']:
        print(f"\n--- Customer {customer_id} ---")
        customer_summary = summary_gen.generate_customer_summary(customer_id)
        summary_gen.print_summary(customer_summary)
    
    # Generate interaction type summary
    print("\n" + "=" * 80)
    print("INTERACTION TYPE SUMMARY - Product Views")
    print("=" * 80)
    type_summary = summary_gen.generate_interaction_type_summary('product_view')
    summary_gen.print_summary(type_summary)
    
    # Generate period summary (last 3 days)
    print("\n" + "=" * 80)
    print("PERIOD SUMMARY - Last 3 Days")
    print("=" * 80)
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    period_summary = summary_gen.generate_period_summary(start_date, end_date)
    summary_gen.print_summary(period_summary)
    
    print("\n" + "=" * 80)
    print("Summary generation complete!")
    print("=" * 80)
