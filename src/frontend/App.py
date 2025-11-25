# -*- coding: utf-8 -*-
import sys
import os
from typing import Dict, List
import json
import zipfile

import pandas as pd
import requests

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont, QAction, QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QMessageBox,
    QMenuBar,
    QDialog,
    QRadioButton,
    QButtonGroup,
)

from report import Report


class Reader:
    def __init__(self):
        pass

    def read_file(self, path: str) -> pd.DataFrame:

        self.path = path
        # path to dir
        self.path_to_dir: str = os.path.split(path)[0]
        # file full name
        self.file_full_name: str = os.path.split(path)[1]
        # file name
        self.file_name: str = os.path.splitext(self.file_full_name)[0]
        # file extension
        self.file_extension: str = os.path.splitext(self.file_full_name)[1]

        match self.file_extension:
            case ".xlsx":
                return pd.read_excel(self.path, names=["text"])
            case ".json":
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return pd.DataFrame(data, columns=["text"])
            case ".csv":
                return pd.read_csv(self.path)
            case ".zip":
                return self.read_zip_file(self.path)
            case ".txt":
                with open(self.path, "r", encoding="utf-8") as f:
                    data = f.read()
                data = pd.DataFrame(data.split("\n"), columns=["text"])
                data = data[data["text"] != ""]
                data = data[data["text"] != "\n"]
                return data
            case _:
                return pd.DataFrame(columns=["text"])

    def read_zip_file(self, path: str) -> pd.DataFrame:

        zip_file_path = path

        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            data = ""
            df_data = pd.DataFrame(columns=["text"])
            for name in zip_ref.namelist():
                if name.endswith(".txt"):
                    with zip_ref.open(name) as file:
                        data += file.read().decode("utf-8")
                if name.endswith(".csv"):
                    with zip_ref.open(name) as file:
                        df_data = pd.concat(df_data, pd.read_csv(file))
        print(data)
        if data:
            return pd.DataFrame(data.split("\n"), columns=["text"])
        else:
            return df_data


# ===============================================================
#                ЛОГИКА РАБОТЫ
# ===============================================================


def read_file(path: str) -> pd.DataFrame:
    """Читает файл и возвращает DataFrame с любыми колонками"""
    reader = Reader()
    df = reader.read_file(path)
    if df is None or df.empty:
        raise ValueError("Файл пустой или не читается")
    return df


def classify(
    df: pd.DataFrame, model_type: str, category: str = "common"
) -> Dict[str, List]:
    API_URL = "http://localhost:8000/string/"

    if model_type.startswith("3"):
        model_type = "rt2_3cls"
    elif model_type.startswith("5"):
        model_type = "rt2_5cls"
    else:
        model_type = "lstm"

    param = {
        "reviews": list(df.iloc[:, 0]),
        "model_type": model_type,
        "category": category,
    }
    response = requests.post(API_URL, json=param)
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    df.to_csv("data.csv")
    return response.json()


def make_report(data: Dict[str, List]) -> str:
    """
    Формирование текстового отчёта из ответа API.
    Собирает положительные и отрицательные отзывы в удобный формат.
    """
    parts = [
        "Краткая сводка о данных",
        f"Количество отзывов: {len(data['output_list'])}",
        f"Количество классов: {len(data['class_names'])}",
        f"Использованные метки классов: {', '.join(data['class_names'])}",
        f"Использованная модель: {data['model_type']}",
    ]

    Report.get_report("data.json", True)
    return "\n".join(parts)


# ===============================================================
#                ДИАЛОГ ВЫБОРА КОЛИЧЕСТВА КЛАССОВ
# ===============================================================


class ClassSelectionDialog(QDialog):
    """
    Диалог с кнопками для выбора: 2, 3 или 5 классов.
    Возвращает выбранный вариант через self.selected_type.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор типа класса")
        self.setGeometry(550, 330, 280, 180)
        self.selected_type = None

        layout = QVBoxLayout(self)

        # Заголовок
        label = QLabel("Выберите количество классов:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Радиокнопки
        self.radio_group = QButtonGroup(self)
        for text in ("2 класса", "3 класса", "5 классов"):
            rb = QRadioButton(text)
            self.radio_group.addButton(rb)
            layout.addWidget(rb)

        # Кнопка подтверждения
        confirm_btn = QPushButton("Подтвердить выбор")
        confirm_btn.setFixedHeight(36)
        confirm_btn.clicked.connect(self.confirm_selection)
        layout.addWidget(confirm_btn)

    def confirm_selection(self):
        """Проверка выбора и завершение диалога."""
        btn = self.radio_group.checkedButton()
        if btn:
            self.selected_type = btn.text()
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите вариант.")


# ===============================================================
#                     ОКНО ОТЧЁТА
# ===============================================================


class ReportWindow(QWidget):
    """
    Отдельное окно, которое показывает итоговый отчёт
    и позволяет сохранить его в файл.
    """

    def __init__(self, report_text: str):
        super().__init__()
        self.setWindowTitle("Отчёт")
        self.setGeometry(500, 300, 600, 400)

        layout = QVBoxLayout(self)

        # Текстовое поле с отчётом
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setText(report_text)
        layout.addWidget(self.text_area)

        # Кнопка сохранения
        save_btn = QPushButton("Отчеты загружены")
        save_btn.setFixedHeight(40)
        save_btn.setEnabled(False)
        layout.addWidget(save_btn)

    # def save_report(self):
    #     """Диалог сохранения отчёта в md или pdf."""
    #     file_path, _ = QFileDialog.getSaveFileName(
    #         self, "Загрузить отчёты", "", "Markdown (*.md);;PDF (*.pdf)"
    #     )
    #     if file_path:
    #         with open(file_path, "w", encoding="utf-8") as f:
    #             f.write(self.text_area.toPlainText())
    #         QMessageBox.information(
    #             self, "Сохранено", f"Отчёт успешно сохранён:\n{file_path}"
    #         )


# ===============================================================
#                     ТЕМЫ UI (CSS-СТИЛИ)
# ===============================================================

# Светлая тема
LIGHT_STYLE = """
QWidget { background-color: #faf8ff; color: #000000; }
QPushButton { background-color: #e7e8f5; border: 1px solid #b5bfff; border-radius: 5px; padding: 6px; color: #000000; }
QPushButton:hover { background-color: #d8d9ef; }
QRadioButton { color: #000000; font-size: 13px; background-color: #faf8ff; }
QLabel { color: #000000; }
QMenuBar { background-color: #dddffe; color: #000000; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; padding: 0px; min-height: 15px; font-size: 12px; }
QMenuBar::item { spacing: 6px; padding: 4px 12px; border-right: 1px solid #b5bfff; }
QMenuBar::item:selected { background-color: #e7e8f5; border-right: 1px solid #000000; }
QDialog { background-color: #faf8ff; color: #000000; }
QDialog QPushButton { background-color: #e7e8f5; color: #000000; border: 1px solid #b5bfff; border-radius: 5px; padding: 6px; }
"""

# Тёмная тема
DARK_STYLE = """
QWidget { background-color: #1e1e1e; color: #f0f0f0; }
QMainWindow { background-color: #1e1e1e; }
QPushButton { background-color: #3c3c3c; border: 1px solid #5a5a5a; border-radius: 5px; padding: 6px; color: #ffffff; }
QPushButton:hover { background-color: #5a5a5a; }
QLabel { color: #f0f0f0; }
QRadioButton { color: #f0f0f0; background-color: #1e1e1e; }
QTextEdit { background-color: #2b2b2b; color: #f0f0f0; border: 1px solid #444; border-radius: 6px; }
QMenuBar { background-color: #181818; color: #e0e0e0; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px; padding: 2px; min-height: 15px; font-size: 12px; }
QMenuBar::item { spacing: 6px; padding: 4px 12px; border-right: 1px solid #5a5a5a; }
QDialog { background-color: #1e1e1e; color: #f0f0f0; }
QDialog QPushButton { background-color: #3c3c3c; color: #ffffff; border: 1px solid #5a5a5a; border-radius: 5px; padding: 6px; }
"""


# ===============================================================
#                        ГЛАВНОЕ ОКНО
# ===============================================================


class MainWindow(QMainWindow):
    """Главное окно программы."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Файловый анализатор")
        self.setGeometry(400, 200, 450, 350)

        # Текущие настройки
        self.theme_mode = "light"
        self.df = None
        self.class_type = None
        self.model_type = None

        # QSettings для сохранения выбранной темы
        self.settings = QSettings("MyApps", "ReviewAnalyzer")

        self._build_ui()  # построить интерфейс
        self._create_menu()  # создать меню

    # -----------------------------------------------------------
    #                ПОСТРОЕНИЕ ГЛАВНОГО UI
    # -----------------------------------------------------------

    def _build_ui(self):
        central = QWidget()
        layout = QVBoxLayout(central)

        # Заголовок
        title = QLabel("Анализатор отзывов")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 35px;")
        layout.addWidget(title)

        # Зона перетаскивания
        self.drop_label = QLabel("Перетащите сюда файл")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_label.setFixedHeight(110)
        self.drop_label.setStyleSheet(
            "border: 2px dashed #a0a0a0; border-radius: 8px; font-size: 14px; padding: 20px;"
        )
        layout.addWidget(self.drop_label)

        # Кнопка выбора файла
        select_btn = QPushButton("Выбрать файл")
        select_btn.setFixedHeight(38)
        select_btn.clicked.connect(self.select_file)
        layout.addWidget(select_btn)

        # Кнопка получения отчёта
        self.report_btn = QPushButton("Получить отчёт")
        self.report_btn.setFixedHeight(38)
        self.report_btn.setEnabled(False)  # активна только когда загружён файл
        self.report_btn.clicked.connect(self.prepare_report)
        layout.addWidget(self.report_btn)

        self.setCentralWidget(central)
        self.setAcceptDrops(True)  # разрешить drag&drop

    # -----------------------------------------------------------
    #                        МЕНЮ
    # -----------------------------------------------------------

    def _create_menu(self):
        """Создаёт верхнее меню."""
        menu_bar = QMenuBar(self)

        # Переключение темы
        self.theme_action = QAction("Светлая тема", self)
        self.theme_action.triggered.connect(self.toggle_theme)
        menu_bar.addAction(self.theme_action)

        # О программе
        info_action = QAction("О программе", self)
        info_action.triggered.connect(self.show_info)
        menu_bar.addAction(info_action)

        self.setMenuBar(menu_bar)

    # -----------------------------------------------------------
    #                 DRAG & DROP ФАЙЛОВ
    # -----------------------------------------------------------

    def dragEnterEvent(self, event):
        """Разрешаем перетаскивать только файлы."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Обработка перетаскивания файла в окно."""
        path = event.mimeData().urls()[0].toLocalFile()
        self.load_file(path)

    # -----------------------------------------------------------
    #                ОБРАБОТКА ВЫБОРА ФАЙЛА
    # -----------------------------------------------------------

    def select_file(self):
        """Выбор файла через диалог."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Все файлы (*.*)"
        )
        if path:
            self.df = read_file(path)
            self.drop_label.setText(f"Выбран файл: {os.path.basename(path)}")
            self.report_btn.setEnabled(True)
            self._update_report_style()

    def load_file(self, path: str):
        """Загрузка файла при перетаскивании."""
        try:
            self.df = Reader().read_file(path)
            if self.df is None or self.df.empty:
                QMessageBox.warning(
                    self, "Ошибка", "Файл нельзя прочитать или он пуст."
                )
                return

            self.drop_label.setText(f"Выбран файл: {os.path.basename(path)}")
            self.report_btn.setEnabled(True)
            self._update_report_style()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    # -----------------------------------------------------------
    #                СОЗДАНИЕ ОТЧЁТА
    # -----------------------------------------------------------

    def prepare_report(self):
        """Открывает диалог выбора количества классов."""
        dlg = ClassSelectionDialog(self)
        if dlg.exec():
            self.class_type = dlg.selected_type
            self.model_type = self._map_class_type(self.class_type)
            self.generate_report()

    def generate_report(self):
        """Запуск классификации + открытие окна отчёта."""
        if self.df is None:
            QMessageBox.warning(self, "Ошибка", "Файл не загружен.")
            return

        try:
            result = classify(self.df, self.class_type)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка API", str(e))
            return

        report_text = make_report(result)
        self.rep_win = ReportWindow(report_text)
        self.rep_win.show()

    def _map_class_type(self, text: str) -> str:
        """Преобразует '2 класса' → название модели."""
        if "2" in text:
            return "lstm"
        if "3" in text:
            return "rt2_3cls"
        if "5" in text:
            return "rt2_5cls"
        return "log_reg"

    # -----------------------------------------------------------
    #                      ТЕМЫ И СТИЛИ
    # -----------------------------------------------------------

    def toggle_theme(self):
        """Переключение между светлой и тёмной темой."""
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self._apply_theme()
        self.settings.setValue("theme", self.theme_mode)
        self.theme_action.setText(
            "Тёмная тема" if self.theme_mode == "dark" else "Светлая тема"
        )

    def _apply_theme(self):
        app = QApplication.instance()
        app.setStyleSheet("")
        self.setStyleSheet("")

        # Применение палитры
        if self.theme_mode == "light":
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#faf8ff"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#000000"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#e7e8f5"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#000000"))
            app.setPalette(palette)
            app.setStyleSheet(LIGHT_STYLE)

        else:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#1f1f1f"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#f0f0f0"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#3c3c3c"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#5a8dee"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            app.setPalette(palette)
            app.setStyleSheet(DARK_STYLE)

        # Каждый top-level виджет должен получить новый стиль
        for w in QApplication.instance().topLevelWidgets():
            w.setPalette(app.palette())
            w.setStyleSheet(app.styleSheet())

        # Обновляем стиль кнопки отчёта
        self._update_report_style()

    def _update_report_style(self):
        """Перекрашивает кнопку отчёта под тему и состояние."""
        if not hasattr(self, "report_btn"):
            return

        if self.report_btn.isEnabled():
            if self.theme_mode == "light":
                self.report_btn.setStyleSheet(
                    "background-color: #b79cff; color: #ffffff; border-radius: 6px; border: none;"
                )
            else:
                self.report_btn.setStyleSheet(
                    "background-color: #3399ff; color: #f1f1f1; border-radius: 6px; border: none;"
                )
        else:
            if self.theme_mode == "light":
                self.report_btn.setStyleSheet(
                    "background-color: #faf8ff; color: #999999; border-radius: 5px;"
                )
            else:
                self.report_btn.setStyleSheet(
                    "background-color: #2b2d30; color: #777; border-radius: 5px;"
                )

    # -----------------------------------------------------------
    #                    О ПРОГРАММЕ
    # -----------------------------------------------------------

    def show_info(self):
        """Показывает окно 'О программе'."""
        msg = QMessageBox(self)
        msg.setWindowTitle("О программе")
        msg.setText(
            "Файловый анализатор v3.0\n\n"
            "Программа для анализа текстовых файлов и генерации отчётов.\n"
        )
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


# ===============================================================
#                   ТОЧКА ВХОДА В ПРОГРАММУ
# ===============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))

    window = MainWindow()

    saved_theme = QSettings("MyApps", "ReviewAnalyzer").value("theme", "light")
    window.theme_mode = (
        saved_theme if isinstance(saved_theme, str) else str(saved_theme)
    )
    window._apply_theme()

    window.show()
    sys.exit(app.exec())
