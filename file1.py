import streamlit as st
import pandas as pd

st.title("2025년 5월 기준 연령별 인구 현황 분석")

file_path = "202505_202505_연령별인구현황_월간 (1).csv"

df = pd.read_csv(file_path, encoding="euc-kr")

st.subheader("📄 원본 데이터")
st.dataframe(df)

age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
df_filtered = df[["행정구역", "총인구수"] + age_columns].copy()

df_filtered.columns = ["행정구역", "총인구수"] + [col.replace("2025년05월_계_", "") for col in age_columns]

top5 = df_filtered.sort_values("총인구수", ascending=False).head(5)

plot_df = top5.set_index("행정구역").drop(columns="총인구수").T

plot_df.index = plot_df.index.astype(int)
plot_df = plot_df.sort_index()

st.subheader("📈 상위 5개 행정구역의 연령별 인구 추이")
st.line_chart(plot_df)
