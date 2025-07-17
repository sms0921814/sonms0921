import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("📍 2025년 5월 기준 연령별 인구 현황 + 지도 시각화")

# 데이터 불러오기 및 전처리
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 연령 컬럼 처리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 괄호 제거
df_age['행정구역'] = df_age['행정구역'].str.replace(r"\s*\(.*\)", "", regex=True)

# 상위 5개 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

st.subheader("📊 상위 5개 행정구역 데이터")
st.dataframe(top5_df)

# 지도 시각화
st.subheader("🗺️ 지도에 인구 표시 (핑크 원)")

# 지오코딩 설정
geolocator = Nominatim(user_agent="population_map")

# 지도 초기화
first_location = geolocator.geocode(top5_df.iloc[0]['행정구역'])
m = folium.Map(location=[first_location.latitude, first_location.longitude], zoom_start=7)

# 지도에 원 추가
for index, row in top5_df.iterrows():
    location = geolocator.geocode(row['행정구역'])
    if location:
        folium.Circle(
            location=[location.latitude, location.longitude],
            radius=row['총인구수'] / 50,  # 인구 수 기반 반지름 조절
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.4,
            popup=f"{row['행정구역']}: {row['총인구수']:,}명"
        ).add_to(m)

# 지도 렌더링
st_data = st_folium(m, width=1000, height=600)

# 연령별 그래프
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")

age_columns_only = top5_df.columns[2:]
for index, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)

