# Linux環境でのユーザーガイド

このドキュメントでは、開発者でない人がLinux環境で広聴AI（kouchou-ai）を使うための手順を説明します。
ソフトウェア開発に必要な要素を取り除いて最小限にしたものです。

## 前提条件

- Ubuntu 20.04 LTS 以降（または同等のLinuxディストリビューション）
- インターネット接続
- OpenAI APIキー（[取得方法](https://platform.openai.com/api-keys)）

## セットアップ手順

### 1. Dockerのインストール

1. 以下のコマンドを実行して、Dockerをインストールします：
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```
2. 一度ログアウトして再ログインし、Docker権限を反映させます。
3. 以下のコマンドでDockerが正常に動作していることを確認します：`docker --version`

### 2. 広聴AIのダウンロード

1. [広聴AI安定版リリース](https://github.com/digitaldemocracy2030/kouchou-ai/releases/latest)から最新の安定版をダウンロードします。
2. ダウンロードしたzipファイルを任意の場所に展開します：
```bash
unzip ダウンロードしたzipファイル -d 展開先のパス
```

### 3. OpenAI APIキーの準備

1. [OpenAI API](https://platform.openai.com/api-keys)にアクセスし、APIキーを取得します。
2. アカウントに$5程度のクレジットをチャージしておくことをお勧めします。

### 4. セットアップの実行

1. ターミナルを開きます。
2. 展開したフォルダに移動します：`cd 展開したフォルダのパス`
3. セットアップスクリプトに実行権限を付与します：`chmod +x setup_linux.sh`
4. 以下のコマンドを実行してセットアップを開始します：`./setup_linux.sh`
5. プロンプトが表示されたら、OpenAI APIキーを入力します。
6. セットアップが自動的に進行し、Dockerコンテナが起動します。

### 5. アプリケーションへのアクセス

セットアップが完了すると、以下のURLでアプリケーションにアクセスできます：

- レポート閲覧画面: http://localhost:3000
- 管理画面: http://localhost:4000

### 6. アプリケーションのアクセス・運用と再起動の手順

セットアップ後は、次回以降の起動や停止を以下のように行ってください。

#### 通常の起動・停止

- アプリケーションの起動:  
  `./start_linux.sh` を実行します

- アプリケーションの停止:  
  `./stop_linux.sh` を実行します

#### OpenAI APIキーを変更したい場合

OpenAI APIキーを再設定したい場合は、再度 `./setup_linux.sh` を実行してください。

1. 既存のアプリケーションが起動中の場合は `./stop_linux.sh` で停止してください。  
2. `./setup_linux.sh` を実行し、新しい APIキーを入力します。  
3. 自動的に再ビルドと起動が行われます。

> ※ `setup_linux.sh` の再実行では、既存の `.env` ファイルが上書きされます。

## トラブルシューティング

### Dockerの権限エラーが発生する場合

「permission denied」などのエラーが表示される場合は、以下のコマンドを実行して、現在のユーザーがdockerグループに正しく追加されていることを確認してください：
```bash
sudo usermod -aG docker $USER
```
その後、ログアウトして再ログインしてください。

### メモリ不足エラーが発生する場合

システムリソースが不足している場合は、スワップ領域を増やすことで改善する可能性があります：
```bash
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```
永続的にスワップを有効にするには、/etc/fstabに追加してください。
