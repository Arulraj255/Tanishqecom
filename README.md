# Tanishqecom - Customer Interactions Summary System

A comprehensive customer interaction tracking and summary system for the Tanishq e-commerce website. This system tracks various types of customer activities and generates detailed summaries to help understand customer behavior and engagement.

## Overview

This system helps track and analyze customer interactions on the Tanishq e-commerce platform, including:
- Page views
- Product views
- Searches
- Add to cart actions
- Purchases
- Reviews
- Customer support contacts

## Features

### 1. **Interaction Tracking**
- Track multiple types of customer interactions
- Store detailed metadata for each interaction
- Support for bulk interaction imports

### 2. **Summary Generation**
- **Overall Summary**: Complete overview of all customer interactions
  - Total interactions count
  - Unique customers
  - Interaction type breakdown
  - Customer engagement levels (high/medium/low)
  - Average interactions per customer
  
- **Customer-Specific Summary**: Detailed view of individual customer behavior
  - Total interactions
  - Interaction breakdown by type
  - Products viewed and purchased
  - Search queries
  - Engagement level
  
- **Interaction Type Summary**: Analysis of specific interaction types
  - Total count
  - Unique customers
  - Average per customer
  
- **Period Summary**: Time-based analysis
  - Interactions within a date range
  - Trend analysis capabilities

### 3. **Customer Engagement Levels**
Customers are automatically categorized based on their activity:
- **High Engagement**: 10+ interactions
- **Medium Engagement**: 5-9 interactions
- **Low Engagement**: 1-4 interactions

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/Arulraj255/Tanishqecom.git
cd Tanishqecom

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (currently no external dependencies required)
pip install -r requirements.txt
```

## Usage

### Running the Demo

The system includes sample customer interactions for demonstration:

```bash
python customer_interactions.py
```

This will generate:
1. Overall interaction summary
2. Individual customer summaries
3. Interaction type analysis
4. Period-based summary

### Using in Your Code

```python
from customer_interactions import (
    CustomerInteraction, 
    InteractionTracker, 
    InteractionSummary
)
from datetime import datetime

# Initialize the tracker
tracker = InteractionTracker()

# Add a customer interaction
interaction = CustomerInteraction(
    customer_id='CUST001',
    interaction_type='product_view',
    timestamp=datetime.now(),
    details={
        'product_id': 'PROD123',
        'product_name': 'Gold Necklace'
    }
)
tracker.add_interaction(interaction)

# Generate summaries
summary_gen = InteractionSummary(tracker)

# Get overall summary
overall = summary_gen.generate_overall_summary()
print(overall)

# Get customer-specific summary
customer = summary_gen.generate_customer_summary('CUST001')
print(customer)
```

## Interaction Types

The system supports the following interaction types:

| Type | Description | Example Details |
|------|-------------|-----------------|
| `page_view` | Customer views a page | `{'page': 'home'}` |
| `product_view` | Customer views a product | `{'product_id': 'PROD101', 'product_name': 'Gold Chain'}` |
| `search` | Customer performs a search | `{'query': 'diamond rings'}` |
| `add_to_cart` | Customer adds item to cart | `{'product_id': 'PROD101', 'quantity': 1}` |
| `purchase` | Customer completes a purchase | `{'items': ['PROD101'], 'total_amount': 45000}` |
| `review` | Customer leaves a review | `{'product_id': 'PROD101', 'rating': 5}` |
| `contact` | Customer contacts support | `{'subject': 'Query', 'type': 'email'}` |

## Sample Output

### Overall Summary
```json
{
  "summary_generated_at": "2026-02-12T05:30:00.000000",
  "total_interactions": 30,
  "unique_customers": 5,
  "date_range": {
    "earliest": "2026-02-05T05:30:00.000000",
    "latest": "2026-02-12T05:30:00.000000"
  },
  "interaction_breakdown": {
    "page_view": 8,
    "product_view": 11,
    "search": 4,
    "add_to_cart": 4,
    "purchase": 2,
    "review": 1,
    "contact": 2
  },
  "customer_engagement_levels": {
    "high": 1,
    "medium": 1,
    "low": 3
  },
  "average_interactions_per_customer": 6.0
}
```

### Customer Summary
```json
{
  "customer_id": "CUST001",
  "total_interactions": 7,
  "interaction_breakdown": {
    "page_view": 1,
    "search": 1,
    "product_view": 2,
    "add_to_cart": 1,
    "purchase": 1,
    "review": 1
  },
  "first_interaction": "2026-02-07T05:30:00.000000",
  "last_interaction": "2026-02-11T05:30:00.000000",
  "products_viewed_count": 2,
  "unique_products_viewed": 2,
  "total_purchases": 1,
  "total_items_purchased": 1,
  "search_queries_count": 1,
  "engagement_level": "medium"
}
```

## Architecture

The system consists of three main components:

1. **CustomerInteraction**: Represents a single customer interaction
   - Stores customer ID, interaction type, timestamp, and details
   - Provides serialization methods

2. **InteractionTracker**: Manages the collection of interactions
   - Add single or bulk interactions
   - Query interactions by customer, type, or time period
   - In-memory storage (can be extended to use databases)

3. **InteractionSummary**: Generates various summaries
   - Overall statistics
   - Customer-specific insights
   - Type-based analysis
   - Period-based reports

## Extending the System

### Adding Custom Interaction Types

```python
# Simply use a new interaction type when creating interactions
custom_interaction = CustomerInteraction(
    customer_id='CUST001',
    interaction_type='wishlist_add',  # New type
    timestamp=datetime.now(),
    details={'product_id': 'PROD200'}
)
```

### Persisting to Database

The system can be extended to use databases:

```python
# Example: Add database persistence
class DatabaseInteractionTracker(InteractionTracker):
    def add_interaction(self, interaction):
        super().add_interaction(interaction)
        # Add database save logic here
        # e.g., save_to_db(interaction)
```

### Integration with Web Applications

```python
# Flask example
from flask import Flask, request, jsonify
from customer_interactions import InteractionTracker, CustomerInteraction

app = Flask(__name__)
tracker = InteractionTracker()

@app.route('/track', methods=['POST'])
def track_interaction():
    data = request.json
    interaction = CustomerInteraction(
        customer_id=data['customer_id'],
        interaction_type=data['type'],
        timestamp=datetime.now(),
        details=data.get('details', {})
    )
    tracker.add_interaction(interaction)
    return jsonify({'status': 'success'})
```

## Use Cases

1. **Customer Behavior Analysis**: Understand how customers interact with the website
2. **Engagement Tracking**: Identify highly engaged vs. low-engagement customers
3. **Conversion Funnel Analysis**: Track customer journey from browsing to purchase
4. **Cart Abandonment Detection**: Identify customers who add items but don't purchase
5. **Product Interest Analysis**: See which products get the most views
6. **Search Analysis**: Understand what customers are looking for
7. **Customer Support Insights**: Track support interactions and common queries

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is part of Tanishq e-commerce lead management system.

## Contact

For questions or support, please open an issue in the repository.
