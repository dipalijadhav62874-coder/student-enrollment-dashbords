import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="Student Enrollment Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Load data
df = pd.read_csv("student_data.csv")

# -----------------------------
# Data Cleaning
# -----------------------------

# Count missing values
missing_values = df.isnull().sum().sum()

# Remove duplicate records
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

st.sidebar.success("✅ Data Cleaning Completed")

st.sidebar.write("Duplicate Records Removed:", duplicates)
st.sidebar.write("Missing Values Found:", missing_values)

# Title
st.title("🎓 Student Enrollment Data Analysis Dashboard")
st.caption("Student enrollment analysis using Python, Pandas and Plotly")

# Sidebar
st.sidebar.header("🔍 Filters")

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

gender = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(df["Gender"].unique().tolist())
)

year = st.sidebar.selectbox(
    "Academic Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)

# Apply filters
filtered_df = df.copy()

if department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == department
    ]

if gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == gender
    ]

if year != "All":
    filtered_df = filtered_df[
        filtered_df["Year"] == year
    ]
    
# student search
st.subheader("🔎 Search Student")

search = st.text_input(
    "Enter Student Name or Student ID"
)

if search:
    filtered_df = filtered_df[
        filtered_df["Name"].astype(str).str.contains(
            search, case=False, na=False
        )
        |
        filtered_df["Student_ID"].astype(str).str.contains(
            search, case=False, na=False
        )
    ]

st.info(f"Students found: {len(filtered_df)}")

# Dashboard metrics
st.subheader("📊 Student Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", len(filtered_df))

with col2:
    st.metric("Departments", filtered_df["Department"].nunique())

with col3:
    st.metric(
        "Male Students",
        len(filtered_df[filtered_df["Gender"] == "Male"])
    )

with col4:
    st.metric(
        "Female Students",
        len(filtered_df[filtered_df["Gender"] == "Female"])
    )

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏫 Department-wise Enrollment")

    dept_data = filtered_df["Department"].value_counts().reset_index()
    dept_data.columns = ["Department", "Students"]

    fig1 = px.bar(
        dept_data,
        x="Department",
        y="Students",
        text="Students",
        title="Students by Department"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("👨‍🎓 Gender-wise Enrollment")

    gender_data = filtered_df["Gender"].value_counts().reset_index()
    gender_data.columns = ["Gender", "Students"]

    fig2 = px.pie(
        gender_data,
        names="Gender",
        values="Students",
        title="Male vs Female Students"
    )

    st.plotly_chart(fig2, use_container_width=True)

# More charts
col3, col4 = st.columns(2)

with col3:
    st.subheader("📚 Year-wise Enrollment")

    year_data = filtered_df["Year"].value_counts().reset_index()
    year_data.columns = ["Year", "Students"]

    fig3 = px.bar(
        year_data,
        x="Year",
        y="Students",
        text="Students",
        title="Students by Academic Year"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📋 Category-wise Enrollment")

    category_data = filtered_df["Category"].value_counts().reset_index()
    category_data.columns = ["Category", "Students"]

    fig4 = px.pie(
        category_data,
        names="Category",
        values="Students",
        title="Students by Category"
    )

    st.plotly_chart(fig4, use_container_width=True)

# Student table
st.subheader("📄 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Student table
st.subheader("📄 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download filtered data
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Student Data",
    data=csv,
    file_name="filtered_student_data.csv",
    mime="text/csv"
)

# Student Details

st.subheader("📄 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# Download Button

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Student Data",
    data=csv,
    file_name="filtered_student_data.csv",
    mime="text/csv",
    key="download_student_data"
)