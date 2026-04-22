# AI-POWERED SUPPLY CHAIN EARLY WARNING SYSTEM

**Author:** Manasa K Krishnan  
**Institution:** National Institute of Technology (NIT), Trichy  
**Field:** B.Tech Civil Engineering

###  **PROJECT OVERVIEW**
This is a **DECISION SUPPORT SYSTEM** designed to mitigate global logistics volatility. By leveraging a **RANDOM FOREST** machine learning model trained on **180,000+ RECORDS**, this dashboard allows supply chain managers to predict shipment delays and visualize systemic risks across the global network.

---

### **CORE FEATURES**

* **PREDICTIVE RISK ASSESSMENT:** Input specific shipment configurations—including **Shipping Mode**, **Destination Region**, and **Category**-to generate a real-time **DELAY PROBABILITY SCORE**.
    
* **GLOBAL RISK HEATMAP:** An executive-level visualization that identifies **"DANGER ZONES"** by intersecting regions with transport modes, highlighting where systemic failures occur.

* **STRATEGIC MITIGATION:** The tool provides actionable logic: if risk exceeds **65%**, the system flags it as **CRITICAL** and suggests immediate carrier reallocation.

---

###  **TECHNICAL STACK**

* **LANGUAGE:** `Python 3.12`
* **MACHINE LEARNING:** `Scikit-Learn` (Random Forest Classifier)
* **DATA ANALYTICS:** `Pandas`, `NumPy`
* **VISUALIZATION:** `Seaborn`, `Matplotlib`
* **DEPLOYMENT:** `Streamlit Cloud`

---

###  **REPOSITORY STRUCTURE**

| **FILE** | **DESCRIPTION** |
| :--- | :--- |
| `app.py` | **MAIN APPLICATION** file containing UI and prediction logic. |
| `rf_model.pkl` | **THE BRAIN**: The trained Random Forest model. |
| `heatmap_data.csv` | **PROCESSED ANALYTICS**: Pre-calculated risk data for fast loading. |
| `requirements.txt` | **DEPENDENCIES**: Necessary libraries for the Cloud environment. |
| `make_heatmap.py` | **DATA PIPELINE**: Script used to pivot raw data into analytics. |

---

###  **ACADEMIC & PROFESSIONAL CONTEXT**
Developed as part of an exploration into **Supply Chain Management and Data Analytics**. This project bridges the gap between traditional supply chain management and modern AI-driven predictive maintenance, focusing on operational efficiency and risk resilience.

---

### 🔗 **HOW TO USE**
1.  Access the **LIVE DASHBOARD** here: [https://predictive-supply-chain-ews-qnkmcrdn4brwic9ffry4rv.streamlit.app/](https://predictive-supply-chain-ews-qnkmcrdn4brwic9ffry4rv.streamlit.app/)
2.  Configure your shipment details in the **SIDEBAR**.
3.  Click **"RUN RISK ANALYSIS"** to see the AI prediction.
4.  Scroll down to view the **GLOBAL ANALYTICS** heatmap for broader context.
