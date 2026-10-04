# Railway へのデプロイ（API サーバー）

広聴AIの API サーバー（`server/`）を [Railway](https://railway.com/) で動かす手順です。
画面（client / client-admin）は使わず、別のアプリ（例：いどばたビジョン）から API を呼び出す構成を想定しています。

## 構成

| 項目 | 設定 |
|---|---|
| サービス | このリポジトリの `server/` を Dockerfile でビルド |
| 起動 | `server/scripts/railway-start.sh`（Railway の `PORT` で起動し、`--reload` は付けない） |
| データの保存 | Volume を `/data` に付ける。起動時に次の4つのフォルダを Volume 内へのリンクに置き換える |
| 台数 | 1台（データをファイルに保存するため、複数台にはできない） |

Volume に保存されるフォルダ：

- `server/data`（レポート一覧・状態 `report_status.json`）
- `server/broadlistening/pipeline/outputs`（分析結果）
- `server/broadlistening/pipeline/inputs`（アップロードされたコメント）
- `server/broadlistening/pipeline/configs`（分析の設定）

## 手順

### 1. サービスを作る

1. Railway のプロジェクトを開き、**+ New** →（**+ Create** と表示される場合もある）**GitHub Repo** を選ぶ。
2. このリポジトリ（例：`samboofficeota-hue/kouchou-ai`）を選ぶ。
3. 作られたサービスの **Settings** を開き、次のように設定する。

| 場所 | 設定値 |
|---|---|
| Source → Root Directory | `/server` |
| Source → Branch | デプロイするブランチ（例：`main`） |
| Build → Builder | Dockerfile（`server/Dockerfile` が自動で選ばれる） |
| Deploy → Custom Start Command | `sh scripts/railway-start.sh` |
| Deploy → Healthcheck Path | `/` |
| Deploy → Region | 呼び出し元のアプリと同じリージョン（例：Southeast Asia） |
| Deploy → Replicas | 1 |

### 2. Volume を付ける

1. サービスを右クリック（またはキャンバスの **+ New**）→ **Volume** を選ぶ。
2. 付け先にこのサービスを選び、**Mount Path** を `/data` にする。

Volume を付けないと、再デプロイのたびに過去の分析がすべて消えます。

### 3. 変数（Variables）を設定する

サービスの **Variables** に次を登録します。

| 変数 | 値 |
|---|---|
| `OPENAI_API_KEY` | OpenAI の API キー |
| `ADMIN_API_KEY` | 推測されにくい長いランダムな文字列（管理用。呼び出し元の backend だけに渡す） |
| `PUBLIC_API_KEY` | 推測されにくいランダムな文字列（閲覧用。ブラウザから見える値） |
| `ENVIRONMENT` | `production`（API の説明ページを非公開にし、本番用の依存関係でビルドする） |
| `STORAGE_TYPE` | `local` |
| `WITH_GPU` | `false` |

`ADMIN_API_KEY` と `PUBLIC_API_KEY` は別の値にしてください。ランダムな文字列は、たとえば `openssl rand -hex 32` で作れます。

### 4. 公開URLを作る

**Settings → Networking → Generate Domain** で `https://〜.up.railway.app` の URL を作ります。
デプロイが終わったら、その URL をブラウザで開いて `{"status":"ok"}` が返ることを確認します。

### 5. 呼び出し元のアプリに設定する（いどばたビジョンの場合）

| 置き場所 | 変数 | 値 |
|---|---|---|
| idea-discussion/backend（Railway） | `KOUCHOU_API_URL` | 手順4の URL |
| idea-discussion/backend（Railway） | `KOUCHOU_ADMIN_API_KEY` | `ADMIN_API_KEY` と同じ値 |
| idea-discussion/backend（Railway） | `KOUCHOU_CREATE_PASSWORD` | 新規分析ページのパスワード |
| frontend（Vercel） | `VITE_KOUCHOU_API_BASE_URL` | 手順4の URL |
| frontend（Vercel） | `VITE_KOUCHOU_PUBLIC_API_KEY` | `PUBLIC_API_KEY` と同じ値 |
| admin（Vercel） | `VITE_FRONTEND_BASE_URL` | 利用者向けサイトの URL（任意） |

Vercel の `VITE_` で始まる変数はビルド時に埋め込まれるため、設定を変えたら再デプロイが必要です。

## 注意

- **分析中の再デプロイ**：分析は API サーバーの中で動くため、分析中に再デプロイや再起動をすると、その分析はエラーで止まります。
- **費用**：Railway の利用料に加え、分析ごとに OpenAI の API 利用料がかかります。
- **イメージの大きさ**：分析に使うライブラリ（PyTorch の CPU 版など）を含むため、ビルドには数分以上かかります。
