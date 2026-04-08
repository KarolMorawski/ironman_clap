# Clap Launcher

Skrypt Python wykrywający podwójne klasnięcie w dłonie przez mikrofon MacBooka i otwierający film w Safari.

## Wymagania

- macOS z Safari
- Python 3.10+
- Homebrew (do instalacji portaudio)

## Uruchomienie

```bash
python3 clap_launcher.py
```

Przy pierwszym uruchomieniu skrypt automatycznie:
1. Instaluje `portaudio` przez Homebrew
2. Tworzy środowisko wirtualne `.venv`
3. Instaluje `pyaudio` i `numpy` w `.venv`

> macOS poprosi o pozwolenie na dostęp do mikrofonu — należy zaakceptować.

## Użycie

Po uruchomieniu skrypt nasłuchuje mikrofonu. **Klasnij dwukrotnie** — Safari otworzy się z filmem w nowym oknie.

## Konfiguracja

Parametry na górze pliku `clap_launcher.py`:

| Zmienna | Domyślnie | Opis |
|---|---|---|
| `YOUTUBE_URL` | `youtube.com/...` | URL filmu do otwarcia |
| `CLAP_THRESHOLD` | `1500` | Czułość wykrywania (niżej = czulej) |
| `DOUBLE_CLAP_WINDOW` | `0.6` | Max czas (s) między dwoma klasnięciami |
| `CLAP_MIN_GAP` | `0.1` | Min czas (s) między klasnięciami (odrzuca echo) |
| `VOLUME` | `80` | Głośność po klasnięciu (0–100), `None` = nie zmieniaj |

## Wersja

Zobacz [CHANGELOG.md](CHANGELOG.md).
