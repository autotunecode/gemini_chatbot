#!/usr/bin/env python3
"""
Gemini Chatbot セットアップスクリプト
"""

import os
import subprocess
import sys

def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8以上が必要です")
        print(f"現在のバージョン: {sys.version}")
        sys.exit(1)
    print(f"✅ Python バージョン: {sys.version}")

def install_requirements():
    """必要なパッケージをインストール"""
    print("📦 パッケージをインストールしています...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ パッケージのインストールが完了しました")
    except subprocess.CalledProcessError:
        print("❌ パッケージのインストールに失敗しました")
        sys.exit(1)

def create_env_file():
    """環境変数ファイルを作成"""
    env_file = ".env"
    env_example = "env_example.txt"
    
    if os.path.exists(env_file):
        print("ℹ️  .envファイルは既に存在します")
        return
    
    if os.path.exists(env_example):
        try:
            with open(env_example, 'r') as src:
                content = src.read()
            with open(env_file, 'w') as dst:
                dst.write(content)
            print("✅ .envファイルを作成しました")
            print("🔑 .envファイルを編集してAPI Keyを設定してください")
        except Exception as e:
            print(f"❌ .envファイルの作成に失敗しました: {e}")
    else:
        print("⚠️  env_example.txtファイルが見つかりません")

def main():
    print("🚀 Gemini Chatbot セットアップを開始します...")
    
    # Python バージョンチェック
    check_python_version()
    
    # パッケージインストール
    install_requirements()
    
    # .envファイル作成
    create_env_file()
    
    print("\n🎉 セットアップが完了しました!")
    print("\n次のステップ:")
    print("1. .envファイルを編集してGemini API Keyを設定")
    print("2. 'streamlit run app.py' でアプリを起動")
    print("3. ブラウザで http://localhost:8501 にアクセス")

if __name__ == "__main__":
    main() 