"""
Chatbot page for SafeBank AI
AI-powered assistant for fraud detection queries
"""
import streamlit as st
import requests
import re
from datetime import datetime


# OpenRouter API Configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-oss-20b:free"


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
            return False, f"API Error: {response.status_code}"
    
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def extract_code_blocks(text):
    """Extract code blocks from markdown text"""
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
    """Render a code block with copy button"""
    code = code.strip()
    block_id = f"code_{index}_{hash(code) % 10000}"
    
    st.markdown(f"""
    <div style="background: #1e293b; border-radius: 12px; overflow: hidden; margin: 1rem 0;">
        <div style="background: #0f172a; padding: 0.75rem 1rem; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;">
            <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; font-family: 'Fira Code', monospace;">{language}</span>
            <button onclick="copyCode_{block_id}()" style="background: #3b82f6; color: white; border: none; padding: 0.4rem 1rem; border-radius: 6px; font-size: 0.85rem; cursor: pointer; font-family: 'Poppins', sans-serif; font-weight: 500;">
                📋 Copy Code
            </button>
        </div>
        <div style="padding: 1rem; overflow-x: auto; font-family: 'Fira Code', monospace; font-size: 0.9rem; line-height: 1.6; color: #e2e8f0;">
            <pre id="{block_id}" style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">{code}</pre>
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
    """Render a chat message"""
    is_user = role == "user"
    
    # Extract code blocks
    code_blocks, processed_text = extract_code_blocks(content)
    
    if is_user:
        # User message (right-aligned)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-end; margin: 1.5rem 0;">
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%); color: white; padding: 1rem 1.5rem; border-radius: 16px; max-width: 70%; border-bottom-right-radius: 4px;">
                {processed_text}
                <div style="font-size: 0.75rem; opacity: 0.8; margin-top: 0.5rem;">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # AI message (left-aligned)
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 1.5rem 0;">
            <div style="background: #f3f4f6; color: #1f2937; padding: 1rem 1.5rem; border-radius: 16px; max-width: 70%; border-bottom-left-radius: 4px;">
        """, unsafe_allow_html=True)
        
        # Render text parts and code blocks
        parts = processed_text.split("__CODE_BLOCK_")
        
        for i, part in enumerate(parts):
            if i == 0:
                if part.strip():
                    st.markdown(part)
            else:
                block_idx = int(part.split("__")[0])
                remaining_text = part.split("__", 1)[1] if "__" in part else ""
                
                if block_idx < len(code_blocks):
                    language, code = code_blocks[block_idx]
                    render_code_block(language, code, block_idx)
                
                if remaining_text.strip():
                    st.markdown(remaining_text)
        
        st.markdown(f"""
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 0.5rem;">{timestamp}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_chatbot_page():
    """Render the chatbot page"""
    
    # Initialize session state for chatbot
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'chat_message_count' not in st.session_state:
        st.session_state.chat_message_count = 0
    
    # Page header
    st.markdown("""
    <div class="card" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1e3a8a; margin: 0; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <span>💬</span>
            <span>AI Chat Assistant</span>
        </h1>
        <p style="color: #6b7280; margin: 0.5rem 0 0 0;">Ask me anything about fraud detection, coding, or general questions!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Display chat messages
    if len(st.session_state.chat_messages) == 0:
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
    else:
        for msg in st.session_state.chat_messages:
            render_message(msg['role'], msg['content'], msg['timestamp'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Type your message...",
            height=100,
            placeholder="Ask me anything! I can help with code, explanations, and more...",
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send_button = st.button("📤 Send", use_container_width=True, type="primary")
    
    # Handle send button
    if send_button and user_input.strip():
        # Add user message
        timestamp = datetime.now().strftime("%I:%M %p")
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        st.session_state.chat_message_count += 1
        
        # Prepare messages for API
        api_messages = [
            {'role': msg['role'], 'content': msg['content']}
            for msg in st.session_state.chat_messages
        ]
        
        # Call API
        with st.spinner("🤔 Thinking..."):
            success, response = call_openrouter_api(api_messages)
        
        if success:
            # Add assistant response
            timestamp = datetime.now().strftime("%I:%M %p")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': response,
                'timestamp': timestamp
            })
        else:
            st.error(f"❌ {response}")
        
        # Rerun to display new messages
        st.rerun()
    
    # Clear chat button
    if len(st.session_state.chat_messages) > 0:
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.chat_message_count = 0
                st.rerun()
    
    # Stats in expander
    if st.session_state.chat_message_count > 0:
        with st.expander("📊 Chat Statistics"):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Messages Sent", st.session_state.chat_message_count)
            with col2:
                st.metric("Total Messages", len(st.session_state.chat_messages))
