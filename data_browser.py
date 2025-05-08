import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Lupus Research Alliance Data Browser")

# Load the data
df = pd.read_csv("data.csv")

# Drop missing values for age onset
df_clean = df.dropna(subset=["age onset"])

# --- Bar Chart: Age of Onset ---
st.header("Age of Onset of Lupus")

# Round age onset to integers for better histogram binning
df_clean["age onset (int)"] = df_clean["age onset"].astype(int)

# Use Streamlit's bar_chart for histogram-like visualization
age_counts = df_clean["age onset (int)"].value_counts().sort_index()
st.bar_chart(age_counts)

# --- Pie Chart: Gender Distribution ---
st.header("Gender Distribution")

# Prepare gender data
gender_counts = df["Gender"].value_counts()

# Plot pie chart using matplotlib
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis("equal")  # Equal aspect ratio ensures a perfect circle

st.pyplot(fig)
