# Kouchou AI E2Eテスト

このディレクトリにはPlaywrightを使用したKouchou AIアプリケーションのエンドツーエンドテストが含まれています。

## セットアップ

1. 依存関係のインストール:
   ```
   npm install
   ```

2. Playwrightブラウザのインストール:
   ```
   npx playwright install
   ```

3. 環境変数の設定:
   ```
   cp .env.example .env
   ```
   その後、`.env`ファイルを編集してテスト用の認証情報を追加します。

## テストの実行

すべてのテストを実行:
```
npm test
```

UIモードでテストを実行:
```
npm run test:ui
```

デバッグモードでテストを実行:
```
npm run test:debug
```

テストレポートを表示:
```
npm run report
```

## ディレクトリ構造

- `tests/`: テストファイル
  - `admin/`: 管理機能のテスト
  - `client/`: クライアント機能のテスト
- `pages/`: ページオブジェクトモデル
- `fixtures/`: テストフィクスチャ
- `utils/`: テストユーティリティ

## 新しいテストの追加

1. 必要に応じて`pages/`に新しいページオブジェクトを作成
2. `tests/`にテストファイルを追加
3. メンテナンス性向上のためにページオブジェクトパターンを使用

## CI連携

テストは以下のタイミングで自動的に実行されます:
- 毎日0時(UTC)
- `e2e-test-required`ラベルが付いたPR

テスト結果はGitHub Actionsのアーティファクトとして利用できます。
