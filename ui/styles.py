"""
Custom CSS Styles for SafeBank AI Fraud Detection System
Premium fintech-inspired design with navy blue, white, and gold/teal accents
"""

def get_custom_css():
    """Returns custom CSS for the application"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Bar */
    .header-bar {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-radius: 0 0 15px 15px;
        margin: -1rem -1rem 2rem -1rem;
    }
    
    .header-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .header-logo h1 {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .header-logo .logo-icon {
        font-size: 2.5rem;
    }
    
    .header-user {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        color: white;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    .sidebar-nav {
        padding: 1rem;
    }
    
    .nav-item {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: white;
        font-weight: 500;
        border-left: 4px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.2);
        border-left: 4px solid #fbbf24;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .nav-item.active {
        background: rgba(251, 191, 36, 0.2);
        border-left: 4px solid #fbbf24;
        box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(30, 58, 138, 0.1);
    }
    
    .card:hover {
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        transform: translateY(-4px);
    }
    
    .card-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #fbbf24;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
    }
    
    .kpi-card.success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .kpi-card.warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .kpi-card.info {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1e3a8a;
        box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
    }
    
    /* Result Cards */
    .result-card {
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    .result-card.high-risk {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
    }
    
    .result-card.medium-risk {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        color: #1e3a8a;
        box-shadow: 0 8px 24px rgba(254, 202, 87, 0.3);
    }
    
    .result-card.low-risk {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(72, 219, 251, 0.3);
    }
    
    .result-card.safe {
        background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
        color: white;
        box-shadow: 0 8px 24px rgba(29, 209, 161, 0.3);
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    
    /* File Upload */
    [data-testid="stFileUploader"] {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #1e3a8a;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #fbbf24;
        background: rgba(251, 191, 36, 0.05);
    }
    
    /* Tables */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1e3a8a 0%, #fbbf24 100%);
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(30, 58, 138, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
        color: white;
    }
    
    /* Dark Mode Toggle */
    .dark-mode-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: white;
        padding: 0.5rem;
        border-radius: 50%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .dark-mode-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #1e3a8a 0%, #fbbf24 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #1e40af 0%, #fbbf24 100%);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-bar {
            flex-direction: column;
            gap: 1rem;
        }
        
        .kpi-card {
            margin: 0.5rem 0;
        }
        
        .card {
            padding: 1rem;
        }
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-badge.active {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-badge.inactive {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .status-badge.warning {
        background: #fef3c7;
        color: #92400e;
    }
    </style>
    """
