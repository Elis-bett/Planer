import sys
import datetime as dt
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QPlainTextEdit, QInputDialog
import speech_recognition as sr
import pyaudio
import wave
import sqlite3
import random

theday = dt.date.today()
weekday = theday.isoweekday()
start = theday - dt.timedelta(days=weekday)
dates = [start + dt.timedelta(days=d) for d in range(1, 8)]


def f():
    #Функция для записи и распознавания речи
    CHUNK = 1024
    FRT = pyaudio.paInt16
    CHAN = 1
    RT = 44100
    REC_SEC = 8
    OUTPUT = "output.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FRT, channels=CHAN, rate=RT, input=True, frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RT / CHUNK * REC_SEC)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(p.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
    w.close()
    r = sr.Recognizer()
    harvard = sr.AudioFile('output.wav')
    with harvard as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="ru-RU")


f = open('phrases', mode='rt', encoding='utf8')
sp = []
for line in f.readlines():
    sp.append(line)


class Planer(QMainWindow):
    # класс для работы с главным окном

    def __init__(self):
        super().__init__()
        uic.loadUi("planer1.ui", self)

        self.pushButton.clicked.connect(self.count)
        self.pushButton_2.clicked.connect(self.count_a)
        self.pushButton_3.clicked.connect(self.updt)
        self.label_12.setText(f'  {dates[0].strftime("%a %d")}')
        self.label_15.setText(f'  {dates[1].strftime("%a %d")}')
        self.label_14.setText(f'  {dates[2].strftime("%a %d")}')
        self.label_11.setText(f'  {dates[3].strftime("%a %d")}')
        self.label_16.setText(f'  {dates[4].strftime("%a %d")}')
        self.label_10.setText(f'  {dates[5].strftime("%a %d")}')
        self.label_13.setText(f'  {dates[6].strftime("%a %d")}')
        self.label_18.setText(f'  {random.choice(sp)}')
        self.plans()
        self.notif()

    def notif(self):
        self.listWidget_8.addItem('Завтра у вас:')
        a = 6
        delta_time1 = dt.timedelta(days=1)
        dat = dt.date.today() + delta_time1
        con = sqlite3.connect("Notes_planer.db")
        cursor = con.cursor()
        result = cursor.execute(f'''
                                SELECT Note FROM Notes
                                WHERE date = "{dat.strftime("%d.%m.%Y")}"
                                AND Notes.categories_id = "{a}"
                            ''').fetchall()
        for el in result:
            self.listWidget_8.addItem(f'  {el[0]}')
        con.commit()
        con.close()

    def updt(self):
        self.listWidget_2.clear()
        self.listWidget_4.clear()
        self.listWidget_5.clear()
        self.listWidget_7.clear()
        self.listWidget_6.clear()
        self.listWidget_3.clear()
        self.listWidget.clear()
        self.plans()
        
        self.listWidget_8.clear()
        self.listWidget_8.addItem('Завтра у вас:')
        a = 6
        delta_time1 = dt.timedelta(days=1)
        dat = dt.date.today() + delta_time1
        con = sqlite3.connect("Notes_planer.db")
        cursor = con.cursor()
        result = cursor.execute(f'''
                                        SELECT Note FROM Notes
                                        WHERE date = "{dat.strftime("%d.%m.%Y")}"
                                        AND Notes.categories_id = "{a}"
                                    ''').fetchall()
        for el in result:
            self.listWidget_8.addItem(f'  {el[0]}')
        con.commit()
        con.close()

    def plans(self):
        a = 5
        sp = []
        sp.append(self.listWidget_2)
        sp.append(self.listWidget_4)
        sp.append(self.listWidget_5)
        sp.append(self.listWidget_7)
        sp.append(self.listWidget_6)
        sp.append(self.listWidget_3)
        sp.append(self.listWidget)
        for i in range(7):
            dat = dates[i].strftime("%d.%m.%Y")
            con = sqlite3.connect("Notes_planer.db")
            cursor = con.cursor()
            result = cursor.execute(f'''
                        SELECT Note FROM Notes
                        WHERE date = "{dat}"
                        AND Notes.categories_id = "{a}"
                    ''').fetchall()
            for el in result:
                sp[i].addItem(el[0])

    def count_a(self):
        self.second = Calendar(self)
        self.second.show()

    def count(self):
        self.second = Notes(self)
        self.second.show()


class Notes(QtWidgets.QMainWindow):
    # класс для работы с окном заметок

    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        uic.loadUi("notes1.ui", self)

        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.count)
        self.pushButton_3.clicked.connect(self.search)
        self.pixmap = QPixmap("0_x2sBgmqVE4_xDagl_.png")
        self.label_4.setPixmap(self.pixmap)

    def save(self):
        answ, ok_pressed = QInputDialog.getItem(
            self, "Сохранение", "Вы уверены?",
            ("Да", "Нет"), 1, False)
        if self.radioButton.isChecked():
            a = 1
        elif self.radioButton_4.isChecked():
            a = 2
        elif self.radioButton_2.isChecked():
            a = 3
        elif self.radioButton_3.isChecked():
            a = 4
        if ok_pressed and answ == "Да":
            text = self.textEdit_4.toPlainText().capitalize()
            dat = dt.date.today().strftime("%d.%m.%Y")
            con = sqlite3.connect("Notes_planer.db")
            cursor = con.cursor()
            cursor.execute(f"INSERT INTO Notes(categories_id,Note,date) VALUES({a},'{text}','{dat}')")
            con.commit()
            con.close()

    def count(self):
        self.textEdit_4.setPlainText(f())

    def search(self):
        self.listWidget.clear()
        text = self.textEdit_2.toPlainText().capitalize()
        dat = self.textEdit_3.toPlainText()
        con = sqlite3.connect("Notes_planer.db")
        cursor = con.cursor()
        result = cursor.execute(f'''
            SELECT Note FROM Notes
            WHERE date = "{dat}"
            AND Notes.categories_id IN(
                SELECT id FROM Category
                WHERE Categories = "{text}"
            )
        ''').fetchall()
        for el in result:
            self.listWidget.addItem(el[0])
        con.close()


class Calendar(QtWidgets.QMainWindow):
    # класс для работы с окном календаря

    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        uic.loadUi("calendar1.ui", self)

        self.pushButton.clicked.connect(self.save)

    def save(self):
        answ, ok_pressed = QInputDialog.getItem(
            self, "Сохранение", "Сохранить как важные планы?",
            ("Да", "Нет"), 1, False)
        if ok_pressed:
            if answ == "Да":
                date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy")
                text = self.textEdit_4.toPlainText().capitalize()
                a = 6
                con = sqlite3.connect("Notes_planer.db")
                cursor = con.cursor()
                cursor.execute(f"INSERT INTO Notes(categories_id,Note,date) VALUES({a},'{text}','{date}')")
                con.commit()
                con.close()

            else:
                date = self.calendarWidget.selectedDate().toString("dd.MM.yyyy")
                text = self.textEdit_4.toPlainText().capitalize()
                a = 5
                con = sqlite3.connect("Notes_planer.db")
                cursor = con.cursor()
                cursor.execute(f"INSERT INTO Notes(categories_id,Note,date) VALUES({a},'{text}','{date}')")
                con.commit()
                con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Planer()
    ex.show()
    sys.exit(app.exec())
