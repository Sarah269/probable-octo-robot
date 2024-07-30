import streamlit as st
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
import warnings
warnings.filterwarnings('ignore') 
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="US Brewery Finder",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded")

# Header
hdr_col1, hdr_col2 = st.columns((4,4))

with hdr_col1:
   st.write(""" 
   # Find a Brewery

   This app helps find breweries located in the United States.  The data was pulled as a snapshot in March 2024.

   **Data Source:** [Open Brewery Public API](https://www.openbrewerydb.org/)

   Data Preview
   - Click on Data Preview to view and/or download dataset.
   - Apply filters to select breweries.
   
   Tiles & Graphs update based on filter selections. Default is all US breweries.
   """ )

with hdr_col2:
   st.image("beer-5026476_640.jpg",width=500)


# Load Data
@st.cache_data
def load_data():
    data = pd.read_csv("US_Breweries.csv")
    data['postal_code'] =   data['postal_code'].str.slice(0,5)
    data = data[['name','brewery_type','address_1','city','state','postal_code','phone','website_url']].copy()
    return data

df = load_data()
selected_breweries = df.copy()

# Filters
st.write("Apply filters:")

dynamic_filters = DynamicFilters(df, filters=['state', 'city', 'brewery_type', 'postal_code', 'name'], filters_name = 'filters1')

dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')

selected_breweries = dynamic_filters.filter_df()

st.write("")
st.write("")

# Columns for metrics
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1,1,1,1,1,1,1,1))

# Metrics
with col1:
   tile = st.container(height=120)
   tile.metric(label=" 🍺 Total Breweries", value = selected_breweries.shape[0])

with col2: 
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='micro'].shape[0] < 1:
      tile.metric(label="🍺 Micro", value = 0)
   else:
      tile.metric(label=" 🍺 Micro", value = selected_breweries[selected_breweries['brewery_type']=='micro'].shape[0])
with col3:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='brewpub'].shape[0] < 1:
      tile.metric(label="🍺 Brewpub", value = 0)
   else:
       tile.metric(label="🍺 Brewpub", value = selected_breweries[selected_breweries['brewery_type']=='brewpub'].shape[0])

with col4:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='regional'].shape[0] < 1:
      tile.metric(label="🍺 Regional", value = 0)
   else:
       tile.metric(label="🍺 Regional", value = selected_breweries[selected_breweries['brewery_type']=='regional'].shape[0])

with col5:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='contract'].shape[0] < 1:
      tile.metric(label="🍺 Contract", value = 0)
   else:
      tile.metric(label="🍺 Contract", value = selected_breweries[selected_breweries['brewery_type']=='contract'].shape[0])

with col6:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='large'].shape[0] < 1:
      tile.metric(label="🍺 Large", value = 0)
   else:
      tile.metric(label="🍺 Large", value = selected_breweries[selected_breweries['brewery_type']=='large'].shape[0])

with col7:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='proprietor'].shape[0] < 1:
      tile.metric(label="🍺 Proprietor", value = 0)
   else:
      tile.metric(label="🍺 Proprietor", value = selected_breweries[selected_breweries['brewery_type']=='proprietor'].shape[0])

with col8:
   tile = st.container(height=120)
   if selected_breweries[selected_breweries['brewery_type']=='nano'].shape[0] < 1:
      tile.metric(label="🍺 Nano", value = 0)
   else:
      tile.metric(label="🍺 Nano", value = selected_breweries[selected_breweries['brewery_type']=='nano'].shape[0])

st.write("")
st.write("")

# Data Preview
with st.expander("Data Preview"):
    st.write("Hover over column name to display icons on the right for download, search, fullscreen") 
    st.write("Click columns names to sort")
    dynamic_filters.display_df()
    
st.write("")


# Columns for Graphs
col9, col10, col11 = st.columns((3,3,3))

# Graphs
with col9:
   fig_state = selected_breweries.groupby(['state'])\
            .agg(Total = ('brewery_type','count'))\
            .sort_values('Total',ascending=False) \
            .head(15)\
            .reset_index()
   fig = px.bar(fig_state,x = "Total", y = "state", 
   text='Total', orientation="h")
   fig.update_traces(textposition='outside', cliponaxis=False, marker_color = "#008000", selector=dict(type='bar'))
   fig.update_layout(yaxis=dict(autorange="reversed"), title_text="Breweries by State",width=350, height=600)
   fig.update_yaxes(type='category', title_text="State", automargin=True)
   st.plotly_chart(fig,use_container_width=True)

with col10:
   fig_data = selected_breweries.groupby(['postal_code'])\
            .agg(Total = ('brewery_type','count'))\
            .sort_values('Total',ascending=False) \
            .head(15)\
            .reset_index()
   fig = px.bar(fig_data,x = "Total", y = "postal_code", 
   text='Total', orientation="h")
   fig.update_traces(textposition='outside', cliponaxis=False, marker_color = "#008000", selector=dict(type='bar'))
   fig.update_layout(yaxis=dict(autorange="reversed"), title_text="Breweries by Zipcode",width=350, height=600)
   fig.update_yaxes(type='category', title_text="Zipcode", automargin=True)
   st.plotly_chart(fig,use_container_width=True)

with col11:
   fig_city = selected_breweries.groupby(['city'])\
            .agg(Total = ('brewery_type','count'))\
            .sort_values('Total',ascending=False) \
            .head(15)\
            .reset_index()
   fig = px.bar(fig_city,x = "Total", y = "city", 
   text='Total', orientation="h")
   fig.update_traces(textposition='outside', cliponaxis=False, marker_color = "#008000", selector=dict(type='bar'))
   fig.update_layout(yaxis=dict(autorange="reversed"), title_text="Breweries by City",width=350, height=600)
   fig.update_yaxes(type='category', title_text="City", automargin=True)
   st.plotly_chart(fig,use_container_width=True)


