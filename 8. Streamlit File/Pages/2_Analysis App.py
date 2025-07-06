import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Ensure numeric columns
cols_to_convert = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
new_df[cols_to_convert] = new_df[cols_to_convert].apply(pd.to_numeric, errors='coerce')
new_df.dropna(subset=cols_to_convert + ['sector'], inplace=True)

# Group by sector
group_df = new_df.groupby('sector')[cols_to_convert].mean()

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                        mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)
st.plotly_chart(fig, use_container_width=True)

# ----------------------- UPDATED WORDCLOUD SECTION -------------------------
st.header('Features Wordcloud (Based on Sector)')

# Load pre-aggregated sector_features.csv
sector_features_df = pd.read_csv('datasets/sector_features.csv')

# Sector selection dropdown
wordcloud_sector_options = sector_features_df['sector'].unique().tolist()
wordcloud_sector_options.insert(0, 'overall')
selected_wordcloud_sector = st.selectbox('Select Sector for Word Cloud', wordcloud_sector_options)

# Extract feature text for word cloud
if selected_wordcloud_sector == 'overall':
    all_features = ' '.join(sector_features_df['features'].dropna().tolist())
else:
    row = sector_features_df[sector_features_df['sector'] == selected_wordcloud_sector]
    all_features = row['features'].values[0] if not row.empty else ''

# Generate and display WordCloud
if all_features.strip():
    wordcloud = WordCloud(
        width=800,
        height=800,
        background_color='black',
        stopwords=set(['s', 'and', 'or', 'the', 'a', 'an', 'is', 'for', 'with', 'property', 'in', 'are', 'this']),
        min_font_size=10
    ).generate(all_features)

    fig_wc, ax_wc = plt.subplots(figsize=(8, 8), facecolor='black')
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis("off")
    fig_wc.tight_layout(pad=0)
    st.pyplot(fig_wc)
else:
    st.write("No features found for the selected sector. Word cloud cannot be generated.")
# ----------------------- END OF UPDATED SECTION -------------------------

st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat', 'house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
st.plotly_chart(fig3, use_container_width=True)

st.header('Side by Side Distplot for property type')

fig4 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'], label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig4)
