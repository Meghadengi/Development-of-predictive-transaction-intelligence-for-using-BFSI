"""
SafeBank AI - Premium Fraud Detection System
Enterprise-grade Streamlit dashboard for bank fraud detection
"""
import streamlit as st
import sys
from pathlib import Path
import joblib

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import local modules
from ui.styles import get_custom_css
from ui.components import render_header, render_sidebar_nav
from ui.pages.single_transaction import render_single_transaction_page
from ui.pages.batch_processing import render_batch_processing_page
from ui.pages.analytics import render_analytics_page
from ui.pages.system_info import render_system_info_page
from ui.pages.chatbot import render_chatbot_page

from src.module3_fraud_detection.fraud_detector import FraudDetector
from src.module1_preprocessing.feature_engineer import FeatureEngineer
from config.config import MODELS_DIR, FRAUD_MODEL_PATH


# Page configuration
st.set_page_config(
    page_title="SafeBank AI - Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.safebank.ai/help',
        'Report a bug': 'https://www.safebank.ai/bug',
        'About': '# SafeBank AI Fraud Detection System\nVersion 2.0.1'
    }
)


@st.cache_resource(show_spinner=False)
def load_models():
    """Load fraud detector and feature engineer (cached)"""
    with st.spinner("🔄 Loading AI models..."):
        # Load Fraud Detector
        if Path(FRAUD_MODEL_PATH).exists():
            fraud_detector = FraudDetector(str(FRAUD_MODEL_PATH))
        else:
            fraud_detector = FraudDetector()
        
        # Load Feature Engineer
        engineer_path = MODELS_DIR / "preprocessing" / "feature_engineer.pkl"
        if engineer_path.exists():
            feature_engineer = joblib.load(engineer_path)
        else:
            feature_engineer = FeatureEngineer()
        
        return fraud_detector, feature_engineer


def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'single'
    
    if 'transaction_history' not in st.session_state:
        st.session_state.transaction_history = []
    
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = []
    
    if 'session_id' not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False


def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Render header
    render_header(user_name="Bank Officer")
    
    # Load models
    try:
        fraud_detector, feature_engineer = load_models()
        models_loaded = True
    except Exception as e:
        st.error(f"❌ Error loading models: {str(e)}")
        models_loaded = False
        fraud_detector, feature_engineer = None, None
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 2rem 0 1rem 0;">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: white; margin: 0;">🛡️ SafeBank AI</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Fraud Detection System</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
        
        if st.button("🏠 Single Transaction", key="nav_single", use_container_width=True):
            st.session_state.current_page = 'single'
            st.rerun()
        
        if st.button("📊 Batch Processing", key="nav_batch", use_container_width=True):
            st.session_state.current_page = 'batch'
            st.rerun()
        
        if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.current_page = 'analytics'
            st.rerun()
        
        if st.button("🔧 System Info", key="nav_system", use_container_width=True):
            st.session_state.current_page = 'system'
            st.rerun()
        
        if st.button("💬 Chatbot", key="nav_chatbot", use_container_width=True):
            st.session_state.current_page = 'chatbot'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model status indicator
        if models_loaded:
            st.success("✅ Models Loaded")
        else:
            st.error("❌ Models Not Loaded")
        
        # Quick stats
        if st.session_state.transaction_history:
            st.markdown("### 📊 Session Stats")
            st.metric("Transactions Analyzed", len(st.session_state.transaction_history))
            
            fraud_count = sum(1 for t in st.session_state.transaction_history if t.get('is_fraud', False))
            st.metric("Frauds Detected", fraud_count)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style="text-align: center; color: white; opacity: 0.7; font-size: 0.85rem; padding: 1rem 0;">
            <p>🛡️ SafeBank AI v2.0.1</p>
            <p>© 2024 All Rights Reserved</p>
            <p style="margin-top: 1rem;">
                <a href="#" style="color: white; text-decoration: none;">Privacy</a> • 
                <a href="#" style="color: white; text-decoration: none;">Terms</a> • 
                <a href="#" style="color: white; text-decoration: none;">Support</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content area
    if not models_loaded:
        st.error("⚠️ Models could not be loaded. Please check the system configuration.")
        st.info("💡 Make sure you have run the training pipeline: `python run_all.py`")
        return
    
    # Route to appropriate page
    current_page = st.session_state.current_page
    
    if current_page == 'single':
        render_single_transaction_page(fraud_detector, feature_engineer)
    
    elif current_page == 'batch':
        render_batch_processing_page(fraud_detector, feature_engineer)
    
    elif current_page == 'analytics':
        render_analytics_page()
    
    elif current_page == 'system':
        render_system_info_page()
    
    elif current_page == 'chatbot':
        render_chatbot_page()
    
    else:
        st.error("Invalid page selection")


if __name__ == "__main__":
    main()
