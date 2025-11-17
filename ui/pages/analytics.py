"""
Analytics Dashboard Page
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ui.components import render_kpi_card, render_info_box


def render_analytics_page():
    """Render the analytics dashboard page"""
    
    st.markdown('<h1 style="color: #1e3a8a; margin-bottom: 2rem;">📈 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Check if we have data
    if 'batch_results' in st.session_state and st.session_state['batch_results']:
        results_df = pd.DataFrame(st.session_state['batch_results'])
        
        # KPI Cards
        st.markdown("### 🎯 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(results_df)
        fraud_count = int(results_df['is_fraud'].sum())
        fraud_rate = fraud_count / total if total > 0 else 0
        avg_risk = float(results_df['combined_risk_score'].mean())
        
        with col1:
            st.markdown(
                render_kpi_card("Total Transactions", f"{total:,}", "info", "📊"),
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                render_kpi_card("Frauds Detected", f"{fraud_count:,}", "warning", "🚨"),
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                render_kpi_card("Fraud Rate", f"{fraud_rate:.1%}", "warning" if fraud_rate > 0.05 else "success", "📉"),
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                render_kpi_card("Avg Risk Score", f"{avg_risk:.2%}", "info", "⚡"),
                unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Section
        tab1, tab2, tab3 = st.tabs(["📊 Risk Analysis", "🎯 Detection Metrics", "📈 Trends"])
        
        with tab1:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Risk Level Distribution
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Risk Level Distribution")
                
                risk_counts = results_df['risk_level'].value_counts()
                fig_donut = go.Figure(data=[go.Pie(
                    labels=risk_counts.index,
                    values=risk_counts.values,
                    hole=.5,
                    marker=dict(colors=['#ef4444', '#f59e0b', '#3b82f6', '#10b981']),
                    textinfo='label+percent',
                    textfont=dict(size=14, family='Poppins')
                )])
                
                fig_donut.update_layout(
                    showlegend=True,
                    height=350,
                    font=dict(family="Poppins"),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_donut, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_chart2:
                # Risk Score Distribution
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Risk Score Distribution")
                
                fig_violin = go.Figure(data=go.Violin(
                    y=results_df['combined_risk_score'],
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor='#1e3a8a',
                    opacity=0.6,
                    line_color='#1e40af'
                ))
                
                fig_violin.update_layout(
                    yaxis_title="Risk Score",
                    showlegend=False,
                    height=350,
                    font=dict(family="Poppins"),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_violin, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # ML vs Rule-Based Comparison
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### ML Score vs Rule-Based Score Comparison")
            
            fig_scatter = px.scatter(
                results_df,
                x='ml_risk_score',
                y='rule_risk_score',
                color='risk_level',
                size='combined_risk_score',
                hover_data=['is_fraud'],
                color_discrete_map={
                    'HIGH': '#ef4444',
                    'MEDIUM': '#f59e0b',
                    'LOW': '#3b82f6',
                    'SAFE': '#10b981'
                },
                labels={
                    'ml_risk_score': 'ML Risk Score',
                    'rule_risk_score': 'Rule-Based Risk Score'
                }
            )
            
            fig_scatter.update_layout(
                height=400,
                font=dict(family="Poppins"),
                showlegend=True
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            col_metric1, col_metric2 = st.columns(2)
            
            with col_metric1:
                # Confusion Matrix Style Display
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Detection Performance")
                
                true_fraud = int(results_df[results_df['is_fraud'] == True]['is_fraud'].count())
                false_fraud = int(results_df[results_df['is_fraud'] == False]['is_fraud'].count())
                
                fig_bar = go.Figure(data=[
                    go.Bar(
                        name='Fraud Detected',
                        x=['Fraud', 'Non-Fraud'],
                        y=[true_fraud, false_fraud],
                        marker_color=['#ef4444', '#10b981'],
                        text=[true_fraud, false_fraud],
                        textposition='auto',
                    )
                ])
                
                fig_bar.update_layout(
                    height=350,
                    font=dict(family="Poppins"),
                    showlegend=False,
                    yaxis_title="Count",
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_metric2:
                # Risk Level Breakdown
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Risk Level Breakdown")
                
                risk_breakdown = results_df.groupby('risk_level').agg({
                    'is_fraud': 'sum',
                    'combined_risk_score': 'mean'
                }).reset_index()
                
                fig_grouped = go.Figure()
                
                fig_grouped.add_trace(go.Bar(
                    x=risk_breakdown['risk_level'],
                    y=risk_breakdown['is_fraud'],
                    name='Fraud Count',
                    marker_color='#ef4444'
                ))
                
                fig_grouped.update_layout(
                    height=350,
                    font=dict(family="Poppins"),
                    yaxis_title="Fraud Count",
                    xaxis_title="Risk Level",
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_grouped, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Top Triggered Rules
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Most Triggered Rules")
            
            all_rules = []
            for rules in results_df['triggered_rules']:
                if isinstance(rules, list):
                    all_rules.extend(rules)
            
            if all_rules:
                rules_df = pd.DataFrame({'rule': all_rules})
                rule_counts = rules_df['rule'].value_counts().head(10)
                
                fig_rules = px.bar(
                    x=rule_counts.values,
                    y=rule_counts.index,
                    orientation='h',
                    labels={'x': 'Count', 'y': 'Rule'},
                    color=rule_counts.values,
                    color_continuous_scale='Reds'
                )
                
                fig_rules.update_layout(
                    height=400,
                    font=dict(family="Poppins"),
                    showlegend=False,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                
                st.plotly_chart(fig_rules, use_container_width=True)
            else:
                st.info("No rules were triggered in the analyzed transactions.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            # Simulated time-series (if timestamp available)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### Risk Score Trend Over Time")
            
            # Add index as time proxy
            results_df['transaction_index'] = range(len(results_df))
            
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=results_df['transaction_index'],
                y=results_df['combined_risk_score'],
                mode='lines+markers',
                name='Risk Score',
                line=dict(color='#1e3a8a', width=2),
                marker=dict(size=6, color=results_df['combined_risk_score'], colorscale='RdYlGn_r', showscale=True)
            ))
            
            fig_trend.add_hline(
                y=0.7,
                line_dash="dash",
                line_color="red",
                annotation_text="High Risk Threshold",
                annotation_position="right"
            )
            
            fig_trend.add_hline(
                y=0.4,
                line_dash="dash",
                line_color="orange",
                annotation_text="Medium Risk Threshold",
                annotation_position="right"
            )
            
            fig_trend.update_layout(
                height=400,
                font=dict(family="Poppins"),
                xaxis_title="Transaction Number",
                yaxis_title="Risk Score",
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Rolling statistics
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Statistical Summary")
                
                stats = results_df[['ml_risk_score', 'rule_risk_score', 'combined_risk_score']].describe()
                st.dataframe(stats.style.format("{:.4f}"), use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_stat2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("#### Risk Distribution")
                
                risk_dist = results_df['risk_level'].value_counts()
                for level, count in risk_dist.items():
                    percentage = (count / total) * 100
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                            <strong>{level}</strong>
                            <span>{count} ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: #e5e7eb; border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: {'#ef4444' if level=='HIGH' else '#f59e0b' if level=='MEDIUM' else '#3b82f6' if level=='LOW' else '#10b981'}; height: 100%; width: {percentage}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    elif 'transaction_history' in st.session_state and st.session_state['transaction_history']:
        # Show single transaction history
        history_df = pd.DataFrame(st.session_state['transaction_history'])
        
        render_info_box(
            "Transaction History",
            f"Showing analytics for {len(history_df)} single transactions analyzed in this session.",
            "info"
        )
        
        # Similar analytics but for single transactions
        st.markdown("### Recent Transactions")
        st.dataframe(
            history_df[['Transaction_Amount', 'risk_level', 'combined_risk_score', 'recommendation']].tail(10),
            use_container_width=True
        )
    
    else:
        # No data available
        render_info_box(
            "No Data Available",
            "Process some transactions in the 'Single Transaction' or 'Batch Processing' pages to see analytics here.",
            "warning"
        )
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 What You'll See Here")
        st.markdown("""
        Once you process transactions, this dashboard will display:
        
        - **KPI Cards**: Total transactions, fraud detection rate, average risk scores
        - **Risk Distribution**: Visual breakdown of risk levels
        - **Performance Metrics**: Detection accuracy and model performance
        - **Trend Analysis**: Risk score patterns over time
        - **Rule Analysis**: Most frequently triggered fraud rules
        - **Statistical Insights**: Detailed statistical summaries
        
        Get started by analyzing transactions in the other sections!
        """)
        st.markdown('</div>', unsafe_allow_html=True)
