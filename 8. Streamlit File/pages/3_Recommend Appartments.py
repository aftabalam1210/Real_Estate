import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="🏢 Apartment Recommender", layout="wide")

# Load data
location_df = pickle.load(open('8. Streamlit File/datasets/location_distance.pkl', 'rb'))
cosine_sim1 = pickle.load(open('8. Streamlit File/datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('8. Streamlit File/datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('8. Streamlit File/datasets/cosine_sim3.pkl', 'rb'))

# Title and description
st.title("🏙️ Smart Apartment Recommender")
st.markdown("Find similar properties or discover places nearby within a set radius.")

# -------------------------------
# Recommendation Function
# -------------------------------
def recommend_properties_with_scores(property_name, top_n=5):
    try:
        # Combine similarity matrices
        cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3

        # Get the similarity scores
        sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get top N results (excluding the property itself at index 0)
        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
        top_properties = location_df.index[top_indices].tolist()

        # Return as a DataFrame
        recommendations_df = pd.DataFrame({
            '🏠 Property Name': top_properties,
            '📈 Similarity Score': [round(score, 3) for score in top_scores]
        })

        return recommendations_df

    except KeyError:
        st.error(f"❌ Property '{property_name}' not found.")
        return pd.DataFrame()

# -------------------------------
# Radius Search Module
# -------------------------------
with st.expander("📍 Find Nearby Properties by Radius"):
    col1, col2 = st.columns(2)

    with col1:
        selected_location = st.selectbox(
            'Choose Reference Location:',
            sorted(location_df.columns.to_list())
        )

    with col2:
        radius = st.number_input('Enter radius (in kms):', min_value=0.0, value=1.0, step=0.5)

    # 🔍 Button to search nearby
    if st.button("🔍 Search Nearby"):
        if selected_location in location_df.columns:
            result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()

            if result_ser.empty:
                st.warning("No properties found within the selected radius.")
            else:
                st.markdown(f"### 🗺️ Top 5 Properties within {int(radius)} km of **{selected_location}**:")
                top_results = result_ser.head(5)  # limit to top 5 closest

                with st.container():
                    for key, value in top_results.items():
                        st.markdown(f"- **{key}** — {round(value / 1000, 2)} km")
        else:
            st.error("Selected location not found in the dataset.")

# -------------------------------
# Recommender Module
# -------------------------------
st.markdown("---")
st.header("🏢 Recommend Similar Apartments")

selected_apartment = st.selectbox(
    'Select an apartment to get recommendations:',
    sorted(location_df.index.to_list())
)

if st.button("🎯 Recommend"):
    recommendation_df = recommend_properties_with_scores(selected_apartment, top_n=5)

    if not recommendation_df.empty:
        st.success(f"Showing top 5 properties similar to **{selected_apartment}**")
        st.dataframe(recommendation_df.head(5), use_container_width=True)
