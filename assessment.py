import streamlit as st
import pandas as pd
from datetime import datetime

st.title("CSV Standardization Tool")

if "step" not in st.session_state:
    st.session_state.step = 1

if st.session_state.step == 1:
    file = st.file_uploader("Upload CSV File", type="csv")

    if file:
        st.session_state.df = pd.read_csv(file)
        st.success("File uploaded successfully")
        st.dataframe(st.session_state.df.head(100))
    if st.button("Next"):
        if "df" in st.session_state:
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please upload CSV file first")
            
elif st.session_state.step == 2:
    df = st.session_state.df
    cols = df.columns
    st.subheader("Map Columns")
    user_id = st.selectbox("Select User_ID Column", cols)
    trans_date = st.selectbox("Select Transaction_Date Column", cols)
    amount = st.selectbox("Select Amount Column", cols)

    if st.button("Next"):
        st.session_state.df = pd.DataFrame({
            "User_ID": df[user_id],
            "Transaction_Date": df[trans_date],
            "Amount": df[amount]
        })
        st.session_state.step = 3
        st.rerun()
    if st.button("Back"):
        st.session_state.step = 1
        st.rerun()

elif st.session_state.step == 3:
    df = st.session_state.df
    st.subheader("Validation and Transformation")
    st.dataframe(df.head(100))
    if pd.to_numeric(df["Amount"], errors="coerce").isna().any():
        st.error("Amount column has invalid values")
    else:
        st.success("Amount column is valid")
    if pd.to_datetime(df["Transaction_Date"], errors="coerce").isna().any():
        st.error("Date column has invalid values")
    else:
        st.success("Date column is valid")
    if st.checkbox("Remove duplicate rows"):
        df = df.drop_duplicates()
    if st.checkbox("Fill empty values with 0"):
        df = df.fillna(0)
    if st.checkbox("Create Adjusted Amount"):
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        tax = st.number_input("Enter Tax Multiplier", value=1.0)
        df["Adjusted_Amount"] = df["Amount"] * tax
    st.session_state.df = df

    if st.button("Next"):
        st.session_state.step = 4
        st.rerun()
    if st.button("Back"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 4:
    df = st.session_state.df
    st.subheader("Download Final File")
    st.dataframe(df.head(100))
    filename = "output_" + datetime.now().strftime("%H%M%S") + ".csv"
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name=filename,
        mime="text/csv"
    )
    if st.button("Back"):
        st.session_state.step = 3
        st.rerun()