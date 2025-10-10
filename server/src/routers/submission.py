from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.config import settings
from src.utils.logger import setup_logger
from src.utils.validation import validate_filename


router = APIRouter()
logger = setup_logger()


class PublicSubmission(BaseModel):
    slug: str = Field(..., description="保存先識別子（レポートID相当）")
    comment: str = Field(..., min_length=1, max_length=4000)
    source: str | None = Field(default=None)
    url: str | None = Field(default=None)
    # 任意属性を受け付ける
    attributes: dict[str, Any] | None = Field(default=None)


@router.post("/submit", status_code=201)
def submit_comment(payload: PublicSubmission) -> dict[str, str]:
    # slug のバリデーション（安全なファイル名のみ許可）
    ok, msg = validate_filename(payload.slug)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    inputs_dir: Path = settings.INPUT_DIR
    inputs_dir.mkdir(parents=True, exist_ok=True)
    csv_path = inputs_dir / f"{payload.slug}.csv"

    # 1レコードの辞書を構築
    record: dict[str, Any] = {
        "comment-id": f"pub-{int(datetime.utcnow().timestamp()*1000)}",
        "comment": payload.comment,
        "source": payload.source,
        "url": payload.url,
    }

    if payload.attributes:
        for k, v in payload.attributes.items():
            key = k if str(k).startswith("attribute_") else f"attribute_{k}"
            record[key] = None if v is None else str(v)

    try:
        # 既存CSVの列を尊重して追記。無ければ新規作成。
        if csv_path.exists():
            try:
                existing_df = pd.read_csv(csv_path)
            except Exception:
                existing_df = pd.DataFrame()

            new_df = pd.DataFrame([record])
            df = pd.concat([existing_df, new_df], ignore_index=True)
            df.to_csv(csv_path, index=False)
        else:
            pd.DataFrame([record]).to_csv(csv_path, index=False)

        logger.info(f"Public submission stored: {csv_path}")
    except Exception as e:
        logger.error(f"Failed to append submission: {e}")
        raise HTTPException(status_code=500, detail="保存に失敗しました")

    return {"status": "ok"}


