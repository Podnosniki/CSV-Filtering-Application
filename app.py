import streamlit as st
import pandas as pd
import os

def filter_csv(df, columns_to_remove, search_column, keywords):
    try:
        if search_column in df.columns:
            partial_keywords = [kw.strip('[]') for kw in keywords if not kw.startswith('[') or not kw.endswith(']')]
            exact_keywords = [kw.strip('[]') for kw in keywords if kw.startswith('[') and kw.endswith(']')]

            df = df[df[search_column].apply(lambda x: 
                any(partial_keyword in str(x) for partial_keyword in partial_keywords) or
                str(x) in exact_keywords
            )]
            st.success(f"Number of rows after keyword filtering: {len(df)}")
        else:
            st.error(f"Column '{search_column}' not found in the DataFrame.")

        filtered_df = df.drop(columns=columns_to_remove, errors='ignore')
        return filtered_df
    except Exception as e:
        st.error(f"Error processing DataFrame: {e}")
        return pd.DataFrame()

def main():
    st.title("CSV Filtering Application")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter='#', on_bad_lines='skip', engine='python')
        st.write("Initial DataFrame:")
        st.dataframe(df)

        # Allow user to select columns to remove from a multiselect box
        all_columns = df.columns.tolist()
        columns_to_remove = st.multiselect("Select Columns to Remove", all_columns)

        search_column = st.selectbox("Select Search Column", options=all_columns)
        keywords = st.text_input("Keywords (comma-separated)").split(',')

        # Filter button
        if st.button("Filter CSV"):
            filtered_df = filter_csv(df, columns_to_remove, search_column, keywords)
            if not filtered_df.empty:
                st.write("Filtered DataFrame:")
                st.dataframe(filtered_df)
            else:
                st.error("No data left after filtering. Adjust your filters and try again.")

if __name__ == "__main__":
    main()
