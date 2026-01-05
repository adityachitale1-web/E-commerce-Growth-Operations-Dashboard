"""
SouqPlus Executive Dashboard
A production-ready analytics dashboard for UAE e-commerce operations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# Page configuration
st.set_page_config(
    page_title="SouqPlus Executive Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for black background theme with white chart backgrounds
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #0e1117;
        padding: 0rem 1rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1d24;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #1a1d24;
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric label {
        color: #f0f0f0 !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 1.8rem !important;
        font-weight: bold;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #ffd700 !important;
    }
    
    /* Headers */
    h1 {
        color: #ffffff;
        padding-bottom: 10px;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    h2 {
        color: #e0e0e0;
        font-size: 1.4rem;
        padding-top: 10px;
        font-weight: 600;
    }
    
    h3 {
        color: #d0d0d0;
    }
    
    /* Text color */
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        padding: 15px;
        border-left: 5px solid #e17055;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        color: #2d3436;
        font-weight: 500;
    }
    
    /* Tabs */
    div[data-testid="stTabs"] {
        background-color: #1a1d24;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0e1117;
        border-radius: 8px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #262730;
        color: #e0e0e0;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Chart containers - WHITE BACKGROUND */
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Divider */
    hr {
        border-color: #333;
    }
    
    /* Selectbox and multiselect */
    .stSelectbox, .stMultiSelect {
        color: #e0e0e0;
    }
    
    .stSelectbox > div > div {
        background-color: #262730;
        color: #e0e0e0;
    }
    
    .stMultiSelect > div > div {
        background-color: #262730;
        color: #e0e0e0;
    }
    
    /* Date input */
    .stDateInput > div > div > input {
        background-color: #262730;
        color: #e0e0e0;
    }
    
    /* Info box */
    .stAlert {
        background-color: #1a1d24;
        color: #e0e0e0;
        border: 1px solid #667eea;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Dataframe */
    .dataframe {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* Footer */
    footer {
        background-color: #0e1117;
        color: #7f8c8d;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0e1117;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    </style>
    """, unsafe_allow_html=True)


def apply_light_theme(fig, height=400):
    """Apply light theme to plotly figure with BLACK text"""
    fig.update_layout(
        height=height,
        paper_bgcolor='#ffffff',
        plot_bgcolor='#f8f9fa',
        font=dict(color='#000000', size=12, family='Arial, sans-serif'),
        xaxis=dict(
            gridcolor='#e0e0e0',
            linecolor='#cccccc',
            zerolinecolor='#cccccc',
            tickfont=dict(color='#000000', size=11)
        ),
        yaxis=dict(
            gridcolor='#e0e0e0',
            linecolor='#cccccc',
            zerolinecolor='#cccccc',
            tickfont=dict(color='#000000', size=11)
        ),
        title_font=dict(color='#000000', size=16, family='Arial, sans-serif'),
        legend=dict(
            bgcolor='#ffffff',
            bordercolor='#cccccc',
            font=dict(color='#000000', size=11)
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='#ffffff',
            font_size=12,
            font_family='Arial, sans-serif',
            font_color='#000000'
        )
    )
    return fig


def load_order_items():
    """Load order_items.csv with special handling for quoted lines"""
    
    # Determine file path
    file_paths = ['data/order_items.csv', 'order_items.csv']
    content = None
    
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
            break
        except FileNotFoundError:
            continue
    
    if content is None:
        raise FileNotFoundError("order_items.csv not found in root or data/ folder")
    
    lines = content.strip().split('\n')
    cleaned_lines = [line.strip().strip('"') for line in lines]
    cleaned_content = '\n'.join(cleaned_lines)
    return pd.read_csv(io.StringIO(cleaned_content))


@st.cache_data
def load_data():
    """Load and prepare all data with proper date parsing"""
    try:
        # Define possible file locations
        data_files = {
            'customers': ['data/customers.csv', 'customers.csv'],
            'orders': ['data/orders.csv', 'orders.csv'],
            'fulfillment': ['data/fulfillment.csv', 'fulfillment.csv', 'data/fullfillment.csv', 'fullfillment.csv'],
            'returns': ['data/returns.csv', 'returns.csv']
        }
        
        # Load customers
        customers = None
        for path in data_files['customers']:
            try:
                customers = pd.read_csv(path)
                break
            except FileNotFoundError:
                continue
        
        if customers is None:
            raise FileNotFoundError("customers.csv not found")
        
        # Load orders
        orders = None
        for path in data_files['orders']:
            try:
                orders = pd.read_csv(path, parse_dates=['order_date'])
                break
            except FileNotFoundError:
                continue
        
        if orders is None:
            raise FileNotFoundError("orders.csv not found")
        
        # Load order_items
        order_items = load_order_items()
        
        # Load fulfillment
        fulfillment = None
        for path in data_files['fulfillment']:
            try:
                fulfillment = pd.read_csv(path, parse_dates=['actual_delivery_date'])
                break
            except FileNotFoundError:
                continue
        
        if fulfillment is None:
            raise FileNotFoundError("fulfillment.csv not found")
        
        # Load returns
        returns = None
        for path in data_files['returns']:
            try:
                returns = pd.read_csv(path, parse_dates=['return_date'])
                break
            except FileNotFoundError:
                continue
        
        if returns is None:
            raise FileNotFoundError("returns.csv not found")
        
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
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("""
        **Troubleshooting:**
        - Ensure all CSV files are uploaded to your repository
        - Files should be in either root directory or 'data/' folder
        - Required files: customers.csv, orders.csv, order_items.csv, fulfillment.csv, returns.csv
        """)
        return None, None, None, None, None, None


def format_currency(value):
    """Format value as AED currency"""
    return f"AED {value:,.0f}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.1f}%"


def create_insight_box(text):
    """Create a styled insight box"""
    st.markdown(f'<div class="insight-box">💡 <strong>Insight:</strong> {text}</div>', 
                unsafe_allow_html=True)


def apply_filters(df, date_range, cities, channels):
    """Apply sidebar filters to dataframe"""
    filtered_df = df.copy()
    
    # Date filter
    if date_range:
        filtered_df = filtered_df[
            (filtered_df['order_date'].dt.date >= date_range[0]) &
            (filtered_df['order_date'].dt.date <= date_range[1])
        ]
    
    # City filter
    if cities and 'All' not in cities:
        filtered_df = filtered_df[filtered_df['city'].isin(cities)]
    
    # Channel filter
    if channels and 'All' not in channels:
        filtered_df = filtered_df[filtered_df['order_channel'].isin(channels)]
    
    return filtered_df


def executive_view(df):
    """Executive View: Revenue, Growth, and Strategic Insights"""
    
    st.header("📊 Executive View")
    st.markdown("---")
    
    # KPIs Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_revenue = df['net_amount'].sum()
        st.metric("Total Revenue", format_currency(total_revenue))
    
    with col2:
        total_orders = df['order_id'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col3:
        aov = total_revenue / total_orders if total_orders > 0 else 0
        st.metric("Average Order Value", format_currency(aov))
    
    with col4:
        total_discount = df['discount_amount'].sum()
        st.metric("Total Discount Given", format_currency(total_discount))
    
    with col5:
        total_refund = df['refund_amount'].sum()
        st.metric("Total Refund Amount", format_currency(total_refund))
    
    st.markdown("---")
    
        # Revenue Trend - Weekly and Monthly
    st.subheader("📈 Revenue Trend Analysis")
    
    # Create two columns for weekly and monthly trends
    col1, col2 = st.columns(2)
    
    with col1:
        # Weekly Revenue Trend
        df['week'] = df['order_date'].dt.to_period('W').apply(lambda r: r.start_time)
        weekly_revenue = df.groupby('week')['net_amount'].sum().reset_index()
        weekly_revenue.columns = ['Week', 'Revenue']
        
        fig_weekly = px.line(
            weekly_revenue, 
            x='Week', 
            y='Revenue',
            title='Weekly Revenue Trend (AED)',
            labels={'Revenue': 'Revenue (AED)', 'Week': 'Week Starting'}
        )
        fig_weekly.update_traces(
            line_color='#3498db', 
            line_width=3,
            mode='lines+markers',
            marker=dict(size=8)
        )
        fig_weekly.update_layout(
            hovermode='x unified', 
            height=400,
            xaxis_title="Week Starting",
            yaxis_title="Revenue (AED)"
        )
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    with col2:
        # Monthly Revenue Trend
        df['month'] = df['order_date'].dt.to_period('M').apply(lambda r: r.start_time)
        monthly_revenue = df.groupby('month')['net_amount'].sum().reset_index()
        monthly_revenue.columns = ['Month', 'Revenue']
        
        fig_monthly = px.bar(
            monthly_revenue, 
            x='Month', 
            y='Revenue',
            title='Monthly Revenue Trend (AED)',
            labels={'Revenue': 'Revenue (AED)', 'Month': 'Month'}
        )
        fig_monthly.update_traces(
            marker_color='#2ecc71',
            marker_line_color='#27ae60',
            marker_line_width=1.5
        )
        fig_monthly.update_layout(
            hovermode='x unified', 
            height=400,
            xaxis_title="Month",
            yaxis_title="Revenue (AED)"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    create_insight_box("Weekly trends reveal short-term patterns and campaign impacts, while monthly trends show overall business trajectory and seasonality.")
    
    st.markdown("---")
    
    # Two columns for next row
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by City
        st.subheader("🏙️ Revenue by City")
        city_revenue = df.groupby('city')['net_amount'].sum().reset_index()
        city_revenue = city_revenue.sort_values('net_amount', ascending=True)
        
        fig_city = px.bar(
            city_revenue,
            x='net_amount',
            y='city',
            orientation='h',
            title='Revenue Distribution by City (AED)',
            labels={'net_amount': 'Revenue (AED)', 'city': 'City'}
        )
        fig_city.update_traces(marker_color='#2ecc71', textfont=dict(color='#000000'))
        fig_city = apply_light_theme(fig_city, height=350)
        st.plotly_chart(fig_city, use_container_width=True)
        
        create_insight_box("Focus marketing efforts on high-performing cities while exploring growth opportunities in underperforming regions.")
    
    with col2:
        # Revenue by Order Channel
        st.subheader("📱 Revenue by Order Channel")
        channel_revenue = df.groupby('order_channel')['net_amount'].sum().reset_index()
        
        fig_channel = px.pie(
            channel_revenue,
            values='net_amount',
            names='order_channel',
            title='Revenue Share by Order Channel',
            hole=0.4
        )
        fig_channel.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(color='#ffffff', size=13),
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        fig_channel.update_layout(
            height=350,
            paper_bgcolor='#ffffff',
            font=dict(color='#000000', size=12),
            title_font=dict(color='#000000', size=16),
            legend=dict(bgcolor='#ffffff', font=dict(color='#000000'))
        )
        st.plotly_chart(fig_channel, use_container_width=True)
        
        create_insight_box("Optimize investment in channels with highest revenue contribution and customer acquisition cost efficiency.")
    
    # Two columns for category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by Product Category
        st.subheader("🏷️ Revenue by Product Category")
        category_revenue = df.groupby('product_category')['net_amount'].sum().reset_index()
        category_revenue = category_revenue.sort_values('net_amount', ascending=True)
        
        fig_category = px.bar(
            category_revenue,
            x='net_amount',
            y='product_category',
            orientation='h',
            title='Revenue by Product Category (AED)',
            labels={'net_amount': 'Revenue (AED)', 'product_category': 'Category'}
        )
        fig_category.update_traces(marker_color='#3498db', textfont=dict(color='#000000'))
        fig_category = apply_light_theme(fig_category, height=350)
        st.plotly_chart(fig_category, use_container_width=True)
        
        create_insight_box("Top categories drive majority of revenue. Consider cross-selling strategies to boost lower-performing categories.")
    
    with col2:
        # Discount % by Category (Margin Proxy)
        st.subheader("💰 Discount % by Category (Margin Proxy)")
        category_discount = df.groupby('product_category').agg({
            'discount_amount': 'sum',
            'net_amount': 'sum'
        }).reset_index()
        category_discount['discount_pct'] = (
            category_discount['discount_amount'] / 
            (category_discount['net_amount'] + category_discount['discount_amount']) * 100
        )
        category_discount = category_discount.sort_values('discount_pct', ascending=True)
        
        fig_discount = px.bar(
            category_discount,
            x='discount_pct',
            y='product_category',
            orientation='h',
            title='Discount % by Category',
            labels={'discount_pct': 'Discount %', 'product_category': 'Category'},
            color='discount_pct',
            color_continuous_scale='Reds'
        )
        fig_discount = apply_light_theme(fig_discount, height=350)
        st.plotly_chart(fig_discount, use_container_width=True)
        
        create_insight_box("High discount categories may indicate pricing pressure or promotional intensity. Monitor for margin impact.")


def operations_view(df, fulfillment, returns):
    """Operations View: Fulfillment, Delivery Performance, Returns"""
    
    st.header("🚚 Operations View")
    st.markdown("---")
    
    # Calculate operational KPIs
    total_deliveries = df['delivery_status'].notna().sum()
    on_time = (df['delivery_status'] == 'On Time').sum()
    delayed = (df['delivery_status'] == 'Delayed').sum()
    failed = (df['delivery_status'] == 'Failed').sum()
    
    on_time_pct = (on_time / total_deliveries * 100) if total_deliveries > 0 else 0
    delayed_pct = (delayed / total_deliveries * 100) if total_deliveries > 0 else 0
    failed_pct = (failed / total_deliveries * 100) if total_deliveries > 0 else 0
    
    total_items = len(df)
    returned_items = (df['refund_amount'] > 0).sum()
    return_rate = (returned_items / total_items * 100) if total_items > 0 else 0
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("On-time Delivery %", format_percentage(on_time_pct), 
                 delta="Good" if on_time_pct >= 80 else "Needs Attention",
                 delta_color="normal" if on_time_pct >= 80 else "inverse")
    
    with col2:
        st.metric("Delayed Delivery %", format_percentage(delayed_pct),
                 delta="High" if delayed_pct > 15 else "Acceptable",
                 delta_color="inverse" if delayed_pct > 15 else "normal")
    
    with col3:
        st.metric("Failed Delivery %", format_percentage(failed_pct),
                 delta="Critical" if failed_pct > 5 else "Acceptable",
                 delta_color="inverse" if failed_pct > 5 else "normal")
    
    with col4:
        st.metric("Return Rate %", format_percentage(return_rate),
                 delta="High" if return_rate > 10 else "Normal",
                 delta_color="inverse" if return_rate > 10 else "normal")
    
    st.markdown("---")
    
    # Delivery Status Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Delivery Status Distribution")
        status_counts = df['delivery_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        fig_status = px.pie(
            status_counts,
            values='Count',
            names='Status',
            title='Delivery Status Breakdown',
            color='Status',
            color_discrete_map={
                'On Time': '#2ecc71',
                'Delayed': '#f39c12',
                'Failed': '#e74c3c'
            }
        )
        fig_status.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(color='#ffffff', size=13),
            marker=dict(line=dict(color='#ffffff', width=2))
        )
        fig_status.update_layout(
            height=350,
            paper_bgcolor='#ffffff',
            font=dict(color='#000000'),
            title_font=dict(color='#000000'),
            legend=dict(bgcolor='#ffffff', font=dict(color='#000000'))
        )
        st.plotly_chart(fig_status, use_container_width=True)
        
        create_insight_box("Monitor failed deliveries closely - they directly impact customer satisfaction and operational costs.")
    
    with col2:
        st.subheader("⏱️ On-time vs Delayed by Warehouse Hub")
        hub_performance = df[df['delivery_status'].isin(['On Time', 'Delayed'])].groupby(
            ['warehouse_hub', 'delivery_status']
        ).size().reset_index(name='Count')
        
        fig_hub = px.bar(
            hub_performance,
            x='warehouse_hub',
            y='Count',
            color='delivery_status',
            title='Delivery Performance by Warehouse Hub',
            labels={'warehouse_hub': 'Warehouse Hub', 'Count': 'Number of Orders'},
            color_discrete_map={
                'On Time': '#2ecc71',
                'Delayed': '#e74c3c'
            },
            barmode='group'
        )
        fig_hub = apply_light_theme(fig_hub, height=350)
        st.plotly_chart(fig_hub, use_container_width=True)
        
        create_insight_box("Identify underperforming hubs for capacity planning and process improvement initiatives.")
    
    # Delays and Reasons
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Delays by Delivery Zone")
        delayed_df = df[df['delivery_status'] == 'Delayed']
        zone_delays = delayed_df['delivery_zone'].value_counts().reset_index()
        zone_delays.columns = ['Zone', 'Delayed Orders']
        zone_delays = zone_delays.sort_values('Delayed Orders', ascending=True)
        
        fig_zone = px.bar(
            zone_delays,
            x='Delayed Orders',
            y='Zone',
            orientation='h',
            title='Delayed Deliveries by Zone',
            labels={'Delayed Orders': 'Number of Delays', 'Zone': 'Delivery Zone'}
        )
        fig_zone.update_traces(marker_color='#e67e22', textfont=dict(color='#000000'))
        fig_zone = apply_light_theme(fig_zone, height=350)
        st.plotly_chart(fig_zone, use_container_width=True)
        
        create_insight_box("High-delay zones may need route optimization or additional delivery partners.")
    
    with col2:
        st.subheader("⚠️ Top Delay Reasons")
        delay_reasons = df[df['delivery_status'] == 'Delayed']['delay_reason'].value_counts().head(10).reset_index()
        delay_reasons.columns = ['Reason', 'Count']
        delay_reasons = delay_reasons.sort_values('Count', ascending=True)
        
        fig_reasons = px.bar(
            delay_reasons,
            x='Count',
            y='Reason',
            orientation='h',
            title='Top 10 Reasons for Delivery Delays',
            labels={'Count': 'Number of Incidents', 'Reason': 'Delay Reason'}
        )
        fig_reasons.update_traces(marker_color='#c0392b', textfont=dict(color='#000000'))
        fig_reasons = apply_light_theme(fig_reasons, height=350)
        st.plotly_chart(fig_reasons, use_container_width=True)
        
        create_insight_box("Address top delay reasons systematically to improve overall delivery performance.")
    
    # Returns Analysis
    st.subheader("🔄 Returns Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        returns_by_category = df[df['refund_amount'] > 0].groupby('product_category').size().reset_index(name='Returns')
        returns_by_category = returns_by_category.sort_values('Returns', ascending=True)
        
        fig_returns_cat = px.bar(
            returns_by_category,
            x='Returns',
            y='product_category',
            orientation='h',
            title='Returns by Product Category',
            labels={'Returns': 'Number of Returns', 'product_category': 'Category'}
        )
        fig_returns_cat.update_traces(marker_color='#8e44ad', textfont=dict(color='#000000'))
        fig_returns_cat = apply_light_theme(fig_returns_cat, height=350)
        st.plotly_chart(fig_returns_cat, use_container_width=True)
        
        create_insight_box("High return rates in specific categories may signal quality issues or sizing problems.")
    
    with col2:
        returns_by_city = df[df['refund_amount'] > 0].groupby('city').size().reset_index(name='Returns')
        returns_by_city = returns_by_city.sort_values('Returns', ascending=True)
        
        fig_returns_city = px.bar(
            returns_by_city,
            x='Returns',
            y='city',
            orientation='h',
            title='Returns by City',
            labels={'Returns': 'Number of Returns', 'city': 'City'}
        )
        fig_returns_city.update_traces(marker_color='#16a085', textfont=dict(color='#000000'))
        fig_returns_city = apply_light_theme(fig_returns_city, height=350)
        st.plotly_chart(fig_returns_city, use_container_width=True)
        
        create_insight_box("Geographic return patterns can reveal logistics or customer expectation issues in specific markets.")


def main():
    """Main application entry point"""
    
    # Header
    st.title("🛍️ SouqPlus Executive Dashboard")
    st.markdown("**Real-time insights for data-driven decision making**")
    
    # Load data
    with st.spinner("Loading data..."):
        orders_full, customers, orders, order_items, fulfillment, returns = load_data()
    
    if orders_full is None:
        st.error("Failed to load data. Please ensure all CSV files are in the correct location.")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("---")
    
    # Date range filter
    min_date = orders_full['order_date'].min().date()
    max_date = orders_full['order_date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Ensure date_range is a tuple with two dates
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range
    
    # City filter
    all_cities = ['All'] + sorted(orders_full['city'].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect(
        "Select Cities",
        options=all_cities,
        default=['All']
    )
    
    # Channel filter
    all_channels = ['All'] + sorted(orders_full['order_channel'].dropna().unique().tolist())
    selected_channels = st.sidebar.multiselect(
        "Select Order Channels",
        options=all_channels,
        default=['All']
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='background-color: #1a1d24; padding: 15px; border-radius: 10px; border: 1px solid #667eea;'>
    <h4 style='color: #667eea; margin-top: 0;'>📊 About this Dashboard</h4>
    <p style='color: #e0e0e0; font-size: 0.9rem;'>
    This dashboard provides real-time insights into SouqPlus operations across the UAE.
    </p>
    <ul style='color: #e0e0e0; font-size: 0.85rem;'>
    <li><strong>Executive View:</strong> Revenue, growth, and strategic metrics</li>
    <li><strong>Operations View:</strong> Fulfillment, delivery, and returns analysis</li>
    </ul>
    <p style='color: #a0a0a0; font-size: 0.8rem; margin-bottom: 0;'>
    Use filters to drill down into specific periods, cities, or channels.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = apply_filters(orders_full, (start_date, end_date), selected_cities, selected_channels)
    
    # Show filter summary
    st.markdown(f"**Showing data from {start_date} to {end_date}** | "
               f"**{len(filtered_df):,} order items** | "
               f"**{filtered_df['order_id'].nunique():,} unique orders**")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Executive View", "🚚 Operations View"])
    
    with tab1:
        executive_view(filtered_df)
    
    with tab2:
        operations_view(filtered_df, fulfillment, returns)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #7f8c8d;'>"
        "SouqPlus Executive Dashboard | Built with Streamlit | "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
