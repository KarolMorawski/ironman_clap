# CHANGELOG

## [Unreleased]

### feat: clap_launcher.py — uruchamianie wideo klasnięciem (2026-04-08)
- Wykrywanie podwójnego klasnięcia przez mikrofon MacBooka (pyaudio + numpy)
- Automatyczne tworzenie venv i instalacja zależności (obsługa Homebrew Python 3.14+)
- Instalacja portaudio przez brew jeśli brakuje (wymagane do kompilacji pyaudio)
- Ustawienie głośności systemowej przed otwarciem przeglądarki
- Otwarcie Safari z filmem w nowym oknie (AppleScript)
- Skrypt kończy działanie po jednorazowym wykryciu podwójnego klasnięcia
