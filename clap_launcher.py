#!/usr/bin/env python3
"""
Clap Launcher - wykrywa klasnięcie w dłonie i otwiera film w Safari.
Wymagania: pip install pyaudio numpy
"""

import os
import subprocess
import sys
import time

YOUTUBE_URL = "https://www.youtube.com/watch?v=qRrElw4TSB4"
CLAP_THRESHOLD = 1500   # Próg amplitudy - zwiększ jeśli zbyt czuły, zmniejsz jeśli nie wykrywa
DOUBLE_CLAP_WINDOW = 0.6  # Max sekund między dwoma klasnięciami
CLAP_MIN_GAP = 0.1        # Min sekund między klasnięciami (odrzuca echo)
VOLUME = 80             # Głośność po klasnięciu (0-100), None = nie zmieniaj
CHUNK = 1024
RATE = 44100


def set_volume(level: int):
    """Ustawia głośność systemową (0-100)."""
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
    subprocess.run(["osascript", "-e", "set volume output muted false"])
    print(f"Głośność ustawiona na {level}%")


VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python3")


PORTAUDIO_PREFIX = "/opt/homebrew"  # domyślna ścieżka Homebrew na Apple Silicon


def _brew_install_portaudio():
    result = subprocess.run(["brew", "list", "portaudio"], capture_output=True)
    if result.returncode != 0:
        print("Instaluję portaudio przez Homebrew (wymagane do pyaudio)...")
        subprocess.check_call(["brew", "install", "portaudio"])


def _pip_install_pyaudio(python: str):
    env = os.environ.copy()
    env["CFLAGS"] = f"-I{PORTAUDIO_PREFIX}/include"
    env["LDFLAGS"] = f"-L{PORTAUDIO_PREFIX}/lib"
    subprocess.check_call(
        [python, "-m", "pip", "install", "--quiet", "pyaudio"],
        env=env,
    )


def check_dependencies():
    # Jeśli nie jesteśmy w venv - utwórz go i uruchom skrypt ponownie w nim
    if sys.prefix == sys.base_prefix:
        _brew_install_portaudio()
        if not os.path.exists(VENV_PYTHON):
            print("Tworzę środowisko wirtualne (.venv)...")
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("Instaluję zależności w .venv...")
        _pip_install_pyaudio(VENV_PYTHON)
        subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "--quiet", "numpy"])
        print("Restartuję w środowisku wirtualnym...\n")
        os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

    # Już jesteśmy w venv - sprawdź czy pakiety są dostępne
    missing = []
    for pkg in ("pyaudio", "numpy"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        _brew_install_portaudio()
        if "pyaudio" in missing:
            _pip_install_pyaudio(sys.executable)
            missing.remove("pyaudio")
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
    import pyaudio
    import numpy as np

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("=" * 50)
    print("Nasłuchuję mikrofonu...")
    print("Klasnij dwukrotnie, aby otworzyć film.")
    print("Ctrl+C aby zatrzymać.")
    print("=" * 50)

    first_clap_time = 0.0
    last_clap_time = 0.0

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio = np.frombuffer(data, dtype=np.int16)
            rms = float(np.sqrt(np.mean(audio.astype(np.float32) ** 2)))

            now = time.time()
            gap = now - last_clap_time

            if rms > CLAP_THRESHOLD and gap > CLAP_MIN_GAP:
                last_clap_time = now

                if first_clap_time == 0.0 or (now - first_clap_time) > DOUBLE_CLAP_WINDOW:
                    # pierwsze klasnięcie (lub minęło okno - reset)
                    first_clap_time = now
                    print(f"Klasnięcie 1... (poziom: {rms:.0f})")
                else:
                    # drugie klasnięcie w oknie czasowym
                    print(f"Podwójne klasnięcie! Otwieram film...")
                    if VOLUME is not None:
                        set_volume(VOLUME)
                    open_in_safari(YOUTUBE_URL)
                    print("Film otwarty.")
                    break

    except KeyboardInterrupt:
        print("\nZatrzymano.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    check_dependencies()
    listen_for_clap()
