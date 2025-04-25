import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QPlainTextEdit,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

import requests  # type: ignore


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем вертикальную компоновку
        layout = QVBoxLayout()

        # Первое поле для текста

        # Создаем метку для первого поля
        self.text_for_simple_read = QLabel("Введите отзыв в поле ниже:")

        font = QFont("Helvetica", 12)  # Шрифт Helvetica, размер 12
        self.text_for_simple_read.setFont(font)
        self.text_for_simple_read.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_for_simple_read)

        # Создаем виджет QPlainTextEdit
        self.plain_text_edit = QPlainTextEdit()
        layout.addWidget(self.plain_text_edit)

        # Создаем кнопку для считывания текста
        self.button_read_text = QPushButton("Считать текст")
        font = QFont("Helvetica", 12)  # Шрифт Helvetica, размер 12
        self.button_read_text.setFont(font)
        self.button_read_text.setMinimumHeight(50)
        layout.addWidget(self.button_read_text)

        # Подключаем сигнал нажатия кнопки к слоту
        self.button_read_text.clicked.connect(self.read_text)

        # Второе поле для файла

        # Создаем метку для второго поля
        self.text_for_open_file = QLabel("ИЛИ\nОткройте текстовый файл с отзывами:")
        font = QFont("Helvetica", 12)  # Шрифт Helvetica, размер 12
        self.text_for_open_file.setFont(font)
        self.text_for_open_file.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_for_open_file)

        # Создаем кнопку для открытия файла
        self.button_open_file = QPushButton("Открыть файл")
        font = QFont("Helvetica", 12)  # Шрифт Helvetica, размер 12
        self.button_open_file.setFont(font)
        self.button_open_file.setMinimumHeight(50)
        layout.addWidget(self.button_open_file)

        # Подключаем сигнал нажатия кнопки к слоту
        self.button_open_file.clicked.connect(self.open_file)

        # ----------------------------------------------------------------

        # Третье поле для результата

        self.output: str = ""

        # Создаем метку для третьего поля
        self.text_for_result = QLabel("Результат:")
        font = QFont("Helvetica", 12)  # Шрифт Helvetica, размер 12
        self.text_for_result.setFont(font)
        self.text_for_result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_for_result)

        # Создаем виджет QLabel для отображения результата
        self.result = QLabel("")
        layout.addWidget(self.result)

        # Кнопка для сохранения результата
        self.button_save_result = QPushButton("Сохранить результат")
        font = QFont("Helvetica", 12)
        self.button_save_result.setFont(font)
        self.button_save_result.setMinimumHeight(50)
        self.button_save_result.setEnabled(False)
        layout.addWidget(self.button_save_result)

        # Подключаем сигнал нажатия кнопки к слоту
        self.button_save_result.clicked.connect(self.save_results)

        # Устанавливаем компоновку
        self.setLayout(layout)

        # Устанавливаем заголовок окна и показываем окно
        self.setWindowTitle("Анализатор")
        self.show()

    def save_results(self):
        # Сохраняем текст из QLabel в текстовый файл
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить результат", "", "Text Files (*.txt)"
        )
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(self.output)

    def read_text(self):
        # Считываем текст из QPlainTextEdit
        content = self.plain_text_edit.toPlainText()
        output = self.classify_all(content)

        # Отображаем результат в QLabel
        self.result.setText(output if len(output) < 42 else (output[:42] + "..."))

        # Сохраняем результат
        self.output = output
        # Делаем кнопку для сохранения активной
        self.button_save_result.setEnabled(True)

    def open_file(self):
        # Открываем текстовый файл
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Text Files (*.txt)"
        )

        if file_name:
            # Если файл выбран, считываем его содержимое
            with open(file_name, "r", encoding="utf-8") as file:
                content = file.read()
        else:
            return

        output = self.classify_all(content)

        # Отображаем результат в QLabel
        self.result.setText(output if len(output) < 42 else (output[:42] + "..."))

        # Сохраняем результат
        self.output = output
        # Делаем кнопку для сохранения активной
        self.button_save_result.setEnabled(True)

    def classify(self, review: str) -> str | None:
        # Отправляем текст на сервер и получаем результат
        try:
            api_url = r"http://localhost:8000/string/"
            param = {"review": review}
            response = requests.post(api_url, json=param)
        except requests.exceptions.RequestException as exception:
            self.show_error_message(
                message="Не удалось получить ответ от сервера",
                detailed_message=str(exception),
            )
            return None

        if response.status_code == 200:
            return response.json()["class_name"]
        else:
            self.show_error_message(
                f"Ошибка при обращении к серверу: {response.status_code}"
            )
            return None

    def classify_all(self, content: str) -> str:
        reviews = content.split("---")
        count = 0
        out = ""
        for review in reviews:
            count += 1
            # Классифицируем текст
            result = self.classify(review)
            if result is not None:
                out += f"{count}) {result}\n"
            else:
                out = "Ошибка во время работы программы"
                break
        return out

    def show_error_message(self, message: str, detailed_message: str = "") -> None:
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(message)
        if detailed_message:
            msg.setDetailedText(str(detailed_message))
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
