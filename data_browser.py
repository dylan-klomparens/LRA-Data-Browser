import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and dataset info
st.title("This is the embedded webpage")
st.markdown("## [Sample dataset](https://data.mendeley.com/datasets/kb36mjdmsn/1) was sourced from Mendeley.")
st.divider()

# Load dataset
df = pd.read_csv("data.csv")

# Fill missing values in 'age onset' with 0
df["age onset (int)"] = df["age onset"].fillna(0).astype(int)

# --- Bar Chart: Age of Onset ---
st.header("Distribution of Lupus Onset Ages")

# Get min and max age (excluding 0 to define the true range)
min_age = df.loc[df["age onset (int)"] > 0, "age onset (int)"].min()
max_age = df["age onset (int)"].max()

# Include age 0 as well
all_ages = list(range(0, max_age + 1))  # from 0 to max age inclusive

# Count all ages and fill missing with 0
age_counts = df["age onset (int)"].value_counts().sort_index()
age_counts = age_counts.reindex(all_ages, fill_value=0)

# Convert x-axis labels to strings, renaming 0 as "Unknown"
age_labels = ["Unknown" if age == 0 else str(age) for age in age_counts.index]

# Plot using matplotlib
fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.bar(age_labels, age_counts.values)
ax1.set_xlabel("Age of Onset")
ax1.set_ylabel("Number of Individuals")
plt.xticks(rotation=90)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

st.pyplot(fig1)

# --- Pie Chart: Gender Distribution ---
st.header("Gender Distribution")

gender_counts = df["Gender"].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax2.axis("equal")

st.pyplot(fig2)
