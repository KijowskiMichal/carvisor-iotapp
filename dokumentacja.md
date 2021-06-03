# CarVisor Moduł IoT

## Moduły:

#### - Main
    Jest to moduł początkowy programu, wywołuje on pozostałe moduły
#### - API
    Moduł ten zarządza komunikacją z serwerem oraz odbiera i przesyła dane
    na/z serwera. 
#### - Config
    Moduł do odbierania, zmiany i propagowania opcji konfiguracyjnych dla
    urządzenia
#### - OBD
    Moduł ten zarządza połączeniem urządzenia IoT z interfejsem OBD
#### - Send
    Moduł służący do przygotowania danych do przesłania na serwer

## Funkcje modułów

### API

    start_session
    Funkcja służaca do rozpoczęcia sesji z serwerem
####
    check_authorization
    Funkcja wysyłająca zapytanie do serwera o podanie statusu autoryzacji
####
    get_config_from_server
    Funkcja wysyłająca zapytanie do serwera o podanie aktualnej 
    konfiguracji dla urządzenia
####
    send_data_to_server
    Funkcja wysyłająca dane(obd, gps, time) na serwer
####
    start_track
    Funkcja wysyłająca na serwer informacje o rozpoczęciu trasy
####
    logout
    Funkcja służąca do zamknięcia sesji z serwerem

### Config
    create_new_config
    Funkcja tworząca nowy plik konfiguracyjny w przypadku
    braku takiego pliku
####
    check_server_credentials
    Funkcja sprawdzająca czy plik konfiguracyjny posiada konfiguracje
####
    section_returner
    Funkcja zwracająca zadaną sekcje z pliku konfiguracyjnego
####
    get_config_from_server
    Funkcja wysyłająca żądanie pobrania konfiguracji
    dla urządzeniada modułu API 
####
    return_send_interval
    Funkcja zwracająca częstotliwość wysyłania danych na serwer
####
    return_API
    Funkcja zwracająca obiekt API dla pozostałych modułów
### Main
    start_logging
    Funkcja rozpoczynająca logowanie działania aplikacji
####
    init_obd
    Funkcja rozpoczynająca połączenie z pojazdem
####
    start_obd_reading
    Funkcja rozpoczynająca odczyt z interfejsu OBD
####
    server_unreachable_handler
    Funkcja do obsługi aplikacji w przypadku braku połączenia z serwerem
### OBD
    logging
    Funkcja określająca wyświetlanie logów OBD o danej ważności
####
    start_read
    Funkcja dodająca parametry do odczytu przez interfejs OBD
####
    check_DTC_codes
    Funkcja sprawdzająca czy są kody usterek po stronie pojazdu
####
    check_supported_commands
    Funkcja zwracająca liste wspieranych parametrów przez interfejs OBD
### Send
    pack
    Funkcja pakująca dane dostarczone przez moduł OBD
####
    get_new_timestamp
    Funkcja pobierająca nowy timestamp na potrzeby kolejnej iteracji
####
    new_iteration
    Funkcja czyszcząca zmienne dla następnej iteracji danych
####
    prepare_to_send
    Funkcja przygotowująca dane do przesłania na serwer przy pomocy modułu API
---
# Testy

- Sprawdzanie czy dane z modułu send są poprawnie przesyłane do modułu API
- Sprawdzanie połączenia z serwerem
- Sprawdzanie czy dane są poprawnie zapisywane w lokalnej bazie
- Sprawdzanie czy odczyty z GPS są prawidłowe