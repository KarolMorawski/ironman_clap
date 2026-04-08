# CHANGELOG

## [1.0.0] — 2026-04-08

### feat
- Wykrywanie podwójnego klasnięcia przez mikrofon MacBooka (pyaudio + numpy)
- Automatyczne tworzenie venv i instalacja zależności (obsługa Homebrew Python 3.14+)
- Automatyczna instalacja portaudio przez brew jeśli brakuje (wymagane do kompilacji pyaudio)
- Ustawienie głośności systemowej przed otwarciem przeglądarki
- Otwarcie Safari z filmem w nowym oknie (AppleScript `make new document`)
- Skrypt kończy działanie po jednorazowym wykryciu podwójnego klasnięcia
