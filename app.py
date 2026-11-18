
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DataVision",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataVision")
st.subheader("Smart Data Analysis Dashboard")

st.write("Upload your data file and analyze it automatically.")

uploaded_file = st.file_uploader(
    "Upload Your File",
    type=["csv", "xlsx", "json"]
)

if uploaded_file is not None:

    try:
        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        elif file_name.endswith(".json"):
            df = pd.read_json(uploaded_file)

        st.success("File Uploaded Successfully!")

        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Data Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows", len(df))
        col2.metric("Total Columns", len(df.columns))
        col3.metric("Duplicate Rows", int(df.duplicated().sum()))

        st.subheader("Statistical Analysis")

        st.write(df.describe(include="all"))

        st.subheader("Missing Values")
        st.write(df.isnull().sum())

        st.divider()

        st.header("📈 Graph Studio")

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        all_columns = df.columns.tolist()

        if numeric_columns:

            graph_type = st.selectbox(
                "Choose Graph Type",
                ["Bar", "Line", "Scatter", "Histogram"]
            )

            x_axis = st.selectbox(
                "Select X-Axis",
                all_columns
            )

            y_axis = st.selectbox(
                "Select Y-Axis",
                numeric_columns
            )

            if graph_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis)

            elif graph_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis)

            elif graph_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis)

            else:
                fig = px.histogram(df, x=y_axis)

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("No numeric columns found for graphs.")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV, Excel or JSON file to begin.")
