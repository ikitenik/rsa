from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal, QThread
import pickle
from os import path, getcwd
from random import randint
import traceback
from sympy import isprime, gcd, mod_inverse

#текст или файл
class What_to_code(QDialog):
    my_signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(What_to_code, self).__init__()
        self.setWindowTitle('Текст или файл?')
        self.resize(400, 30)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 380, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setText("Выберите, что надо шифровать")

        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("Текст")
        self.comboBox.addItem("Файл")
        self.horizontalLayout.addWidget(self.comboBox)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Выбрать")
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton.clicked.connect(self.choice_type)

    def choice_type(self):
        self.my_signal.emit(self.comboBox.currentText())
        self.accept()

class Generator(QDialog):
    my_signal = QtCore.pyqtSignal(list)
    def __init__(self):
        super(Generator, self).__init__()
        self.setWindowTitle('Сгенерировать ключи')
        self.resize(400, 90)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 380, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setText("Введите простое число P")
        self.horizontalLayout.addWidget(self.label)

        self.p_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.p_line.setObjectName("p_line")
        self.horizontalLayout.addWidget(self.p_line)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 380, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Введите простое число Q")
        self.horizontalLayout_2.addWidget(self.label_2)

        self.q_line = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        self.q_line.setObjectName("q_line")
        self.horizontalLayout_2.addWidget(self.q_line)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 180, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Cгенерировать")

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 60, 190, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Cлучайные числа")

        self.pushButton.clicked.connect(self.generate_keys)
        self.pushButton_2.clicked.connect(self.random_numbers)

    def random_numbers(self):
        p = randint(100000000000000000000000, 999999999999999999999999)
        q = randint(100000000000000000000000, 999999999999999999999999)
        while(isprime(p) == False or isprime(q) == False):
            p = randint(100000000000000000000000, 999999999999999999999999)
            q = randint(100000000000000000000000, 999999999999999999999999)
        self.p_line.setText(str(p))
        self.q_line.setText(str(q))

    def generate_keys(self):
        try:
            if self.p_line.text() == "" or self.q_line.text() == "":
                self.my_signal.emit([0, 0, 0])
                self.accept()
                return

            p = int(self.p_line.text())
            q = int(self.q_line.text())
            if p == q:
                self.my_signal.emit([0, 0, 0])
                self.accept()
                return

            if isprime(p) == False or isprime(q) == False:
                self.my_signal.emit([0, 0, 0])
                self.accept()
                return

            n = p*q
            φ = (p-1)*(q-1)
            opened_key = randint(2, φ - 1)
            while gcd(opened_key, φ) != 1:
                opened_key = randint(2, φ - 1)
            closed_key = mod_inverse(opened_key, φ)
            self.my_signal.emit([opened_key, closed_key, n])
            self.accept()
        except:
            traceback.print_exc()

# фоновый процесс, в котором идет вычисление данных и посылка результата и единиц прогресса в главное окно
class WorkerThreadProgress(QThread):
    update_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.is_running = True

    def stop(self):
        self.is_running = False

    def run(self):
        try:
            i = 0
            while self.is_running:
                self.update_signal.emit(i)
                i += 1
                self.msleep(10)
        except:
            traceback.print_exc()

class WorkerThread(QThread):
    update_result = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    stop_progress = pyqtSignal(int)

    def __init__(self, data, param, key, p):
        super().__init__()
        # данные
        self.data = data
        # параметры шифрования
        self.param = param
        self.key = key
        self.p = p

    def run(self):
        try:

            if self.param == "encode":
                for i in range(len(self.data)):
                    if (self.data[i] >= self.p):
                        self.error_signal.emit("Модуль слишком маленький, шифрование невозможно")
                        return

                decimal_list_big = list(map(lambda x: pow(x, self.key, self.p), self.data))
                bytes_after_encrypt = pickle.dumps(decimal_list_big)
                decimal_list = list(map(lambda x: int(x), bytes_after_encrypt))
            else:
                bytes_before_decrypt = bytes(self.data)
                decimal_list_big = pickle.loads(bytes_before_decrypt)
                decimal_list = list(map(lambda x: pow(x, self.key, self.p), decimal_list_big))

            self.stop_progress.emit(1)
            self.update_result.emit(decimal_list)
        except:
            self.error_signal.emit("Проверьте корректность входных данных")
            traceback.print_exc()
            #return

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.temp_encoding = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸ0123456789"
        self.crypt_file_name = ""
        self.text_from_file = ""
        self.type = ""

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 610)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.input_text.setGeometry(QtCore.QRect(0, 30, 441, 221))
        self.input_text.setReadOnly(False)
        self.input_text.setObjectName("input_text")
        self.output_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.output_text.setGeometry(QtCore.QRect(0, 330, 891, 251))
        self.output_text.setReadOnly(True)
        self.output_text.setObjectName("output_text")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 260, 441, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.encode_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.encode_button.setObjectName("encode_button")
        self.horizontalLayout.addWidget(self.encode_button)
        self.decode_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.decode_button.setObjectName("decode_button")
        self.horizontalLayout.addWidget(self.decode_button)
        self.up_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.up_button.setObjectName("up_button")
        self.horizontalLayout.addWidget(self.up_button)
        self.clear_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear_button.setObjectName("clear_button")
        self.horizontalLayout.addWidget(self.clear_button)
        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(10, 10, 331, 16))
        self.message_label.setObjectName("message_label")
        self.opened_key_label = QtWidgets.QLabel(self.centralwidget)
        self.opened_key_label.setGeometry(QtCore.QRect(450, 30, 161, 16))
        self.opened_key_label.setObjectName("opened_key_label")
        self.opened_key_line = QtWidgets.QLineEdit(self.centralwidget)
        self.opened_key_line.setGeometry(QtCore.QRect(620, 30, 271, 22))
        self.opened_key_line.setObjectName("opened_key_line")
        self.modulo_opened_line = QtWidgets.QLineEdit(self.centralwidget)
        self.modulo_opened_line.setGeometry(QtCore.QRect(620, 60, 271, 22))
        self.modulo_opened_line.setText("")
        self.modulo_opened_line.setObjectName("modulo_opened_line")
        self.modulo_opened_label = QtWidgets.QLabel(self.centralwidget)
        self.modulo_opened_label.setGeometry(QtCore.QRect(450, 60, 151, 16))
        self.modulo_opened_label.setObjectName("modulo_opened_label")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(450, 90, 441, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.load_opened_key = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.load_opened_key.setObjectName("load_opened_key")
        self.horizontalLayout_2.addWidget(self.load_opened_key)
        self.save_opened_key = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.save_opened_key.setObjectName("save_opened_key")
        self.horizontalLayout_2.addWidget(self.save_opened_key)
        self.modulo_closed_label = QtWidgets.QLabel(self.centralwidget)
        self.modulo_closed_label.setGeometry(QtCore.QRect(450, 160, 191, 16))
        self.modulo_closed_label.setObjectName("modulo_closed_label")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(450, 190, 441, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.load_closed_key = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.load_closed_key.setObjectName("load_closed_key")
        self.horizontalLayout_4.addWidget(self.load_closed_key)
        self.save_closed_key = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.save_closed_key.setObjectName("save_closed_key")
        self.horizontalLayout_4.addWidget(self.save_closed_key)
        self.modulo_closed_line = QtWidgets.QLineEdit(self.centralwidget)
        self.modulo_closed_line.setGeometry(QtCore.QRect(620, 160, 271, 22))
        self.modulo_closed_line.setText("")
        self.modulo_closed_line.setObjectName("modulo_closed_line")
        self.closed_key_line = QtWidgets.QLineEdit(self.centralwidget)
        self.closed_key_line.setGeometry(QtCore.QRect(620, 130, 271, 22))
        self.closed_key_line.setObjectName("closed_key_line")
        self.closed_key_label = QtWidgets.QLabel(self.centralwidget)
        self.closed_key_label.setGeometry(QtCore.QRect(450, 130, 191, 16))
        self.closed_key_label.setObjectName("closed_key_label")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(450, 260, 441, 41))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.input_file_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.input_file_button.setObjectName("input_file_button")
        self.horizontalLayout_5.addWidget(self.input_file_button)
        self.input_file_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        self.input_file_name.setObjectName("input_file_name")
        self.horizontalLayout_5.addWidget(self.input_file_name)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(450, 220, 441, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.generate_label = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.generate_label.setObjectName("generate_label")
        self.horizontalLayout_6.addWidget(self.generate_label)
        self.generate_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.generate_button.setObjectName("generate_button")
        self.horizontalLayout_6.addWidget(self.generate_button)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 300, 930, 25))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.up_button.clicked.connect(self.up)
        self.clear_button.clicked.connect(self.clear)

        self.generate_button.clicked.connect(self.generator)
        self.load_opened_key.clicked.connect(lambda: self.load("открытый"))
        self.save_opened_key.clicked.connect(lambda: self.save("открытый"))
        self.load_closed_key.clicked.connect(lambda: self.load("закрытый"))
        self.save_closed_key.clicked.connect(lambda: self.save("закрытый"))

        self.encode_button.clicked.connect(lambda: self.code("encode"))
        self.decode_button.clicked.connect(lambda: self.code("decode"))
        self.input_file_button.clicked.connect(self.select_file)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def check_input(self, number):
        try:
            number = int(number)
            if number <= 1:
                return False
            return True
        except ValueError:
            return False

    def code(self, param):
        try:

            if (self.input_text.toPlainText() == "" and self.text_from_file == ""):
                self.error_input("Введите текст или выберите файл")
                return

            if (self.input_text.toPlainText() != "" and self.text_from_file != ""):
                self.what_to_code()

            if (self.input_text.toPlainText() == "" and self.text_from_file != ""):
                self.type = "Файл"

            if (self.input_text.toPlainText() != "" and self.text_from_file == ""):
                self.type = "Текст"

            if param == "encode":
                if self.opened_key_line.text() == "" or self.modulo_opened_line.text() == "" \
                        or self.check_input(self.opened_key_line.text()) == False \
                        or self.check_input(self.modulo_opened_line.text()) == False:
                    self.error_input("Введите открытый ключ и модуль или сгенерируйте ключи ")
                    return
            else:
                if self.closed_key_line.text() == "" or self.modulo_closed_line.text() == ""\
                        or self.check_input(self.closed_key_line.text()) == False \
                        or self.check_input(self.modulo_closed_line.text()) == False:
                    self.error_input("Введите закрытый ключ и модуль или сгенерируйте ключи ")
                    return

            self.text_input = ""
            if self.type == "Текст":
                text = self.input_text.toPlainText()
                if param == "encode":
                    self.text_input = self.utf8_to_decimal(text)
                else:
                    self.text_input = self.temp_encoding_to_decimal(text)

            else:
                self.text_input = list(map(lambda x: int(x), self.text_from_file))

            self.opened_key = int(self.opened_key_line.text())
            self.closed_key = int(self.closed_key_line.text())
            self.param_to_continue = param
            if param == "encode":
                self.worker_thread = WorkerThread(self.text_input, param, self.opened_key, int(self.modulo_opened_line.text()))
            else:
                self.worker_thread = WorkerThread(self.text_input, param, self.closed_key, int(self.modulo_closed_line.text()))
            self.worker_thread.update_result.connect(self.code_continue)
            self.worker_thread.stop_progress.connect(self.stop_thread)
            self.worker_thread.error_signal.connect(self.error_input)
            self.worker_thread.start()
            self.worker_thread_progress = WorkerThreadProgress()
            self.worker_thread_progress.update_signal.connect(self.progress_bar)
            self.worker_thread_progress.start()
        except:
            traceback.print_exc()

    def progress_bar(self, number):
        number_2 = number % 101
        self.progressBar.setValue(number_2)

    def stop_thread(self, param):
        self.worker_thread_progress.stop()
        self.progressBar.setValue(100)

    def code_continue(self, data):
        try:
            texter = ""
            decimal_list = data
            if self.type == "Текст":
                if self.param_to_continue == "encode":
                    texter = self.decimal_to_temp_encoding(decimal_list)
                else:
                    texter = self.decimal_to_utf8(decimal_list)

                self.output_text.setText(texter)
            else:
                temp_bytes = bytes(decimal_list)
                file_type = "зашифрованный"
                if self.param_to_continue == "decode":
                    file_type = "расшифрованный"

                file_name = ""
                file_extension = ""
                dot_pos = 0
                check = False
                for i in range(len(self.crypt_file_name) - 1, 0, - 1):
                    if check == False:
                        if self.crypt_file_name[i] == ".":
                            dot_pos = i
                            file_extension = self.crypt_file_name[i:]
                            check = True
                    if check == True:
                        if self.crypt_file_name[i] == "/":
                            file_name = self.crypt_file_name[i:dot_pos]
                            break

                file_name = file_name.replace(" (зашифрованный)", "")
                file_name = file_name.replace(" (расшифрованный)", "")
                if self.param_to_continue == "encode":
                    file_name += " (зашифрованный)"
                else:
                    file_name += " (расшифрованный)"
                cwd = getcwd()[2:].replace('\\', '/')
                file = QFileDialog.getSaveFileName(None, f"Сохранить {file_type} файл",
                                                   f"{cwd}/файлы/{file_name}",
                                                   f"(*{file_extension});;Все файлы (*)")[0]
                if file:
                    with open(file, 'wb') as f:
                        f.write(temp_bytes)
        except:
            traceback.print_exc()

    def generator(self):
        try:
            self.w2 = Generator()
            self.w2.my_signal.connect(self.get_keys)
            self.w2.exec_()
        except:
            traceback.print_exc()

    def get_keys(self, parameters):
        if parameters[0] == 0 and parameters[1] == 0 and parameters[2] == 0:
            self.error_input("P и Q должны быть простыми")
            return
        self.opened_key_line.setText(str(parameters[0]))
        self.closed_key_line.setText(str(parameters[1]))
        self.modulo_opened_line.setText(str(parameters[2]))
        self.modulo_closed_line.setText(str(parameters[2]))

    def what_to_code(self):
        self.w1 = What_to_code()
        self.w1.my_signal.connect(self.get_type)
        self.w1.exec_()

    def get_type(self, type):
        self.type = type

    def select_file(self):
        try:
            cwd = getcwd()[2:].replace('\\', '/')
            file = QFileDialog.getOpenFileName(None, f"Загрузить файл",
                                               f"{cwd}/файлы/1.txt")[0]
            if file == "":
                return

            self.input_file_name.setText(path.basename(file))
            file_in = open(file, 'rb')
            self.text_from_file = file_in.read()
            self.crypt_file_name = file
            file_in.close()
        except:
            traceback.print_exc()

    def load(self, param):
        file_type = "открытого ключа"
        file_name = "открытый ключ"
        if param == "закрытый":
            file_type = "закрытого ключа"
            file_name = "закрытый ключ"
        cwd = getcwd()[2:].replace('\\', '/')
        file = QFileDialog.getOpenFileName(None, f"Загрузить файл {file_type}",
                                           f"{cwd}/параметры/{file_name}_1.txt", "(*.txt)")[0]

        if file == "":
            return

        file_in = open(file, 'r')
        temp = file_in.read()
        for i in temp:
            if i not in ['0','1','2','3','4','5','6','7','8','9',' ']:
                self.error_input("Загружен неправильный ключ")
                return

        if temp.count(" ") != 1:
            self.error_input("Загружен неправильный ключ")
            return

        parameters = temp.split(" ")
        if param == "открытый":
            self.opened_key_line.setText(parameters[0])
            self.modulo_opened_line.setText(parameters[1])
        else:
            self.closed_key_line.setText(parameters[0])
            self.modulo_closed_line.setText(parameters[1])
        file_in.close()

    def save(self, param):
        self.closed_key = self.closed_key_line.text()
        self.opened_key = self.opened_key_line.text()
        if param == "закрытый":
            self.modulo = self.modulo_closed_line.text()
        else:
            self.modulo = self.modulo_opened_line.text()

        if self.modulo == "":
            self.error_input("Сначала введите модуль или сгенерируйте ключи")
            return

        file_type = "открытого ключа"
        file_name = "открытый ключ"
        if param == "закрытый":
            file_type = "секретного ключа"
            file_name = "секретный ключ"
            if self.closed_key == "":
                self.error_input("Сначала сгенерируйте или введите закрытый ключ")
                return
        else:
            if self.opened_key == "":
                self.error_input("Сначала сгенерируйте или введите открытый ключ")
                return
        cwd = getcwd()[2:].replace('\\', '/')
        file = \
        QFileDialog.getSaveFileName(None, f"Сохранить файл {file_type}",
                                    f"/{cwd}/параметры/{file_name}_1",
                                    "(*.txt)")[0]
        if file:
            with open(file, 'w') as f:
                if param == "открытый":
                    f.write(self.opened_key + " " + self.modulo)
                else:
                    f.write(self.closed_key + " " + self.modulo)

    def utf8_to_decimal(self, symbols):
        decimal_list = []
        for i in range(len(symbols)):
            decimal_list.append(ord(symbols[i]))
        return decimal_list

    def decimal_to_utf8(self, decimal_list):
        symbols = ""
        for i in range(len(decimal_list)):
            symbols += chr(decimal_list[i])
        return symbols

    def temp_encoding_to_decimal(self, symbols):
        decimal_list = []
        for i in range(len(symbols)):
            for j in range(len(self.temp_encoding)):
                if symbols[i] == self.temp_encoding[j]:
                    decimal_list.append(j)
                    break
        return decimal_list

    def decimal_to_temp_encoding(self, decimal_list):
        symbols = ""
        for i in decimal_list:
            symbols += self.temp_encoding[i]
        return symbols

    def up(self):
        self.input_text.setText(self.output_text.toPlainText())
        self.output_text.setText("")

    def clear(self):
        self.input_text.setText("")
        self.output_text.setText("")

    def error_input(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка ввода")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RSA"))
        self.encode_button.setText(_translate("MainWindow", "Зашифровать"))
        self.decode_button.setText(_translate("MainWindow", "Расшифровать"))
        self.up_button.setText(_translate("MainWindow", "Наверх"))
        self.clear_button.setText(_translate("MainWindow", "Очистить"))
        self.message_label.setText(_translate("MainWindow", "Введите сообщение"))
        self.opened_key_label.setText(_translate("MainWindow", "Введите открытый ключ"))
        self.modulo_opened_label.setText(_translate("MainWindow", "Введите модуль"))
        self.load_opened_key.setText(_translate("MainWindow", "Загрузить"))
        self.save_opened_key.setText(_translate("MainWindow", "Сохранить"))
        self.modulo_closed_label.setText(_translate("MainWindow", "Введите модуль"))
        self.load_closed_key.setText(_translate("MainWindow", "Загрузить"))
        self.save_closed_key.setText(_translate("MainWindow", "Сохранить"))
        self.closed_key_label.setText(_translate("MainWindow", "Введите закрытый ключ"))
        self.input_file_button.setText(_translate("MainWindow", "Введите файл"))
        self.generate_label.setText(_translate("MainWindow", "Сгенерировать ключи"))
        self.generate_button.setText(_translate("MainWindow", "Сгенерировать"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
