import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    # Load the dataset
    data=pd.read_csv(r'C:\Users\HP\Documents\streamlit_project\cosmetics.csv')
    return data

# Filter and recommend products
def recommend_products(data, skin_type, product_type, price_range, specific_ingredient):
    # Filter by skin type
    filtered_data = data[data[skin_type] == 1]

    # Filter by product type
    filtered_data = filtered_data[filtered_data['Label'].str.contains(product_type, case=False)]

    # Filter by price range
    filtered_data = filtered_data[
        (filtered_data['Price'] >= price_range[0]) & (filtered_data['Price'] <= price_range[1])
    ]

    # Filter by specific ingredient, if provided
    if specific_ingredient:
        filtered_data = filtered_data[
            filtered_data['Ingredients'].str.contains(specific_ingredient, case=False, na=False)
        ]

    # Sort by rank and return top 5 products
    top_products = filtered_data.sort_values(by='Rank', ascending=False).head(5)
    return top_products

# Main app
def main():
    st.title("Skincare Product Recommendation System")

    # Load data
    data = load_data()

    # User Inputs
    st.sidebar.header("Input Preferences")
    skin_type = st.sidebar.selectbox(
        "Select Skin Type", ["Combination", "Dry", "Normal", "Oily", "Sensitive"]
    )
    product_type = st.sidebar.selectbox(
        "Select Product Type", ["Moisturizer", "Cleanser", "Treatment", "Eye cream", "Face Mask", "Sun protect"]
    )
    price_range = st.sidebar.slider("Select Price Range", min_value=0, max_value=500, value=(50, 200))
    specific_ingredient = st.sidebar.text_input("Specific Ingredient (optional)")

    # Get recommendations
    top_products = recommend_products(data, skin_type, product_type, price_range, specific_ingredient)

    # Display recommendations
    st.subheader("Top 5 Product Recommendations")
    if not top_products.empty:
        st.table(top_products[['Label', 'Brand', 'Name', 'Price', 'Rank', 'Ingredients']])
    else:
        st.write("No products found matching your criteria.")

# Run the app
if __name__ == "__main__":
    main()
