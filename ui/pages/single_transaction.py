"""
Single Transaction Fraud Detection Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ui.components import render_card, render_result_card, render_info_box


def render_single_transaction_page(fraud_detector, feature_engineer):
    """Render the single transaction fraud detection page"""
    
    st.markdown('<h1 style="color: #1e3a8a; margin-bottom: 2rem;">🔍 Single Transaction Analysis</h1>', unsafe_allow_html=True)
    
    # Info box
    render_info_box(
        "Real-Time Fraud Detection",
        "Enter transaction details below to get instant fraud risk assessment powered by AI and rule-based detection.",
        "info"
    )
    
    # Create two columns for input and result
    col_input, col_result = st.columns([3, 2], gap="large")
    
    with col_input:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">💳 Transaction Details</div>', unsafe_allow_html=True)
        
        with st.form("transaction_form", clear_on_submit=False):
            # Row 1: Amount and Date
            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input(
                    "Transaction Amount (₹)",
                    min_value=0,
                    value=50000,
                    step=1000,
                    help="Enter the transaction amount in Indian Rupees"
                )
            with col2:
                date = st.date_input(
                    "Transaction Date",
                    value=datetime.now(),
                    help="Select the transaction date"
                )
            
            # Row 2: Time and Location
            col3, col4 = st.columns(2)
            with col3:
                time = st.time_input(
                    "Transaction Time",
                    value=datetime.now().time(),
                    help="Select the transaction time"
                )
            with col4:
                location = st.text_input(
                    "Transaction Location",
                    value="Mumbai",
                    help="Enter the transaction location"
                )
            
            # Row 3: Card Type and Currency
            col5, col6 = st.columns(2)
            with col5:
                card_type = st.selectbox(
                    "Card Type",
                    ["Visa", "Mastercard", "American Express", "RuPay", "Discover"],
                    help="Select the card type"
                )
            with col6:
                currency = st.selectbox(
                    "Currency",
                    ["INR", "USD", "EUR", "GBP", "AED"],
                    help="Select the transaction currency"
                )
            
            # Row 4: Status and Category
            col7, col8 = st.columns(2)
            with col7:
                status = st.selectbox(
                    "Transaction Status",
                    ["Completed", "Pending", "Failed", "Processing"],
                    help="Current transaction status"
                )
            with col8:
                category = st.selectbox(
                    "Transaction Category",
                    ["Shopping", "Transfer", "Payment", "Cash Out", "Cash In", "Bill Payment", "Investment"],
                    help="Select transaction category"
                )
            
            # Row 5: Authentication and Velocity
            col9, col10 = st.columns(2)
            with col9:
                auth_method = st.selectbox(
                    "Authentication Method",
                    ["PIN", "Biometric", "OTP", "Password", "Failed"],
                    help="Authentication method used"
                )
            with col10:
                velocity = st.number_input(
                    "Transaction Velocity",
                    min_value=1,
                    max_value=50,
                    value=3,
                    help="Number of transactions in last hour"
                )
            
            # Row 6: Previous Count and Distance
            col11, col12 = st.columns(2)
            with col11:
                prev_count = st.number_input(
                    "Previous Transaction Count",
                    min_value=0,
                    max_value=10000,
                    value=25,
                    help="Total previous transactions"
                )
            with col12:
                distance = st.number_input(
                    "Distance from Last Transaction (km)",
                    min_value=0.0,
                    max_value=20000.0,
                    value=10.5,
                    step=0.1,
                    help="Distance from previous transaction location"
                )
            
            # Row 7: Time Gap
            time_gap = st.number_input(
                "Time Since Last Transaction (minutes)",
                min_value=0,
                max_value=100000,
                value=120,
                help="Minutes since the last transaction"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Submit button
            submitted = st.form_submit_button(
                "🚨 Analyze Transaction",
                use_container_width=True,
                type="primary"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_result:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📊 Analysis Result</div>', unsafe_allow_html=True)
        
        if submitted:
            # Prepare transaction data
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
            
            # Show loading spinner
            with st.spinner("🔄 Analyzing transaction..."):
                try:
                    # Run fraud detection
                    start_time = datetime.now()
                    df = pd.DataFrame([transaction_data])
                    df_eng = feature_engineer.engineer_all_features(df, fit=False)
                    result = fraud_detector.detect_fraud(df_eng, transaction_data)
                    processing_time = (datetime.now() - start_time).total_seconds() * 1000
                    
                    # Display result
                    risk_level = result['risk_level']
                    risk_score = result['combined_risk_score']
                    recommendation = result['recommendation']
                    triggered_rules = result.get('triggered_rules', [])
                    
                    st.markdown(
                        render_result_card(risk_level, risk_score, recommendation, triggered_rules),
                        unsafe_allow_html=True
                    )
                    
                    # Detailed metrics
                    st.markdown("---")
                    st.markdown("### 📈 Detailed Metrics")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric(
                            "ML Risk Score",
                            f"{result['ml_risk_score']:.2%}",
                            help="Machine Learning model prediction"
                        )
                    with col_b:
                        st.metric(
                            "Rule Risk Score",
                            f"{result['rule_risk_score']:.2%}",
                            help="Rule-based detection score"
                        )
                    with col_c:
                        st.metric(
                            "Processing Time",
                            f"{processing_time:.1f}ms",
                            help="Time taken to analyze"
                        )
                    
                    # Save to session for analytics
                    if 'transaction_history' not in st.session_state:
                        st.session_state.transaction_history = []
                    
                    st.session_state.transaction_history.append({
                        **transaction_data,
                        **result,
                        'processing_time_ms': processing_time
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing transaction: {str(e)}")
                    st.exception(e)
        else:
            st.info("👈 Fill in the transaction details and click 'Analyze Transaction' to get fraud risk assessment.")
            
            # Show example
            st.markdown("---")
            st.markdown("### 💡 Example Scenarios")
            
            with st.expander("🚨 High Risk Transaction"):
                st.markdown("""
                - **Amount:** ₹9,50,00,000 (Very high)
                - **Time:** 2:30 AM (Night transaction)
                - **Distance:** 800 km (Unusual location)
                - **Velocity:** 15 (Multiple rapid transactions)
                - **Authentication:** Failed
                """)
            
            with st.expander("⚠️ Medium Risk Transaction"):
                st.markdown("""
                - **Amount:** ₹2,50,000 (Moderate)
                - **Time:** 11:00 PM (Late night)
                - **Distance:** 150 km (Moderate distance)
                - **Velocity:** 8 (Elevated activity)
                """)
            
            with st.expander("✅ Low Risk Transaction"):
                st.markdown("""
                - **Amount:** ₹5,000 (Normal)
                - **Time:** 2:00 PM (Business hours)
                - **Distance:** 5 km (Local)
                - **Velocity:** 2 (Normal activity)
                - **Authentication:** PIN/Biometric
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
