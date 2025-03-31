import streamlit as st
import requests
import time
import os
from datetime import datetime
from collections import Counter

def analyze_sales(items):
    """
    Analyzes the sales data and provides the required output.
    
    Parameters:
    items (list): A list of items sold.
    
    Returns:
    None
    """
    # (a) Number of unique products sold
    num_products = len(set(items))
    print(f"Number of products sold is {num_products}")
    
    # (b) Quantity of each product sold
    product_counter = Counter(items)
    print(f"Counter({product_counter})")
    
    # (c) The product that was sold the most
    most_sold_product = product_counter.most_common(1)[0][0]
    print(f"The Product sold the most is {most_sold_product}")

# Main program
if __name__ == "__main__":
    # Accept input from the user
    items_sold = input("Enter the list of items sold (comma-separated): ")
    
  
    items_sold = items_sold.replace("(", "").replace(")", "")
    
    items_sold = [item.strip() for item in items_sold.split(",")]
    
    analyze_sales(items_sold)
