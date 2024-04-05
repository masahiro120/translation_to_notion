# 英文翻訳 & Notion 送信スクリプト

このスクリプトは、英文を自動で翻訳し、結果をNotionのデータベースに送信するものです。`translation.py`を中心に、`shortcut.bat`と`shortcut_split.bat`というバッチファイルを使用して、Windows環境で簡単に実行できるようになっています。

## 前提条件

- Pythonがインストールされていること
- `requests`, `pyperclip`, `deepl` Pythonライブラリがインストールされていること
- DeepL APIキーが必要です（`DEEPL_API_KEY`に設定）
- Notion APIキーとデータベースIDが必要です（`NOTION_API_KEY`, `NOTION_DATABASE_ID`に設定）

## 設定

1. `translation.py`に必要なAPIキーを設定します。
   - `DEEPL_API_KEY`にDeepLのAPIキーを設定してください。
   - `NOTION_API_KEY`にNotionのIntegration APIキーを設定してください。
   - `NOTION_PAGE_URL`に送信先のNotionページのURLを設定してください。これにより、`NOTION_DATABASE_ID`が自動で設定されます。

## 使い方

1. `shortcut.bat`または`shortcut_split.bat`を実行することで、スクリプトが起動します。
   - `shortcut.bat`は、クリップボードの内容を直接翻訳してNotionに送信します。
   - `shortcut_split.bat`は、クリップボードの内容が長文の場合に、分割してから翻訳しNotionに送信します。これは、DeepL APIの文字数制限を回避するために使用します。

2. スクリプト実行後、翻訳された文書がNotionに自動的に送信されます。

## 注意点

- このスクリプトは、英文から日本語への翻訳を想定しています。他の言語に対応させる場合は、`translation.py`内の`source_lang`および`target_lang`を適宜変更してください。
- Notion APIのバージョンアップに伴い、スクリプトの修正が必要になる場合があります。

## ライセンス

このスクリプトはフリーソフトウェアです。自由に使用、修正、配布が可能ですが、すべて自己責任でお願いします。
