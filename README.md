# Skrypt Filtracji CSV

Ten skrypt zapewnia funkcje przetwarzania i filtrowania plików CSV na podstawie różnych kryteriów zdefiniowanych w pliku konfiguracyjnym. Poniżej przedstawiamy przegląd jego głównych funkcji:

## Funkcje

1. **Usuwanie Kolumn**: Skrypt może usuwać określone kolumny z plików CSV. Kolumny do usunięcia są zdefiniowane w pliku konfiguracyjnym (`config.txt`).

2. **Filtrowanie Wierszy na Podstawie Słów Kluczowych**:

   - Skrypt może filtrować wiersze na podstawie obecności określonych słów kluczowych w określonej kolumnie.
   - Obsługuje dwa rodzaje dopasowania słów kluczowych:
     - **Częściowe Dopasowanie**: Jeśli słowo kluczowe jest wymienione bez nawiasów kwadratowych, skrypt szuka tego słowa kluczowego jako podciągu w określonej kolumnie.
     - **Dokładne Dopasowanie**: Jeśli słowo kluczowe jest zamknięte w nawiasach kwadratowych (np. `[słowo_kluczowe]`), skrypt sprawdza, czy istnieje dokładne dopasowanie w określonej kolumnie.

3. **Plik Konfiguracyjny**: Plik `config.txt` służy do określania kolumn do usunięcia, kolumny do wyszukiwania słów kluczowych oraz słów kluczowych do filtrowania.

Format pliku konfiguracyjnego jest następujący:
kolumny_do_usunięcia = ['kolumna1', 'kolumna2', ...] kolumna_wyszukiwania_danych = 'nazwa_kolumny' słowa_kluczowe = ['częściowe_słowo_kluczowe1', '[dokładne_słowo_kluczowe1]', 'częściowe_słowo_kluczowe2', ...]

4. **Solidne Obsługiwanie Błędów**: Skrypt zawiera obsługę błędów dla różnych scenariuszy, takich jak brakujące pliki, nieprawidłowe typy danych i błędy składni w pliku konfiguracyjnym.

5. **Generowanie Wyników**: Przefiltrowane pliki CSV są zapisywane z prefiksem `filtered_` w tym samym katalogu co oryginalne pliki.

## Użycie

Aby użyć skryptu, umieść pliki CSV w wyznaczonym folderze, utwórz i skonfiguruj plik `config.txt` zgodnie z powyższym formatem, a następnie uruchom skrypt. Skrypt przetworzy wszystkie pliki CSV w folderze zgodnie z konfiguracją.

Teraz dostępne są dwie główne metody użytkowania skryptu:

### W Terminalu

Uruchom `terminal_app.py` w terminalu za pomocą `python terminal_app.py`, aby przetwarzać pliki CSV zgodnie z konfiguracją w trybie tekstowym.

### Za Pomocą Streamlit

Uruchom `streamlit_app.py` za pomocą `streamlit run streamlit_app.py`, aby uruchomić aplikację internetową, która umożliwia interaktywne filtrowanie plików CSV poprzez lokalny serwer.
