import streamlit as st
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title= "Lebanon: 2006 vs 2023-2024 airstrikes", page_icon="📌" , layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    df_2006 = pd.read_csv("Lebanon_2006_ICEWS.csv")

    df_2023 = pd.read_csv("ACLED_Lebanon_airstrikes_2023-2024.csv")

    return df_2006, df_2023

#Columns
st.subheader("Israeli strikes in Lebanon: 2006 vs 2023-2024")
col_1, col_2 = st.columns([1.5,1], gap="medium")
df_2006, df_2023 = load_data()

with col_1:
    mapbox_token = st.secrets["mapbox"]["token"]
    #Plot main map
    if 'fig' not in st.session_state:
        fig = go.Figure(go.Scattermapbox(
                lat=df_2006["Latitude"],
                lon=df_2006["Longitude"],
                mode='markers',
                marker=dict(size=9, color='blue'),
                name='2006 Airstrikes',
                hovertext='Date: ' + df_2006["Event Date"].astype(str) + '<br>Lat: ' + df_2006["Latitude"].astype(str) + '<br>Lon: ' + df_2006["Longitude"].astype(str),
                hoverinfo='text'  # Tells Plotly to use the hovertext attribute for hover information  # Label for legend
                    ))

        fig.add_trace(go.Scattermapbox(lat=df_2023["latitude"],
                        lon=df_2023["longitude"],
                        mode='markers',
                        marker=dict(size=9, color='red'),  # Optional: set color for 2023 data points,
                        name='2023-2024 Aistrikes',
                        hovertext='Date: ' + df_2023["date"].astype(str) + '<br>Lat: ' + df_2023["latitude"].astype(str) + '<br>Lon: ' + df_2023["longitude"].astype(str),
                        hoverinfo='text'  # Tells Plotly to use the hovertext attribute for hover information
                    ))
        fig.update_layout(
        mapbox_style="streets",
        mapbox_accesstoken=mapbox_token,
        width=800, 
        height=600,
        mapbox=dict(center=dict(lat=33.9, lon=35.7), zoom=7.5),
        showlegend=True,
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            title=dict(
            text="<b>Legend</b>: <br> <i>Click year to highlight in map</i> <br> ",  # Title for the legend
            font=dict(
                size=16,  # Font size for the legend title
                color="black"  # Font color for the legend title
            )),
        x=0,  # Position the legend to the left
        y=1,  # Position the legend to the top
        xanchor='left',  # Anchor the legend's x position to the left
        yanchor='top',# Anchor the legend's y position to the top
        font=dict(
        size=16)# Increase the font size of the legend 
        )
        )
        st.session_state['fig'] = fig

    map_placeholder = st.empty()
    map_placeholder.plotly_chart(st.session_state['fig'])

    st.markdown("""***Data Sources**:  
                - 2023-2024 airstrikes: Armed Conflict Location & Event Data Project (ACLED); www.acleddata.com;  
                - 2006 airstrikes: Boschee, Elizabeth; Lautenschlager, Jennifer; O'Brien, Sean; Shellman, Steve; Starz, James; Ward, Michael, 2015, 'ICEWS Coded Event Data', https://doi.org/10.7910/DVN/28075, Harvard Dataverse, V37*""")

with col_2:
    # Get user input for new point
    st.markdown("**Search specific coordinates in map:**")
    st.markdown("***Try example coordinates for Beirut:*** Latitude: 33.89, Longitude: 35.50")
    lat_input = st.text_input("Latitude", "")
    lon_input = st.text_input("Longitude", "")

    add_point = st.button("Add Point")

    if add_point:
        try:
            # Convert input to float
            lat_new = float(lat_input)
            lon_new = float(lon_input)

            # Add new point to the map
            st.session_state['fig'].add_trace(go.Scattermapbox(lat=[lat_new], lon=[lon_new], mode='markers',
                                marker=go.scattermapbox.Marker(size=12, color='black'), name='Searched location'))

            st.success(f"Point added: ({lat_new}, {lon_new})")
                    # Set the map's center to the new point and zoom in
            st.session_state['fig'].update_layout(
                mapbox=dict(
                    center=dict(lat=lat_new, lon=lon_new),
                    zoom=10  # Adjust zoom level as needed
                )
            )
            map_placeholder.plotly_chart(st.session_state['fig'])

        except ValueError:
            st.error("Please enter valid coordinates.")

    st.markdown(
        """ 
        **Details:**
        - The data only includes airstrikes. Artillery/Rocket strikes are not included.
        - The ACLED dataset contains 2,453 incidents, and covers the period from October 1, 2023 to July 27, 2024.
        - ICEWS data for Israeli airstrikes in 2006 has 1,123 entries, and covers the period between July 1-August 30, 2006. 
        - Israel is estimated to have launched over 7,000 rocket strikes in 2006. The data available, despite being lower, still reflects notable locations targeted.
"""
    )
