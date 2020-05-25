import apiai
import json
import asyncio
from asyncio import transports

from PySide2.QtWidgets import QMainWindow, QApplication
from asyncqt import QEventLoop

from day3.interface import Ui_MainWindow

class ClientProtocol(asyncio.Protocol):
    transport: transports.Transport
    window: 'MainWindow'

    def __init__(self, chat_window: 'MainWindow'):
        self.window = chat_window

    def data_received(self, data: bytes):
        decoded = data.decode()
        self.window.append_text(decoded)
    def send_data(self, message: str):
        encoded = message.encode()
        self.transport.write(encoded)

        request = apiai.ApiAI('51d0db55271a40e79439cac98e13fbb3').text_request()
        request.lang = 'ru'
        request.session_id = 'session_1'
        request.query = message
        response = json.loads(request.getresponse().read().decode('utf-8'))
        print(response['result']['fulfillment']['speech'])
        return response['result']['action']

    def connection_made(self, transport: transports.Transport):
        self.window.append_text("Connected")
        self.transport = transport

    def connection_lost(self, exception):
        self.window.append_text("Disconnected")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.message_button.clicked.connect(self.button_handler)

    def button_handler(self, response):
         message_text = self.response()
         self.message_input.clear()
         self.protocol.send_data(message_text)


    def append_text(self, content: str):
        request = apiai.ApiAI('51d0db55271a40e79439cac98e13fbb3').text_request()
        request.lang = 'ru'
        request.session_id = 'session_1'
        request.query = content
        response = json.loads(request.getresponse().read().decode('utf-8'))
        print(response['result']['fulfillment']['speech'])
        return response['result']['action']
        self.message_box.response

    def build_protocol(self):
        self.protocol = ClientProtocol(self)
        return self.protocol

    async def start(self):
        self.show()

        event_loop = asyncio.get_running_loop()

        coroutine = event_loop.create_connection(
            self.build_protocol,
            "127.0.0.1",
            "9999"
        )

        await asyncio.wait_for(coroutine, 1000)

app = QApplication()
loop = QEventLoop(app)
asyncio.set_event_loop(loop)

window = MainWindow()

loop.create_task(window.start())
loop.run_forever()

