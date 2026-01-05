def load_order_items():
    """Load order_items.csv with special handling for quoted lines"""
    import io
    try:
        # Try with data/ folder first
        with open('data/order_items.csv', 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        # Fallback to root directory
        with open('order_items.csv', 'r', encoding='utf-8-sig') as f:
            content = f.read()
    
    lines = content.strip().split('\n')
    cleaned_lines = [line.strip().strip('"') for line in lines]
    cleaned_content = '\n'.join(cleaned_lines)
    return pd.read_csv(io.StringIO(cleaned_content))


@st.cache_data
def load_data():
    """Load and prepare all data with proper date parsing"""
    try:
        # Try loading from data/ folder first, then fallback to root
        try:
            customers = pd.read_csv('data/customers.csv')
            orders = pd.read_csv('data/orders.csv', parse_dates=['order_date'])
            order_items = load_order_items()
            fulfillment = pd.read_csv('data/fulfillment.csv', parse_dates=['actual_delivery_date'])
            returns = pd.read_csv('data/returns.csv', parse_dates=['return_date'])
        except FileNotFoundError:
            # Fallback to root directory
            customers = pd.read_csv('customers.csv')
            orders = pd.read_csv('orders.csv', parse_dates=['order_date'])
            order_items = load_order_items()
            fulfillment = pd.read_csv('fulfillment.csv', parse_dates=['actual_delivery_date'])
            returns = pd.read_csv('returns.csv', parse_dates=['return_date'])
        
        # Merge orders with order_items to get complete order data
        orders_full = orders.merge(order_items, on='order_id', how='left')
        
        # Merge with fulfillment data
        orders_full = orders_full.merge(
            fulfillment[['order_id', 'delivery_status', 'actual_delivery_date', 
                        'warehouse_hub', 'delivery_zone', 'delay_reason']],
            on='order_id', 
            how='left'
        )
        
        # Merge with customer data
        orders_full = orders_full.merge(
            customers[['customer_id', 'city']],
            on='customer_id',
            how='left'
        )
        
        # Merge with returns data
        returns_agg = returns.groupby('order_id').agg({
            'refund_amount': 'sum',
            'return_date': 'first'
        }).reset_index()
        
        orders_full = orders_full.merge(
            returns_agg,
            on='order_id',
            how='left'
        )
        
        # Fill NaN values
        orders_full['refund_amount'] = orders_full['refund_amount'].fillna(0)
        orders_full['discount_amount'] = orders_full['discount_amount'].fillna(0)
        orders_full['delay_reason'] = orders_full['delay_reason'].fillna('No Delay')
        
        return orders_full, customers, orders, order_items, fulfillment, returns
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure CSV files are in either the root directory or 'data/' folder")
        return None, None, None, None, None, None
