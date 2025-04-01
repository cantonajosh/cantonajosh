import streamlit as st
from collections import Counter

def analyze_sales(items):
    """
    Analyzes the sales data and provides the required output.
    
    Parameters:
    items (list): A list of items sold.
    
    Returns:
    dict: Analysis results containing:
        - num_products: Number of unique products
        - product_counts: Counter object with quantities
        - most_sold: Most sold product (name, count)
    """
    # (a) Number of unique products sold
    num_products = len(set(items))
    
    # (b) Quantity of each product sold
    product_counter = Counter(items)
    
    # (c) The product that was sold the most
    most_sold_product = product_counter.most_common(1)[0]
    
    return {
        'num_products': num_products,
        'product_counts': product_counter,
        'most_sold': most_sold_product
    }

# Streamlit UI
st.title("Sales Data Analysis")
st.write("Enter the items sold (comma-separated) to analyze sales data")

# Input field
user_input = st.text_input("Items sold:", "apple, banana, apple, orange, banana, apple")

# Clean and process input
if user_input:
    # Remove parentheses if present and clean items
    cleaned_input = user_input.replace("(", "").replace(")", "")
    items_list = [item.strip() for item in cleaned_input.split(",") if item.strip()]
    
    if items_list:
        # Analyze the data
        results = analyze_sales(items_list)
        
        # Display results
        st.subheader("Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Unique Products", results['num_products'])
        
        with col2:
            st.metric("Most Sold Product", results['most_sold'][0])
        
        with col3:
            st.metric("Times Sold", results['most_sold'][1])
        
        st.subheader("Product Counts")
        st.write(results['product_counts'])
        
        # Optional: Show as a bar chart
        if st.checkbox("Show as chart"):
            st.bar_chart(results['product_counts'])
    else:
        st.warning("Please enter at least one item")
