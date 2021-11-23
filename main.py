import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import statistics
import glob

client_id = '****************'
client_secret = '****************'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

top_records = []
for csv in sorted(glob.glob("./csv/*.csv")):
    top_records.append(pd.read_csv(csv, header=1))

top_track_info = []
top_records_count = len(top_records)
# 国ごとに曲の情報を取得する
for i in range(top_records_count):
    top_ure_list = top_records[i]["URL"].unique()
    top_track_id = [top_url.split('/')[-1] for top_url in top_ure_list]

    top_track_info.append(pd.DataFrame())
    for id in top_track_id:
        info = pd.DataFrame.from_dict(sp.audio_features(id))
        top_track_info[i] = top_track_info[i].append(info)

    top_track_info[i] = top_track_info[i].reset_index(drop=True)
    top_track_info[i].head(10)
    top_track_info[i]["rank"] = top_track_info[i].index + 1

cols = top_track_info[0].columns
excludes = ("analysis_url", "id", "rank", "track_href", "type", "uri", 'instrumentalness', 'key', 'mode', 'time_signature')
col_nm = {"acousticness": "アコースティック感", "danceability": "ダンス感", "duration_ms": "長さ[ms]", "energy": "エナジー感", "liveness": "ライブ感", "loudness": "音圧", "speechiness": "スピーチ感", "tempo": "曲のテンポ(BPM)", "valence": "曲の明るさ"}
contry = ("ブラジル", "カナダ", "ドイツ", "エジプト", "スペイン", "フィンランド", "日本", "アメリカ",  "香港", "南アフリカ")
# 特徴ごとにグラフを生成する
for col in cols:
    avgs = []
    if(col in excludes): continue
    plt.title("各国の週間TOP200ランキングの" + col_nm[col] + "（平均）")

    # 国ごとに平均値を取得
    for i in range(top_records_count):
        avgs.append(statistics.mean(top_track_info[i][col]))

    plt.bar(contry, avgs, alpha=0.8)
    plt.legend(loc="upper left", fontsize=11)
    plt.xlabel("国名")
    plt.ylabel(col_nm[col])
    plt.savefig("./images/" + col + ".png")
    plt.clf()
