import pandas as pd
import os
import streamlit as st
import plotly.express as px

# Set up file paths
data_folder = "data"
order_file = os.path.join(data_folder, "DataCoSupplyChainDataset.csv")
geo_file = os.path.join(data_folder, "DescriptionDataCoSupplyChain.csv")


def load_data():
    """Load order and geopolitical data"""
    if not os.path.exists(order_file) or not os.path.exists(geo_file):
        st.error("⚠️ Data files not found. Please check file paths!")
        return None, None

    order_data = pd.read_csv(order_file, encoding='ISO-8859-1',
                             usecols=["Order Id", "Order Status", "Customer Country", "Order Profit Per Order",
                                      "Latitude", "Longitude", "Late_delivery_risk"])
    geo_data = pd.read_csv(geo_file, encoding='ISO-8859-1', usecols=["FIELDS", "DESCRIPTION"])
    return order_data, geo_data


# Streamlit UI Setup
st.set_page_config(page_title="📦 Supply Chain Risk Management", layout="wide")

# Custom CSS for Background and Theme
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f4;
        color: #333333;
    }
    .stApp {
        background-color: #e0f7fa;
        padding: 20px;
        border-radius: 10px;
    }
    .stTitle {
        color: #00796b;
        font-size: 28px;
        font-weight: bold;
    }
    .stSubheader {
        color: #004d40;
        font-size: 24px;
    }
    .stDataframe {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='stTitle'>📦 Supply Chain Risk Management System</h1>", unsafe_allow_html=True)

# Load Data
st.write("🔄 Loading data...")
order_data, geo_data = load_data()

if order_data is not None and geo_data is not None:
    # Interactive Filters
    country_list = order_data["Customer Country"].unique()
    selected_country = st.selectbox("🌍 Select a Country to Analyze:", options=["All"] + list(country_list))

    if selected_country != "All":
        order_data = order_data[order_data["Customer Country"] == selected_country]

    st.markdown("<h2 class='stSubheader'>📊 Order Data Overview</h2>", unsafe_allow_html=True)
    st.dataframe(order_data.head())

    st.markdown("<h2 class='stSubheader'>📍 Geopolitical & Supplier Risk Data</h2>", unsafe_allow_html=True)
    st.dataframe(geo_data.head())

    st.markdown("---")
    st.markdown("<h2 class='stSubheader'>🚨 Risk Analysis & Alerts</h2>", unsafe_allow_html=True)

    # Find High-Risk Orders
    high_risk_orders = order_data[order_data["Late_delivery_risk"] == 1]
    if not high_risk_orders.empty:
        st.warning(f"⚠️ {len(high_risk_orders)} High-Risk Orders Found!")
        st.dataframe(high_risk_orders)
    else:
        st.success("✅ No high-risk orders detected.")

    # Show Risk Locations on Map
    st.markdown("<h2 class='stSubheader'>🌍 Risk Locations on Realistic Map</h2>", unsafe_allow_html=True)

    sample_data = order_data.sample(min(500, len(order_data)))

    fig = px.scatter_mapbox(sample_data,
                            lat="Latitude",
                            lon="Longitude",
                            color="Late_delivery_risk",
                            hover_name="Customer Country",  # Show country name on hover
                            text="Customer Country",  # Display country name on the map
                            hover_data={"Latitude": False, "Longitude": False, "Late_delivery_risk": True},
                            title="Geopolitical & Delivery Risks",
                            color_continuous_scale="reds",
                            size_max=15,
                            zoom=1)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces(textposition='top center')  # Place country names above points
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("⚠️ Data not loaded. Please check file paths and restart the app.")