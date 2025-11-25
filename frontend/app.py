import streamlit as st
import asyncio
import os
from datetime import datetime
from typing import Optional
import uuid
from services.api_client import ResearchAPIClient

# Page config
st.set_page_config(
    page_title="Open Deep Research",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API client
@st.cache_resource
def get_api_client():
    return ResearchAPIClient()

api_client = get_api_client()

# Initialize session state
if 'session_id' not in st.session_state:
    try:
        response = asyncio.run(api_client.create_session())
        st.session_state.session_id = response['session_id']
    except Exception as e:
        st.error(f"Failed to create session: {e}")
        st.session_state.session_id = None

if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        'EXA_API_KEY': '',
        'SERPER_API_KEY': '',
        'GITHUB_ACCESS_TOKEN': '',
        'TOGETHER_API_KEY': '',
        'TAVLIY_API_KEY': '',
        'GROQ_API_KEY': '',
        'LANGFUSE_SECRET_KEY': '',
        'LANGFUSE_PUBLIC_KEY': '',
        'LANGFUSE_HOST': 'https://cloud.langfuse.com',
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None

if 'current_chat_messages' not in st.session_state:
    st.session_state.current_chat_messages = []

if 'processing' not in st.session_state:
    st.session_state.processing = False

if 'current_task_id' not in st.session_state:
    st.session_state.current_task_id = None

def validate_required_keys():
    """Check if all required API keys are set"""
    required_keys = [
        'EXA_API_KEY',
        'SERPER_API_KEY',
        'GITHUB_ACCESS_TOKEN',
        'TOGETHER_API_KEY',
        'TAVLIY_API_KEY',
        'GROQ_API_KEY',
    ]
    missing_keys = [key for key in required_keys if not st.session_state.api_keys.get(key, '').strip()]
    return len(missing_keys) == 0, missing_keys

def create_new_chat():
    """Create a new chat session"""
    if st.session_state.current_chat_id and st.session_state.current_chat_messages:
        # Save current chat to history
        st.session_state.chat_history.append({
            'id': st.session_state.current_chat_id,
            'title': st.session_state.current_chat_messages[0]['content'][:50] + '...' if st.session_state.current_chat_messages else 'New Chat',
            'messages': st.session_state.current_chat_messages.copy(),
            'timestamp': datetime.now().isoformat()
        })
    
    # Create new chat
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.current_chat_messages = []
    st.session_state.current_task_id = None

def load_chat(chat_id: str):
    """Load a chat from history"""
    for chat in st.session_state.chat_history:
        if chat['id'] == chat_id:
            st.session_state.current_chat_id = chat_id
            st.session_state.current_chat_messages = chat['messages'].copy()
            break

def delete_chat(chat_id: str):
    """Delete a chat from history"""
    st.session_state.chat_history = [chat for chat in st.session_state.chat_history if chat['id'] != chat_id]
    if st.session_state.current_chat_id == chat_id:
        create_new_chat()

async def run_research_pipeline(query: str, user_feedback: str = " "):
    """Run the complete research pipeline via API"""
    try:
        # Start research task
        result = await api_client.start_research(
            query=query,
            api_keys=st.session_state.api_keys,
            langfuse_config={
                'public_key': st.session_state.api_keys.get('LANGFUSE_PUBLIC_KEY', ''),
                'secret_key': st.session_state.api_keys.get('LANGFUSE_SECRET_KEY', ''),
                'host': st.session_state.api_keys.get('LANGFUSE_HOST', 'https://cloud.langfuse.com')
            } if st.session_state.api_keys.get('LANGFUSE_PUBLIC_KEY') else None,
            session_id=st.session_state.session_id,
            user_feedback=user_feedback
        )
        
        task_id = result['task_id']
        st.session_state.current_task_id = task_id
        
        # Poll for status
        while True:
            status = await api_client.get_research_status(task_id)
            
            if status['status'] == 'completed':
                if status.get('result') and status['result'].get('markdown'):
                    return status['result']['markdown'], None
                else:
                    return None, "Report generated but markdown not found"
            elif status['status'] == 'failed':
                return None, status.get('error', 'Unknown error')
            
            # Wait before next poll
            await asyncio.sleep(2)
            
    except Exception as e:
        return None, str(e)

# Left Sidebar - Chat History
with st.sidebar:
    st.title("💬 Chat History")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()
    
    st.divider()
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Previous Chats")
        for chat in reversed(st.session_state.chat_history):
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    chat['title'],
                    key=f"chat_{chat['id']}",
                    use_container_width=True,
                    help=chat.get('timestamp', '')
                ):
                    load_chat(chat['id'])
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{chat['id']}", help="Delete chat"):
                    delete_chat(chat['id'])
                    st.rerun()
    else:
        st.info("No chat history yet. Start a new conversation!")
    
    # Current Chat Info
    if st.session_state.current_chat_id:
        st.divider()
        st.caption(f"Current Chat: {st.session_state.current_chat_id[:8]}...")

# Main content area
st.title("🔭 Open Deep Research")

# Create two columns for side-by-side layout
col_main, col_right = st.columns([2, 1])

with col_right:
    st.header("⚙️ API Configuration")
    
    with st.expander("API Keys", expanded=True):
        st.markdown("### Required Keys")
        
        st.session_state.api_keys['EXA_API_KEY'] = st.text_input(
            "EXA API Key",
            value=st.session_state.api_keys.get('EXA_API_KEY', ''),
            type="password",
            help="Get your key from https://dashboard.exa.ai/playground"
        )
        
        st.session_state.api_keys['SERPER_API_KEY'] = st.text_input(
            "Serper API Key",
            value=st.session_state.api_keys.get('SERPER_API_KEY', ''),
            type="password",
            help="Get your key from https://serper.dev/dashboard"
        )
        
        st.session_state.api_keys['GITHUB_ACCESS_TOKEN'] = st.text_input(
            "GitHub Access Token",
            value=st.session_state.api_keys.get('GITHUB_ACCESS_TOKEN', ''),
            type="password",
            help="Get your token from https://github.com/settings/profile"
        )
        
        st.session_state.api_keys['TOGETHER_API_KEY'] = st.text_input(
            "Together API Key",
            value=st.session_state.api_keys.get('TOGETHER_API_KEY', ''),
            type="password",
            help="Get your key from https://www.together.ai/"
        )
        
        st.session_state.api_keys['TAVLIY_API_KEY'] = st.text_input(
            "Tavily API Key",
            value=st.session_state.api_keys.get('TAVLIY_API_KEY', ''),
            type="password",
            help="Get your key from https://tavily.com/"
        )
        
        st.session_state.api_keys['GROQ_API_KEY'] = st.text_input(
            "Groq API Key",
            value=st.session_state.api_keys.get('GROQ_API_KEY', ''),
            type="password",
            help="Get your key from https://groq.com/"
        )
        
        st.divider()
        st.markdown("### Optional Keys (Langfuse)")
        
        st.session_state.api_keys['LANGFUSE_PUBLIC_KEY'] = st.text_input(
            "Langfuse Public Key",
            value=st.session_state.api_keys.get('LANGFUSE_PUBLIC_KEY', ''),
            type="password",
            help="Optional: Get your key from https://langfuse.com/"
        )
        
        st.session_state.api_keys['LANGFUSE_SECRET_KEY'] = st.text_input(
            "Langfuse Secret Key",
            value=st.session_state.api_keys.get('LANGFUSE_SECRET_KEY', ''),
            type="password",
            help="Optional: Get your key from https://langfuse.com/"
        )
        
        st.session_state.api_keys['LANGFUSE_HOST'] = st.text_input(
            "Langfuse Host",
            value=st.session_state.api_keys.get('LANGFUSE_HOST', 'https://cloud.langfuse.com'),
            help="Optional: Langfuse host URL"
        )
    
    # Validate keys
    keys_valid, missing_keys = validate_required_keys()
    
    if keys_valid:
        st.success("✅ All required API keys are set!")
    else:
        st.error(f"❌ Missing required keys: {', '.join(missing_keys)}")
        st.info("Please add all required API keys to start researching.")

with col_main:
    # Initialize current chat if needed
    if not st.session_state.current_chat_id:
        create_new_chat()
    
    # Display chat messages
    st.header("💬 Research Chat")
    
    # Display messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.current_chat_messages:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            elif message['role'] == 'assistant':
                with st.chat_message("assistant"):
                    if message.get('type') == 'markdown':
                        st.markdown(message['content'])
                    else:
                        st.write(message['content'])
                    if message.get('error'):
                        st.error(message['error'])
    
    # Chat input
    if keys_valid:
        user_query = st.chat_input("Enter your research query here...")
        
        if user_query and not st.session_state.processing:
            # Add user message
            st.session_state.current_chat_messages.append({
                'role': 'user',
                'content': user_query,
                'timestamp': datetime.now().isoformat()
            })
            
            st.session_state.processing = True
            st.rerun()
    else:
        st.info("⚠️ Please configure all required API keys in the right panel to start researching.")
        user_query = None
    
    # Process query if needed
    if st.session_state.processing and st.session_state.current_chat_messages:
        last_message = st.session_state.current_chat_messages[-1]
        if last_message['role'] == 'user':
            # Add processing message
            st.session_state.current_chat_messages.append({
                'role': 'assistant',
                'content': 'Processing your research query... This may take a few minutes.',
                'timestamp': datetime.now().isoformat()
            })
            st.rerun()
    
    # Run research pipeline
    if (st.session_state.processing and 
        st.session_state.current_chat_messages and 
        len(st.session_state.current_chat_messages) >= 2 and
        st.session_state.current_chat_messages[-1]['role'] == 'assistant' and
        'Processing your research query' in st.session_state.current_chat_messages[-1]['content']):
        
        user_query = st.session_state.current_chat_messages[-2]['content']
        
        with st.spinner("🔍 Researching... This may take several minutes."):
            try:
                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result, error = loop.run_until_complete(run_research_pipeline(user_query))
                loop.close()
                
                # Remove processing message
                if st.session_state.current_chat_messages and 'Processing your research query' in st.session_state.current_chat_messages[-1].get('content', ''):
                    st.session_state.current_chat_messages.pop()
                
                if result:
                    # Add result message
                    st.session_state.current_chat_messages.append({
                        'role': 'assistant',
                        'content': result,
                        'type': 'markdown',
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    # Add error message
                    st.session_state.current_chat_messages.append({
                        'role': 'assistant',
                        'content': 'Sorry, I encountered an error while processing your query.',
                        'error': error or 'Unknown error',
                        'timestamp': datetime.now().isoformat()
                    })
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                print(f"Error in research pipeline: {error_trace}")
                
                # Remove processing message
                if st.session_state.current_chat_messages and 'Processing your research query' in st.session_state.current_chat_messages[-1].get('content', ''):
                    st.session_state.current_chat_messages.pop()
                # Add error message
                st.session_state.current_chat_messages.append({
                    'role': 'assistant',
                    'content': 'Sorry, I encountered an error while processing your query.',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
            finally:
                st.session_state.processing = False
                st.rerun()

# Footer
st.divider()
st.caption("Open Deep Research - Automated Research Pipeline")
