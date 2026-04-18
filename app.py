import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. LOAD THE ML BRAIN ---
@st.cache_resource
def load_ml_components():
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    return model, encoders

# --- 2. LOAD THE ANALYTICS ---
@st.cache_data
def load_heatmap():
    # Loading the pre-processed tiny file we created
    return pd.read_csv('heatmap_data.csv', index_col='Order Region')

# Initial Load
try:
    model, encoders = load_ml_components()
except FileNotFoundError:
    st.error("🚨 Model files not found! Make sure you ran 'model_training.py' first.")
    st.stop()

# --- 3. UI SETUP ---
st.set_page_config(page_title="AI Supply Chain Risk Dashboard", layout="wide")
st.title("🌍 AI-Powered Early Warning System")
st.markdown("Predict shipment delays and visualize global systemic risks.")

# --- 4. THE PM INTERFACE (Sidebar) ---
st.sidebar.header("📦 Shipment Configuration")
ship_mode = st.sidebar.selectbox("Shipping Mode", encoders['Shipping Mode'].classes_)
region = st.sidebar.selectbox("Destination Region", encoders['Order Region'].classes_)
category = st.sidebar.selectbox("Product Category", encoders['Category Name'].classes_)
days = st.sidebar.slider("Scheduled Days", 1, 14, 4)

# --- 5. PREDICTION LOGIC ---
if st.sidebar.button("Run Risk Analysis"):
    input_df = pd.DataFrame({
        'Shipping Mode': [ship_mode],
        'Order Region': [region],
        'Category Name': [category],
        'Days for shipment (scheduled)': [days]
    })

    # Encode inputs
    for col in ['Shipping Mode', 'Order Region', 'Category Name']:
        input_df[col] = encoders[col].transform(input_df[col])

    # Get prediction
    prob = model.predict_proba(input_df)[0][1] * 100

    st.subheader("🔍 Predictive Risk Assessment")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Delay Probability", f"{prob:.1f}%")
    
    with col2:
        if prob > 65:
            st.error("🚨 CRITICAL RISK: High likelihood of late delivery.")
        elif prob > 35:
            st.warning("⚠️ MODERATE RISK: Potential for minor delays.")
        else:
            st.success("✅ LOW RISK: Optimized for on-time delivery.")
    
    st.progress(int(prob))

# --- 6. ANALYTICS SECTION (Always Visible) ---
st.divider()
st.subheader("📊 Global Risk Heatmap")
st.write("Average delay percentages across regions and transport modes.")

try:
    heatmap_data = load_heatmap()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
    plt.title("Regional Risk Analysis (%)")
    st.pyplot(fig)
except Exception as e:
    st.info("Heatmap data is loading or being updated... Please ensure 'heatmap_data.csv' is uploaded.")