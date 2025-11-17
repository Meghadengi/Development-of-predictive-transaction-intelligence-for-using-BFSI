"""
Reusable UI Components for SafeBank AI Fraud Detection System
"""
import streamlit as st
from datetime import datetime

def render_header(user_name="Bank Officer"):
    """Render the top header bar with logo and user info"""
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-logo">
            <span class="logo-icon">🛡️</span>
            <h1>SafeBank AI</h1>
        </div>
        <div class="header-user">
            <div class="user-info">
                <span>👤</span>
                <span>Welcome, {user_name}</span>
            </div>
            <span style="font-size: 0.9rem; opacity: 0.8;">{datetime.now().strftime("%B %d, %Y")}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(label, value, card_type="info", icon="📊"):
    """Render a KPI card with gradient background"""
    return f"""
    <div class="kpi-card {card_type}">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """


def render_result_card(risk_level, risk_score, recommendation, triggered_rules=None):
    """Render fraud detection result card"""
    risk_class_map = {
        "HIGH": ("high-risk", "🚨", "BLOCK TRANSACTION"),
        "MEDIUM": ("medium-risk", "⚠️", "REVIEW REQUIRED"),
        "LOW": ("low-risk", "ℹ️", "MONITOR"),
        "SAFE": ("safe", "✅", "APPROVE")
    }
    
    risk_class, icon, action = risk_class_map.get(risk_level, ("low-risk", "ℹ️", "REVIEW"))
    
    rules_html = ""
    if triggered_rules:
        rules_html = "<div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);'>"
        rules_html += "<strong>Triggered Rules:</strong><ul style='margin-top: 0.5rem;'>"
        for rule in triggered_rules:
            rules_html += f"<li>{rule}</li>"
        rules_html += "</ul></div>"
    
    return f"""
    <div class="result-card {risk_class}">
        <div style="text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h2 style="margin: 0; font-size: 2rem;">{risk_level} RISK</h2>
            <div style="font-size: 3rem; font-weight: 700; margin: 1rem 0;">{risk_score:.1%}</div>
            <div style="font-size: 1.2rem; font-weight: 600; margin: 1rem 0; padding: 1rem; background: rgba(0,0,0,0.1); border-radius: 10px;">
                {action}
            </div>
            <p style="margin-top: 1rem; opacity: 0.9;">{recommendation}</p>
            {rules_html}
        </div>
    </div>
    """


def render_card(title, content, icon="📋"):
    """Render a generic card container"""
    return f"""
    <div class="card fade-in">
        <div class="card-header">
            <span style="margin-right: 0.5rem;">{icon}</span>
            {title}
        </div>
        <div>
            {content}
        </div>
    </div>
    """


def render_status_badge(status, label):
    """Render a status badge"""
    status_class = {
        "active": "active",
        "inactive": "inactive",
        "warning": "warning"
    }.get(status.lower(), "inactive")
    
    return f'<span class="status-badge {status_class}">{label}</span>'


def render_metric_row(metrics_data):
    """Render a row of metrics"""
    cols = st.columns(len(metrics_data))
    for col, (label, value, delta) in zip(cols, metrics_data):
        with col:
            st.metric(label=label, value=value, delta=delta)


def render_sidebar_nav(current_page):
    """Render sidebar navigation"""
    pages = {
        "🏠 Single Transaction": "single",
        "📊 Batch Processing": "batch",
        "📈 Analytics": "analytics",
        "🔧 System Info": "system"
    }
    
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    
    for page_name, page_key in pages.items():
        active_class = "active" if current_page == page_key else ""
        if st.sidebar.button(page_name, key=page_key, use_container_width=True):
            st.session_state.current_page = page_key
            st.rerun()
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Add footer to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; color: white; opacity: 0.7; font-size: 0.85rem;">
        <p>🛡️ SafeBank AI v2.0</p>
        <p>© 2024 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)


def render_file_upload_area(label="Upload CSV File", help_text="Drag and drop or click to browse"):
    """Render a styled file upload area"""
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #1e3a8a; margin-bottom: 0.5rem;">📁 {label}</h3>
        <p style="color: #6b7280; font-size: 0.9rem;">{help_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    return st.file_uploader("", type=['csv'], label_visibility="collapsed")


def render_info_box(title, content, box_type="info"):
    """Render an information box"""
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    colors = {
        "info": "#3b82f6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444"
    }
    
    icon = icons.get(box_type, "ℹ️")
    color = colors.get(box_type, "#3b82f6")
    
    st.markdown(f"""
    <div style="background: {color}15; border-left: 4px solid {color}; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <div style="display: flex; align-items: start; gap: 0.75rem;">
            <span style="font-size: 1.5rem;">{icon}</span>
            <div>
                <strong style="color: {color}; font-size: 1.1rem;">{title}</strong>
                <p style="margin: 0.5rem 0 0 0; color: #374151;">{content}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_indicator(label, value, max_value=100):
    """Render a progress indicator"""
    percentage = (value / max_value) * 100
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #1e3a8a;">{label}</span>
            <span style="font-weight: 600; color: #1e3a8a;">{value}/{max_value}</span>
        </div>
        <div style="background: #e5e7eb; border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #1e3a8a 0%, #fbbf24 100%); height: 100%; width: {percentage}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
