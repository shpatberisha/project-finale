import streamlit as st
import requests
import os

API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Sneaker Management", layout="wide")

st.title("👟 Sneaker Management System")

# Get API key from .env or prompt user
def get_api_key():
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("API_KEY")
    if not key:
        st.warning("⚠️ No API key found. Run `python generate_key.py` first.")
    return key

api_key = get_api_key()

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["View Sneakers", "View Brands", "Add Sneaker", "Add Brand", "Manage"])

# ========== VIEW SNEAKERS ==========
if page == "View Sneakers":
    st.header("All Sneakers")
    try:
        response = requests.get(f"{API_URL}/sneakers")
        if response.status_code == 200:
            sneakers = response.json()
            if sneakers:
                cols = st.columns([1, 2, 1, 1, 1, 1])
                with cols[0]:
                    st.write("**ID**")
                with cols[1]:
                    st.write("**Name**")
                with cols[2]:
                    st.write("**Brand**")
                with cols[3]:
                    st.write("**Price**")
                with cols[4]:
                    st.write("**Year**")
                with cols[5]:
                    st.write("**Colorway**")
                st.divider()
                
                for sneaker in sneakers:
                    cols = st.columns([1, 2, 1, 1, 1, 1])
                    with cols[0]:
                        st.write(sneaker["id"])
                    with cols[1]:
                        st.write(sneaker["name"])
                    with cols[2]:
                        st.write(sneaker["brand"]["name"])
                    with cols[3]:
                        st.write(f"${sneaker['price']}" if sneaker['price'] else "N/A")
                    with cols[4]:
                        st.write(sneaker['release_year'] if sneaker['release_year'] else "N/A")
                    with cols[5]:
                        st.write(sneaker['colorway'] if sneaker['colorway'] else "N/A")
            else:
                st.info("No sneakers found. Add one to get started!")
    except Exception as e:
        st.error(f"Error fetching sneakers: {str(e)}")

# ========== VIEW BRANDS ==========
elif page == "View Brands":
    st.header("All Brands")
    try:
        response = requests.get(f"{API_URL}/brands")
        if response.status_code == 200:
            brands = response.json()
            if brands:
                for brand in brands:
                    st.write(f"**{brand['name']}** (ID: {brand['id']})")
            else:
                st.info("No brands found. Add one to get started!")
    except Exception as e:
        st.error(f"Error fetching brands: {str(e)}")

# ========== ADD SNEAKER ==========
elif page == "Add Sneaker":
    st.header("Add New Sneaker")
    
    if not api_key:
        st.error("API key required. Run `python generate_key.py`")
    else:
        # Get brands for dropdown
        try:
            response = requests.get(f"{API_URL}/brands")
            brands = response.json() if response.status_code == 200 else []
            brand_options = {b["name"]: b["id"] for b in brands}
            
            if not brands:
                st.warning("No brands found. Please add a brand first.")
            else:
                with st.form("add_sneaker_form"):
                    name = st.text_input("Sneaker Name*")
                    brand = st.selectbox("Brand*", options=list(brand_options.keys()))
                    product_link = st.text_input("Product Link")
                    categories = st.text_input("Categories")
                    price = st.number_input("Price", min_value=0.0)
                    release_year = st.number_input("Release Year", min_value=1980, max_value=2100)
                    colorway = st.text_input("Colorway")
                    
                    submitted = st.form_submit_button("Add Sneaker")
                    
                    if submitted:
                        if not name or not brand:
                            st.error("Name and Brand are required")
                        else:
                            sneaker_data = {
                                "name": name,
                                "brand_id": brand_options[brand],
                                "product_link": product_link or None,
                                "categories": categories or None,
                                "price": price if price > 0 else None,
                                "release_year": release_year if release_year > 0 else None,
                                "colorway": colorway or None
                            }
                            
                            response = requests.post(
                                f"{API_URL}/sneakers",
                                json=sneaker_data,
                                headers={"api-key": api_key}
                            )
                            
                            if response.status_code == 200:
                                st.success("✓ Sneaker added successfully!")
                                st.balloons()
                            else:
                                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ========== ADD BRAND ==========
elif page == "Add Brand":
    st.header("Add New Brand")
    
    if not api_key:
        st.error("API key required. Run `python generate_key.py`")
    else:
        with st.form("add_brand_form"):
            name = st.text_input("Brand Name*")
            submitted = st.form_submit_button("Add Brand")
            
            if submitted:
                if not name:
                    st.error("Brand name is required")
                else:
                    brand_data = {"name": name}
                    response = requests.post(
                        f"{API_URL}/brands",
                        json=brand_data,
                        headers={"api-key": api_key}
                    )
                    
                    if response.status_code == 200:
                        st.success("✓ Brand added successfully!")
                        st.balloons()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

# ========== MANAGE ==========
elif page == "Manage":
    st.header("Management")
    
    if not api_key:
        st.error("API key required. Run `python generate_key.py`")
    else:
        st.subheader("Delete Brand")
        try:
            response = requests.get(f"{API_URL}/brands")
            brands = response.json() if response.status_code == 200 else []
            brand_options = {b["name"]: b["id"] for b in brands}
            
            if brands:
                brand_to_delete = st.selectbox("Select brand to delete", options=list(brand_options.keys()), key="delete_brand")
                if st.button("Delete Brand"):
                    response = requests.delete(
                        f"{API_URL}/brands/{brand_options[brand_to_delete]}",
                        headers={"api-key": api_key}
                    )
                    if response.status_code == 200:
                        st.success("✓ Brand deleted successfully!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.divider()
        
        st.subheader("Delete Sneaker")
        try:
            response = requests.get(f"{API_URL}/sneakers")
            sneakers = response.json() if response.status_code == 200 else []
            sneaker_options = {f"{s['name']} ({s['brand']['name']})": s["id"] for s in sneakers}
            
            if sneakers:
                sneaker_to_delete = st.selectbox("Select sneaker to delete", options=list(sneaker_options.keys()), key="delete_sneaker")
                if st.button("Delete Sneaker"):
                    response = requests.delete(
                        f"{API_URL}/sneakers/{sneaker_options[sneaker_to_delete]}",
                        headers={"api-key": api_key}
                    )
                    if response.status_code == 200:
                        st.success("✓ Sneaker deleted successfully!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
