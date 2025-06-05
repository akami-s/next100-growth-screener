import streamlit as st
import pandas as pd
import math

# タイトル部分
st.markdown("### 🎯 次の100億企業を探せ！")
st.caption("2022〜2024年上場の東証グロース銘柄から成長シナリオを描く")

# データ読み込み
@st.cache_data
def load_data():
    df = pd.read_csv("data/next100_required_cagr_corrected.csv")
    df.columns = df.columns.str.strip()
    df["必要CAGR(%)"] = pd.to_numeric(df["必要CAGR(%)"], errors="coerce")
    return df.dropna(subset=["必要CAGR(%)"])

data = load_data()

# スライダーの設定
min_cagr = int(data["必要CAGR(%)"].min())
max_cagr = math.ceil(data["必要CAGR(%)"].max())

cagr_range = st.slider(
    "必要CAGR(%)の範囲を選択（5年後に時価総額100億円を目指す）",
    min_value=min_cagr,
    max_value=max_cagr,
    value=(min_cagr, max_cagr),
    step=1,
)

# 🎯 コメント表示（スライダーの上限に応じて）
max_selected_cagr = cagr_range[1]
if max_selected_cagr <= 20:
    st.success("🟢 実現可能な水準。過去にも多くの企業が到達しています。")
elif max_selected_cagr <= 30:
    st.info("🟡 頑張れば狙えるゾーン。ただし成長戦略の精査が必要。")
elif max_selected_cagr <= 40:
    st.warning("🟠 高成長が求められる領域。成功企業は限られます。")
else:
    st.error("🔴 極めて高い成長率が必要。現実的かどうか慎重に検討を。")

# フィルタ処理
filtered = data[(data["必要CAGR(%)"] >= cagr_range[0]) & (data["必要CAGR(%)"] <= cagr_range[1])]

# カラム名短縮
filtered = filtered.rename(columns={
    "時価総額(百万円)": "時価総額",
    "必要CAGR(%)": "CAGR"
})

display_cols = ["コード", "銘柄名", "上場日", "時価総額", "経過年数", "残り年数", "CAGR"]

# 表示
st.subheader(f"📋 該当企業一覧：{len(filtered)}社")
st.dataframe(filtered[display_cols], use_container_width=True)

# カラム補足
with st.expander("📘 カラムの補足"):
    st.markdown("""
    - **時価総額**: 単位は百万円（例: 7500 = 75億円）  
    - **CAGR**: 5年後に時価総額100億円を達成するために必要な年率成長率（%）  
    """)
