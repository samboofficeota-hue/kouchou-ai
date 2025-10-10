import re

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse


def register_security_middleware(app: FastAPI):
    """
    不審なパターンのリクエストをブロックするミドルウェアを登録する関数。
    """

    @app.middleware("http")
    async def block_suspicious_requests(request: Request, call_next):
        # 環境変数ファイルへのアクセスなど、怪しいパスパターンを定義
        blocked_patterns = [r"/\.env.*", r"/config\.php", r"/wp-login\.php"]

        path = request.url.path
        for pattern in blocked_patterns:
            if re.match(pattern, path):
                return ORJSONResponse(status_code=403, content={"message": "Access forbidden"})

        # 簡易レート制限（IP x path 単位での極端な連打を抑制）
        # 過度な状態保持は避け、極小のメモリで簡易的に抑止
        try:
            state = getattr(app.state, "_rl", {})
            app.state._rl = state
            key = (request.client.host if request.client else "unknown", request.url.path)
            from time import time
            now = time()
            last = state.get(key, 0)
            # 0.2秒未満の連投は拒否
            if now - last < 0.2:
                return ORJSONResponse(status_code=429, content={"message": "Too Many Requests"})
            state[key] = now
        except Exception:
            pass

        response = await call_next(request)
        return response
