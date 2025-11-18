"""
SafeBank AI - ChatGPT OSS Chat Assistant
Powered by OpenRouter API with syntax highlighting and code copy features
"""
import streamlit as st
import requests
import json
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SafeBank AI - Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OpenRouter API Configuration
OPENROUTER_API_KEY = "API_KEY"
OPENROUTER_API_URL = "API_KEY_URL"
MODEL = "openai/gpt-oss-20b:free"

# Custom CSS for chat interface
def get_chat_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Chat container */
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat header */
    .chat-header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 2px solid #e5e7eb;
        margin-bottom: 2rem;
    }
    
    .chat-header h1 {
        color: #1e3a8a;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .chat-header p {
        color: #6b7280;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Message bubbles */
    .message {
        margin: 1.5rem 0;
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message-user {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
    }
    
    .message-assistant {
        display: flex;
        justify-content: flex-start;
        gap: 1rem;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    
    .avatar-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .avatar-assistant {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .message-content {
        max-width: 70%;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        position: relative;
    }
    
    .content-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .content-assistant {
        background: #f3f4f6;
        color: #1f2937;
        border-bottom-left-radius: 4px;
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    
    /* Code blocks */
    .code-block-container {
        position: relative;
        margin: 1rem 0;
        border-radius: 12px;
        overflow: hidden;
        background: #1e293b;
    }
    
    .code-header {
        background: #0f172a;
        padding: 0.75rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #334155;
    }
    
    .code-language {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        font-family: 'Fira Code', monospace;
    }
    
    .code-copy-btn {
        background: #3b82f6;
        color: white;
        border: none;
        padding: 0.4rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
        font-weight: 500;
    }
    
    .code-copy-btn:hover {
        background: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .code-copy-btn:active {
        transform: translateY(0);
    }
    
    .code-content {
        padding: 1rem;
        overflow-x: auto;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #e2e8f0;
    }
    
    .code-content pre {
        margin: 0;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Inline code */
    code {
        background: #e5e7eb;
        color: #dc2626;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
        font-size: 0.9em;
    }
    
    /* Input area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e5e7eb !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
    }
    </style>
    """


def call_openrouter_api(messages):
    """
    Call OpenRouter API with chat messages
    Returns: (success: bool, response: str or error message)
    """
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://safebank-ai.app",
            "X-Title": "SafeBank AI Chat",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": messages
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data['choices'][0]['message']['content']
            return True, message
        else:
            return False, f"API Error: {response.status_code} - {response.text}"
    
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def extract_code_blocks(text):
    """
    Extract code blocks from markdown text
    Returns: list of (language, code) tuples and text with placeholders
    """
    code_blocks = []
    pattern = r'```(\w+)?\n(.*?)```'
    
    def replacer(match):
        language = match.group(1) or 'text'
        code = match.group(2)
        code_blocks.append((language, code))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"
    
    processed_text = re.sub(pattern, replacer, text, flags=re.DOTALL)
    return code_blocks, processed_text


def render_code_block(language, code, index):
    """Render a code block with syntax highlighting and copy button"""
    # Clean up code
    code = code.strip()
    
    # Generate unique ID for this code block
    block_id = f"code_{index}_{hash(code) % 10000}"
    
    st.markdown(f"""
    <div class="code-block-container">
        <div class="code-header">
            <span class="code-language">{language}</span>
            <button class="code-copy-btn" onclick="copyCode_{block_id}()">
                📋 Copy Code
            </button>
        </div>
        <div class="code-content">
            <pre id="{block_id}">{code}</pre>
        </div>
    </div>
    <script>
    function copyCode_{block_id}() {{
        const code = document.getElementById('{block_id}').innerText;
        navigator.clipboard.writeText(code).then(() => {{
            const btn = event.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = '✅ Copied!';
            setTimeout(() => {{
                btn.innerHTML = originalText;
            }}, 2000);
        }});
    }}
    </script>
    """, unsafe_allow_html=True)


def render_message(role, content, timestamp):
    """Render a chat message with proper formatting"""
    is_user = role == "user"
    
    # Extract code blocks
    code_blocks, processed_text = extract_code_blocks(content)
    
    # Avatar
    avatar_class = "avatar-user" if is_user else "avatar-assistant"
    avatar_icon = "👤" if is_user else "🤖"
    
    # Message alignment
    message_class = "message-user" if is_user else "message-assistant"
    content_class = "content-user" if is_user else "content-assistant"
    
    # Start message container
    if is_user:
        col1, col2 = st.columns([3, 1])
        with col2:
            st.markdown(f"""
            <div class="{message_class}">
                <div class="message-content {content_class}">
                    {processed_text}
                    <div class="message-time">{timestamp}</div>
                </div>
                <div class="message-avatar {avatar_class}">{avatar_icon}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div class="{message_class}">
                <div class="message-avatar {avatar_class}">{avatar_icon}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            # Render text parts and code blocks
            parts = processed_text.split("__CODE_BLOCK_")
            
            st.markdown(f'<div class="message-content {content_class}">', unsafe_allow_html=True)
            
            for i, part in enumerate(parts):
                if i == 0:
                    # First part is always text
                    if part.strip():
                        st.markdown(part)
                else:
                    # Extract code block index
                    block_idx = int(part.split("__")[0])
                    remaining_text = part.split("__", 1)[1] if "__" in part else ""
                    
                    # Render code block
                    if block_idx < len(code_blocks):
                        language, code = code_blocks[block_idx]
                        render_code_block(language, code, block_idx)
                    
                    # Render remaining text
                    if remaining_text.strip():
                        st.markdown(remaining_text)
            
            st.markdown(f'<div class="message-time">{timestamp}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


def main():
    """Main chat application"""
    
    # Apply custom CSS
    st.markdown(get_chat_css(), unsafe_allow_html=True)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: white; margin: 0;">💬 Chat Assistant</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Powered by ChatGPT OSS</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Stats
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{st.session_state.message_count}</div>
            <div class="stats-label">Messages Sent</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Model info
        st.markdown("### 🤖 Model Info")
        st.info(f"**Model**: {MODEL}")
        st.info("**Provider**: OpenRouter")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.message_count = 0
            st.rerun()
        
        st.markdown("---")
        
        # Features
        st.markdown("### ✨ Features")
        st.markdown("""
        - 💬 Real-time chat
        - 🎨 Syntax highlighting
        - 📋 Copy code blocks
        - 🚀 Fast responses
        - 🔒 Secure API
        """)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="text-align: center; color: white; opacity: 0.7; font-size: 0.85rem;">
            <p>🛡️ SafeBank AI</p>
            <p>© 2024 All Rights Reserved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat area
    st.markdown("""
    <div class="chat-header">
        <h1>💬 SafeBank AI Chat Assistant</h1>
        <p>Ask me anything about fraud detection, coding, or general questions!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            render_message(msg['role'], msg['content'], msg['timestamp'])
    
    # Input area
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message...",
            height=100,
            placeholder="Ask me anything! I can help with code, explanations, and more...",
            key="user_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    # Handle send button
    if send_button and user_input.strip():
        # Add user message
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        st.session_state.message_count += 1
        
        # Prepare messages for API
        api_messages = [
            {'role': msg['role'], 'content': msg['content']}
            for msg in st.session_state.messages
        ]
        
        # Call API
        with st.spinner("🤔 Thinking..."):
            success, response = call_openrouter_api(api_messages)
        
        if success:
            # Add assistant response
            timestamp = datetime.now().strftime("%I:%M %p")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': response,
                'timestamp': timestamp
            })
        else:
            # Show error
            st.error(f"❌ {response}")
        
        # Rerun to display new messages
        st.rerun()
    
    # Welcome message if no messages
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0; color: #6b7280;">
            <h3>👋 Welcome to SafeBank AI Chat!</h3>
            <p>Start a conversation by typing a message below.</p>
            <br>
            <p><strong>Try asking:</strong></p>
            <ul style="list-style: none; padding: 0;">
                <li>💡 "Explain fraud detection algorithms"</li>
                <li>💻 "Write Python code for data validation"</li>
                <li>🔍 "How does machine learning detect fraud?"</li>
                <li>📊 "Show me a data visualization example"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
