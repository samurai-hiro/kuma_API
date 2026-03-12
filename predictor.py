from model.load_model import pipemodel
from services.population_density import (
    get_city_code,
    fetch_estat_value,
    get_elevation,
)
import numpy as np
import pandas as pd
from typing import Dict, Union


def predict(lat: float, lon: float, date: str) -> Dict[str, Union[float, int, None]]:
    """緯度・経度と統計年月から人口密度を算出し、モデルで予測を行う。

    指定された緯度・経度から市区町村コードを取得し、e-Stat から人口と
    土地面積を取得して人口密度を計算する。その後、標高情報とあわせて
    特徴量を作成し、事前に学習済みのパイプラインモデルで予測値を算出する。

    Args:
        lat: 緯度（10進表記）。
        lon: 経度（10進表記）。
        date: 統計データの年月（例: "2020" や "202010" など、fetch_estat_value が想定する形式）。

    Returns:
        予測結果および付随情報を格納した辞書。

        - "result": 予測値。
        - "municd": 市区町村コード。
        - "population_density": 対数変換後の人口密度。
        - "elevation": 標高。

    Raises:
        ValueError: 日本以外のエリアが指定された場合など、入力値に起因するエラー。
        Exception: 予測処理中にその他のエラーが発生した場合。
    """
    
    #変数の初期化(エラー時に返すため)
    muni_cd = None
    population_density = None
    elevation = None    
    try:
        #緯度経度から市区町村コードを取得
        muni_cd = get_city_code(lat, lon)

        #市区町村コードから人口を取得
        population = fetch_estat_value(
            STATS_DATA_ID='0000020201',
            muni_cd=muni_cd,
            cat_code='A1101',
            date=date
        )
        
        #市区町村コードから土地面積を取得
        land_area = fetch_estat_value(
            STATS_DATA_ID='0000020102',
            muni_cd=muni_cd,
            cat_code='B1101',
            date=date
        )
        #人口密度を計算
        #人/km2
        population_density = round((population / land_area) *100, 8)
                
        #対数変換
        population_density = np.log(population_density)

        #標高を取得
        elevation = get_elevation(lat, lon)

        #予測に必要な特徴量をデータフレームにまとめる
        feature_df = pd.DataFrame([{
                    'lat':lat,
                    'lon':lon,
                    'date':date,
                    'elevation':elevation,
                    'prefecture':'',
                    'municd':muni_cd,
                    'populationdensity':population_density,
                    'muniname':'',
                }])

        #特徴量の型を予測モデルに合わせる
        feature_df['municd'] = feature_df['municd'].astype(int)

        #予測モデルに特徴量を入れて予測を行う
        targetVal = pipemodel.predict(feature_df)
        targetVal = round(targetVal[0], 8)

        return {'result': targetVal,
                'municd': muni_cd,
                'population_density': population_density, 
                'elevation': elevation,
                }
    except ValueError as e:
        #日本以外のエリアが選択された場合
        print(f"ValueError: {e}")

        #エラー内容をそのまま返す
        raise
    except Exception as e:
        print(f"Error during prediction: {e}")
        
        #エラー内容に必要な情報を追加して返す
        raise Exception(f"Error during prediction: muni_cd={muni_cd}, population_density={population_density}, elevation={elevation}")
    