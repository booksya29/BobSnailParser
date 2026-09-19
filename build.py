import io
import os
import shutil
import subprocess
import sys
import winreg
from pathlib import Path

# Встановлюємо UTF-8 кодування для коректного відображення в консолі
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = ROOT / "release"
DIST_DIR = OUTPUT_ROOT / "BobSnailParser"
ZIP_BASE = ROOT / "BobSnailParser"


def is_app_running() -> bool:
    """Перевіряє, чи запущений процес BobSnailParser.exe."""
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq BobSnailParser.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return "BobSnailParser.exe".lower() in result.stdout.lower()


def compile_ui() -> bool:
    """Компілює form.ui у ui_form.py, якщо form.ui існує."""
    ui_file = ROOT / "form.ui"
    out_file = ROOT / "ui_form.py"
    if not ui_file.exists():
        return True

    print("=== 0. Компіляція UI форми (form.ui -> ui_form.py) ===")
    try:
        import PySide6
        uic_exe = Path(PySide6.__file__).parent / "uic.exe"
        if uic_exe.exists():
            subprocess.run([str(uic_exe), "-g", "python", str(ui_file), "-o", str(out_file)], check=True)
            print("✓ Інтерфейс успішно оновлено з form.ui")
            return True
    except Exception as e:
        print(f"Увага: не вдалося автоматично скомпільувати UI: {e}")
    return True


def get_desktop_paths() -> list[Path]:
    """Визначає шлях до Робочого столу користувача (з урахуванням OneDrive)."""
    desktops = []
    
    # 1. Спроба отримати шлях через реєстр Windows (найточніший спосіб)
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        )
        desktop_val, _ = winreg.QueryValueEx(key, "Desktop")
        winreg.CloseKey(key)
        reg_desktop = Path(os.path.expandvars(desktop_val))
        if reg_desktop.exists():
            desktops.append(reg_desktop)
    except Exception:
        pass

    # 2. Стандартні шляхи
    user_profile = os.environ.get("USERPROFILE", "")
    onedrive = os.environ.get("OneDrive", "") or os.environ.get("OneDriveConsumer", "")

    candidates = [
        Path(onedrive) / "Desktop" if onedrive else None,
        Path(user_profile) / "OneDrive" / "Desktop" if user_profile else None,
        Path(user_profile) / "Desktop" if user_profile else None,
    ]

    for candidate in candidates:
        if candidate and candidate.exists() and candidate not in desktops:
            desktops.append(candidate)

    return desktops


def build() -> bool:
    if is_app_running():
        print("ПОМИЛКА: BobSnailParser зараз запущений!")
        print("Будь ласка, закрийте програму перед збіркою та повторіть спробу.")
        return False

    # 0. Оновлюємо UI файл з актуального .ui
    compile_ui()

    print("\n=== 1. Збірка виконуваного файлу через PyInstaller ===")
    excludes = [
        "PyQt6", "PyQt5",
        "matplotlib", "scipy", "sklearn", "skimage", "torch", "statsmodels",
        "numba", "h5py", "pywt", "bottleneck", "tables", "sqlalchemy",
        "IPython", "pytest", "black", "sphinx", "docutils", "dask",
        "astroid", "nbformat", "notebook", "jupyter", "zmq", "mistune",
        "jsonschema", "jedi", "pygments",
        "sqlite3", "pycparser", "setuptools", "wheel", "pip",
        "panel", "plotly", "xarray", "altair", "nbconvert", "intake",
    ]
    exclude_args = []
    for exc in excludes:
        exclude_args.extend(["--exclude-module", exc])

    new_tab_modules = [
        "dnipro_fozzy",
        "kyiv_fozzy_zabolotnogo",
        "ashan_banderu",
        "ashan_dnipro",
        "lviv_ashan",
        "odesa_ashan",
        "dripro_metro",
        "lviv_metro",
        "odesa_metro",
        "kyiv_metro",
        "kharkiv_metro",
        "kyiv_novus_zdolbunivska",
        "kyiv_varus_malushka",
        "dnipro_varus_panikahi",
        "dnipro_atb_zoryanuy",
        "kyiv_atb_rudnutskogo",
        "kyiv_silpo_beresteyski",
        "dnipro_silpo_novokrumskiy",
        "lviv_silpo_kulparivska",
        "kyiv_fora_berest",
    ]
    hidden_args = []
    for mod in new_tab_modules:
        hidden_args.extend(["--hidden-import", mod])

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onedir",
        "--distpath", str(OUTPUT_ROOT),
        "--paths", str(ROOT / "src"),
        "--paths", str(ROOT / "src" / "new_tab"),
        *hidden_args,
        *exclude_args,
        "--collect-all", "patchright",
        "--collect-all", "openpyxl",
        "--collect-submodules", "pandas",
        "--add-data", f"src/urls_db{os.pathsep}src/urls_db",
        "--name", "BobSnailParser",
        "widget.py",
        "-y"
    ]
    try:
        subprocess.run(cmd, cwd=str(ROOT), check=True)
    except subprocess.CalledProcessError:
        print("ПОМИЛКА: не вдалося зібрати проект PyInstaller.")
        print("Переконайтеся, що BobSnailParser.exe закритий та папка release не заблокована.")
        return False

    print("\n=== 2. Очищення зайвих вихідних файлів (.py) ===")
    for py_file in DIST_DIR.glob("**/*.py"):
        try:
            py_file.unlink()
        except Exception:
            pass

    # Переконуємося, що всі файли urls_db та storage_state є в dist
    src_db = ROOT / "src" / "urls_db"
    for dest_parent in [DIST_DIR, DIST_DIR / "_internal"]:
        dest_db = dest_parent / "src" / "urls_db"
        dest_db.mkdir(parents=True, exist_ok=True)
        if src_db.exists():
            for item in src_db.glob("*.json"):
                shutil.copy2(item, dest_db / item.name)

    st_file = ROOT / "storage_state.json"
    if st_file.exists():
        shutil.copy2(st_file, DIST_DIR / "storage_state.json")

    print("\n=== 3. Вшивання браузера Chromium (Patchright) ===")
    local_browsers_dst = DIST_DIR / "_internal" / "patchright" / "driver" / "package" / ".local-browsers"
    local_browsers_dst.mkdir(parents=True, exist_ok=True)
    
    # Визначаємо тільки актуальні версії браузера з browsers.json (щоб не копіювати старі дублікати)
    browsers_json = DIST_DIR / "_internal" / "patchright" / "driver" / "package" / "browsers.json"
    required_names = set()
    if browsers_json.exists():
        try:
            import json
            b_info = json.loads(browsers_json.read_text(encoding="utf-8"))
            for b in b_info.get("browsers", []):
                if b.get("name") in ("chromium", "ffmpeg"):
                    required_names.add(f"{b['name']}-{b['revision']}")
        except Exception:
            pass

    appdata = os.environ.get("LOCALAPPDATA", "")
    src_browsers = Path(appdata) / "ms-playwright"
    if src_browsers.exists():
        for item in src_browsers.glob("*"):
            if required_names:
                should_copy = item.name in required_names
            else:
                should_copy = (item.name.startswith("chromium-") and "headless" not in item.name) or item.name.startswith("ffmpeg-")
            if should_copy:
                dst_item = local_browsers_dst / item.name
                if not dst_item.exists():
                    print(f"Копіювання {item.name}...")
                    if item.is_dir():
                        shutil.copytree(item, dst_item)
                    else:
                        shutil.copy2(item, dst_item)

    print("\n=== 4. Створення ZIP-архіву ===")
    zip_path = shutil.make_archive(str(ZIP_BASE), "zip", root_dir=str(OUTPUT_ROOT), base_dir=DIST_DIR.name)
    print(f"Створено архів: {zip_path}")

    print("\n=== 5. Копіювання на Робочий стіл ===")
    desktop_dirs = get_desktop_paths()
    copied = False
    for desktop in desktop_dirs:
        try:
            target = desktop / "BobSnailParser.zip"
            shutil.copy2(zip_path, target)
            print(f"✓ Скопійовано на: {target}")
            copied = True
        except Exception as e:
            print(f"Не вдалося скопіювати на {desktop}: {e}")

    if not copied:
        print(f"Увага: не вдалося знайти папку Робочого столу. Архів доступний тут: {zip_path}")

    print("\n Готово! Програму повністю зібрано та оновлено.")
    return True


if __name__ == "__main__":
    sys.exit(0 if build() else 1)
