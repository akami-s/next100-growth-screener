import streamlit as st
import pandas as pd
import numpy as np
import math

st.markdown("### 🎯 次の100億企業を探せ！")
st.caption("2022〜2024年上場グロース銘柄の成長力を多段階スクリーニング")

@st.cache_data
def load_data():
    df = pd.read_csv("data/next100_required_cagr_with_edinet.csv")
    df['粗利益率'] = np.where(
        df['売上原価'].isnull() | (df['売上原価'] == 0),
        1.0,
        (df['売上高'] - df['売上原価']) / df['売上高']
    )
    df['粗利益率'] = (df['粗利益率'] * 100).round(2)
    df['時価総額'] = df['時価総額(百万円)']
    return df

df = load_data()

# スライダー①：必要CAGR
min_cagr = int(df["必要CAGR(%)"].min())
max_cagr = math.ceil(df["必要CAGR(%)"].max())
cagr_range = st.slider("必要CAGR(%)の範囲を選択（5年後に時価総額100億円を目指す）", min_cagr, max_cagr, (min_cagr, max_cagr), step=1)

max_selected_cagr = cagr_range[1]
if max_selected_cagr <= 20:
    st.success("🟢 実現可能な水準。過去にも多くの企業が到達しています。")
elif max_selected_cagr <= 30:
    st.info("🟡 頑張れば狙えるゾーン。ただし成長戦略の精査が必要。")
elif max_selected_cagr <= 40:
    st.warning("🟠 高成長が求められる領域。成功企業は限られます。")
else:
    st.error("🔴 極めて高い成長率が必要。現実的かどうか慎重に検討を。")

filtered = df[(df["必要CAGR(%)"] >= cagr_range[0]) & (df["必要CAGR(%)"] <= cagr_range[1])]

# スライダー②：売上高
sales_min = int(df["売上高"].min())
sales_max = int(df["売上高"].max())
sales_lower = st.slider("売上高（百万円）がこの値以上の企業のみ表示", sales_min, sales_max, sales_min, step=100)

if sales_lower < 1000:
    st.error("🔴 売上高が小さいため、スケールには時間がかかる可能性があります。")
elif sales_lower < 3000:
    st.warning("🟠 売上高はある程度あるが、黒字化には慎重な見極めが必要です。")
elif sales_lower < 5000:
    st.info("🟡 一定の売上規模あり。成長戦略次第でスケールアップ可能。")
elif sales_lower < 10000:
    st.success("🟢 売上規模は十分。粗利・戦略次第で100億円が視野に入ります。")
else:
    st.success("💎 売上10億超。規模と事業構造が備わっていれば有力候補です。")

filtered = filtered[filtered["売上高"] >= sales_lower]

# スライダー③：粗利益率
st.markdown("### 💡 粗利益率でさらに絞り込む")
gp_min = 0
gp_max = 100
gp_lower = st.slider("粗利益率(%)がこの値以上の企業のみ表示（1%刻み）", gp_min, gp_max, gp_min, step=1)
if gp_lower < 20:
    st.error("🔴 粗利益率が極端に低いゾーン。ビジネスモデルの再考が必要。")
elif gp_lower < 40:
    st.warning("🟠 競争が激しくコストが重いビジネス。効率化や付加価値が課題。")
elif gp_lower < 60:
    st.info("🟡 一般的な上場企業の粗利益率水準。事業拡大次第で高収益化も狙える。")
elif gp_lower < 80:
    st.success("🟢 高粗利益率。サービス型や強いブランド力を持つ企業。")
else:
    st.success("💎 極めて高い粗利益率。付加価値が高く、競争優位性が際立つビジネス。")
filtered = filtered[filtered["粗利益率"] >= gp_lower]

# スライダー④：営業利益
op_min = int(df["営業利益"].min())
op_max = int(df["営業利益"].max())
op_lower = st.slider("営業利益（百万円）がこの値以上の企業", op_min, op_max, op_min, step=100)

if op_lower < -1000:
    st.error("🔴 大幅な営業赤字。早期の収益改善が不可欠です。")
elif op_lower < 0:
    st.warning("🟠 営業赤字。高粗利でも販管費に課題がある可能性あり。")
elif op_lower < 500:
    st.info("🟡 黒字化済み。利益の積み上げに注目。")
elif op_lower < 2000:
    st.success("🟢 営業利益は順調。拡大フェーズに入りつつあります。")
else:
    st.success("💎 高い営業利益水準。ビジネスモデルが確立されています。")

filtered = filtered[filtered["営業利益"] >= op_lower]

# スライダー⑤：営業CF
cf_min = int(df["営業CF"].min())
cf_max = int(df["営業CF"].max())
cf_lower = st.slider("営業キャッシュフロー（百万円）がこの値以上の企業", cf_min, cf_max, cf_min, step=100)

if cf_lower < -1000:
    st.error("🔴 大きな営業キャッシュアウト。資金繰りに注意が必要です。")
elif cf_lower < 0:
    st.warning("🟠 キャッシュ流出中。成長投資中である可能性もあります。")
elif cf_lower < 500:
    st.info("🟡 キャッシュ黒字。堅実なオペレーションが伺えます。")
elif cf_lower < 2000:
    st.success("🟢 安定してキャッシュを生み出しています。")
else:
    st.success("💎 強力なキャッシュ創出力。投資余力も十分です。")

filtered = filtered[filtered["営業CF"] >= cf_lower]

# タグ表示用関数
def generate_tags(row):
    tags = []
    if row["営業利益"] > 0:
        tags.append("🟢黒字")
    if row["営業CF"] > 0:
        tags.append("💰CF黒字")
    if row["粗利益率"] >= 60:
        tags.append("💎高粗利")
    return " ".join(tags)

filtered["評価タグ"] = filtered.apply(generate_tags, axis=1)

# 表示列
show_cols = ['証券コード', '企業名', '時価総額', '売上高', '必要CAGR(%)', '粗利益率', '営業利益', '営業CF', '評価タグ']
st.markdown(f"#### 🎯 条件に合致する企業一覧：{len(filtered)}件")
st.dataframe(filtered[show_cols].reset_index(drop=True), use_container_width=True)
