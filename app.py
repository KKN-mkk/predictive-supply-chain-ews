import streamlit as st
import pandas as pd
import pickle

# --- 1. LOAD THE ML BRAIN ---
@st.cache_resource
def load_ml_components():
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    return model, encoders

# Try to load the model
try:
    model, encoders = load_ml_components()
except FileNotFoundError:
    st.error("🚨 Model files not found! Make sure you ran 'model_training.py' first.")
    st.stop()

# --- 2. UI SETUP ---
st.set_page_config(page_title="AI Supply Chain Risk Dashboard", layout="wide")
st.title("🌍 AI-Powered Early Warning System")
st.markdown("This dashboard uses a **Random Forest** model trained on 180,000 DataCo records to predict shipment delays.")

# --- 3. THE PM INTERFACE (Sidebar) ---
st.sidebar.header("📦 Shipment Configuration")

# These dropdowns are powered by your real data!
ship_mode = st.sidebar.selectbox("Shipping Mode", encoders['Shipping Mode'].classes_)
region = st.sidebar.selectbox("Destination Region", encoders['Order Region'].classes_)
category = st.sidebar.selectbox("Product Category", encoders['Category Name'].classes_)
days = st.sidebar.slider("Scheduled Days", 1, 14, 4)

if st.sidebar.button("Run Risk Analysis"):
    # Prepare the input for the model
    input_df = pd.DataFrame({
        'Shipping Mode': [ship_mode],
        'Order Region': [region],
        'Category Name': [category],
        'Days for shipment (scheduled)': [days]
    })

    # Encode the text into numbers for the ML model
    for col in ['Shipping Mode', 'Order Region', 'Category Name']:
        input_df[col] = encoders[col].transform(input_df[col])

    # Get prediction
    prob = model.predict_proba(input_df)[0][1] * 100

    # Display Results
    st.subheader("Predictive Risk Assessment")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Delay Probability", f"{prob:.1f}%")
    
    with col2:
        if prob > 65:
            st.error("🚨 CRITICAL RISK: High likelihood of late delivery.")
            st.write("**Strategy:** Optimize shipping mode or notify local distribution centers of expected lag.")
        elif prob > 35:
            st.warning("⚠️ MODERATE RISK: Potential for minor delays.")
        else:
            st.success("✅ LOW RISK: Optimized for on-time delivery.")
    
    st.progress(int(prob))
else:
    st.info("Select shipment details in the sidebar to begin.")