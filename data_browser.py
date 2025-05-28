import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

st.title("LRA data browser embedded dashboard")

st.divider()

df = pd.read_csv("data.csv")

# Pie chart: gender distribution
st.header("Gender Distribution")
gender_counts = df["sex_at_birth"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=90)
ax2.axis("equal")
st.pyplot(fig2)

st.divider()

# Histogram of SLEDAI 2K scores with Gaussian KDE
st.header("SLEDAI 2K scores")
with st.expander("Introductory information"):
	st.markdown(f"""
## What Is It?
The SLEDAI is a clinical tool used by doctors to measure disease activity in patients with systemic lupus erythematosus (SLE), commonly known as lupus.
## How Does It Work?
* SLEDAI assigns numerical scores to a list of symptoms and laboratory findings seen in lupus, including things like seizures, arthritis, rash, and low blood counts.
* Each manifestation is weighted, and the total score gives an overall measure of lupus activity over the past 10 days.
* Higher scores indicate more active disease.
## What’s It Used For?
* To monitor changes in lupus activity over time.
* To help guide treatment decisions.
* To assess response to therapy in both clinical practice and research studies.
	""")
slicc_indexes = df["latest SLEDAI 2K score"].dropna()
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(slicc_indexes, bins=15, edgecolor="black", alpha=0.7, label="Participant count")
density = gaussian_kde(slicc_indexes)
xs = np.linspace(slicc_indexes.min(), slicc_indexes.max(), 200)
ax.plot(xs, density(xs) * len(slicc_indexes) * (slicc_indexes.max() - slicc_indexes.min()) / 15, color="red", lw=2, label="Gaussian Kernel Density Estimation")
ax.set_xlabel("Latest SLEDAI 2K Score")
ax.set_ylabel("Participant count")
ax.set_title("Histogram of SLEDAI 2K Scores")
ax.legend()
st.pyplot(fig)
with st.expander("Additional details"):
	st.markdown(f"""
	Number of valid SLEDAI scores: {len(slicc_indexes)}

	This figure presents the distribution of SLEDAI 2K scores in our lupus cohort, visualized with both a histogram and an overlaid Gaussian kernel density estimate (KDE). The Gaussian KDE provides a non-parametric, smooth estimate of the underlying probability density function for disease activity scores, independent of binning artifacts inherent to histograms.

	Notably, the KDE highlights the presence and position of peaks (modes) and the overall shape of the distribution, allowing for more precise assessment of central tendency, spread, and potential skewness or multimodality in the SLEDAI 2K data. This method offers improved resolution in identifying subpopulations or atypical distributions that may be clinically relevant but obscured in binned representations.
	""")

st.divider()

# Histogram of SLICC Damage Index scores with Gaussian KDE
st.header("SLICC Damage Index scores")
with st.expander("Introductory information"):
	st.markdown(f"""
## What Is It?

The SLICC Damage Index is a tool used to measure permanent organ damage in lupus patients, regardless of its cause (from the disease or from its treatment).

## How Does It Work?

The SLICC Damage Index tallies irreversible damage that has occurred since the onset of lupus, in organs like the kidneys, heart, skin, nervous system, and others. Damage must be present for at least 6 months to be counted. Each type of damage has a point value, and the total score reflects the cumulative burden of organ damage.

## What’s It Used For?
* To track the long-term impact of lupus and its treatments.
* To predict outcomes and prognosis (higher damage index = greater risk for poor outcomes).
* For research to compare damage across populations.

## Example of Damage Assessed
* Renal failure
* Stroke
* Cardiovascular disease
* Avascular necrosis (bone damage)
* Cataracts
* Diabetes (from steroid use)
	""")
slicc_indexes = df["latest SLICC damage index"].dropna()
fig, ax = plt.subplots(figsize=(8, 5))
# Calculate bins based on observed data (e.g., 0 to max, integer bins)
min_val = int(slicc_indexes.min())
max_val = int(slicc_indexes.max())
bins = np.arange(min_val, max_val + 2) - 0.5  # Center bars on integers

# Plot histogram
ax.hist(slicc_indexes, bins=bins, edgecolor="black", alpha=0.7)

# Set x-ticks to integer values under bars
ax.set_xticks(np.arange(min_val, max_val + 1))
ax.set_xlabel("Latest SLICC damage index")
ax.set_ylabel("Participant count")
ax.set_title("Histogram of SLICC Damage Indexes")
st.pyplot(fig)

with st.expander("Additional details"):
	st.markdown(f"""
	Number of valid SLICC damage indexes: {len(slicc_indexes)}

	This figure presents the distribution of the most recent SLICC damage indexes in our lupus cohort, visualized with a histogram.
	""")

st.divider()

st.header("Cohort")

cohort_counts = df["cohort"].value_counts()
fig, ax = plt.subplots()
ax.pie(cohort_counts, labels=cohort_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

st.divider()

st.header("Waterfall selection")

with st.expander("Introduction and usage instructions"):
	st.markdown(f"This waterfall chart visually summarizes the sequential attrition of the study cohort as increasingly specific inclusion criteria are applied. Each bar represents the remaining participant count after implementing a particular filter, which can be: sex at birth, race, ethnicity, cohort, disease activity (SLEDAI), organ damage (SLICC), and medication use. This allows you to see sample size reduction at each step, highlighting the effect of individual and combined eligibility criteria on cohort composition.")

# --- Filter options ---
drug_cols = [
	'abatacept', 'anifrolumab-fnia', 'azathioprine', 'belimumab', 'chloroquine',
	'cyclosporine', 'cyclophosphamide', 'dapsone', 'hydroxychloroquine',
	'leflunomide', 'methotrexate', 'methylprednisolone', 'mycophenolate mofetil',
	'mycophenolic acid', 'prednisone', 'rituximab', 'tacrolimus',
	'voclosporine', 'triamcinolone', 'other drugs'
]

# 1. Sex at birth
sex = st.selectbox("Sex at birth", options=['All'] + sorted(df['sex_at_birth'].dropna().unique().tolist()))
# 2. Race
race = st.selectbox("Race", options=['All'] + sorted(df['race'].dropna().unique().tolist()))
# 3. Ethnicity
ethnicity = st.selectbox("Ethnicity", options=['All'] + sorted(df['ethnicity'].dropna().unique().tolist()))
# 4. Cohort
cohort = st.selectbox("Cohort", options=['All'] + sorted(df['cohort'].dropna().unique().tolist()))
# 5. SLEDAI (range)
sledaicol = [col for col in df.columns if "SLEDAI" in col and "score" in col][0]
sld_min, sld_max = int(df[sledaicol].min()), int(df[sledaicol].max())
sledai_range = st.slider("SLEDAI 2K score range", min_value=sld_min, max_value=sld_max, value=(sld_min, sld_max))
# 6. SLICC (range)
slicccol = [col for col in df.columns if "SLICC" in col and "damage index" in col][0]
slc_min, slc_max = int(df[slicccol].min()), int(df[slicccol].max())
slicc_range = st.slider("SLICC damage index range", min_value=slc_min, max_value=slc_max, value=(slc_min, slc_max))
# 7. Drugs (multiselect)
drug_selection = st.multiselect("On which medications? (must be on ALL selected)", options=drug_cols)

# --- Waterfall Logic ---
counts = []
labels = []

df_current = df.copy()
# 1. All
counts.append(len(df_current))
labels.append("All participants")

# 2. Sex at birth
if sex != 'All':
	df_current = df_current[df_current['sex_at_birth'] == sex]
	labels.append(f"Sex: {sex}")
	counts.append(len(df_current))

# 3. Race
if race != 'All':
	df_current = df_current[df_current['race'] == race]
	labels.append(f"Race: {race}")
	counts.append(len(df_current))

# 4. Ethnicity
if ethnicity != 'All':
	df_current = df_current[df_current['ethnicity'] == ethnicity]
	labels.append(f"Ethnicity: {ethnicity}")
	counts.append(len(df_current))

# 5. Cohort
if cohort != 'All':
	df_current = df_current[df_current['cohort'] == cohort]
	labels.append(f"Cohort: {cohort}")
	counts.append(len(df_current))

# 6. SLEDAI range
df_current = df_current[(df_current[sledaicol] >= sledai_range[0]) & (df_current[sledaicol] <= sledai_range[1])]
labels.append(f"SLEDAI: {sledai_range[0]}–{sledai_range[1]}")
counts.append(len(df_current))

# 7. SLICC range
df_current = df_current[(df_current[slicccol] >= slicc_range[0]) & (df_current[slicccol] <= slicc_range[1])]
labels.append(f"SLICC: {slicc_range[0]}–{slicc_range[1]}")
counts.append(len(df_current))

# 8. Drugs
if drug_selection:
	for drug in drug_selection:
		df_current = df_current[df_current[drug] > 0]
		labels.append(f"On {drug}")
		counts.append(len(df_current))

# --- Plot Waterfall ---
fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.bar(range(len(counts)), counts, color='deepskyblue', edgecolor='black')
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, rotation=22, ha='right')
ax.set_ylabel("Participant Count")
ax.set_title("Cohort Size After Each Filter (Waterfall Plot)")
for i, c in enumerate(counts):
	ax.text(i, c + max(counts)*0.015, str(c), ha='center', va='bottom')
# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)
