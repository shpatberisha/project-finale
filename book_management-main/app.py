import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

load_dotenv()
# Define the base URL of the FastAPI application
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000/api')

st.set_page_config(page_title="Nike Sneakers Management", page_icon="👟", layout="wide")

api_key_input = st.text_input("Enter API Key", type="password")


def validate_api_key(api_key):
    headers = {"api-key": api_key}
    response = requests.get(f"{BASE_URL}/validate_key/", headers=headers)
    return response.status_code == 200


# Helper functions for API communication
def get_brands():
    response = requests.get(f"{BASE_URL}/brands/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch brands.")
        return []


def add_brand(api_key, name, country):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/brands/", json={"name": name, "country": country}, headers=headers)
    if response.status_code == 200:
        st.success(f"Brand '{name}' added successfully!")
    else:
        st.error(f"Failed to add brand: {response.json().get('detail', 'Unknown error')}")


def update_brand(api_key, brand_id, name, country):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/brands/{brand_id}", json={"name": name, "country": country}, headers=headers)
    if response.status_code == 200:
        st.success(f"Brand '{name}' updated successfully!")
    else:
        st.error(f"Failed to update brand: {response.json().get('detail', 'Unknown error')}")


def delete_brand(api_key, brand_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/brands/{brand_id}", headers=headers)
    if response.status_code == 200:
        st.success("Brand deleted successfully!")
    else:
        st.error(f"Failed to delete brand: {response.json().get('detail', 'Unknown error')}")


def get_sneakers():
    response = requests.get(f"{BASE_URL}/sneakers/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch sneakers.")
        return []


def add_sneaker(api_key, sneaker_data):
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/sneakers/", json=sneaker_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Sneaker '{sneaker_data['name']}' added successfully!")
    else:
        st.error(f"Failed to add sneaker: {response.json().get('detail', 'Unknown error')}")


def update_sneaker(api_key, sneaker_id, sneaker_data):
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/sneakers/{sneaker_id}", json=sneaker_data, headers=headers)
    if response.status_code == 200:
        st.success(f"Sneaker '{sneaker_data['name']}' updated successfully!")
    else:
        st.error(f"Failed to update sneaker: {response.json().get('detail', 'Unknown error')}")


def delete_sneaker(api_key, sneaker_id):
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/sneakers/{sneaker_id}", headers=headers)
    if response.status_code == 200:
        st.success("Sneaker deleted successfully!")
    else:
        st.error(f"Failed to delete sneaker: {response.json().get('detail', 'Unknown error')}")


# Dashboard for managing Brands
def brands_dashboard(api_key):
    st.title("🏷️ Brands Management")

    # Display existing brands
    st.subheader("Existing Brands")
    brands = get_brands()
    df_brands = pd.DataFrame(brands)
    st.dataframe(df_brands, use_container_width=True)

    # Form to add a new brand
    st.subheader("Add New Brand")
    col1, col2 = st.columns(2)
    with col1:
        new_brand_name = st.text_input("Brand Name")
    with col2:
        new_brand_country = st.text_input("Country", value="USA")

    if st.button("Add Brand"):
        if new_brand_name.strip():
            add_brand(api_key, new_brand_name, new_brand_country)
        else:
            st.error("Brand name cannot be empty.")

    # Choose an action to perform
    action = st.radio("What would you like to do?", options=["Update Brand", "Delete Brand"])

    if action == "Update Brand":
        selected_brand = st.selectbox("Select Brand to Update", options=[brand['name'] for brand in brands])
        brand = next((b for b in brands if b['name'] == selected_brand), None)
        
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("New Brand Name", value=selected_brand)
        with col2:
            new_country = st.text_input("New Country", value=brand.get('country', 'USA') if brand else 'USA')

        if st.button("Update Brand"):
            brand_id = next((brand['id'] for brand in brands if brand['name'] == selected_brand), None)
            update_brand(api_key, brand_id, new_name, new_country)

    elif action == "Delete Brand":
        brand_to_delete = st.selectbox("Select Brand to Delete", options=[brand['name'] for brand in brands])
        if st.button("Delete Brand"):
            brand_id = next((brand['id'] for brand in brands if brand['name'] == brand_to_delete), None)
            delete_brand(api_key, brand_id)


# Dashboard for managing Sneakers
def sneakers_dashboard(api_key):
    st.title("👟 Sneakers Management")

    # Display existing sneakers
    st.subheader("Existing Sneakers")
    sneakers = get_sneakers()
    brands = get_brands()

    brand_id_to_name = {brand['id']: brand['name'] for brand in brands}
    for sneaker in sneakers:
        sneaker['brand'] = brand_id_to_name.get(sneaker['brand_id'], 'Unknown')
        sneaker['categories'] = ', '.join(sneaker.get('categories', []))
        del sneaker['brand_id']

    df_sneakers = pd.DataFrame(sneakers)
    st.dataframe(df_sneakers, use_container_width=True)

    # Form to add a new sneaker
    st.subheader("Add New Sneaker")
    col1, col2 = st.columns(2)
    with col1:
        new_sneaker_name = st.text_input("Sneaker Name")
        selected_brand_name = st.selectbox("Select Brand", options=[brand['name'] for brand in brands], key="select_brand_add")
        new_sneaker_price = st.number_input("Price ($)", min_value=0.0, max_value=10000.0, step=5.0, value=150.0)
    with col2:
        new_sneaker_colorway = st.text_input("Colorway")
        new_sneaker_categories = st.text_input("Categories (comma-separated)", value="Lifestyle")
        new_sneaker_year = st.number_input("Release Year", min_value=1970, max_value=datetime.now().year + 1, step=1, value=datetime.now().year)
    
    new_sneaker_link = st.text_input("Product Link (optional)")

    if st.button("Add Sneaker"):
        if new_sneaker_name.strip() and new_sneaker_colorway.strip():
            categories_list = [c.strip() for c in new_sneaker_categories.split(',') if c.strip()]
            selected_brand_id = next((brand['id'] for brand in brands if brand['name'] == selected_brand_name), None)
            sneaker_data = {
                "name": new_sneaker_name,
                "brand_id": selected_brand_id,
                "product_link": new_sneaker_link,
                "categories": categories_list,
                "price": new_sneaker_price,
                "release_year": new_sneaker_year,
                "colorway": new_sneaker_colorway
            }
            add_sneaker(api_key, sneaker_data)
        else:
            st.error("Name and Colorway cannot be empty.")

    # Choose an action to perform
    action = st.radio("What would you like to do?", options=["Update Sneaker", "Delete Sneaker"], key="radio_action")

    if action == "Update Sneaker":
        selected_sneaker = st.selectbox("Select Sneaker to Update", options=[sneaker['name'] for sneaker in sneakers], key="select_sneaker_update")

        if selected_sneaker:
            sneaker = next((s for s in sneakers if s['name'] == selected_sneaker), None)
            
            col1, col2 = st.columns(2)
            with col1:
                new_sneaker_name = st.text_input("Name", value=sneaker['name'])
                selected_brand_name = st.selectbox(
                    "Select Brand", 
                    options=[brand['name'] for brand in brands],
                    index=[brand['name'] for brand in brands].index(sneaker['brand']) if sneaker['brand'] in [b['name'] for b in brands] else 0,
                    key="select_brand_update"
                )
                new_sneaker_price = st.number_input("Price ($)", min_value=0.0, max_value=10000.0, step=5.0, value=float(sneaker.get('price', 150)))
            with col2:
                new_sneaker_colorway = st.text_input("Colorway", value=sneaker.get('colorway', ''))
                new_sneaker_categories = st.text_input("Categories (comma-separated)", value=sneaker.get('categories', ''))
                new_sneaker_year = st.number_input("Release Year", min_value=1970, max_value=datetime.now().year + 1, step=1, value=int(sneaker.get('release_year', datetime.now().year)))
            
            new_sneaker_link = st.text_input("Product Link", value=sneaker.get('product_link', ''))
            sneaker_id = sneaker['id']

            if st.button("Update Sneaker"):
                categories_list = [c.strip() for c in new_sneaker_categories.split(',') if c.strip()]
                sneaker_data = {
                    "name": new_sneaker_name,
                    "brand_id": next((brand['id'] for brand in brands if brand['name'] == selected_brand_name), None),
                    "product_link": new_sneaker_link,
                    "categories": categories_list,
                    "price": new_sneaker_price,
                    "release_year": new_sneaker_year,
                    "colorway": new_sneaker_colorway
                }
                update_sneaker(api_key, sneaker_id, sneaker_data)

    elif action == "Delete Sneaker":
        sneaker_to_delete = st.selectbox("Select Sneaker to Delete", options=[sneaker['name'] for sneaker in sneakers], key="select_sneaker_delete")
        if st.button("Delete Sneaker"):
            sneaker_id = next((sneaker['id'] for sneaker in sneakers if sneaker['name'] == sneaker_to_delete), None)
            delete_sneaker(api_key, sneaker_id)


# Visualizations Dashboard
def visualizations_dashboard():
    st.title("📊 Visualizations Dashboard")

    # Fetch the sneakers and brands data
    sneakers = get_sneakers()
    brands = get_brands()

    if sneakers:
        # Convert sneakers to a DataFrame
        df_sneakers = pd.DataFrame(sneakers)

        if 'brand_id' in df_sneakers.columns:
            # Map brand_id to brand names
            brand_id_to_name = {brand['id']: brand['name'] for brand in brands}
            df_sneakers['brand'] = df_sneakers['brand_id'].map(brand_id_to_name)
            df_sneakers.drop('brand_id', axis=1, inplace=True)

        # Sidebar filters
        st.sidebar.title("Filters")

        # Filter by Brand
        selected_brand = st.sidebar.selectbox("Select Brand", options=["All"] + list(brand_id_to_name.values()))

        # Filter by Release Year
        if 'release_year' in df_sneakers.columns and not df_sneakers['release_year'].isna().all():
            min_year = int(df_sneakers['release_year'].min())
            max_year = int(df_sneakers['release_year'].max())
            selected_year = st.sidebar.slider("Select Release Year", min_value=min_year, max_value=max_year, value=(min_year, max_year))
        else:
            min_year, max_year = 2020, datetime.now().year
            selected_year = (min_year, max_year)

        # Filter by Price
        if 'price' in df_sneakers.columns and not df_sneakers['price'].isna().all():
            min_price = float(df_sneakers['price'].min())
            max_price = float(df_sneakers['price'].max())
            selected_price = st.sidebar.slider("Select Price Range ($)", min_value=min_price, max_value=max_price, value=(min_price, max_price), step=10.0)
        else:
            min_price, max_price = 0.0, 500.0
            selected_price = (min_price, max_price)

        # Check if any filters are applied
        filters_applied = selected_brand != "All" or selected_year != (min_year, max_year) or selected_price != (min_price, max_price)

        # Apply Filters Button
        if st.sidebar.button("Apply Filters") or not filters_applied:
            filtered_sneakers = df_sneakers.copy()

            if filters_applied:
                if selected_brand != "All":
                    filtered_sneakers = filtered_sneakers[filtered_sneakers['brand'] == selected_brand]

                if 'release_year' in filtered_sneakers.columns:
                    filtered_sneakers = filtered_sneakers[
                        (filtered_sneakers['release_year'] >= selected_year[0]) & 
                        (filtered_sneakers['release_year'] <= selected_year[1])
                    ]
                
                if 'price' in filtered_sneakers.columns:
                    filtered_sneakers = filtered_sneakers[
                        (filtered_sneakers['price'] >= selected_price[0]) & 
                        (filtered_sneakers['price'] <= selected_price[1])
                    ]

            if not filtered_sneakers.empty:
                # Visualization 1: Sneakers by Year
                if 'release_year' in filtered_sneakers.columns:
                    st.subheader("Sneakers by Release Year")
                    sneakers_by_year = filtered_sneakers.groupby('release_year').size().reset_index(name='Count')
                    fig_years = px.bar(
                        sneakers_by_year,
                        x='release_year',
                        y='Count',
                        title='Number of Sneakers by Release Year',
                        labels={"release_year": "Release Year", "Count": "Number of Sneakers"},
                        text='Count'
                    )
                    fig_years.update_traces(texttemplate='%{text}', textposition='outside')
                    fig_years.update_layout(title_x=0.5)
                    st.plotly_chart(fig_years, use_container_width=True)

                # Visualization 2: Sneakers by Price Distribution
                if 'price' in filtered_sneakers.columns:
                    st.subheader("Sneakers by Price")
                    fig_prices = px.histogram(
                        filtered_sneakers,
                        x='price',
                        nbins=20,
                        title='Price Distribution of Sneakers',
                        labels={"price": "Price ($)", "count": "Number of Sneakers"}
                    )
                    fig_prices.update_layout(title_x=0.5)
                    st.plotly_chart(fig_prices, use_container_width=True)

                # Visualization 3: Sneakers by Brand
                st.subheader("Sneakers by Brand")
                sneakers_by_brand = filtered_sneakers.groupby('brand').size().reset_index(name='Count')
                fig_brands = px.pie(
                    sneakers_by_brand,
                    values='Count',
                    names='brand',
                    title='Sneakers Distribution by Brand'
                )
                fig_brands.update_layout(title_x=0.5)
                st.plotly_chart(fig_brands, use_container_width=True)
            else:
                st.warning("No sneaker data available for the selected filters.")
    else:
        st.warning("No sneaker data available for visualizations.")


# Main app logic
st.sidebar.title("🏀 Nike Sneakers")
st.sidebar.markdown("---")
st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose a dashboard", ["Sneakers Dashboard", "Brands Dashboard", "Visualizations"])

if option == "Visualizations":
    visualizations_dashboard()
elif api_key_input and validate_api_key(api_key_input):
    if option == "Brands Dashboard":
        brands_dashboard(api_key_input)
    elif option == "Sneakers Dashboard":
        sneakers_dashboard(api_key_input)
else:
    if option != "Visualizations":
        st.error("Invalid API Key or API Key is missing.")
