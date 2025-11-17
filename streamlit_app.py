import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import joblib

# Local imports: add project root to path
sys.path.append(str(Path(__file__).parent))
from src.module3_fraud_detection.fraud_detector import FraudDetector
from src.module1_preprocessing.feature_engineer import FeatureEngineer
from config.config import MODELS_DIR, FRAUD_MODEL_PATH


# Page configuration
st.set_page_config(
    page_title="🛡️ Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 0.25rem solid #1f77b4;
}
.risk-high {
    color: #dc3545;
    font-weight: bold;
}
.risk-medium {
    color: #ffc107;
    font-weight: bold;
}
.risk-low {
    color: #28a745;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_resources():
    """Load fraud detector and feature engineer from disk (cached)."""
    # Load Fraud Detector model
    if Path(FRAUD_MODEL_PATH).exists():
        fraud_detector = FraudDetector(str(FRAUD_MODEL_PATH))
    else:
        fraud_detector = FraudDetector()

    # Load FeatureEngineer if available
    engineer_path = MODELS_DIR / "preprocessing" / "feature_engineer.pkl"
    if engineer_path.exists():
        feature_engineer = joblib.load(engineer_path)
    else:
        feature_engineer = FeatureEngineer()

    return fraud_detector, feature_engineer

def run_single_detection(fraud_detector: FraudDetector, feature_engineer: FeatureEngineer, transaction_data: dict):
    df = pd.DataFrame([transaction_data])
    df_eng = feature_engineer.engineer_all_features(df, fit=False)
    result = fraud_detector.detect_fraud(df_eng, transaction_data)
    return result

def run_batch_detection(fraud_detector: FraudDetector, feature_engineer: FeatureEngineer, df: pd.DataFrame):
    df_eng = feature_engineer.engineer_all_features(df, fit=False)
    results = []
    for _, row in df.iterrows():
        row_df = pd.DataFrame([row.to_dict()])
        row_eng = feature_engineer.engineer_all_features(row_df, fit=False)
        res = fraud_detector.detect_fraud(row_eng, row.to_dict())
        results.append(res)
    return results

def main():
    st.markdown('<div class="main-header">🛡️ Predictive Transaction Intelligence</div>', unsafe_allow_html=True)
    st.markdown("**Real-time AI-powered fraud detection for BFSI**")

    # Load models/resources
    fraud_detector, feature_engineer = load_resources()
    st.sidebar.success("Models loaded locally")
    st.sidebar.caption(f"Fraud model: {'found' if Path(FRAUD_MODEL_PATH).exists() else 'not found'}")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Single Transaction", "📊 Batch Processing", "📈 Analytics", "🔧 System Info"])

    with tab1:
        st.header("🔍 Single Transaction Fraud Detection")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Transaction Details")

            # Transaction form
            with st.form("transaction_form"):
                col_a, col_b = st.columns(2)

                with col_a:
                    amount = st.number_input("Transaction Amount (₹)", min_value=0, value=50000, step=1000)
                    date = st.date_input("Transaction Date", datetime.now())
                    time = st.time_input("Transaction Time", datetime.now().time())
                    location = st.text_input("Transaction Location", "Mumbai")
                    card_type = st.selectbox("Card Type", ["Visa", "Mastercard", "American Express", "RuPay"])

                with col_b:
                    currency = st.selectbox("Currency", ["INR", "USD", "EUR", "GBP"])
                    status = st.selectbox("Transaction Status", ["Completed", "Pending", "Failed"])
                    prev_count = st.number_input("Previous Transaction Count", min_value=0, value=25)
                    distance = st.number_input("Distance from Last Transaction (km)", min_value=0.0, value=10.5, step=0.1)
                    time_gap = st.number_input("Time Since Last Transaction (min)", min_value=0, value=120)

                auth_method = st.selectbox("Authentication Method", ["PIN", "Biometric", "OTP", "Password"])
                velocity = st.number_input("Transaction Velocity", min_value=1, value=3)
                category = st.selectbox("Transaction Category", ["Shopping", "Transfer", "Payment", "Cash Out", "Cash In"])

                submitted = st.form_submit_button("🚨 Detect Fraud", use_container_width=True)

        with col2:
            st.subheader("Detection Result")

            if submitted:
                transaction_data = {
                    "Transaction_Amount": amount,
                    "Transaction_Date": date.strftime("%Y-%m-%d"),
                    "Transaction_Time": time.strftime("%H:%M:%S"),
                    "Transaction_Location": location,
                    "Card_Type": card_type,
                    "Transaction_Currency": currency,
                    "Transaction_Status": status,
                    "Previous_Transaction_Count": prev_count,
                    "Distance_Between_Transactions_km": distance,
                    "Time_Since_Last_Transaction_min": time_gap,
                    "Authentication_Method": auth_method,
                    "Transaction_Velocity": velocity,
                    "Transaction_Category": category
                }
                start = datetime.now()
                result = run_single_detection(fraud_detector, feature_engineer, transaction_data)
                result['processing_time_ms'] = (datetime.now() - start).total_seconds() * 1000

                risk_level = result['risk_level']
                risk_score = result['combined_risk_score']

                if risk_level == "HIGH":
                    st.error(f"🚨 HIGH RISK ({risk_score:.2f})")
                    st.error(f"**Recommendation:** {result['recommendation']}")
                elif risk_level == "MEDIUM":
                    st.warning(f"⚠️ MEDIUM RISK ({risk_score:.2f})")
                    st.warning(f"**Recommendation:** {result['recommendation']}")
                else:
                    st.success(f"✅ LOW RISK ({risk_score:.2f})")
                    st.success(f"**Recommendation:** {result['recommendation']}")

                st.write("**Detailed Analysis:**")
                col_x, col_y, col_z = st.columns(3)
                with col_x:
                    st.metric("ML Risk Score", f"{result['ml_risk_score']:.2f}")
                with col_y:
                    st.metric("Rule Risk Score", f"{result['rule_risk_score']:.2f}")
                with col_z:
                    st.metric("Processing Time", f"{result['processing_time_ms']:.1f}ms")

                if result['triggered_rules']:
                    st.write("**Triggered Rules:**")
                    for rule in result['triggered_rules']:
                        st.write(f"• {rule}")

    with tab2:
        st.header("📊 Batch Transaction Processing")

        st.write("Upload a CSV file with transaction data or enter transactions manually.")

        # File upload
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Loaded {len(df)} transactions")

                if st.button("🚨 Process Batch", use_container_width=True):
                    start = datetime.now()
                    results = run_batch_detection(fraud_detector, feature_engineer, df)
                    processing_time_ms = (datetime.now() - start).total_seconds() * 1000
                    # Save to session for analytics tab
                    st.session_state['batch_results'] = results

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Transactions", len(results))
                    with col2:
                        st.metric("Fraud Detected", sum(1 for r in results if r['is_fraud']))
                    with col3:
                        st.metric("Processing Time", f"{processing_time_ms:.1f}ms")

                    results_df = pd.DataFrame(results)
                    st.dataframe(results_df)

                    risk_counts = results_df['risk_level'].value_counts()
                    fig = px.pie(values=risk_counts.values, names=risk_counts.index,
                                   title="Risk Distribution", color_discrete_map={
                                       'HIGH': '#dc3545', 'MEDIUM': '#ffc107', 'LOW': '#28a745'
                                   })
                    st.plotly_chart(fig)

            except Exception as e:
                st.error(f"Error reading file: {e}")

    with tab3:
        st.header("📈 Analytics Dashboard")

        st.info("Metrics are computed locally for this session.")
        if 'batch_results' in st.session_state:
            results_df = pd.DataFrame(st.session_state['batch_results'])
            total = len(results_df)
            fraud_count = int((results_df['is_fraud']).sum())
            fraud_rate = fraud_count / total if total else 0
            avg_score = float(results_df['combined_risk_score'].mean()) if total else 0

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Processed", total)
            with col2:
                st.metric("Fraud Detected", fraud_count)
            with col3:
                st.metric("Fraud Rate", f"{fraud_rate:.1%}")
            with col4:
                st.metric("Avg Risk Score", f"{avg_score:.2f}")
        else:
            st.warning("Run a batch to populate analytics.")

    with tab4:
        st.header("🔧 System Information")

        # Model Health
        st.subheader("Model Status")
        st.success("✅ Models loaded for local inference")

        # System info
        st.subheader("Model Files")
        model_paths = [
            "models/preprocessing/feature_engineer.pkl",
            "models/predictive/ensemble/",
            "models/fraud_detection/fraud_detector.pkl"
        ]

        for path in model_paths:
            full_path = Path(path)
            if full_path.exists():
                st.success(f"✅ {path}")
                if full_path.is_dir():
                    files = list(full_path.glob("*"))
                    st.info(f"Contains {len(files)} files")
                else:
                    size = full_path.stat().st_size / 1024
                    st.info(f"Size: {size:.1f}KB")
            else:
                st.warning(f"⚠️ {path} not found")

if __name__ == "__main__":
    main()
