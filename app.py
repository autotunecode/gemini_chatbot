import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #667eea;
    }
    .assistant-message {
        background-color: #e8f4f8;
        border-left-color: #764ba2;
    }
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Gemini APIの設定
def configure_gemini():
    """Gemini APIを設定する"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        st.error("🚨 GOOGLE_API_KEYが設定されていません。.envファイルにAPI Keyを設定してください。")
        st.markdown(
            """
            📍 **Gemini APIキーの取得方法:**
            [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセスして無料のAPIキーを取得してください。
            """,
            unsafe_allow_html=True
        )
        return None
    
    try:
        genai.configure(api_key=api_key)
        # 最新のgemini-2.5-flashモデルを使用（無料枠に適している）
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except Exception as e:
        st.error(f"❌ Gemini APIの設定エラー: {str(e)}")
        st.markdown(
            """
            📍 **APIキーの確認:**
            [Google AI Studio](https://aistudio.google.com/app/apikey) でAPIキーが正しく生成されているか確認してください。
            """,
            unsafe_allow_html=True
        )
        return None

# チャット履歴の初期化
def init_chat_history():
    """チャット履歴を初期化"""
    # Streamlitのベストプラクティスに従った初期化
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'model' not in st.session_state:
        st.session_state.model = None

# チャット履歴の保存
def save_chat_history():
    """チャット履歴をJSONファイルに保存"""
    # セッションステートの初期化確認
    if 'chat_history' in st.session_state and st.session_state.chat_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.chat_history, f, ensure_ascii=False, indent=2)
        st.success(f"💾 チャット履歴を {filename} に保存しました")
    else:
        st.warning("💾 保存する履歴がありません")

# チャット履歴の読み込み
def load_chat_history(file):
    """チャット履歴をJSONファイルから読み込み"""
    try:
        chat_data = json.load(file)
        # セッションステートの初期化確認
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        st.session_state.chat_history = chat_data
        st.success("📂 チャット履歴を読み込みました")
    except Exception as e:
        st.error(f"❌ ファイル読み込みエラー: {str(e)}")

# メイン画面
def main():
    # ヘッダー
    st.markdown('<div class="main-header"><h1>🤖 Gemini Chatbot</h1><p>Google Gemini APIを使用したチャットボット</p></div>', unsafe_allow_html=True)
    
    # チャット履歴の初期化（最優先で実行）
    init_chat_history()
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # API Key設定
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.subheader("🔑 API Key設定")
        api_key_input = st.text_input(
            "Google API Key",
            type="password",
            value=os.getenv('GOOGLE_API_KEY', ''),
            help="Gemini APIキーを入力してください"
        )
        if api_key_input:
            os.environ['GOOGLE_API_KEY'] = api_key_input
        
        # APIキー取得のリンク
        st.markdown(
            """
            💡 **APIキーをお持ちでない場合:**  
            [Google AI Studio](https://aistudio.google.com/app/apikey) で無料のAPIキーを取得できます
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # モデル設定
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.subheader("🔧 モデル設定")
        temperature = st.slider(
            "創造性レベル",
            min_value=0.0,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="値が高いほど創造的な回答になります"
        )
        max_tokens = st.slider(
            "最大トークン数",
            min_value=100,
            max_value=8000,
            value=2000,
            step=100,
            help="生成される回答の最大長"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # チャット履歴管理
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.subheader("📋 チャット履歴")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ 履歴クリア"):
                if 'chat_history' in st.session_state:
                    st.session_state.chat_history = []
                    st.success("履歴をクリアしました")
                    st.rerun()
                else:
                    st.warning("⚠️ クリアする履歴がありません")
        
        with col2:
            if st.button("💾 履歴保存"):
                save_chat_history()
        
        # ファイルアップロード
        uploaded_file = st.file_uploader(
            "📂 履歴読み込み",
            type=['json'],
            help="以前に保存したチャット履歴を読み込みます"
        )
        if uploaded_file is not None:
            load_chat_history(uploaded_file)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 統計情報
        st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
        st.subheader("📊 統計")
        # セッションステートが初期化されているかチェック
        if 'chat_history' in st.session_state:
            st.write(f"💬 メッセージ数: {len(st.session_state.chat_history)}")
            if st.session_state.chat_history:
                total_chars = sum(len(msg['content']) for msg in st.session_state.chat_history)
                st.write(f"📝 総文字数: {total_chars:,}")
        else:
            st.write("💬 メッセージ数: 0")
            st.write("📝 総文字数: 0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Geminiモデルの設定
    if not st.session_state.model:
        st.session_state.model = configure_gemini()
    
    # メインチャット領域
    if st.session_state.model:
        # チャット履歴の表示
        chat_container = st.container()
        with chat_container:
            # セッションステートが初期化されているかチェック
            if 'chat_history' in st.session_state:
                for i, message in enumerate(st.session_state.chat_history):
                    if message['role'] == 'user':
                        st.markdown(
                            f'<div class="chat-message user-message">'
                            f'<strong>👤 あなた:</strong><br>{message["content"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="chat-message assistant-message">'
                            f'<strong>🤖 Gemini:</strong><br>{message["content"]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )
        
        # メッセージ入力
        st.markdown("---")
        user_input = st.text_area(
            "メッセージを入力してください:",
            height=100,
            placeholder="Geminiに質問や依頼をしてください...",
            key="user_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            send_button = st.button("📤 送信", type="primary")
        
        with col2:
            if st.button("🔄 再生成"):
                if 'chat_history' in st.session_state and st.session_state.chat_history:
                    # 最後のユーザーメッセージを取得
                    last_user_msg = None
                    for msg in reversed(st.session_state.chat_history):
                        if msg['role'] == 'user':
                            last_user_msg = msg['content']
                            break
                    
                    if last_user_msg:
                        # 最後のアシスタントメッセージを削除
                        if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == 'assistant':
                            st.session_state.chat_history.pop()
                        
                        # 再生成
                        with st.spinner("🔄 再生成中..."):
                            try:
                                response = st.session_state.model.generate_content(
                                    last_user_msg,
                                    generation_config=genai.types.GenerationConfig(
                                        temperature=temperature,
                                        max_output_tokens=max_tokens,
                                    )
                                )
                                st.session_state.chat_history.append({
                                    'role': 'assistant',
                                    'content': response.text,
                                    'timestamp': datetime.now().isoformat()
                                })
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ 再生成エラー: {str(e)}")
                else:
                    st.warning("⚠️ 再生成する履歴がありません")
        
        # メッセージ送信処理
        if send_button and user_input.strip():
            # セッションステートが初期化されているかチェック
            if 'chat_history' not in st.session_state:
                st.session_state.chat_history = []
            
            # ユーザーメッセージを履歴に追加
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().isoformat()
            })
            
            # Geminiからの応答を取得
            with st.spinner("🤖 Geminiが考えています..."):
                try:
                    response = st.session_state.model.generate_content(
                        user_input,
                        generation_config=genai.types.GenerationConfig(
                            temperature=temperature,
                            max_output_tokens=max_tokens,
                        )
                    )
                    
                    # アシスタントメッセージを履歴に追加
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response.text,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ エラーが発生しました: {str(e)}")
    
    else:
        st.warning("⚠️ 先にAPI Keyを設定してください。")
        st.markdown(
            """
            💡 **APIキーの取得と設定方法:**
            1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
            2. 無料のGemini APIキーを取得
            3. `.env` ファイルに `GOOGLE_API_KEY=あなたのAPIキー` として保存
            
            または、左のサイドバーで直接APIキーを入力することもできます。
            """,
            unsafe_allow_html=True
        )

# フッター
def footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem; color: #666;">
            <p>🤖 Gemini Chatbot | Made with ❤️ using Streamlit & Google Gemini API</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    footer() 