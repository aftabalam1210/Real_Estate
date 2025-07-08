import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Gurugram Real Estate Insights & Navigator", # More descriptive title
    page_icon="🏡", # Changed icon to a house for relevance
    layout="centered", # Use centered layout for a cleaner look
    initial_sidebar_state="expanded" # Ensure sidebar is expanded by default
)

# --- Sidebar Navigation (as per your original code) ---
# This message will appear in the sidebar, guiding users to select a demo.
st.sidebar.success("Navigate through the app's features using the menu above! ⬆️")

# --- Main Content Area ---

# Hero Section with a clear, engaging title
st.write("""
# Welcome to Your Gurugram Real Estate Command Center! 🚀
""")

st.markdown("""
Unlock the power of data to make smarter property decisions in Gurugram. Whether you're looking to buy, sell, or simply understand the market, this app is your ultimate guide.
""")

# IMPORTANT: For self-contained code in this environment, local image paths like "Cyber_City_View.jpg"
# cannot be directly accessed. Reverting to a reliable external URL for demonstration purposes.
# If you wish to use a local image, ensure it's uploaded to your Streamlit app's deployment environment.
st.image("Cyber_City_View.jpg", caption="Gurugram's Dynamic Real Estate Landscape", use_container_width=True)


st.write("---") # Separator for better visual flow

# --- Key Features Section ---
st.markdown("## What Can You Do Here? 🤔")

col1, col2, col3 = st.columns(3) # Use columns for a neat layout of features

with col1:
    st.markdown("""
    ### 💰 Price Prediction
    Get an accurate, data-driven estimate for any property in Gurugram. Input key details and let our Random Forest model do the work!
    """)

with col2:
    st.markdown("""
    ### 📊 Society & Locality Analysis
    Dive deep into market trends. Understand property values, demand, and supply dynamics specific to different societies and areas.
    """)

with col3:
    st.markdown("""
    ### 🏡 Apartment Recommendations
    Looking for your dream apartment? Our smart system recommends properties tailored to your preferences, making your search effortless.
    """)

st.write("---")

# --- Call to Action / How to Use ---
st.markdown("## Ready to Get Started? 👇")
st.markdown("""
Simply select a feature from the **sidebar on the left** to begin your exploration.
""")

st.info("💡 **Tip:** Use the navigation menu in the sidebar to switch between 'Price Prediction', 'Analysis', and 'Apartment Recommendations'.")

st.write("---")

# --- Footer or About Section (Optional but good for branding) ---
st.markdown("""
<small>Built with ❤️ and Data Science by Aftab Alam.</small>
""", unsafe_allow_html=True)

