# 🤖 Gemini Chatbot

Google Gemini APIを使用した自分専用のチャットボットアプリケーションです。StreamlitのWebインターフェースを通じて、Gemini APIの機能を実践的に学ぶことができます。

## 📋 目次

- [特徴](#特徴)
- [必要要件](#必要要件)
- [Gemini API Keyの取得方法](#gemini-api-keyの取得方法)
- [インストール手順](#インストール手順)
- [使用方法](#使用方法)
- [機能説明](#機能説明)
- [トラブルシューティング](#トラブルシューティング)
- [注意事項](#注意事項)

## ✨ 特徴

- 🆓 **無料**: Gemini APIの無料枠を使用
- 🖥️ **直感的なUI**: Streamlitによる美しいWebインターフェース
- 💬 **リアルタイムチャット**: Geminiとの自然な対話
- 📊 **設定可能**: 創造性レベルやトークン数の調整
- 💾 **履歴管理**: チャット履歴の保存・読み込み
- 🔄 **再生成機能**: 回答の再生成
- 📈 **統計表示**: メッセージ数や文字数の表示

## 📦 必要要件

- Python 3.8以上
- インターネット接続
- Google アカウント

## 🔑 Gemini API Keyの取得方法

### 1. Google AI Studioにアクセス

1. [Google AI Studio](https://makersuite.google.com/app/apikey) にアクセス
2. Googleアカウントでログイン

### 2. API Keyの作成

1. 「Create API Key」または「APIキーを作成」をクリック
2. 既存のGoogleクラウドプロジェクトを選択するか、新しく作成
3. 生成されたAPI Keyをコピーして保存

### 3. 重要な注意事項

- ⚠️ **API Keyは機密情報です** - 他人と共有しないでください
- 📝 **安全な場所に保存** - パスワードマネージャーなどを使用
- 🔄 **定期的に更新** - セキュリティのため定期的に新しいキーを生成

## 🚀 インストール手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd gemini_api_test
```

### 2. 仮想環境の作成（推奨）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. 環境変数の設定（オプション）

```bash
# env_example.txt を .env にコピー
copy env_example.txt .env  # Windows
cp env_example.txt .env    # macOS/Linux

# .env ファイルを編集してAPI Keyを設定
```

## 🎮 使用方法

### 1. アプリケーションの起動

```bash
streamlit run app.py
```

### 2. ブラウザでアクセス

アプリケーションが起動すると、ブラウザが自動的に開きます。
手動でアクセスする場合は: `http://localhost:8501`

### 3. API Keyの設定

1. サイドバーの「🔑 API Key設定」セクションを開く
2. 取得したGemini API Keyを入力
3. 設定が完了すると、メインチャット画面が使用可能になります

### 4. チャットの開始

1. メインページのテキストエリアにメッセージを入力
2. 「📤 送信」ボタンをクリック
3. Geminiからの応答を待ちます

## 🛠️ 機能説明

### サイドバー機能

#### 🔑 API Key設定
- Gemini API Keyを安全に入力
- パスワード形式で表示されるため、他人に見られる心配がありません

#### 🔧 モデル設定
- **創造性レベル**: 0.0〜2.0の範囲で調整（高いほど創造的）
- **最大トークン数**: 回答の最大長を制御（100〜8000）

#### 📋 チャット履歴
- **🗑️ 履歴クリア**: 現在のチャット履歴を削除
- **💾 履歴保存**: チャット履歴をJSONファイルとして保存
- **📂 履歴読み込み**: 以前に保存した履歴を読み込み

#### 📊 統計
- **💬 メッセージ数**: 現在のセッションでのメッセージ数
- **📝 総文字数**: 現在のセッションでの総文字数

### メイン機能

#### 💬 チャット
- リアルタイムでGeminiと対話
- 美しいUI設計でメッセージが見やすい

#### 🔄 再生成
- 最後の回答を再生成
- 違う回答を得たい場合に便利

## 🔧 トラブルシューティング

### よくある問題と解決法

#### 1. API Keyエラー
**エラー**: `GOOGLE_API_KEYが設定されていません`
**解決法**: 
- サイドバーでAPI Keyを正しく入力
- API Keyが有効か確認
- [Google AI Studio](https://makersuite.google.com/app/apikey)で新しいキーを生成

#### 2. インストールエラー
**エラー**: `pip install` が失敗する
**解決法**:
```bash
# pip のアップグレード
python -m pip install --upgrade pip

# 依存関係の個別インストール
pip install streamlit
pip install google-generativeai
pip install python-dotenv
```

#### 3. モジュールが見つからない
**エラー**: `ModuleNotFoundError`
**解決法**:
```bash
# 仮想環境がアクティブか確認
# 必要に応じて仮想環境を再作成
```

#### 4. API制限エラー
**エラー**: `Quota exceeded` や `Rate limit`
**解決法**:
- 少し時間をおいてから再試行
- API使用量を確認
- 無料枠の制限内であることを確認

### デバッグ方法

1. **コンソールログの確認**
   - Streamlitアプリのターミナル出力を確認
   - ブラウザのF12開発者ツールでエラーを確認

2. **API接続テスト**
   ```python
   import google.generativeai as genai
   
   genai.configure(api_key="YOUR_API_KEY")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello!")
   print(response.text)
   ```

## ⚠️ 注意事項

### セキュリティ
- **API Keyを他人と共有しないでください**
- **GitHubなどに.envファイルをアップロードしないでください**
- **定期的にAPI Keyを更新してください**

### 使用制限
- **無料枠の制限**: 1分間に60リクエスト、1日に1500リクエスト
- **コンテンツポリシー**: Googleのコンテンツポリシーに準拠
- **レート制限**: 大量のリクエストを短時間で送信しないでください

### プライバシー
- **データの保存**: チャット履歴はローカルにのみ保存
- **Google AI**: 入力内容はGoogleのAIサービスに送信されます
- **機密情報**: 機密情報や個人情報の入力は避けてください

## 📚 学習リソース

### Gemini API
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Python SDK Documentation](https://ai.google.dev/api/python/google/generativeai)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Community](https://discuss.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

## 🤝 サポート

問題が発生した場合や改善提案がある場合は、以下の方法でお知らせください：

1. **GitHub Issues**: バグレポートや機能要求
2. **Documentation**: このREADMEファイルの改善提案
3. **Code**: プルリクエストによる機能追加や修正

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**🎉 Gemini APIを使った開発を楽しんでください！** 