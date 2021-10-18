import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import math
import altair as alt
import requests

from utility import *

df = load_data("house_data.csv")

st.set_page_config(
    page_title="Exploring second-hand house transaction in Shanghai",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.header("Exploring second-hand house transaction in Shanghai :house: :dollar:")



st.header(":star: Unit Price By Location")
"""
The map below visualizes the distribution of second house transaction data in shanghai.\n
Each dot is a transaction with radius representing the total amount of transaction price.\n
The color density indicates the unit price of this house: deeper color represents higher unit price.\n
Feel free to **zoom in** or ** zoom out** to interact with the map.
"""

################################################################################
##################################### Map ######################################
# Define a layer to display on a map
layer0 = pdk.Layer(
    "ScatterplotLayer",
    df[df["UnitPrice"] < 50000],
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=0.1,
    radius_min_pixels=0.1,
    radius_max_pixels=5,
    get_position=['lon', 'lat'],
    get_radius="TotalPrice",
    get_fill_color=[162, 133, 248],
)

above50000 = df["UnitPrice"] >= 50000
below80000 = df["UnitPrice"] < 80000
layer1 = pdk.Layer(
    "ScatterplotLayer",
    df[above50000 & below80000],
    pickable=True,
    opacity=0.9,
    stroked=True,
    filled=True,
    radius_scale=0.1,
    radius_min_pixels=0.1,
    radius_max_pixels=5,
    get_position=['lon', 'lat'],
    get_radius="TotalPrice",
    get_fill_color=[126, 192, 238],
)


above80000 = df["UnitPrice"] >= 80000
below100000 = df["UnitPrice"] < 100000
layer2 = pdk.Layer(
    "ScatterplotLayer",
    df[above80000 & below100000],
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=0.1,
    radius_min_pixels=0.1,
    radius_max_pixels=5,
    get_position=['lon', 'lat'],
    get_radius="TotalPrice",
    get_fill_color=[255, 255, 255],
)

above100000  = df["UnitPrice"] >= 100000 
below120000 = df["UnitPrice"] < 120000
layer3 = pdk.Layer(
    "ScatterplotLayer",
    df[above100000 & below120000],
    pickable=True,
    opacity=1,
    stroked=True,
    filled=True,
    radius_scale=0.1,
    radius_min_pixels=0.1,
    radius_max_pixels=5,
    get_position=['lon', 'lat'],
    get_radius="TotalPrice",
    get_fill_color=[249, 124, 67],
)

above120000  = df["UnitPrice"] >= 120000 
layer4 = pdk.Layer(
    "ScatterplotLayer",
    df[above120000],
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=0.1,
    radius_min_pixels=0.1,
    radius_max_pixels=5,
    get_position=['lon', 'lat'],
    get_radius="TotalPrice",
    get_fill_color=[251, 3, 3],
)


# Set the viewport location
view_state = pdk.ViewState(
    longitude=121.507935,
    latitude=31.235556,
    zoom=10,
    min_zoom=7,
    max_zoom=16,
    pitch=40,
    bearing=0)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer0, layer1, layer2, layer3, layer4], initial_view_state=view_state)

st.pydeck_chart(r)

################################################################################
################################## Bar Chart ###################################

def pretty(s: str) -> str:
    try:
        return dict(js="JavaScript")[s]
    except KeyError:
        return s.capitalize()


st.header(":star: Unit Price By District")
"""
Let's take a look at the average unit price in different districts.\n
The bar chart shows that Jingan is the most prosperous district, 
so its average unit price is much higher than the rest \n
Qingpu, Jiading, and Songjiang are in the periphery of Shanghai, 
so the house price is relatively lower
"""
all_districts = df.District.unique().tolist()
districts = st.multiselect(
    "", options=all_districts, default=all_districts, format_func=pretty
)
base_df = get_avg_unit_price_by_district(df)
plot_df = base_df[base_df.District.isin(districts)]

chart = (
    alt.Chart(
        plot_df,
        title="Average Unit Price by District",
    )
    .mark_bar()
    .encode(
        x=alt.X("UnitPrice", title="Average Unit Price"),
        y=alt.Y(
            "District",
            sort=alt.EncodingSortField(field="UnitPrice", order="descending"),
            title="",
        ),
        tooltip=["UnitPrice", "District"],
    )
)


st.altair_chart(chart, use_container_width=True)



st.header(":star: Change Of Unit Price From 2012-2017")
"""
Time is also an important dimension to explore the unit price change in Shanghai.\n
An average unit price by area is calculated and plot for different years.\n

From 2012-2017, the unit price overall grows a lot.

In early years, the smaller the total area of an apartment is, the higher unit price it would have.

This tendency changes recently. As houses with large area become scarcer, the unit price actually increases a lot.
"""
plot_df = get_avg_unit_price_by_area_year(df)

import plotly.express as px
fig = px.scatter(plot_df, x="Area", y="UnitPrice", animation_frame="Year",
           range_x=[0,200], range_y=[0,100000])
st.plotly_chart(fig)