# @Author: Marcel Maluta
# @Date:   2022-03-11T15:39:02+01:00
# @Email:  marcelmaluta@gmail.com
# @Last modified by:   Marcel Maluta
# @Last modified time: 2022-03-27T19:19:30+02:00



import wx
import wx.lib.scrolledpanel
import random
import socket
from threading import Thread
from datetime import datetime

class ChatPanel(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent, size=(640, 400), pos=(0, 28), style=wx.SIMPLE_BORDER)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = ""
        self.textbox = self.addMessage("")
        self.SetSizer(self.main_sizer)

    def addText(self, message):
        self.text += f"{message}\n"
        self.textbox.SetLabel(self.text)
        self.Layout()
        self.SetupScrolling(scrollToTop=False)
        self.Scroll((0, 100000))

    def addMessage(self, message, color=(0, 0, 0)):
        text = wx.StaticText(self, -1, message)
        text.SetForegroundColour(wx.Colour(color))
        self.main_sizer.Add(text, 0, wx.ALL, 1)
        return text

class MessagePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, "Nachricht:")
        self.main_sizer.Add(text, 0, wx.ALL, 1)

        self.message = wx.TextCtrl(self, -1, size = (585, 100), style = wx.TE_MULTILINE | wx.SUNKEN_BORDER | wx.TE_PROCESS_ENTER)
        self.main_sizer.Add(self.message, 0, wx.ALL, 1)

        self.SetSizer(self.main_sizer)


class ChatFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Chat", size=wx.Size(655, 600), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Das GUI aufbauen
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.chat = ChatPanel(self.panel)
        messageBox = MessagePanel(self.panel)
        btn = wx.Button(self.panel, label = "Abschicken")
        self.textctrl = messageBox.message
        btn.Bind(wx.EVT_BUTTON, self.onSubmit)
        self.textctrl.Bind(wx.EVT_TEXT_ENTER, self.onSubmit)
        main_sizer.Add(self.chat)
        main_sizer.Add(messageBox)
        main_sizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        self.panel.SetSizer(main_sizer)
        self.Show()

        # Name abfragen
        dialog = wx.TextEntryDialog(self, "Gib deinen Namen ein")
        if dialog.ShowModal() == wx.ID_OK:
            if(len(dialog.GetValue()) != 0):
                print(f"Name: {dialog.GetValue()}")
                self.name = dialog.GetValue()
                self.sock = initializeSocket(self.chat)
            else:
                print("Du musst einen Namen eingeben!")
                self.Destroy()
        else:
            self.Destroy()

    def onSubmit(self, event):
        message = self.textctrl.GetValue()
        seperator_token = "<SEP>"
        date_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        message = f"[{date_now}] {self.name}{seperator_token}{message}"
        self.sock.send(message.encode())
        self.textctrl.SetValue("")

def initializeSocket(chat):
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = 5002

    s = socket.socket()
    chat.addText(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}")
    s.connect((SERVER_HOST, SERVER_PORT))
    chat.addText("[*] Connected.")

    def listenForMessages():
        while True:
            message = s.recv(1024).decode()
            chat.addText(message)

    t = Thread(target=listenForMessages)
    t.daemon = True
    t.start()
    return s

if __name__ == '__main__':
    app = wx.App(False)
    frame = ChatFrame()
    app.MainLoop()
