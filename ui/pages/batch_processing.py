"""
Batch Processing Page for Multiple Transactions
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ui.components import render_info_box, render_file_upload_area, render_progress_indicator


def render_batch_processing_page(fraud_detector, feature_engineer):
    """Render the batch processing page"""
    
    st.markdown('<h1 style="color: #1e3a8a; margin-bottom: 2rem;">📊 Batch Transaction Processing</h1>', unsafe_allow_html=True)
    
    render_info_box(
        "Bulk Analysis",
        "Upload a CSV file containing multiple transactions to analyze them all at once. Get comprehensive insights and export results.",
        "info"
    )
    
    # File upload section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = render_file_upload_area(
        "Upload Transaction Data",
        "Supported format: CSV with required columns"
    )
    
    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Successfully loaded **{len(df)}** transactions")
            
            # Show data preview
            with st.expander("👁️ Preview Data", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Total Columns", len(df.columns))
                with col3:
                    st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Process button
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                process_button = st.button(
                    "🚀 Process All Transactions",
                    use_container_width=True,
                    type="primary"
                )
            
            if process_button:
                # Processing section
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">⚙️ Processing Results</div>', unsafe_allow_html=True)
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    start_time = datetime.now()
                    results = []
                    
                    # Process each transaction
                    for idx, row in df.iterrows():
                        progress = (idx + 1) / len(df)
                        progress_bar.progress(progress)
                        status_text.text(f"Processing transaction {idx + 1} of {len(df)}...")
                        
                        transaction_dict = row.to_dict()
                        transaction_df = pd.DataFrame([transaction_dict])
                        
                        # Engineer features and detect fraud
                        df_eng = feature_engineer.engineer_all_features(transaction_df, fit=False)
                        result = fraud_detector.detect_fraud(df_eng, transaction_dict)
                        results.append(result)
                    
                    processing_time = (datetime.now() - start_time).total_seconds()
                    progress_bar.progress(1.0)
                    status_text.text("✅ Processing complete!")
                    
                    # Create results dataframe
                    results_df = pd.DataFrame(results)
                    
                    # Summary metrics
                    st.markdown("---")
                    st.markdown("### 📈 Summary Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_transactions = len(results_df)
                    fraud_detected = int(results_df['is_fraud'].sum())
                    fraud_rate = fraud_detected / total_transactions if total_transactions > 0 else 0
                    avg_risk_score = float(results_df['combined_risk_score'].mean())
                    
                    with col1:
                        st.markdown(f"""
                        <div class="kpi-card info">
                            <div style="font-size: 1.5rem;">📊</div>
                            <div class="kpi-label">Total Processed</div>
                            <div class="kpi-value">{total_transactions}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="kpi-card warning">
                            <div style="font-size: 1.5rem;">🚨</div>
                            <div class="kpi-label">Frauds Detected</div>
                            <div class="kpi-value">{fraud_detected}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="kpi-card">
                            <div style="font-size: 1.5rem;">📉</div>
                            <div class="kpi-label">Fraud Rate</div>
                            <div class="kpi-value">{fraud_rate:.1%}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="kpi-card success">
                            <div style="font-size: 1.5rem;">⚡</div>
                            <div class="kpi-label">Processing Time</div>
                            <div class="kpi-value">{processing_time:.1f}s</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # Visualizations
                    col_viz1, col_viz2 = st.columns(2)
                    
                    with col_viz1:
                        # Risk distribution pie chart
                        risk_counts = results_df['risk_level'].value_counts()
                        fig_pie = px.pie(
                            values=risk_counts.values,
                            names=risk_counts.index,
                            title="Risk Level Distribution",
                            color_discrete_map={
                                'HIGH': '#ef4444',
                                'MEDIUM': '#f59e0b',
                                'LOW': '#3b82f6',
                                'SAFE': '#10b981'
                            },
                            hole=0.4
                        )
                        fig_pie.update_layout(
                            font=dict(family="Poppins", size=12),
                            showlegend=True,
                            height=400
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col_viz2:
                        # Risk score distribution histogram
                        fig_hist = px.histogram(
                            results_df,
                            x='combined_risk_score',
                            nbins=30,
                            title="Risk Score Distribution",
                            labels={'combined_risk_score': 'Risk Score'},
                            color_discrete_sequence=['#1e3a8a']
                        )
                        fig_hist.update_layout(
                            font=dict(family="Poppins", size=12),
                            showlegend=False,
                            height=400,
                            xaxis_title="Risk Score",
                            yaxis_title="Count"
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    # Detailed results table
                    st.markdown("---")
                    st.markdown("### 📋 Detailed Results")
                    
                    # Add filters
                    col_filter1, col_filter2 = st.columns(2)
                    with col_filter1:
                        risk_filter = st.multiselect(
                            "Filter by Risk Level",
                            options=['HIGH', 'MEDIUM', 'LOW', 'SAFE'],
                            default=['HIGH', 'MEDIUM', 'LOW', 'SAFE']
                        )
                    with col_filter2:
                        fraud_filter = st.selectbox(
                            "Filter by Fraud Status",
                            options=['All', 'Fraud Only', 'Non-Fraud Only']
                        )
                    
                    # Apply filters
                    filtered_df = results_df[results_df['risk_level'].isin(risk_filter)]
                    if fraud_filter == 'Fraud Only':
                        filtered_df = filtered_df[filtered_df['is_fraud'] == True]
                    elif fraud_filter == 'Non-Fraud Only':
                        filtered_df = filtered_df[filtered_df['is_fraud'] == False]
                    
                    # Display table
                    st.dataframe(
                        filtered_df[[
                            'risk_level', 'combined_risk_score', 'ml_risk_score',
                            'rule_risk_score', 'is_fraud', 'recommendation'
                        ]].style.background_gradient(subset=['combined_risk_score'], cmap='RdYlGn_r'),
                        use_container_width=True,
                        height=400
                    )
                    
                    # Download results
                    st.markdown("---")
                    col_download1, col_download2, col_download3 = st.columns([1, 2, 1])
                    with col_download2:
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=f"fraud_detection_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                    # Save to session state
                    st.session_state['batch_results'] = results
                    st.session_state['batch_df'] = results_df
                    
                except Exception as e:
                    st.error(f"❌ Error processing transactions: {str(e)}")
                    st.exception(e)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            st.info("Please ensure your CSV file has the required columns.")
    
    else:
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show required format
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-header">📋 Required CSV Format</div>', unsafe_allow_html=True)
        
        st.markdown("""
        Your CSV file should contain the following columns:
        
        | Column Name | Description | Example |
        |------------|-------------|---------|
        | `Transaction_Amount` | Transaction amount | 50000 |
        | `Transaction_Date` | Date of transaction | 2024-01-15 |
        | `Transaction_Time` | Time of transaction | 14:30:00 |
        | `Transaction_Location` | Location | Mumbai |
        | `Card_Type` | Type of card | Visa |
        | `Transaction_Currency` | Currency code | INR |
        | `Transaction_Status` | Status | Completed |
        | `Previous_Transaction_Count` | Previous count | 25 |
        | `Distance_Between_Transactions_km` | Distance in km | 10.5 |
        | `Time_Since_Last_Transaction_min` | Time in minutes | 120 |
        | `Authentication_Method` | Auth method | PIN |
        | `Transaction_Velocity` | Velocity | 3 |
        | `Transaction_Category` | Category | Shopping |
        """)
        
        # Sample data download
        sample_data = pd.DataFrame({
            'Transaction_Amount': [50000, 95000000, 25000],
            'Transaction_Date': ['2024-01-15', '2024-01-15', '2024-01-15'],
            'Transaction_Time': ['14:30:00', '02:30:00', '10:00:00'],
            'Transaction_Location': ['Mumbai', 'Unknown', 'Delhi'],
            'Card_Type': ['Visa', 'Mastercard', 'RuPay'],
            'Transaction_Currency': ['INR', 'INR', 'INR'],
            'Transaction_Status': ['Completed', 'Pending', 'Completed'],
            'Previous_Transaction_Count': [25, 2, 50],
            'Distance_Between_Transactions_km': [10.5, 800.0, 5.0],
            'Time_Since_Last_Transaction_min': [120, 1, 240],
            'Authentication_Method': ['PIN', 'Failed', 'Biometric'],
            'Transaction_Velocity': [3, 15, 2],
            'Transaction_Category': ['Shopping', 'Transfer', 'Payment']
        })
        
        st.download_button(
            label="📥 Download Sample CSV Template",
            data=sample_data.to_csv(index=False),
            file_name="sample_transactions.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
