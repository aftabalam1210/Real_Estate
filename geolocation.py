import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeopyError
import time

# Initialize geolocator
geolocator = Nominatim(user_agent="sector_lat_long_finder")

# Function to handle timeouts and fetch coordinates
def get_coordinates(place):
    if pd.isna(place) or place.strip() == "":
        return pd.Series([None, None])

    # Optional: add city and country for accuracy
    full_place = f"{place}, Gurgaon, India"
    print(f"Looking up: {full_place}")

    try:
        location = geolocator.geocode(full_place)
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            print(f"Location not found: {full_place}")
            return pd.Series([None, None])
    except GeocoderTimedOut:
        print("Timeout. Retrying...")
        time.sleep(1)
        return get_coordinates(place)
    except GeopyError as e:
        print(f"Geocoding error for {place}: {e}")
        return pd.Series([None, None])

# Load your CSV
try:
    df = pd.read_csv("gurgaon_properties_missing_value_imputation.csv")
    print("CSV loaded successfully.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Apply geocoding on 'sector' column
print("Starting geocoding...")

df[['lat', 'long']] = df['sector'].apply(get_coordinates)

# Optional: Pause to avoid being rate-limited
time.sleep(1)

# Save to a new CSV with lat/long columns
output_path = "output_with_coordinates.csv"
df.to_csv(output_path, index=False)
print(f"Geocoding completed and saved to {output_path}")
