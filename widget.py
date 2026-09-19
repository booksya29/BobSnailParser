# This Python file uses the following encoding: utf-8

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

if getattr(sys, "frozen", False):
    app_dir = Path(sys.executable).resolve().parent
    local_browsers = app_dir / "_internal" / "patchright" / "driver" / "package" / ".local-browsers"
    if local_browsers.exists():
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(local_browsers)

APP_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
STORAGE_STATE_PATH = APP_DIR / "storage_state.json"

SRC_DIR = Path(__file__).resolve().parent / "src"
NEW_TAB_DIR = SRC_DIR / "new_tab"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(NEW_TAB_DIR) not in sys.path:
    sys.path.insert(0, str(NEW_TAB_DIR))

import excel_add
import json_manager
import atb_async_parser_product
import ashan_parser_product
import novus_parser_product
import fozzy_parser_product
import fora_parser_product
import tavria_parser_product
import silpo_parser_product
import varus_parser_product
import metro_parser_product

# Нові парсери з src/new_tab
import dnipro_fozzy
import kyiv_fozzy_zabolotnogo
import ashan_banderu
import ashan_dnipro
import lviv_ashan
import odesa_ashan
import dripro_metro
import lviv_metro
import odesa_metro
import kyiv_metro
import kharkiv_metro
import kyiv_novus_zdolbunivska
import kyiv_varus_malushka
import dnipro_varus_panikahi
import dnipro_atb_zoryanuy
import kyiv_atb_rudnutskogo
import kyiv_silpo_beresteyski
import dnipro_silpo_novokrumskiy
import lviv_silpo_kulparivska
import kyiv_fora_berest

from PySide6.QtWidgets import (
    QApplication, QWidget, QMessageBox, QPlainTextEdit, QPushButton,
    QLabel, QHBoxLayout,
)
from PySide6.QtCore import QObject, QThread, Signal

from ui_form import Ui_Widget
from config_dialog import ConfigDialog


class GuiLogStream(QObject):
    """Routes print() output from the parser thread into the app window."""

    line_written = Signal(str)

    def __init__(self):
        super().__init__()
        self._buffer = ""

    def write(self, text):
        if not text:
            return 0
        self._buffer += str(text)
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            if line.strip():
                self.line_written.emit(line.rstrip())
        return len(text)

    def flush(self):
        if self._buffer.strip():
            self.line_written.emit(self._buffer.rstrip())
        self._buffer = ""


class Worker(QObject):
    finished = Signal()
    failed = Signal(str)
    progress = Signal(str, int)

    def __init__(self, target_shop: str = None):
        super().__init__()
        self.target_shop = target_shop
        self._is_stopped = False
        self._browser = None
        self._context = None
        self._loop = None

    def stop(self):
        """Signals worker to stop and cancels all running tasks."""
        self._is_stopped = True
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._cancel_all_tasks)

    def _cancel_all_tasks(self):
        try:
            for task in asyncio.all_tasks(self._loop):
                task.cancel()
        except Exception:
            pass

    def run(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._parse())
        except BaseException as error:
            if not self._is_stopped and not isinstance(error, asyncio.CancelledError):
                self.failed.emit(str(error))
        finally:
            try:
                if self._loop and not self._loop.is_closed():
                    self._loop.close()
            except Exception:
                pass
            self.finished.emit()

    async def _parse(self):
        parsers = self._load_parsers()
        if not parsers:
            return

        if self.target_shop:
            parsers = [p for p in parsers if p[0] == self.target_shop]
            if not parsers:
                self.failed.emit(f"Не знайдено конфігурації для магазину {self.target_shop}.")
                return

        active_shops = []
        for shop_key, parser_func, json_name in parsers:
            urls = await json_manager.read_json(json_name)
            if urls:
                active_shops.append((shop_key, parser_func, urls))
            else:
                self.progress.emit(shop_key, 100)

        if not active_shops:
            if self.target_shop:
                self.failed.emit("Не знайдено жодного посилання для цього магазину. Додайте посилання через 'Відредагувати конфіг'.")
            else:
                self.failed.emit("Не знайдено жодного посилання. Будь ласка, додайте посилання у конфігурацію магазинів через 'Відредагувати конфіг'.")
            return

        from patchright.async_api import async_playwright

        async def run_shop(shop_key, parser_func, page):
            def on_progress(p):
                if not self._is_stopped:
                    self.progress.emit(shop_key, p)

            on_progress(0)
            print(f"[{shop_key.upper()}] Початок обробки.")
            try:
                import inspect
                if "on_progress" in inspect.signature(parser_func).parameters:
                    await parser_func(page, on_progress=on_progress)
                else:
                    await parser_func(page)
            except Exception as e:
                if not self._is_stopped:
                    print(f"Error parsing {shop_key}: {e}")
            finally:
                if not self._is_stopped:
                    on_progress(100)
                print(f"[{shop_key.upper()}] Обробку завершено.")

        async with async_playwright() as playwright:
            self._browser = await playwright.chromium.launch(
                headless=False,
                args=[
                    "--blink-settings=imagesEnabled=false",
                    "--disk-cache-size=1",
                    "--media-cache-size=1",
                    "--disable-dev-shm-usage",
                ]
            )
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 800}
            )
            try:
                semaphore = asyncio.Semaphore(3 if not self.target_shop else 1)

                async def process_shop(shop_key, parser_func):
                    if self._is_stopped:
                        return
                    async with semaphore:
                        if self._is_stopped:
                            return
                        page = await self._context.new_page()
                        try:
                            await run_shop(shop_key, parser_func, page)
                        finally:
                            try:
                                await page.close()
                            except Exception:
                                pass

                await asyncio.gather(
                    *(process_shop(shop_key, parser_func) for shop_key, parser_func, _ in active_shops),
                    return_exceptions=True
                )
            finally:
                try:
                    if self._context:
                        await asyncio.shield(self._context.close())
                except Exception:
                    pass
                try:
                    if self._browser:
                        await asyncio.shield(self._browser.close())
                except Exception:
                    pass

    @staticmethod
    def _load_parsers():
        return [
            ("atb", atb_async_parser_product.atb_all_parsing, "atb.json"),
            ("ashan", ashan_parser_product.ashan_parsing_all, "ashan.json"),
            ("novus", novus_parser_product.novus_parsing_all, "novus.json"),
            ("fozzy", fozzy_parser_product.fozzy_parsing_all, "fozzy.json"),
            ("fora", fora_parser_product.fora_parsing_all, "fora.json"),
            ("tavria", tavria_parser_product.tavria_parsing_all, "tavria.json"),
            ("silpo", silpo_parser_product.silpo_parsing_all, "silpo.json"),
            ("varus", varus_parser_product.varus_parsing_all, "varus.json"),
            ("metro", metro_parser_product.metro_parsing_all, "metro.json"),
        ]


class NewTabWorker(QObject):
    finished = Signal()
    failed = Signal(str)
    progress = Signal(str, int)

    def __init__(self, target_shop: str = None):
        super().__init__()
        self.target_shop = target_shop
        self._is_stopped = False
        self._browser = None
        self._context = None
        self._loop = None

    def stop(self):
        """Signals worker to stop and cancels all running tasks."""
        self._is_stopped = True
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._cancel_all_tasks)

    def _cancel_all_tasks(self):
        try:
            for task in asyncio.all_tasks(self._loop):
                task.cancel()
        except Exception:
            pass

    def run(self):
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._parse())
        except BaseException as error:
            if not self._is_stopped and not isinstance(error, asyncio.CancelledError):
                self.failed.emit(str(error))
        finally:
            try:
                if self._loop and not self._loop.is_closed():
                    self._loop.close()
            except Exception:
                pass
            self.finished.emit()

    async def _parse(self):
        parsers = self._load_parsers()
        if not parsers:
            return

        if self.target_shop:
            parsers = [p for p in parsers if p[0] == self.target_shop]
            if not parsers:
                self.failed.emit(f"Не знайдено конфігурації для магазину {self.target_shop}.")
                return

        active_shops = []
        for shop_key, parser_func, json_name, display_name in parsers:
            urls = await json_manager.read_json(json_name)
            if urls:
                active_shops.append((shop_key, parser_func, urls, display_name))
            else:
                self.progress.emit(shop_key, 100)

        if not active_shops:
            if self.target_shop:
                self.failed.emit("Не знайдено жодного посилання для цього магазину. Додайте посилання через 'Відредагувати конфіг'.")
            else:
                self.failed.emit("Не знайдено жодного посилання. Будь ласка, додайте посилання у конфігурацію магазинів через 'Відредагувати конфіг'.")
            return

        from patchright.async_api import async_playwright

        async def run_shop(shop_key, parser_func, page, display_name):
            def on_progress(p):
                if not self._is_stopped:
                    self.progress.emit(shop_key, p)

            on_progress(0)
            print(f"[{display_name}] Початок обробки.")
            try:
                import inspect
                if "on_progress" in inspect.signature(parser_func).parameters:
                    await parser_func(page, on_progress=on_progress)
                else:
                    await parser_func(page)
            except Exception as e:
                if not self._is_stopped:
                    print(f"Error parsing {display_name}: {e}")
            finally:
                if not self._is_stopped:
                    on_progress(100)
                print(f"[{display_name}] Обробку завершено.")

        def get_chain_key(k: str) -> str:
            for chain in ["fozzy", "ashan", "metro", "novus", "varus", "atb", "silpo", "fora"]:
                if chain in k:
                    return chain
            return k

        import collections
        chain_locks = collections.defaultdict(asyncio.Lock)
        semaphore = asyncio.Semaphore(3 if not self.target_shop else 1)

        async with async_playwright() as playwright:
            self._browser = await playwright.chromium.launch(
                headless=False,
            )
            context_kwargs = {"viewport": {"width": 1280, "height": 800}}
            if STORAGE_STATE_PATH.exists() and STORAGE_STATE_PATH.stat().st_size > 0:
                try:
                    context_kwargs["storage_state"] = str(STORAGE_STATE_PATH)
                except Exception as e:
                    print(f"Error loading storage state: {e}")

            self._context = await self._browser.new_context(**context_kwargs)
            try:
                async def process_shop(shop_key, parser_func, urls, display_name):
                    if self._is_stopped:
                        return
                    chain_key = get_chain_key(shop_key)
                    async with chain_locks[chain_key]:
                        if self._is_stopped:
                            return
                        async with semaphore:
                            if self._is_stopped:
                                return
                            page = await self._context.new_page()
                            try:
                                await run_shop(shop_key, parser_func, page, display_name)
                            finally:
                                if chain_key == "fozzy":
                                    try:
                                        if self._context and not self._is_stopped:
                                            await asyncio.shield(self._context.storage_state(path=str(STORAGE_STATE_PATH)))
                                    except Exception as e:
                                        print(f"Помилка збереження storage_state: {e}")
                                try:
                                    await asyncio.shield(page.close())
                                except Exception:
                                    pass

                await asyncio.gather(
                    *(process_shop(shop_key, parser_func, urls, display_name) for shop_key, parser_func, urls, display_name in active_shops),
                    return_exceptions=True
                )
            finally:
                try:
                    if self._context:
                        await asyncio.shield(self._context.storage_state(path=str(STORAGE_STATE_PATH)))
                except Exception as e:
                    print(f"Помилка збереження storage_state: {e}")
                try:
                    if self._context:
                        await asyncio.shield(self._context.close())
                except Exception:
                    pass
                self._context = None
                try:
                    if self._browser:
                        await asyncio.shield(self._browser.close())
                except Exception:
                    pass
                self._browser = None

    @staticmethod
    def _load_parsers():
        # Фоззі парситься першим за окремою вимогою користувача!
        return [
            ("dnipro_fozzy", dnipro_fozzy.fozzy_parsing_all, "dnipro_fozzy.json", "Fozzy Дніпро"),
            ("kyiv_fozzy_zabolotnogo", kyiv_fozzy_zabolotnogo.fozzy_parsing_all, "kyiv_fozzy_zabolotnogo.json", "Fozzy Київ"),
            ("ashan_banderu", ashan_banderu.ashan_parsing_all, "ashan_banderu.json", "Auchan Київ"),
            ("ashan_dnipro", ashan_dnipro.ashan_parsing_all, "ashan_dnipro.json", "Auchan Дніпро"),
            ("lviv_ashan", lviv_ashan.ashan_parsing_all, "lviv_ashan.json", "Auchan Львів"),
            ("odesa_ashan", odesa_ashan.ashan_parsing_all, "odesa_ashan.json", "Auchan Одеса"),
            ("dripro_metro", dripro_metro.ashan_parsing_all, "dripro_metro.json", "Metro Дніпро"),
            ("lviv_metro", lviv_metro.ashan_parsing_all, "lviv_metro.json", "Metro Львів"),
            ("odesa_metro", odesa_metro.ashan_parsing_all, "odesa_metro.json", "Metro Одеса"),
            ("kyiv_metro", kyiv_metro.ashan_parsing_all, "kyiv_metro.json", "Metro Київ"),
            ("kharkiv_metro", kharkiv_metro.ashan_parsing_all, "kharkiv_metro.json", "Metro Харків"),
            ("kyiv_novus_zdolbunivska", kyiv_novus_zdolbunivska.ashan_parsing_all, "kyiv_novus_zdolbunivska.json", "Novus Київ"),
            ("kyiv_varus_malushka", kyiv_varus_malushka.varus_parsing_all, "kyiv_varus_malushka.json", "Varus Київ"),
            ("dnipro_varus_panikahi", dnipro_varus_panikahi.varus_parsing_all, "dnipro_varus_panikahi.json", "Varus Дніпро"),
            ("dnipro_atb_zoryanuy", dnipro_atb_zoryanuy.atb_all_parsing, "dnipro_atb_zoryanuy.json", "АТБ Дніпро"),
            ("kyiv_atb_rudnutskogo", kyiv_atb_rudnutskogo.atb_all_parsing, "kyiv_atb_rudnutskogo.json", "АТБ Київ"),
            ("kyiv_silpo_beresteyski", kyiv_silpo_beresteyski.silpo_parsing_all, "kyiv_silpo_beresteyski.json", "Сільпо Київ"),
            ("dnipro_silpo_novokrumskiy", dnipro_silpo_novokrumskiy.silpo_parsing_all, "dnipro_silpo_novokrumskiy.json", "Сільпо Дніпро"),
            ("lviv_silpo_kulparivska", lviv_silpo_kulparivska.silpo_parsing_all, "lviv_silpo_kulparivska.json", "Сільпо Львів"),
            ("kyiv_fora_berest", kyiv_fora_berest.fora_parsing_all, "kyiv_fora_berest.json", "Фора Київ"),
        ]


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("Bob Snail")

        self.log_output = QPlainTextEdit(self)
        self.log_output.setReadOnly(True)
        self.log_output.setMaximumBlockCount(3000)
        self.log_output.setPlaceholderText("Тут з'являться повідомлення про роботу парсера…")
        self.log_output.setMinimumHeight(190)
        self.log_output.setStyleSheet(
            "QPlainTextEdit { background: #151515; color: #e6e6e6; "
            "font-family: Consolas, monospace; font-size: 10pt; }"
        )
        log_label = QLabel("Журнал роботи", self)
        clear_log_button = QPushButton("Очистити журнал", self)
        clear_log_button.clicked.connect(self.log_output.clear)
        log_header = QHBoxLayout()
        log_header.addWidget(log_label)
        log_header.addStretch()
        log_header.addWidget(clear_log_button)

        # Розміщуємо журнал роботи під вкладками, щоб він був видимим для обох вкладок
        self.ui.gridLayout.addLayout(log_header, 1, 0)
        self.ui.gridLayout.addWidget(self.log_output, 2, 0)

        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._log_stream = GuiLogStream()
        self._log_stream.line_written.connect(self.append_log)
        sys.stdout = self._log_stream
        sys.stderr = self._log_stream
        self.append_log("Програма запущена. Журнал готовий.")

        self.thread = None
        self.worker = None

        # Вкладка 1 (main)
        self.progress_bars = {
            "ashan": self.ui.AshanProgressBar,
            "silpo": self.ui.SilpoProgressBar,
            "atb": self.ui.ATBProgressBar,
            "fozzy": self.ui.FozzyProgressBar,
            "novus": self.ui.NovusProgressBar,
            "fora": self.ui.ForaProgressBar,
            "varus": self.ui.VarusProgressBar,
            "metro": self.ui.MetroProgressBar,
            "tavria": self.ui.TavriaProgressBar,
        }

        self.solo_buttons = {
            "ashan": self.ui.AshanParsingButton,
            "silpo": self.ui.SilpoParsing,
            "atb": self.ui.ATBParsing,
            "fozzy": self.ui.FozzyParsing,
            "novus": self.ui.ParsingNovus,
            "fora": self.ui.ForaParsing,
            "varus": self.ui.VarusParsing,
            "metro": self.ui.MatroParsing,
            "tavria": self.ui.TavriaParsing,
        }

        self.ui.StartButton.clicked.connect(lambda: self.start_worker(target_shop=None))
        self.ui.StopButton.clicked.connect(self.stop_worker)

        self.ui.AshanButton.clicked.connect(lambda: self.open_config("Ашан", "ashan.json"))
        self.ui.SilpoButton.clicked.connect(lambda: self.open_config("Сільпо", "silpo.json"))
        self.ui.ATBButton.clicked.connect(lambda: self.open_config("АТБ", "atb.json"))
        self.ui.FozzyButton.clicked.connect(lambda: self.open_config("Фоззі", "fozzy.json"))
        self.ui.NovusButton.clicked.connect(lambda: self.open_config("Новус", "novus.json"))
        self.ui.ForaButton.clicked.connect(lambda: self.open_config("Фора", "fora.json"))
        self.ui.VarusButton.clicked.connect(lambda: self.open_config("Варус", "varus.json"))
        self.ui.MetroButton.clicked.connect(lambda: self.open_config("Метро", "metro.json"))
        self.ui.TavriaButton.clicked.connect(lambda: self.open_config("Таврія", "tavria.json"))

        for shop_key, btn in self.solo_buttons.items():
            btn.clicked.connect(lambda checked=False, k=shop_key: self.start_worker(target_shop=k))

        # Вкладка 2 (new)
        self.new_progress_bars = {
            "dnipro_fozzy": self.ui.NewDniproFozzyProgressBar,
            "kyiv_fozzy_zabolotnogo": self.ui.NewKyivFozzyZabolotnogoProgressBar,
            "ashan_banderu": self.ui.NewAshanBanderuProgressBar,
            "ashan_dnipro": self.ui.NewAshanDniproProgressBar,
            "lviv_ashan": self.ui.NewLvivAshanProgressBar,
            "odesa_ashan": self.ui.NewOdesaAshanProgressBar,
            "dripro_metro": self.ui.NewDniproMetroProgressBar,
            "lviv_metro": self.ui.NewLvivMetroProgressBar,
            "odesa_metro": self.ui.NewOdesaMetroProgressBar,
            "kyiv_metro": self.ui.NewKyivMetroProgressBar,
            "kharkiv_metro": self.ui.NewKharkivMetroProgressBar,
            "kyiv_novus_zdolbunivska": self.ui.NewKyivNovusZdolbunivskaProgressBar,
            "kyiv_varus_malushka": self.ui.NewKyivVarusMalushkaProgressBar,
            "dnipro_varus_panikahi": self.ui.NewDniproVarusPanikahiProgressBar,
            "dnipro_atb_zoryanuy": self.ui.NewDniproAtbZoryanuyProgressBar,
            "kyiv_atb_rudnutskogo": self.ui.NewKyivAtbRudnutskogoProgressBar,
            "kyiv_silpo_beresteyski": self.ui.NewKyivSilpoBeresteyskiProgressBar,
            "dnipro_silpo_novokrumskiy": self.ui.NewDniproSilpoNovokrumskiyProgressBar,
            "lviv_silpo_kulparivska": self.ui.NewLvivSilpoKulparivskaProgressBar,
            "kyiv_fora_berest": self.ui.NewKyivForaBerestProgressBar,
        }

        self.new_solo_buttons = {
            "dnipro_fozzy": self.ui.NewDniproFozzyParsingButton,
            "kyiv_fozzy_zabolotnogo": self.ui.NewKyivFozzyZabolotnogoParsingButton,
            "ashan_banderu": self.ui.NewAshanBanderuParsingButton,
            "ashan_dnipro": self.ui.NewAshanDniproParsingButton,
            "lviv_ashan": self.ui.NewLvivAshanParsingButton,
            "odesa_ashan": self.ui.NewOdesaAshanParsingButton,
            "dripro_metro": self.ui.NewDniproMetroParsingButton,
            "lviv_metro": self.ui.NewLvivMetroParsingButton,
            "odesa_metro": self.ui.NewOdesaMetroParsingButton,
            "kyiv_metro": self.ui.NewKyivMetroParsingButton,
            "kharkiv_metro": self.ui.NewKharkivMetroParsingButton,
            "kyiv_novus_zdolbunivska": self.ui.NewKyivNovusZdolbunivskaParsingButton,
            "kyiv_varus_malushka": self.ui.NewKyivVarusMalushkaParsingButton,
            "dnipro_varus_panikahi": self.ui.NewDniproVarusPanikahiParsingButton,
            "dnipro_atb_zoryanuy": self.ui.NewDniproAtbZoryanuyParsingButton,
            "kyiv_atb_rudnutskogo": self.ui.NewKyivAtbRudnutskogoParsingButton,
            "kyiv_silpo_beresteyski": self.ui.NewKyivSilpoBeresteyskiParsingButton,
            "dnipro_silpo_novokrumskiy": self.ui.NewDniproSilpoNovokrumskiyParsingButton,
            "lviv_silpo_kulparivska": self.ui.NewLvivSilpoKulparivskaParsingButton,
            "kyiv_fora_berest": self.ui.NewKyivForaBerestParsingButton,
        }

        self.new_config_buttons = [
            (self.ui.NewDniproFozzyButton, "Fozzy Дніпро", "dnipro_fozzy.json"),
            (self.ui.NewKyivFozzyZabolotnogoButton, "Fozzy Київ", "kyiv_fozzy_zabolotnogo.json"),
            (self.ui.NewAshanBanderuButton, "Auchan Київ", "ashan_banderu.json"),
            (self.ui.NewAshanDniproButton, "Auchan Дніпро", "ashan_dnipro.json"),
            (self.ui.NewLvivAshanButton, "Auchan Львів", "lviv_ashan.json"),
            (self.ui.NewOdesaAshanButton, "Auchan Одеса", "odesa_ashan.json"),
            (self.ui.NewDniproMetroButton, "Metro Дніпро", "dripro_metro.json"),
            (self.ui.NewLvivMetroButton, "Metro Львів", "lviv_metro.json"),
            (self.ui.NewOdesaMetroButton, "Metro Одеса", "odesa_metro.json"),
            (self.ui.NewKyivMetroButton, "Metro Київ", "kyiv_metro.json"),
            (self.ui.NewKharkivMetroButton, "Metro Харків", "kharkiv_metro.json"),
            (self.ui.NewKyivNovusZdolbunivskaButton, "Novus Київ", "kyiv_novus_zdolbunivska.json"),
            (self.ui.NewKyivVarusMalushkaButton, "Varus Київ", "kyiv_varus_malushka.json"),
            (self.ui.NewDniproVarusPanikahiButton, "Varus Дніпро", "dnipro_varus_panikahi.json"),
            (self.ui.NewDniproAtbZoryanuyButton, "АТБ Дніпро", "dnipro_atb_zoryanuy.json"),
            (self.ui.NewKyivAtbRudnutskogoButton, "АТБ Київ", "kyiv_atb_rudnutskogo.json"),
            (self.ui.NewKyivSilpoBeresteyskiButton, "Сільпо Київ", "kyiv_silpo_beresteyski.json"),
            (self.ui.NewDniproSilpoNovokrumskiyButton, "Сільпо Дніпро", "dnipro_silpo_novokrumskiy.json"),
            (self.ui.NewLvivSilpoKulparivskaButton, "Сільпо Львів", "lviv_silpo_kulparivska.json"),
            (self.ui.NewKyivForaBerestButton, "Фора Київ", "kyiv_fora_berest.json"),
        ]

        for btn, name, cfg_file in self.new_config_buttons:
            btn.clicked.connect(lambda checked=False, n=name, f=cfg_file: self.open_config(n, f))

        for shop_key, btn in self.new_solo_buttons.items():
            btn.clicked.connect(lambda checked=False, k=shop_key: self.start_new_worker(target_shop=k))

        self.ui.NewStartButton.clicked.connect(lambda: self.start_new_worker(target_shop=None))
        self.ui.NewStopButton.clicked.connect(self.stop_new_worker)

    def set_running_state(self, is_running: bool, is_new_tab: bool = False):
        """Вмикає або вимикає кнопки в залежності від того, чи працює парсер."""
        self.ui.StartButton.setEnabled(not is_running)
        for btn in self.solo_buttons.values():
            btn.setEnabled(not is_running)
        self.ui.StopButton.setEnabled(is_running and not is_new_tab)

        self.ui.NewStartButton.setEnabled(not is_running)
        for btn in self.new_solo_buttons.values():
            btn.setEnabled(not is_running)
        self.ui.NewStopButton.setEnabled(is_running and is_new_tab)

    def open_config(self, shop_name: str, json_filename: str):
        dialog = ConfigDialog(shop_name, json_filename, self)
        dialog.exec()

    def update_progress(self, shop_key: str, value: int):
        if shop_key in self.progress_bars:
            self.progress_bars[shop_key].setValue(value)

    def update_new_progress(self, shop_key: str, value: int):
        if shop_key in self.new_progress_bars:
            self.new_progress_bars[shop_key].setValue(value)

    def append_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_output.appendPlainText(f"[{timestamp}] {message}")
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def start_worker(self, target_shop: str = None):
        if self.thread is not None and self.thread.isRunning():
            if self.worker is not None and self.worker._is_stopped:
                self.thread.quit()
                self.thread.wait(500)
            else:
                return

        if target_shop:
            if target_shop in self.progress_bars:
                self.progress_bars[target_shop].setValue(0)
            self.append_log(f"Запуск парсингу для магазину: {target_shop.upper()}.")
        else:
            for pb in self.progress_bars.values():
                pb.setValue(0)
            self.append_log("Запуск парсингу всіх налаштованих магазинів.")

        self.set_running_state(True, is_new_tab=False)
        self.thread = QThread(self)

        self.worker = Worker(target_shop=target_shop)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.show_error)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker_finished)

        self.thread.start()

    def stop_worker(self):
        self.append_log("Запит на зупинку парсингу... Закриваємо браузер.")
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
        self.set_running_state(False)

    def start_new_worker(self, target_shop: str = None):
        if self.thread is not None and self.thread.isRunning():
            if self.worker is not None and self.worker._is_stopped:
                self.thread.quit()
                self.thread.wait(500)
            else:
                return

        if target_shop:
            if target_shop in self.new_progress_bars:
                self.new_progress_bars[target_shop].setValue(0)
            self.append_log(f"[Нові парсери] Запуск парсингу для магазину: {target_shop}.")
        else:
            for pb in self.new_progress_bars.values():
                pb.setValue(0)
            self.append_log("[Нові парсери] Запуск парсингу всіх налаштованих магазинів (Fozzy першим).")

        self.set_running_state(True, is_new_tab=True)
        self.thread = QThread(self)

        self.worker = NewTabWorker(target_shop=target_shop)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_new_progress)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.failed.connect(self.show_error)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.worker_finished)

        self.thread.start()

    def stop_new_worker(self):
        self.append_log("[Нові парсери] Запит на зупинку парсингу... Зберігаємо storage_state та закриваємо браузер.")
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
        self.set_running_state(False)

    def show_error(self, message):
        print(f"Parser error: {message}")
        QMessageBox.warning(self, "Інформація", str(message))

    def worker_finished(self):
        self.append_log("Парсинг завершено.")
        self.set_running_state(False)
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        if self.worker is not None:
            self.worker.stop()
        if self.thread is not None and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(2000)
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
