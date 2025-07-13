# 🛠️ 開発ガイド

このファイルでは、Gemini Chatbotの開発・カスタマイズについて説明します。

## 📁 プロジェクト構造

```
gemini_api_test/
├── app.py              # メインアプリケーション
├── requirements.txt    # 依存関係
├── setup.py           # セットアップスクリプト
├── env_example.txt    # 環境変数の例
├── README.md          # ユーザーガイド
└── DEVELOPMENT.md     # このファイル
```

## 🔧 主要コンポーネント

### 1. アプリケーション構造 (app.py)

```python
# 主要な関数とその役割

configure_gemini()      # Gemini API設定
init_chat_history()     # セッション状態初期化
save_chat_history()     # 履歴保存
load_chat_history()     # 履歴読み込み
main()                  # メイン画面
footer()                # フッター
```

### 2. 主要な機能

#### チャット機能
- Streamlitのセッション状態を使用してチャット履歴を管理
- `st.session_state.chat_history`にメッセージを格納
- JSON形式でローカルファイルに保存・読み込み

#### UI設計
- カスタムCSSでモダンなデザイン
- レスポンシブデザイン
- 絵文字とアイコンで直感的な操作

#### API連携
- `google.generativeai`パッケージを使用
- エラーハンドリングと再試行機能
- 設定可能なパラメータ（temperature, max_tokens）

## 🎨 カスタマイズポイント

### 1. UIの変更

#### カラーテーマの変更
```python
# app.py のCSSセクションで以下を変更
.main-header {
    background: linear-gradient(90deg, #新しい色1, #新しい色2);
}
```

#### メッセージボックスのスタイル
```python
.chat-message {
    background-color: #新しい背景色;
    border-left-color: #新しいボーダー色;
}
```

### 2. 機能の追加

#### 新しいモデルの追加
```python
def configure_gemini():
    # 新しいモデル選択機能
    model_choice = st.selectbox(
        "モデル選択",
        ["gemini-pro", "gemini-pro-vision"]
    )
    model = genai.GenerativeModel(model_choice)
    return model
```

#### 音声入力の追加
```python
# streamlit-audio-recorder などのライブラリを使用
import streamlit_audio_recorder as sar

audio_bytes = sar.st_audio_recorder()
if audio_bytes:
    # 音声をテキストに変換
    text = speech_to_text(audio_bytes)
    # チャット処理
```

### 3. 設定の拡張

#### プリセットプロンプトの追加
```python
def add_preset_prompts():
    """プリセットプロンプトを追加"""
    presets = {
        "翻訳": "以下の文章を日本語に翻訳してください：",
        "要約": "以下のテキストを要約してください：",
        "コード解説": "以下のコードを解説してください：",
    }
    
    selected_preset = st.selectbox("プリセット", list(presets.keys()))
    return presets[selected_preset]
```

#### 応答フォーマットの設定
```python
def configure_response_format():
    """応答フォーマットを設定"""
    formats = {
        "普通": "",
        "箇条書き": "箇条書きで回答してください。",
        "表形式": "表形式で回答してください。",
        "コード例付き": "コード例を含めて回答してください。"
    }
    
    format_choice = st.selectbox("応答フォーマット", list(formats.keys()))
    return formats[format_choice]
```

## 🧪 テストとデバッグ

### 1. 単体テスト

```python
import pytest
from app import configure_gemini, init_chat_history

def test_configure_gemini():
    """Gemini設定のテスト"""
    # API Keyが設定されている場合のテスト
    os.environ['GOOGLE_API_KEY'] = 'test_key'
    model = configure_gemini()
    assert model is not None

def test_init_chat_history():
    """チャット履歴初期化のテスト"""
    init_chat_history()
    assert 'chat_history' in st.session_state
    assert 'model' in st.session_state
```

### 2. デバッグ機能

#### ログ出力の追加
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_mode():
    """デバッグモード"""
    if st.sidebar.checkbox("デバッグモード"):
        st.sidebar.json(st.session_state.chat_history)
        logger.debug("チャット履歴を表示")
```

#### API応答の詳細表示
```python
def show_api_response_details(response):
    """API応答の詳細を表示"""
    if st.sidebar.checkbox("API詳細表示"):
        st.sidebar.write("**使用トークン数:**", response.usage_metadata)
        st.sidebar.write("**応答時間:**", response.response_time)
```

## 🔧 パフォーマンス最適化

### 1. キャッシュの活用

```python
@st.cache_data
def load_chat_history_cached(filename):
    """キャッシュされた履歴読み込み"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_resource
def get_gemini_model():
    """キャッシュされたモデル取得"""
    return genai.GenerativeModel('gemini-pro')
```

### 2. 非同期処理

```python
import asyncio
import aiohttp

async def async_generate_content(prompt):
    """非同期でコンテンツを生成"""
    # 非同期API呼び出し
    async with aiohttp.ClientSession() as session:
        # API呼び出し処理
        pass
```

## 📦 デプロイメント

### 1. Streamlit Cloud

```bash
# requirements.txt に以下を追加
streamlit>=1.28.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
```

### 2. Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

### 3. 環境変数の管理

```python
# Streamlit Cloudの場合
import streamlit as st

# secrets.tomlファイルを使用
api_key = st.secrets["GOOGLE_API_KEY"]

# または環境変数
api_key = os.getenv("GOOGLE_API_KEY")
```

## 🔒 セキュリティ

### 1. API Key管理

```python
def secure_api_key_input():
    """安全なAPI Key入力"""
    # セッション状態からAPI Keyを削除
    if 'api_key' in st.session_state:
        del st.session_state['api_key']
    
    # 一時的にのみメモリに保存
    api_key = st.text_input("API Key", type="password")
    
    # 使用後は変数をクリア
    return api_key
```

### 2. 入力サニタイズ

```python
def sanitize_input(user_input):
    """ユーザー入力のサニタイズ"""
    # HTMLタグの除去
    import re
    cleaned = re.sub(r'<[^>]*>', '', user_input)
    
    # 不正な文字の除去
    cleaned = re.sub(r'[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]', '', cleaned)
    
    return cleaned
```

## 🤝 コントリビューション

### 1. コードスタイル

```python
# PEP 8準拠
# Black フォーマッター使用
# docstring の記載

def example_function(param1: str, param2: int) -> str:
    """
    関数の説明
    
    Args:
        param1: パラメータ1の説明
        param2: パラメータ2の説明
    
    Returns:
        戻り値の説明
    """
    return f"{param1}_{param2}"
```

### 2. プルリクエストの流れ

1. フォークとブランチ作成
2. 機能実装・テスト
3. コードレビュー
4. マージ

---

**🎯 開発を楽しんで、素晴らしいチャットボットを作成してください！** 