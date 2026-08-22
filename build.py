import subprocess
import shutil
import os
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent
DIST_DIR = ROOT / "dist" / "BobSnailParser"
ZIP_BASE = ROOT / "BobSnailParser"

def build():
    print("=== 1. Збірка виконуваного файлу через PyInstaller ===")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onedir",
        "--paths", "src",
        "--collect-all", "patchright",
        "--collect-all", "openpyxl",
        "--collect-all", "pandas",
        "--add-data", f"src/urls_db{os.pathsep}src/urls_db",
        "--name", "BobSnailParser",
        "widget.py",
        "-y"
    ]
    subprocess.run(cmd, cwd=str(ROOT), check=True)

    print("\n=== 2. Очищення вихідного коду (.py) ===")
    for py_file in DIST_DIR.glob("**/*.py"):
        try:
            py_file.unlink()
        except Exception:
            pass

    print("\n=== 3. Вшивання браузера Chromium ===")
    local_browsers_dst = DIST_DIR / "_internal" / "patchright" / "driver" / "package" / ".local-browsers"
    local_browsers_dst.mkdir(parents=True, exist_ok=True)
    
    appdata = os.environ.get("LOCALAPPDATA", "")
    src_browsers = Path(appdata) / "ms-playwright"
    if src_browsers.exists():
        for item in src_browsers.glob("*"):
            if item.name.startswith("chromium-") or item.name.startswith("ffmpeg-"):
                dst_item = local_browsers_dst / item.name
                if not dst_item.exists():
                    print(f"Копіювання {item.name}...")
                    if item.is_dir():
                        shutil.copytree(item, dst_item)
                    else:
                        shutil.copy2(item, dst_item)

    print("\n=== 4. Створення ZIP-архіву ===")
    zip_path = shutil.make_archive(str(ZIP_BASE), "zip", root_dir=str(DIST_DIR.parent), base_dir=DIST_DIR.name)
    print(f"Створено архів: {zip_path}")

    print("\n=== 5. Копіювання на Робочий стіл ===")
    desktop_targets = [
        Path(r"C:\Users\books\OneDrive\Desktop\BobSnailParser.zip"),
        Path(r"C:\Users\books\Desktop\BobSnailParser.zip")
    ]
    for target in desktop_targets:
        if target.parent.exists():
            shutil.copy2(zip_path, target)
            print(f"Скопійовано на: {target}")

    print("\n Готово! Програму повністю зібрано.")

if __name__ == "__main__":
    build()
