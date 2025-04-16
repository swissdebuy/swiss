
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Herrenlose Grundstücke", layout="wide")

st.title("🔍 Herrenlose Grundstücke – Kanton Aargau (Testdaten)")

# Daten laden
@st.cache_data
def load_data():
    return pd.read_csv("herrenlose_parzellen_test.csv")

df = load_data()

# Filteroptionen
gemeinden = df["Gemeinde"].unique().tolist()
auswahl = st.multiselect("Gemeinde auswählen", gemeinden, default=gemeinden)

gefiltert = df[df["Gemeinde"].isin(auswahl)]

st.write("Gefundene Grundstücke:", len(gefiltert))
st.dataframe(gefiltert, use_container_width=True)

# Karte anzeigen
st.subheader("📍 Karte")
m = folium.Map(location=[47.39, 8.05], zoom_start=9)
for _, row in gefiltert.iterrows():
    lat, lon = map(float, row["Koordinaten"].split(","))
    folium.Marker(
        location=[lat, lon],
        tooltip=f"{row['Gemeinde']} – Parzelle {row['Parzelle']}",
        popup=row["Status"]
    ).add_to(m)

st_folium(m, width=700, height=500)

# Download
st.subheader("📥 Exportieren")
st.download_button("⬇ CSV herunterladen", gefiltert.to_csv(index=False), "herrenlose_parzellen.csv", "text/csv")
