import streamlit as st
import pandas as pd
import numpy as np
import math

st.markdown("### 🎯 次の100億企業を探せ！")
st.caption("2022〜2024年上場グロース銘柄の成長力を多段階スクリーニング")

# データ読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("data/next100_required_cagr_with_edinet.csv")
    # 粗利益率計算（売上原価が空欄/0なら100％）
    df['粗利益率'] = np.where(
        df['売上原価'].isnull() | (df['売上原価'] == 0),
        1.0,
        (df['売上高'] - df['売上原価']) / df['売上高']
    )
    df['粗利益率'] = (df['粗利益率'] * 100).round(2)
    # 表示用に「時価総額」カラム追加（元は「時価総額(百万円)」）
    df['時価総額'] = df['時価総額(百万円)']
    return df

df = load_data()

# 必要CAGR(%) スライダー
min_cagr = int(df["必要CAGR(%)"].min())
max_cagr = math.ceil(df["必要CAGR(%)"].max())

cagr_range = st.slider(
    "必要CAGR(%)の範囲を選択（5年後に時価総額100億円を目指す）",
    min_value=min_cagr,
    max_value=max_cagr,
    value=(min_cagr, max_cagr),
    step=1,
)

# 色付きコメント
max_selected_cagr = cagr_range[1]
if max_selected_cagr <= 20:
    st.success("🟢 実現可能な水準。過去にも多くの企業が到達しています。")
elif max_selected_cagr <= 30:
    st.info("🟡 頑張れば狙えるゾーン。ただし成長戦略の精査が必要。")
elif max_selected_cagr <= 40:
    st.warning("🟠 高成長が求められる領域。成功企業は限られます。")
else:
    st.error("🔴 極めて高い成長率が必要。現実的かどうか慎重に検討を。")

# まずCAGR条件で絞り込み
filtered_cagr = df[(df["必要CAGR(%)"] >= cagr_range[0]) & (df["必要CAGR(%)"] <= cagr_range[1])]

# 表示カラム
show_cols = ['証券コード', '企業名', '時価総額', '残り年数', '必要CAGR(%)', '粗利益率']

# 件数表示を追加
st.markdown(f"#### 🚀 必要CAGR(%)条件に合致する企業一覧：{len(filtered_cagr)}件")
st.dataframe(filtered_cagr[show_cols].reset_index(drop=True), use_container_width=True)

# カラム補足説明
with st.expander("【カラムの補足説明】"):
    st.markdown("""
- **証券コード**：上場時の証券コード
- **企業名**：上場企業名
- **時価総額**：2025年6月5日時点の時価総額（**単位：百万円**）
- **残り年数**：「5年後100億円」達成まで残る年数
- **必要CAGR(%)**：今の時価総額から5年後100億円に到達するために必要な年平均成長率
- **粗利益率**：売上総利益 ÷ 売上高（売上原価が空欄/ゼロの場合は100%として自動計算）
""")

# --- 粗利益率スライダー（下限のみ指定） ---
st.markdown("### 💡 粗利益率でさらに絞り込む")
gp_min = 0
gp_max = 100

gp_lower = st.slider(
    "粗利益率(%)がこの値以上の企業のみ表示（1%刻み）",
    min_value=gp_min,
    max_value=gp_max,
    value=gp_min,
    step=1,
)

# 粗利益率コメント（下限で切り替え）
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

filtered_both = filtered_cagr[filtered_cagr["粗利益率"] >= gp_lower]

# 件数表示を追加
st.markdown(f"#### 🎯 必要CAGR(%) × 粗利益率 条件に合致する企業一覧：{len(filtered_both)}件")
st.dataframe(filtered_both[show_cols].reset_index(drop=True), use_container_width=True)
