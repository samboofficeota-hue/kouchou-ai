#!/bin/sh
# Railway などのクラウドで API サーバーを起動するためのスクリプト
#
# - Railway の Volume は1つの場所にしか付けられないため、データを書き込む4つのフォルダを
#   Volume（既定は /data）の中のフォルダへのリンクに置き換え、再デプロイしても消えないようにする
# - ポートは Railway が指定する PORT を使う
# - 開発用の --reload は付けない
#
# ローカル開発（docker compose）では使わない
set -e

PERSIST_DIR="${PERSIST_DIR:-/data}"
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# $1: アプリ内のフォルダ（APP_DIR からの相対パス）、$2: Volume 内のフォルダ名
link_dir() {
  src="$APP_DIR/$1"
  dst="$PERSIST_DIR/$2"
  mkdir -p "$dst"
  if [ -d "$src" ] && [ ! -L "$src" ]; then
    # イメージに含まれていたファイルは、Volume に同じ名前がなければ引き継ぐ
    cp -Rn "$src"/. "$dst"/ 2>/dev/null || true
    rm -rf "$src"
  fi
  mkdir -p "$(dirname "$src")"
  ln -sfn "$dst" "$src"
}

link_dir data data
link_dir broadlistening/pipeline/outputs outputs
link_dir broadlistening/pipeline/inputs inputs
link_dir broadlistening/pipeline/configs configs

cd "$APP_DIR"
exec python -m uvicorn src.main:app --host 0.0.0.0 --port "${PORT:-8000}"
