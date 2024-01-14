import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import zipfile
import os

def download_and_extract_zip(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall("temp")
            # Assuming there's only one file in the zip
            extracted_file = zip_ref.namelist()[0]
            return pd.read_csv(f"temp/{extracted_file}", delimiter='#', on_bad_lines='skip', engine='python')
    except Exception as e:
        st.error(f"Błąd pobierania pliku: {e}")
        return None

def filter_csv(df, columns_to_remove, search_column, keywords):
    try:
        if search_column in df.columns:
            partial_keywords = [kw.strip('[]') for kw in keywords if not kw.startswith('[') or not kw.endswith(']')]
            exact_keywords = [kw.strip('[]') for kw in keywords if kw.startswith('[') and kw.endswith(']')]

            df = df[df[search_column].apply(lambda x: 
                any(partial_keyword in str(x) for partial_keyword in partial_keywords) or
                str(x) in exact_keywords
            )]
            st.success(f"Liczba rekordów po zakończonym filtrowaniu: {len(df)}")
        else:
            st.error(f"Kolumna '{search_column}' nie została znaleziona w pliku.")

        filtered_df = df.drop(columns=columns_to_remove, errors='ignore')
        return filtered_df
    except Exception as e:
        st.error(f"Błąd filtrowania danych: {e}")
        return pd.DataFrame()

def main():
    st.title("CSV Filtering Application")

    region_urls = {
        "Dolnośląskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_dolnoslaskie.zip",
        "Kujawsko Pomorskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_kujawsko-pomorskie.zip",
        "Lubelskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_lubelskie.zip",
        "Lubuskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_lubuskie.zip",
        "Łódzkie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_lodzkie.zip",
        "Mazowieckie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_mazowieckie.zip",
        "Małopolskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_malopolskie.zip",
        "Opolskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_opolskie.zip",
        "Podkarpackie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_podkarpackie.zip",
        "Podlaskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_podlaskie.zip",
        "Pomorskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_pomorskie.zip",
        "Śląskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_slaskie.zip",
        "Świętokrzyskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_swietokrzyskie.zip",
        "Warmińsko-Mazurskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_warminsko-mazurskie.zip",
        "Wielkopolskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_wielkopolskie.zip",
        "Zachodniopomorskie": "https://wyszukiwarka.gunb.gov.pl/pliki_pobranie/wynik_zachodniopomorskie.zip"
        
        }

    # Selection box for regions
    selected_region = st.selectbox("Wybierz region", [''] + list(region_urls.keys()))

    # File uploader
    uploaded_file = st.file_uploader("lub wgraj własny plik CSV (kolumny muszą być rozdzielane #)", type='csv')

    df = None
    # Determine which file to use
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter='#', on_bad_lines='skip', engine='python')
    elif selected_region:
        df = download_and_extract_zip(region_urls[selected_region])

    if df is not None:
        st.write("Surowy plik CSV:")
        st.dataframe(df)

        # Allow user to select columns to remove from a multiselect box
        all_columns = df.columns.tolist()
        columns_to_remove = st.multiselect("Kolumny do usunięcia", all_columns)

        search_column = st.selectbox("Kolumna filtrująca", options=all_columns)
        keywords = st.text_input("Słowa kluczowe (rozdzielone przecinkami)").split(',')

        # Filter button
        if st.button("Filtruj"):
            filtered_df = filter_csv(df, columns_to_remove, search_column, keywords)
            if not filtered_df.empty:
                st.write("Przefiltrowane dane:")
                st.dataframe(filtered_df)
            else:
                st.error("Brak danych do wyświetlenia.")
    else:
        st.warning("Wybierz region lub wgraj własny plik CSV.")

if __name__ == "__main__":
    main()