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
    
    # Monthly Revenue Trend
    st.subheader("📈 Monthly Revenue Trend")
    
    # Create month column from order_date
    df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
    monthly_revenue = df.groupby('year_month')['net_amount'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('year_month')
    monthly_revenue.columns = ['Month', 'Revenue']
    
    # Check if we have data
    if len(monthly_revenue) > 0:
        # Create the line chart with markers
        fig_monthly = px.line(
            monthly_revenue, 
            x='Month', 
            y='Revenue',
            title='Monthly Revenue Trend (AED)',
            labels={'Revenue': 'Revenue (AED)', 'Month': 'Month'},
            markers=True
        )
        fig_monthly.update_traces(
            line_color='#667eea', 
            line_width=3,
            marker=dict(size=10, color='#667eea', line=dict(width=2, color='#ffffff'))
        )
        fig_monthly = apply_light_theme(fig_monthly, height=400)
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        create_insight_box("Track monthly revenue patterns to identify seasonal trends and plan strategic initiatives accordingly.")
    else:
        st.warning("No monthly revenue data available for the selected filters.")
    
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
