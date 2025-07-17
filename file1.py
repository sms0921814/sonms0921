import streamlit as st
import pandas as pd

FILE_PATH = "202505_202505_연령별인구현황_월간 (1).csv"

@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')
    return df

df = load_data()

age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]

age_map = {col: col.replace('2025년05월_계_', '') for col in age_columns}
df = df.rename(columns=age_map)

cols_to_use = ['행정구역', '총인구수'] + list(age_map.values())
df_filtered = df[cols_to_use]

top5 = df_filtered.sort_values(by='총인구수', ascending=False).head(5)

age_only_cols = list(age_map.values())
top5_age = top5.set_index('행정구역')[age_only_cols].transpose()

st.title("2025년 5월 기준 연령별 인구 현황")
st.subheader("상위 5개 행정구역의 연령대별 인구 선 그래프")
st.line_chart(top5_age)

st.subheader("📄 원본 데이터")
st.dataframe(df_filtered)
