import time

import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice

#Подключение к Com порту

app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("XY")
#Установка скорости получение данных с датчиков
serial = QSerialPort()
serial.setBaudRate(2000000)
#Выбор и подключение к датчику
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)


def onRead():
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    #print(data)
    line = data[0].split(':')
    id=data[0].split(':')[line.__len__()-1].strip()
    if(id.__len__()<4):
        tx = str('1')
        serial.write(tx.encode())
        print("error")
        return
#Отправка данных полученных с датчика температуры
    #print('line[0]', line[0])
    if (line[0] == '1'):
        temp = "Temp" + id
        print(temp)
        url = 'http://127.0.0.1:8000/api/p_temp/?format=json'
        payload = {'guid': "1", 'types': 'temperature', 'meaning': id}
        r = requests.post(url=url, data=payload)
        print(r)

#Отправка данных полученных с датчика влажности
    if (line[0] == '2'):
        humd = "Humidity" + id
        print(humd)
        url = 'http://127.0.0.1:8000/api/p_humidity/?format=json'
        payload = {'guid': "1", 'types': 'humidity', 'meaning': id}
        r = requests.post(url=url, data=payload)
        print(r)

#Отправка данных полученных с датчика Аммиака
    if (line[0] == '3'):
        ammon = "Ammonia" + id
        print(ammon)
        url = 'http://127.0.0.1:8000/api/p_ammonia/?format=json'
        payload = {'guid': "1", 'types': 'ammonia', 'meaning': id}
        r = requests.post(url=url, data=payload)
        print(r)

#Отправка данных полученных с датчика СО2
    if (line[0] == '4'):
        diox = "Diox" + id
        print(diox)
        url = 'http://127.0.0.1:8000/api/p_Dioxide/?format=json'
        payload = {'guid': "1", 'types': 'diox', 'meaning': id}
        r = requests.post(url=url, data=payload)
        print(r)


def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)


def onClose():
    serial.close()


serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.show()
app.exec()