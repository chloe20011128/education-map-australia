
import streamlit as st
import pandas as pd
import plotly.express as px

# 页面设置
st.set_page_config(page_title="Education Services Map", layout="wide")
st.title("📍 Education Services in Australian Suburbs")
st.markdown("Explore the relationship between **average rating** and **service coverage** by suburb.")

# 读取数据
df = pd.read_csv("grouped_suburb_state.csv")
coords = pd.read_csv("suburb_coordinates.csv")

# 合并经纬度
df = pd.merge(df, coords, on=["Suburb", "State"], how="inner")
df = df.dropna(subset=["Latitude", "Longitude", "AvgRating", "ServiceCount"])

# 添加评分分类
def classify_color(rating):
    if rating < 3.5:
        return "Needs Improvement"
    elif rating < 4.0:
        return "Below Average"
    elif rating < 5.0:
        return "Moderate"
    else:
        return "High Quality"

df["QualityLevel"] = df["AvgRating"].apply(classify_color)

# 自定义颜色映射
color_map = {
    "Needs Improvement": "red",
    "Below Average": "orange",
    "Moderate": "gold",
    "High Quality": "green"
}

# 绘图
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    size="ServiceCount",
    color="QualityLevel",
    color_discrete_map=color_map,
    hover_name="Suburb",
    hover_data={"AvgRating": True, "ServiceCount": True},
    zoom=3,
    height=650
)

fig.update_layout(
    mapbox_style="carto-positron",
    margin={"r":0,"t":0,"l":0,"b":0},
    legend_title_text="Service Quality Level"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
🔴 **Needs Improvement**: Low average rating (< 3.5)  
🟠 **Below Average**: 3.5–3.9  
🟡 **Moderate**: 4.0–4.9  
🟢 **High Quality**: ≥ 5.0  
Bubble size indicates the number of approved services per suburb.
""")


