from fastapi import FastAPI
from schemas import PredictRequest
from predictor import predict
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()
app = FastAPI()


@app.post("/predict")
def predict_api(request: PredictRequest) -> Dict[str, Any]:
    """予測用エンドポイント。

    リクエストで受け取った緯度・経度・日付を元に `predict` 関数を呼び出し、
    モデルによる予測結果を返す。予測処理中に例外が発生した場合は、
    `result` を `None` とし、`error` キーにエラーメッセージを格納して返却する。

    Args:
        request: 予測に必要な入力値（緯度・経度・日付）を含むリクエストボディ。

    Returns:
        予測結果またはエラー内容を含む JSON 形式の辞書。
    """
    try:
        result = predict(request.lat, request.lon, request.date)
        return result
    except Exception as e:
        return {
            "result": None,
            "error": str(e),
        }


@app.get("/health")
def health() -> Dict[str, str]:
    """ヘルスチェック用エンドポイント。

    Returns:
        API が正常に動作していることを示すステータス。
    """
    return {"status": "ok"}


@app.get("/")
def root() -> Dict[str, str]:
    """ルートエンドポイント。

    Returns:
        API のウェルカムメッセージ。
    """
    return {"message": "welcome to the kuma predictor API"}


