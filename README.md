# Clap Launcher

Skrypt Python wykrywający podwójne klasnięcie w dłonie przez mikrofon MacBooka i otwierający film w Safari.

## Warianty

| Plik | Wymaga Homebrew | Biblioteka audio |
|---|---|---|
| `clap_launcher.py` | tak | `pyaudio` + portaudio z brew |
| `clap_launcher_nobrew.py` | **nie** | `sounddevice` (binaria wbudowane) |

## Wymagania

- macOS z Safari
- Python 3.10+
- Homebrew — tylko dla `clap_launcher.py`

## Uruchomienie

**Z Homebrew:**
```bash
python3 clap_launcher.py
```

**Bez Homebrew:**
```bash
python3 clap_launcher_nobrew.py
```

Przy pierwszym uruchomieniu skrypt automatycznie tworzy venv i instaluje zależności.

> macOS poprosi o pozwolenie na dostęp do mikrofonu — należy zaakceptować.

## Użycie

Po uruchomieniu skrypt nasłuchuje mikrofonu. **Klasnij dwukrotnie** — Safari otworzy się z filmem w nowym oknie.

## Konfiguracja

Parametry na górze każdego pliku (identyczne w obu wariantach):

| Zmienna | Domyślnie | Opis |
|---|---|---|
| `YOUTUBE_URL` | `youtube.com/...` | URL filmu do otwarcia |
| `CLAP_THRESHOLD` | `1500` | Czułość wykrywania (niżej = czulej) |
| `DOUBLE_CLAP_WINDOW` | `0.6` | Max czas (s) między dwoma klasnięciami |
| `CLAP_MIN_GAP` | `0.1` | Min czas (s) między klasnięciami (odrzuca echo) |
| `VOLUME` | `80` | Głośność po klasnięciu (0–100), `None` = nie zmieniaj |

## Wersja

Zobacz [CHANGELOG.md](CHANGELOG.md).
