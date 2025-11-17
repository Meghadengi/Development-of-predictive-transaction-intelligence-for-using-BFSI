"""
Custom CSS styles for authentication pages
Professional fintech-inspired design
"""

def get_auth_css():
    """Returns custom CSS for authentication pages"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Auth Container */
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* Auth Card */
    .auth-card {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        max-width: 450px;
        width: 100%;
        animation: slideUp 0.5s ease;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Logo Section */
    .auth-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-logo-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .auth-logo h1 {
        color: #1e3a8a;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .auth-logo p {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Form Styles */
    .auth-form {
        margin-top: 2rem;
    }
    
    .stTextInput > div > div > input,
    .stPasswordInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        background: #f9fafb !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stPasswordInput > div > div > input:focus {
        border-color: #1e3a8a !important;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1) !important;
        background: white !important;
    }
    
    .stTextInput > label,
    .stPasswordInput > label {
        font-weight: 600 !important;
        color: #374151 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.875rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3) !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%) !important;
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Secondary Button */
    .secondary-button {
        background: transparent !important;
        color: #1e3a8a !important;
        border: 2px solid #1e3a8a !important;
    }
    
    .secondary-button:hover {
        background: #1e3a8a !important;
        color: white !important;
    }
    
    /* Links */
    .auth-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    .auth-link a {
        color: #1e3a8a;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .auth-link a:hover {
        color: #2563eb;
        text-decoration: underline;
    }
    
    /* Divider */
    .auth-divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 2rem 0;
        color: #9ca3af;
        font-size: 0.85rem;
    }
    
    .auth-divider::before,
    .auth-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .auth-divider span {
        padding: 0 1rem;
    }
    
    /* Alert Messages */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Success Message */
    .stSuccess {
        background: #d1fae5 !important;
        color: #065f46 !important;
    }
    
    /* Error Message */
    .stError {
        background: #fee2e2 !important;
        color: #991b1b !important;
    }
    
    /* Info Message */
    .stInfo {
        background: #dbeafe !important;
        color: #1e40af !important;
    }
    
    /* Profile Card */
    .profile-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        margin: 2rem 0;
        text-align: center;
    }
    
    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.5rem auto;
        font-size: 3rem;
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
    }
    
    .profile-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
        margin: 0.5rem 0;
    }
    
    .profile-email {
        font-size: 1rem;
        color: #6b7280;
        margin: 0.5rem 0 1.5rem 0;
    }
    
    .profile-info {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: left;
    }
    
    .profile-info-item {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .profile-info-item:last-child {
        border-bottom: none;
    }
    
    .profile-info-label {
        font-weight: 600;
        color: #374151;
    }
    
    .profile-info-value {
        color: #6b7280;
    }
    
    /* Checkbox */
    .stCheckbox {
        margin: 1rem 0 !important;
    }
    
    .stCheckbox > label {
        font-size: 0.9rem !important;
        color: #6b7280 !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .auth-card {
            padding: 2rem;
            margin: 1rem;
        }
        
        .auth-logo h1 {
            font-size: 1.5rem;
        }
        
        .profile-avatar {
            width: 100px;
            height: 100px;
            font-size: 2.5rem;
        }
        
        .profile-name {
            font-size: 1.5rem;
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Forgot Password Link */
    .forgot-password {
        text-align: right;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .forgot-password a {
        color: #1e3a8a;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .forgot-password a:hover {
        color: #2563eb;
        text-decoration: underline;
    }
    
    /* Password Strength Indicator */
    .password-strength {
        margin-top: 0.5rem;
        height: 4px;
        border-radius: 2px;
        background: #e5e7eb;
        overflow: hidden;
    }
    
    .password-strength-bar {
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .strength-weak {
        width: 33%;
        background: #ef4444;
    }
    
    .strength-medium {
        width: 66%;
        background: #f59e0b;
    }
    
    .strength-strong {
        width: 100%;
        background: #10b981;
    }
    </style>
    """
