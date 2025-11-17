"""
SafeBank AI - Fraud Detection System with Authentication
Enterprise-grade Streamlit dashboard with secure login/signup
"""
import streamlit as st
import sys
from pathlib import Path
import re
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import authentication modules
from auth.database import AuthDatabase
from auth.auth_styles import get_auth_css

# Import existing UI modules (will be loaded after authentication)
try:
    from ui.pages.single_transaction import render_single_transaction_page
    from ui.pages.batch_processing import render_batch_processing_page
    from ui.pages.analytics import render_analytics_page
    from ui.pages.system_info import render_system_info_page
    from ui.pages.chatbot import render_chatbot_page
    from src.module3_fraud_detection.fraud_detector import FraudDetector
    from src.module1_preprocessing.feature_engineer import FeatureEngineer
    from config.config import MODELS_DIR, FRAUD_MODEL_PATH
    import joblib
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False


# Page configuration
st.set_page_config(
    page_title="SafeBank AI - Login",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Initialize database
@st.cache_resource
def get_database():
    """Initialize and return database instance"""
    return AuthDatabase()


# Load models (cached)
@st.cache_resource(show_spinner=False)
def load_models():
    """Load fraud detector and feature engineer (cached)"""
    if not MODULES_AVAILABLE:
        return None, None
    
    try:
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
            from src.module1_preprocessing.feature_engineer import FeatureEngineer
            feature_engineer = FeatureEngineer()
        
        return fraud_detector, feature_engineer
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    Validate password strength
    Returns: (is_valid: bool, message: str, strength: str)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long", "weak"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    strength_score = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength_score < 2:
        return False, "Password must contain uppercase, lowercase, and numbers", "weak"
    elif strength_score == 2:
        return True, "Password strength: Medium", "medium"
    elif strength_score == 3:
        return True, "Password strength: Good", "medium"
    else:
        return True, "Password strength: Strong", "strong"


def login_page():
    """Render the login page"""
    db = get_database()
    
    # Apply custom CSS
    st.markdown(get_auth_css(), unsafe_allow_html=True)
    
    # Center container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and branding
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">
                <div class="auth-logo-icon">🛡️</div>
                <h1>SafeBank AI</h1>
                <p>Secure Fraud Detection Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="Enter your email",
                key="login_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            # Forgot password link
            st.markdown("""
            <div class="forgot-password">
                <a href="#" onclick="alert('Password reset feature coming soon!')">Forgot Password?</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Remember me checkbox
            remember_me = st.checkbox("Remember me")
            
            # Login button
            login_button = st.form_submit_button("🔐 Login to Dashboard", use_container_width=True)
        
        # Handle login
        if login_button:
            if not email or not password:
                st.error("⚠️ Please fill in all fields")
            elif not validate_email(email):
                st.error("⚠️ Please enter a valid email address")
            else:
                with st.spinner("🔄 Authenticating..."):
                    success, user_data = db.verify_user(email, password)
                    
                    if success:
                        # Set session state
                        st.session_state.authenticated = True
                        st.session_state.user = user_data
                        st.session_state.page = 'dashboard'
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
        
        # Divider
        st.markdown("""
        <div class="auth-divider">
            <span>OR</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Switch to signup
        st.markdown('<div class="auth-link">', unsafe_allow_html=True)
        if st.button("Don't have an account? Sign Up", use_container_width=True, key="goto_signup"):
            st.session_state.page = 'signup'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Footer info
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: white; font-size: 0.85rem;">
            <p>🔒 Secure Authentication • 🛡️ Bank-Grade Security</p>
            <p style="opacity: 0.8;">© 2024 SafeBank AI. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)


def signup_page():
    """Render the signup page"""
    db = get_database()
    
    # Apply custom CSS
    st.markdown(get_auth_css(), unsafe_allow_html=True)
    
    # Center container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo and branding
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">
                <div class="auth-logo-icon">🛡️</div>
                <h1>Create Account</h1>
                <p>Join SafeBank AI Platform</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="auth-form">', unsafe_allow_html=True)
        
        # Signup form
        with st.form("signup_form", clear_on_submit=True):
            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                key="signup_name"
            )
            
            email = st.text_input(
                "Email Address",
                placeholder="Enter your email",
                key="signup_email"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a strong password",
                key="signup_password",
                help="At least 8 characters with uppercase, lowercase, and numbers"
            )
            
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter your password",
                key="signup_confirm_password"
            )
            
            # Terms and conditions
            agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            # Signup button
            signup_button = st.form_submit_button("🚀 Create Account", use_container_width=True)
        
        # Handle signup
        if signup_button:
            # Validation
            if not all([full_name, email, password, confirm_password]):
                st.error("⚠️ Please fill in all fields")
            elif not validate_email(email):
                st.error("⚠️ Please enter a valid email address")
            elif password != confirm_password:
                st.error("⚠️ Passwords do not match")
            elif not agree_terms:
                st.error("⚠️ Please agree to the Terms of Service")
            else:
                # Validate password strength
                is_valid, message, strength = validate_password(password)
                
                if not is_valid:
                    st.error(f"⚠️ {message}")
                else:
                    with st.spinner("🔄 Creating your account..."):
                        success, msg = db.create_user(full_name, email, password)
                        
                        if success:
                            st.success("✅ Account created successfully!")
                            st.info("👉 Please login with your credentials")
                            st.balloons()
                            
                            # Auto-switch to login after 2 seconds
                            import time
                            time.sleep(2)
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
        
        # Divider
        st.markdown("""
        <div class="auth-divider">
            <span>OR</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Switch to login
        st.markdown('<div class="auth-link">', unsafe_allow_html=True)
        if st.button("Already have an account? Login", use_container_width=True, key="goto_login"):
            st.session_state.page = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Footer info
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; color: white; font-size: 0.85rem;">
            <p>🔒 Your data is encrypted and secure</p>
            <p style="opacity: 0.8;">© 2024 SafeBank AI. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)


def profile_page():
    """Render the user profile page"""
    if 'user' not in st.session_state:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    user = st.session_state.user
    db = get_database()
    
    st.markdown('<h1 style="color: #1e3a8a; margin-bottom: 2rem;">👤 User Profile</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Profile card
        st.markdown(f"""
        <div class="profile-card">
            <div class="profile-avatar">
                {user['name'][0].upper()}
            </div>
            <div class="profile-name">{user['name']}</div>
            <div class="profile-email">{user['email']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="primary"):
            # Clear session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Logged out successfully")
            st.rerun()
    
    with col2:
        # Profile information
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Account Information")
        
        # Get fresh user data
        user_data = db.get_user_by_email(user['email'])
        
        if user_data:
            st.markdown(f"""
            <div class="profile-info">
                <div class="profile-info-item">
                    <span class="profile-info-label">User ID:</span>
                    <span class="profile-info-value">#{user_data['id']}</span>
                </div>
                <div class="profile-info-item">
                    <span class="profile-info-label">Full Name:</span>
                    <span class="profile-info-value">{user_data['name']}</span>
                </div>
                <div class="profile-info-item">
                    <span class="profile-info-label">Email:</span>
                    <span class="profile-info-value">{user_data['email']}</span>
                </div>
                <div class="profile-info-item">
                    <span class="profile-info-label">Member Since:</span>
                    <span class="profile-info-value">{user_data['created_at'][:10]}</span>
                </div>
                <div class="profile-info-item">
                    <span class="profile-info-label">Last Login:</span>
                    <span class="profile-info-value">{user_data.get('last_login', 'N/A')[:19] if user_data.get('last_login') else 'N/A'}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Edit profile section
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.markdown("### ✏️ Edit Profile")
        
        with st.form("edit_profile_form"):
            new_name = st.text_input("Full Name", value=user['name'])
            
            col_a, col_b = st.columns(2)
            with col_a:
                update_button = st.form_submit_button("💾 Update Profile", use_container_width=True)
            with col_b:
                cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if update_button:
            if new_name and new_name != user['name']:
                success, msg = db.update_user_profile(user['email'], new_name)
                if success:
                    st.success("✅ Profile updated successfully!")
                    st.session_state.user['name'] = new_name
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
            else:
                st.info("ℹ️ No changes made")
        
        st.markdown('</div>', unsafe_allow_html=True)


def dashboard_page():
    """Render the main dashboard with fraud detection features"""
    if 'user' not in st.session_state:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    user = st.session_state.user
    
    # Import styles from premium UI
    from ui.styles import get_custom_css
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Header with user info
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-logo">
            <span class="logo-icon">🛡️</span>
            <h1>SafeBank AI</h1>
        </div>
        <div class="header-user">
            <div class="user-info">
                <span>👤</span>
                <span>Welcome, {user['name']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load models
    fraud_detector, feature_engineer = load_models()
    
    if not fraud_detector or not feature_engineer:
        st.error("⚠️ Models not loaded. Please run training pipeline first.")
        st.info("💡 Run: `python run_all.py`")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 2rem 0 1rem 0;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: white; margin: 0;">👤 {user["name"]}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{user["email"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Single Transaction", key="nav_single", use_container_width=True):
            st.session_state.dashboard_page = 'single'
            st.rerun()
        
        if st.button("📊 Batch Processing", key="nav_batch", use_container_width=True):
            st.session_state.dashboard_page = 'batch'
            st.rerun()
        
        if st.button("📈 Analytics", key="nav_analytics", use_container_width=True):
            st.session_state.dashboard_page = 'analytics'
            st.rerun()
        
        if st.button("🔧 System Info", key="nav_system", use_container_width=True):
            st.session_state.dashboard_page = 'system'
            st.rerun()
        
        if st.button("💬 Chatbot", key="nav_chatbot", use_container_width=True):
            st.session_state.dashboard_page = 'chatbot'
            st.rerun()
        
        st.markdown("---")
        
        if st.button("👤 My Profile", key="nav_profile", use_container_width=True):
            st.session_state.page = 'profile'
            st.rerun()
        
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: white; opacity: 0.7; font-size: 0.85rem;">
            <p>🛡️ SafeBank AI v2.0</p>
            <p>© 2024 All Rights Reserved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content based on selected page
    if 'dashboard_page' not in st.session_state:
        st.session_state.dashboard_page = 'single'
    
    current_page = st.session_state.dashboard_page
    
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


def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        # Show login or signup page
        if st.session_state.page == 'signup':
            signup_page()
        else:
            login_page()
    else:
        # Show authenticated pages
        if st.session_state.page == 'profile':
            profile_page()
        else:
            dashboard_page()


if __name__ == "__main__":
    main()
