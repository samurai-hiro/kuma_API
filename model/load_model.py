"""
load_model.py

このファイルは、LightGBMモデルの読み込みと前処理パイプラインのインポートを行います。
Django設定からモデルパスを取得し、joblibを用いて学習済みモデルをロードします。
"""
import os  # OS操作用モジュール
import joblib  # モデルの保存・読み込み用
from src.preprocess import xTrainPrePro  # 前処理関数のインポート
from lightgbm import LGBMRegressor  # LightGBM回帰モデル
from sklearn.preprocessing import StandardScaler  # 標準化用スケーラー
from sklearn.pipeline import Pipeline  # パイプライン構築用

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'kuma_analysis_LGBM.joblib')  # モデルファイルのパスをDjango設定から取得
pipemodel = joblib.load(model_path)  # 学習済みモデルのロード
