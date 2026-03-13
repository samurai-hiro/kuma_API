# kuma_api README

## 概要

緯度・経度と統計年月から人口密度などの統計情報を取得し、
LightGBM モデルで推定を行う FastAPI ベースの API です。

主なエンドポイントは以下の通りです。

- `GET /` : ウェルカムメッセージを返却
- `GET /health` : ヘルスチェック（`{"status": "ok"}` を返却）
- `POST /predict` : 緯度・経度・日付を受け取り、人口関連情報を元にモデルで予測

---

## 環境要件

- Python 3.12 系を推奨
- OS: Windows（他 OS でも Python と依存ライブラリが動作すれば可）

---

## セットアップ手順

このリポジトリのルート（`main.py` があるディレクトリ）で以下を実行します。

### 1. 仮想環境の作成（任意）

```bash
python -m venv apivenv
```

### 2. 仮想環境の有効化 (Windows PowerShell)

```powershell
apivenv\Scripts\Activate.ps1
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

---

## 開発サーバの起動

FastAPI アプリケーションは `main.py` 内の `app` をエントリーポイントとしています。

```bash
uvicorn main:app --reload --port 8001
```

起動後、主な動作確認は以下の URL から行えます。

- ルート: http://localhost:8001/
- ヘルスチェック: http://localhost:8001/health
- 自動ドキュメント: http://localhost:8001/docs

---

## エンドポイント仕様

### `GET /`

- 概要: API の疎通確認用エンドポイント
- レスポンス例:

```json
{"message": "welcome to the kuma predictor API"}
```

### `GET /health`

- 概要: アプリケーションのヘルスチェック
- レスポンス例:

```json
{"status": "ok"}
```

### `POST /predict`

- 概要: 緯度・経度・日付を元に特徴量を作成し、学習済み LightGBM モデルで予測を行います。
- URL: `/predict`
- メソッド: `POST`
- リクエストボディ (JSON):

```json
{
	"lat": 35.0,
	"lon": 139.0,
	"date": "2026-03-12"
}
```

`date` は ISO 形式 (`YYYY-MM-DD`) の日付文字列です。

- レスポンスボディ (成功時の例):

```json
{
	"result": 0.12345678,
	"municd": 13101,
	"population_density": 6.78901234,
	"elevation": 50.0
}
```

- エラー発生時の例:

```json
{
	"result": null,
	"error": "invalid input"
}
```

※ 実際のメッセージ内容はエラーの種類により異なります。

---

## モデルファイルについて

ディレクトリ `model/` 内の `kuma_analysis_LGBM.joblib` が学習済みモデルです。

- モデルロード処理: `model/load_model.py`
- 特徴量前処理: `src/preprocess.py` 内の `xTrainPrePro` など

これらを通じて `predictor.py` の `predict` 関数からモデルが呼び出されます。

---

## テストの実行

`pytest` を使用したテストが `tests/` 配下に用意されています。

```bash
pytest
```

主なテスト:

- `tests/test_main.py`: ルートエンドポイントと `/predict` エンドポイントの動作確認
- `tests/test_predictor.py`: 予測処理ロジックのテスト

---

## デプロイのヒント

- 本番環境では、`Procfile` を利用して `gunicorn` + `uvicorn` workers での起動を構成できます。
- 環境変数が必要な場合は `.env` に定義し、`python-dotenv` 経由で読み込まれます（`main.py` で `load_dotenv()` を実行）。

具体的なデプロイ設定は利用する PaaS / IaaS 環境に合わせて調整してください。
