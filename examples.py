"""
Example usage of the Customer Interactions Summary System

This script demonstrates various ways to use the customer interaction tracking
and summary generation system.
"""

from customer_interactions import (
    CustomerInteraction,
    InteractionTracker,
    InteractionSummary,
    create_sample_interactions
)
from datetime import datetime, timedelta


def example_basic_usage():
    """Example: Basic interaction tracking and summary generation"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70)
    
    # Create a tracker
    tracker = InteractionTracker()
    
    # Add some interactions
    tracker.add_interaction(CustomerInteraction(
        customer_id='CUST100',
        interaction_type='page_view',
        timestamp=datetime.now(),
        details={'page': 'home'}
    ))
    
    tracker.add_interaction(CustomerInteraction(
        customer_id='CUST100',
        interaction_type='search',
        timestamp=datetime.now(),
        details={'query': 'gold bangles'}
    ))
    
    tracker.add_interaction(CustomerInteraction(
        customer_id='CUST100',
        interaction_type='product_view',
        timestamp=datetime.now(),
        details={'product_id': 'PROD999', 'product_name': 'Traditional Gold Bangle'}
    ))
    
    # Generate summary
    summary_gen = InteractionSummary(tracker)
    overall = summary_gen.generate_overall_summary()
    
    print("\nOverall Summary:")
    summary_gen.print_summary(overall)


def example_customer_journey():
    """Example: Tracking a complete customer journey"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Customer Journey Tracking")
    print("=" * 70)
    
    tracker = InteractionTracker()
    customer_id = 'CUST200'
    
    # Simulate a customer journey
    journey_steps = [
        ('page_view', {'page': 'home'}, 'Customer lands on homepage'),
        ('search', {'query': 'diamond earrings'}, 'Customer searches for product'),
        ('product_view', {'product_id': 'PROD201', 'product_name': 'Diamond Studs'}, 'Views first product'),
        ('product_view', {'product_id': 'PROD202', 'product_name': 'Diamond Drops'}, 'Views second product'),
        ('add_to_cart', {'product_id': 'PROD201', 'quantity': 1}, 'Adds to cart'),
        ('page_view', {'page': 'cart'}, 'Views cart'),
        ('purchase', {'items': ['PROD201'], 'total_amount': 35000}, 'Completes purchase'),
    ]
    
    base_time = datetime.now() - timedelta(hours=1)
    
    print("\nCustomer Journey:")
    for i, (interaction_type, details, description) in enumerate(journey_steps):
        timestamp = base_time + timedelta(minutes=i*5)
        tracker.add_interaction(CustomerInteraction(
            customer_id=customer_id,
            interaction_type=interaction_type,
            timestamp=timestamp,
            details=details
        ))
        print(f"  {i+1}. [{timestamp.strftime('%H:%M:%S')}] {description} ({interaction_type})")
    
    # Generate customer summary
    summary_gen = InteractionSummary(tracker)
    customer_summary = summary_gen.generate_customer_summary(customer_id)
    
    print("\nCustomer Summary:")
    summary_gen.print_summary(customer_summary)


def example_engagement_analysis():
    """Example: Analyzing customer engagement levels"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Customer Engagement Analysis")
    print("=" * 70)
    
    tracker = InteractionTracker()
    
    # Add sample interactions with different engagement levels
    tracker.add_bulk_interactions(create_sample_interactions())
    
    summary_gen = InteractionSummary(tracker)
    overall = summary_gen.generate_overall_summary()
    
    print("\nEngagement Level Distribution:")
    engagement = overall['customer_engagement_levels']
    print(f"  High Engagement (10+ interactions): {engagement['high']} customers")
    print(f"  Medium Engagement (5-9 interactions): {engagement['medium']} customers")
    print(f"  Low Engagement (1-4 interactions): {engagement['low']} customers")
    
    print(f"\nTotal Customers: {overall['unique_customers']}")
    print(f"Average Interactions per Customer: {overall['average_interactions_per_customer']}")


def example_time_based_analysis():
    """Example: Analyzing interactions over different time periods"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Time-Based Analysis")
    print("=" * 70)
    
    tracker = InteractionTracker()
    tracker.add_bulk_interactions(create_sample_interactions())
    
    summary_gen = InteractionSummary(tracker)
    
    # Last 24 hours
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    print("\nLast 24 Hours Summary:")
    recent_summary = summary_gen.generate_period_summary(start_date, end_date)
    summary_gen.print_summary(recent_summary)
    
    # Last 7 days
    start_date = end_date - timedelta(days=7)
    
    print("\nLast 7 Days Summary:")
    weekly_summary = summary_gen.generate_period_summary(start_date, end_date)
    summary_gen.print_summary(weekly_summary)


def example_interaction_type_analysis():
    """Example: Analyzing specific interaction types"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Interaction Type Analysis")
    print("=" * 70)
    
    tracker = InteractionTracker()
    tracker.add_bulk_interactions(create_sample_interactions())
    
    summary_gen = InteractionSummary(tracker)
    
    # Analyze different interaction types
    interaction_types = ['product_view', 'purchase', 'add_to_cart', 'search']
    
    print("\nInteraction Type Breakdown:")
    for itype in interaction_types:
        print(f"\n--- {itype.upper().replace('_', ' ')} ---")
        type_summary = summary_gen.generate_interaction_type_summary(itype)
        summary_gen.print_summary(type_summary)


def example_conversion_funnel():
    """Example: Analyzing conversion funnel"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Conversion Funnel Analysis")
    print("=" * 70)
    
    tracker = InteractionTracker()
    tracker.add_bulk_interactions(create_sample_interactions())
    
    summary_gen = InteractionSummary(tracker)
    overall = summary_gen.generate_overall_summary()
    
    breakdown = overall['interaction_breakdown']
    
    print("\nConversion Funnel:")
    print(f"  1. Product Views: {breakdown.get('product_view', 0)}")
    print(f"  2. Add to Cart: {breakdown.get('add_to_cart', 0)}")
    print(f"  3. Purchases: {breakdown.get('purchase', 0)}")
    
    if breakdown.get('product_view', 0) > 0:
        cart_rate = (breakdown.get('add_to_cart', 0) / breakdown['product_view']) * 100
        print(f"\n  Add-to-Cart Rate: {cart_rate:.1f}%")
    
    if breakdown.get('add_to_cart', 0) > 0:
        purchase_rate = (breakdown.get('purchase', 0) / breakdown['add_to_cart']) * 100
        print(f"  Purchase Conversion Rate: {purchase_rate:.1f}%")
    
    if breakdown.get('product_view', 0) > 0:
        overall_rate = (breakdown.get('purchase', 0) / breakdown['product_view']) * 100
        print(f"  Overall Conversion Rate: {overall_rate:.1f}%")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("TANISHQ E-COMMERCE - Customer Interactions Examples")
    print("=" * 70)
    
    # Run all examples
    example_basic_usage()
    example_customer_journey()
    example_engagement_analysis()
    example_time_based_analysis()
    example_interaction_type_analysis()
    example_conversion_funnel()
    
    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
