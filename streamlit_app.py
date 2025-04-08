import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Add logo
st.image("logo.png", use_container_width=True)  # Updated for compatibility

# File uploader
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

df = load_data(uploaded_file)

if df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")

    if "Life Status" in df.columns:
        life_status_filter = st.sidebar.multiselect("Select Life Status", sorted(df["Life Status"].dropna().unique()))
        if life_status_filter:
            df = df[df["Life Status"].isin(life_status_filter)]
    print('\n')
    if "Sex" in df.columns:
        sex_filter = st.sidebar.multiselect("Select Sex", sorted(df["Sex"].dropna().unique()))
        if sex_filter:
            df = df[df["Sex"].isin(sex_filter)]
    print('\n')
    if "Colony Name" in df.columns:
        colony_filter = st.sidebar.multiselect("Select Colony Name", sorted(df["Colony Name"].dropna().unique()))
        if colony_filter:
            df = df[df["Colony Name"].isin(colony_filter)]
    print('\n')
    if "All Cohorts" in df.columns:
        cohort_options = sorted(df["All Cohorts"].dropna().unique()) + ["Not in any Cohort"]
        cohort_filter = st.sidebar.multiselect("Select All Cohorts", cohort_options)
        if cohort_filter:
            if "Not in any Cohort" in cohort_filter:
                df = df[df["All Cohorts"].isna() | df["All Cohorts"].isin(cohort_filter)]
            else:
                df = df[df["All Cohorts"].isin(cohort_filter)]
    print('\n')
    if "Current Mating" in df.columns:
        mating_filter = st.sidebar.multiselect("Select Mating Status", ["Mating", "Not Mating"])
        if "Mating" in mating_filter and "Not Mating" not in mating_filter:
            df = df[df["Current Mating"].notna() & (df["Current Mating"] != "")]
        elif "Not Mating" in mating_filter and "Mating" not in mating_filter:
            df = df[df["Current Mating"].isna() | (df["Current Mating"] == "")]

    # Display filtered data
    st.write("### Filtered Data", df)

    # Violin plot with individual sample points and median
    st.write("### Violin Plot")
    if "Colony Name" in df.columns and "Age (Weeks)" in df.columns:
        num_mice = len(df)
        strains = df["Colony Name"].nunique()
        min_age = df["Age (Weeks)"].min()
        real_max_age = df["Age (Weeks)"].max()
        max_age = real_max_age + 8  # Add a small buffer for y-axis only
        median_age = df["Age (Weeks)"].median()
        
        st.write(f"Filtered dataset includes {num_mice} mice across {strains} unique colonies, with ages ranging from {min_age} to {real_max_age} weeks (median age: {median_age} weeks).")
        
        fig, ax = plt.subplots(figsize=(7, 10))  # Adjusted plot size
        sns.violinplot(x="Colony Name", y="Age (Weeks)", data=df, inner=None, linewidth=1, width=0.1, ax=ax)  # Narrower violin plot

        # Ensure individual points are clearly visible
        sns.stripplot(x="Colony Name", y="Age (Weeks)", data=df, hue="Colony Name", palette="dark", marker="^", alpha=1, jitter=True, dodge=True, ax=ax)

        # Adding median lines
        medians = df.groupby("Colony Name")["Age (Weeks)"].median()
        for i, median in enumerate(medians):
            ax.hlines(y=median, xmin=i-0.1, xmax=i+0.1, colors='black', linestyles='solid', linewidth=2)

        ax.set_ylim(0, max_age)  # Set y-axis limit dynamically
        plt.xticks()  # rotation=45
        
        # Move the legend outside the plot
        legend = ax.legend(title="Colony Name", bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
        plt.setp(legend.get_texts(), fontsize='small')  # Adjust legend font size if needed
        
        st.pyplot(fig)
        
else:
    st.write("Please upload a CSV file to begin.")
