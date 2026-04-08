#!/usr/bin/env python3
"""
Clap Launcher (no-Homebrew) — wykrywa podwójne klasnięcie i otwiera film w Safari.
Używa sounddevice zamiast pyaudio — nie wymaga Homebrew ani portaudio z systemu.
Wymagania: pip install sounddevice numpy
"""

import os
import subprocess
import sys
import time

YOUTUBE_URL = "https://www.youtube.com/watch?v=qRrElw4TSB4"
CLAP_THRESHOLD = 0.05   # Próg amplitudy 0.0–1.0 - zwiększ jeśli zbyt czuły, zmniejsz jeśli nie wykrywa
DOUBLE_CLAP_WINDOW = 0.6  # Max sekund między dwoma klasnięciami
CLAP_MIN_GAP = 0.1        # Min sekund między klasnięciami (odrzuca echo)
VOLUME = 80               # Głośność po klasnięciu (0-100), None = nie zmieniaj
CHUNK = 1024
RATE = 44100

VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv_nobrew")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python3")


def set_volume(level: int):
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
    subprocess.run(["osascript", "-e", "set volume output muted false"])
    print(f"Głośność ustawiona na {level}%")


def check_dependencies():
    # Jeśli nie jesteśmy w venv - utwórz go i uruchom skrypt ponownie w nim
    if sys.prefix == sys.base_prefix:
        if not os.path.exists(VENV_PYTHON):
            print("Tworzę środowisko wirtualne (.venv_nobrew)...")
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("Instaluję zależności w .venv_nobrew...")
        subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "--quiet", "sounddevice", "numpy"])
        print("Restartuję w środowisku wirtualnym...\n")
        os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

    # Już jesteśmy w venv - sprawdź czy pakiety są dostępne
    missing = []
    for pkg in ("sounddevice", "numpy"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + missing)


def open_in_safari(url: str):
    script = f'''
    tell application "Safari"
        activate
        make new document with properties {{URL:"{url}"}}
    end tell
    '''
    subprocess.run(["osascript", "-e", script])


def listen_for_clap():
    import sounddevice as sd
    import numpy as np

    print("=" * 50)
    print("Nasłuchuję mikrofonu...")
    print("Klasnij dwukrotnie, aby otworzyć film.")
    print("Ctrl+C aby zatrzymać.")
    print("=" * 50)

    first_clap_time = 0.0
    last_clap_time = 0.0

    try:
        with sd.InputStream(samplerate=RATE, channels=1, blocksize=CHUNK, dtype="float32") as stream:
            while True:
                data, _ = stream.read(CHUNK)
                rms = float(np.sqrt(np.mean(data ** 2)))

                now = time.time()
                gap = now - last_clap_time

                if rms > CLAP_THRESHOLD and gap > CLAP_MIN_GAP:
                    last_clap_time = now

                    if first_clap_time == 0.0 or (now - first_clap_time) > DOUBLE_CLAP_WINDOW:
                        first_clap_time = now
                        print(f"Klasnięcie 1... (poziom: {rms:.3f})")
                    else:
                        print(f"Podwójne klasnięcie! Otwieram film...")
                        if VOLUME is not None:
                            set_volume(VOLUME)
                        open_in_safari(YOUTUBE_URL)
                        print("Film otwarty.")
                        break

    except KeyboardInterrupt:
        print("\nZatrzymano.")


if __name__ == "__main__":
    check_dependencies()
    listen_for_clap()
