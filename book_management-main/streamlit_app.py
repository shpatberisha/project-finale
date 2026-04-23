import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os
from auth.auth_database import create_user, authenticate_user, regenerate_api_key

load_dotenv()

# Configure page
st.set_page_config(
    page_title="Nike Sneakers Management",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the base URL of the FastAPI application
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111111;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: #f8f8f8;
        border-radius: 12px;
    }
    .success-box {
        padding: 1rem;
        background: #d4edda;
        border-radius: 8px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background: #f8d7da;
        border-radius: 8px;
        color: #721c24;
        margin: 1rem 0;
    }
    .api-key-box {
        padding: 1rem;
        background: #e7f3ff;
        border-radius: 8px;
        font-family: monospace;
        word-break: break-all;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #111111;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #333333;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'


def validate_api_key(api_key):
    """Validate API key against the backend"""
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{BASE_URL}/api/validate_key/", headers=headers)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def login_page():
    """Display login page"""
    st.markdown('<h1 class="main-header">👟 Nike Sneakers Management</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Sign in to manage your sneaker collection</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            st.subheader("Welcome Back")
            
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit:
                    if username and password:
                        result = authenticate_user(username, password)
                        if result.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.user = result
                            st.session_state.api_key = result.get("api_key")
                            st.success("Login successful!")
                            st.experimental_rerun()
                        else:
                            st.error(result.get("error", "Invalid credentials"))
                    else:
                        st.error("Please enter both username and password")
        
        with tab2:
            st.subheader("Create Account")
            
            with st.form("signup_form"):
                new_username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
                new_email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
                new_password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
                submit_signup = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit_signup:
                    if new_username and new_email and new_password and confirm_password:
                        if new_password != confirm_password:
                            st.error("Passwords do not match")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters")
                        elif "@" not in new_email:
                            st.error("Please enter a valid email address")
                        else:
                            result = create_user(new_username, new_email, new_password)
                            if result.get("success"):
                                st.success("Account created successfully! You can now sign in.")
                                st.markdown(f"""
                                    <div class="api-key-box">
                                        <strong>Your API Key:</strong><br>
                                        {result.get('api_key')}
                                    </div>
                                    <p style="color: #666; font-size: 0.9rem;">
                                        Save this API key! You'll need it to access the API directly.
                                    </p>
                                """, unsafe_allow_html=True)
                            else:
                                st.error(result.get("error", "Failed to create account"))
                    else:
                        st.error("Please fill in all fields")


def get_brands(api_key):
    """Fetch all brands from the API"""
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{BASE_URL}/api/brands/", headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the FastAPI server is running.")
    return []


def get_sneakers(api_key):
    """Fetch all sneakers from the API"""
    headers = {"api-key": api_key}
    try:
        response = requests.get(f"{BASE_URL}/api/sneakers/", headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API. Make sure the FastAPI server is running.")
    return []


def add_brand(api_key, name):
    """Add a new brand"""
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/api/brands/", json={"name": name}, headers=headers)
    return response.status_code == 200, response.json() if response.status_code != 200 else None


def update_brand(api_key, brand_id, name):
    """Update an existing brand"""
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/api/brands/{brand_id}", json={"name": name}, headers=headers)
    return response.status_code == 200


def delete_brand(api_key, brand_id):
    """Delete a brand"""
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/api/brands/{brand_id}", headers=headers)
    return response.status_code == 200


def add_sneaker(api_key, sneaker_data):
    """Add a new sneaker"""
    headers = {"api-key": api_key}
    response = requests.post(f"{BASE_URL}/api/sneakers/", json=sneaker_data, headers=headers)
    return response.status_code == 200, response.json() if response.status_code != 200 else None


def update_sneaker(api_key, sneaker_id, sneaker_data):
    """Update an existing sneaker"""
    headers = {"api-key": api_key}
    response = requests.put(f"{BASE_URL}/api/sneakers/{sneaker_id}", json=sneaker_data, headers=headers)
    return response.status_code == 200


def delete_sneaker(api_key, sneaker_id):
    """Delete a sneaker"""
    headers = {"api-key": api_key}
    response = requests.delete(f"{BASE_URL}/api/sneakers/{sneaker_id}", headers=headers)
    return response.status_code == 200


def brands_dashboard(api_key):
    """Dashboard for managing brands"""
    st.title("Brands Management")
    
    brands = get_brands(api_key)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("All Brands")
        if brands:
            df = pd.DataFrame(brands)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No brands found. Add your first brand!")
    
    with col2:
        st.subheader("Add New Brand")
        with st.form("add_brand_form"):
            brand_name = st.text_input("Brand Name", placeholder="e.g., Nike, Adidas")
            if st.form_submit_button("Add Brand", use_container_width=True):
                if brand_name.strip():
                    success, error = add_brand(api_key, brand_name)
                    if success:
                        st.success(f"Brand '{brand_name}' added!")
                        st.experimental_rerun()
                    else:
                        st.error(error.get("detail", "Failed to add brand") if error else "Failed to add brand")
                else:
                    st.error("Brand name cannot be empty")
    
    if brands:
        st.divider()
        st.subheader("Manage Existing Brands")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Update Brand**")
            selected_brand = st.selectbox(
                "Select Brand to Update",
                options=brands,
                format_func=lambda x: x['name'],
                key="update_brand_select"
            )
            if selected_brand:
                new_name = st.text_input("New Name", value=selected_brand['name'])
                if st.button("Update Brand", key="update_brand_btn"):
                    if update_brand(api_key, selected_brand['id'], new_name):
                        st.success("Brand updated!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to update brand")
        
        with col2:
            st.markdown("**Delete Brand**")
            brand_to_delete = st.selectbox(
                "Select Brand to Delete",
                options=brands,
                format_func=lambda x: x['name'],
                key="delete_brand_select"
            )
            if brand_to_delete:
                st.warning(f"This will delete '{brand_to_delete['name']}'")
                if st.button("Delete Brand", key="delete_brand_btn", type="primary"):
                    if delete_brand(api_key, brand_to_delete['id']):
                        st.success("Brand deleted!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete brand")


def sneakers_dashboard(api_key):
    """Dashboard for managing sneakers"""
    st.title("Sneakers Management")
    
    sneakers = get_sneakers(api_key)
    brands = get_brands(api_key)
    brand_id_to_name = {b['id']: b['name'] for b in brands}
    
    # Display sneakers
    st.subheader("All Sneakers")
    if sneakers:
        display_data = []
        for s in sneakers:
            display_data.append({
                "ID": s['id'],
                "Name": s['name'],
                "Brand": brand_id_to_name.get(s['brand_id'], 'Unknown'),
                "Price": f"${s['price']:.2f}" if s['price'] else "N/A",
                "Release Year": s['release_year'] or "N/A",
                "Colorway": s['colorway'] or "N/A",
                "Categories": ', '.join(s['categories']) if s['categories'] else "N/A"
            })
        df = pd.DataFrame(display_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No sneakers found. Add your first sneaker!")
    
    st.divider()
    
    # Add new sneaker
    st.subheader("Add New Sneaker")
    
    if not brands:
        st.warning("Please add at least one brand before adding sneakers.")
    else:
        with st.form("add_sneaker_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Sneaker Name", placeholder="e.g., Air Jordan 1 Retro High")
                selected_brand = st.selectbox("Brand", options=brands, format_func=lambda x: x['name'])
                price = st.number_input("Price ($)", min_value=0.0, step=10.0)
                colorway = st.text_input("Colorway", placeholder="e.g., Chicago, Bred, Royal")
            
            with col2:
                release_year = st.number_input("Release Year", min_value=1970, max_value=datetime.now().year, value=datetime.now().year)
                categories = st.text_input("Categories (comma-separated)", placeholder="e.g., Basketball, Lifestyle, Retro")
                product_link = st.text_input("Product Link (optional)", placeholder="https://...")
            
            if st.form_submit_button("Add Sneaker", use_container_width=True):
                if name.strip():
                    sneaker_data = {
                        "name": name,
                        "brand_id": selected_brand['id'],
                        "price": price,
                        "release_year": release_year,
                        "colorway": colorway or None,
                        "categories": [c.strip() for c in categories.split(',') if c.strip()],
                        "product_link": product_link or ""
                    }
                    success, error = add_sneaker(api_key, sneaker_data)
                    if success:
                        st.success(f"Sneaker '{name}' added!")
                        st.experimental_rerun()
                    else:
                        st.error(error.get("detail", "Failed to add sneaker") if error else "Failed to add sneaker")
                else:
                    st.error("Sneaker name cannot be empty")
    
    # Manage existing sneakers
    if sneakers:
        st.divider()
        st.subheader("Manage Existing Sneakers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Update Sneaker**")
            selected_sneaker = st.selectbox(
                "Select Sneaker",
                options=sneakers,
                format_func=lambda x: f"{x['name']} ({brand_id_to_name.get(x['brand_id'], 'Unknown')})",
                key="update_sneaker_select"
            )
            
            if selected_sneaker:
                with st.form("update_sneaker_form"):
                    new_name = st.text_input("Name", value=selected_sneaker['name'])
                    new_brand = st.selectbox(
                        "Brand", 
                        options=brands, 
                        format_func=lambda x: x['name'],
                        index=next((i for i, b in enumerate(brands) if b['id'] == selected_sneaker['brand_id']), 0)
                    )
                    new_price = st.number_input("Price ($)", value=float(selected_sneaker['price'] or 0), min_value=0.0, step=10.0)
                    new_year = st.number_input("Year", value=int(selected_sneaker['release_year'] or datetime.now().year), min_value=1970, max_value=datetime.now().year)
                    new_colorway = st.text_input("Colorway", value=selected_sneaker['colorway'] or "")
                    new_categories = st.text_input("Categories", value=', '.join(selected_sneaker['categories'] or []))
                    
                    if st.form_submit_button("Update Sneaker"):
                        sneaker_data = {
                            "name": new_name,
                            "brand_id": new_brand['id'],
                            "price": new_price,
                            "release_year": new_year,
                            "colorway": new_colorway or None,
                            "categories": [c.strip() for c in new_categories.split(',') if c.strip()],
                            "product_link": selected_sneaker.get('product_link', '')
                        }
                        if update_sneaker(api_key, selected_sneaker['id'], sneaker_data):
                            st.success("Sneaker updated!")
                            st.experimental_rerun()
                        else:
                            st.error("Failed to update sneaker")
        
        with col2:
            st.markdown("**Delete Sneaker**")
            sneaker_to_delete = st.selectbox(
                "Select Sneaker to Delete",
                options=sneakers,
                format_func=lambda x: f"{x['name']} ({brand_id_to_name.get(x['brand_id'], 'Unknown')})",
                key="delete_sneaker_select"
            )
            if sneaker_to_delete:
                st.warning(f"This will permanently delete '{sneaker_to_delete['name']}'")
                if st.button("Delete Sneaker", key="delete_sneaker_btn", type="primary"):
                    if delete_sneaker(api_key, sneaker_to_delete['id']):
                        st.success("Sneaker deleted!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to delete sneaker")


def visualizations_dashboard(api_key):
    """Dashboard for visualizations"""
    st.title("Analytics Dashboard")
    
    sneakers = get_sneakers(api_key)
    brands = get_brands(api_key)
    
    if not sneakers:
        st.info("No data available for visualizations. Add some sneakers first!")
        return
    
    brand_id_to_name = {b['id']: b['name'] for b in brands}
    
    # Prepare data
    df = pd.DataFrame(sneakers)
    df['brand_name'] = df['brand_id'].map(brand_id_to_name)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sneakers", len(sneakers))
    with col2:
        st.metric("Total Brands", len(brands))
    with col3:
        avg_price = df['price'].mean() if df['price'].notna().any() else 0
        st.metric("Avg Price", f"${avg_price:.2f}")
    with col4:
        latest_year = df['release_year'].max() if df['release_year'].notna().any() else "N/A"
        st.metric("Latest Release", latest_year)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sneakers by Brand")
        brand_counts = df['brand_name'].value_counts().reset_index()
        brand_counts.columns = ['Brand', 'Count']
        fig = px.pie(brand_counts, values='Count', names='Brand', hole=0.4)
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sneakers by Release Year")
        year_counts = df[df['release_year'].notna()].groupby('release_year').size().reset_index(name='Count')
        if not year_counts.empty:
            fig = px.bar(year_counts, x='release_year', y='Count', labels={'release_year': 'Year'})
            fig.update_layout(xaxis_title="Year", yaxis_title="Number of Sneakers")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No release year data available")
    
    # Price distribution
    st.subheader("Price Distribution")
    price_data = df[df['price'].notna() & (df['price'] > 0)]
    if not price_data.empty:
        fig = px.histogram(price_data, x='price', nbins=20, labels={'price': 'Price ($)'})
        fig.update_layout(xaxis_title="Price ($)", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No price data available")


def profile_page(api_key, user):
    """User profile page"""
    st.title("Your Profile")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Account Information")
        st.markdown(f"**Username:** {user.get('username', 'N/A')}")
        st.markdown(f"**Email:** {user.get('email', 'N/A')}")
        
        st.divider()
        
        st.subheader("Your API Key")
        st.markdown("""
            Use this API key to access the API directly from your applications.
            Keep it secure and never share it publicly.
        """)
        
        api_key_display = st.session_state.api_key
        st.code(api_key_display, language=None)
        
        if st.button("Regenerate API Key"):
            result = regenerate_api_key(user.get('id'))
            if result.get("success"):
                st.session_state.api_key = result.get("api_key")
                st.success("API key regenerated!")
                st.experimental_rerun()
            else:
                st.error("Failed to regenerate API key")
    
    with col2:
        st.subheader("Quick Stats")
        sneakers = get_sneakers(api_key)
        brands = get_brands(api_key)
        
        st.metric("Your Sneakers", len(sneakers))
        st.metric("Your Brands", len(brands))


def main():
    """Main application logic"""
    init_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"### Welcome, {st.session_state.user.get('username', 'User')}!")
            st.divider()
            
            page = st.radio(
                "Navigation",
                options=["Sneakers", "Brands", "Analytics", "Profile"],
                label_visibility="collapsed"
            )
            
            st.divider()
            
            if st.button("Sign Out", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.session_state.api_key = None
                st.experimental_rerun()
        
        # Main content
        api_key = st.session_state.api_key
        
        if page == "Sneakers":
            sneakers_dashboard(api_key)
        elif page == "Brands":
            brands_dashboard(api_key)
        elif page == "Analytics":
            visualizations_dashboard(api_key)
        elif page == "Profile":
            profile_page(api_key, st.session_state.user)


if __name__ == "__main__":
    main()
