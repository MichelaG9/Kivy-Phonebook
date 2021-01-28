import sqlite3
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

popupWindow = ""

class NewContact(Screen):
    newcon = ObjectProperty(None)
    newnumber = ObjectProperty(None)

    def btn(self):
        name = self.newcon.text
        number = self.newnumber.text
        db.execute("INSERT INTO contacts (first_name, number) VALUES (?,?)", (name, number))
        db.commit()
        self.newcon.text = ""
        self.newnumber.text = ""
        self.showPopup()

    def showPopup(self):
        show = PopupNewCont()
        global popupWindow 
        popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(400,400))
        popupWindow.open()

    def closePopup(self):
        global popupWindow 
        popupWindow.dismiss()

class PopupNewCont(FloatLayout):
    pointer = NewContact()
    def closePop(self):
        self.pointer.closePopup()

class AllContacts(Screen):
    listall = ObjectProperty(None)
    def getAll(self):
        self.listall.text = ""
        cursor = db.execute("SELECT * FROM contacts").fetchall()
        for i in cursor:
            self.listall.text += str(i[1]) + " " + str(i[3]) + "\n"

    def goBack(self):
        self.listall.text = ""
    
class DeleteContact(Screen):
    todelete = ObjectProperty(None)
    def delete(self):
        name = self.todelete.text
        db.execute("DELETE FROM contacts WHERE first_name= ? ", (name,))
        db.commit()
        self.todelete.text = ""

class SearchContact(Screen):
    tosearch = ObjectProperty(None)
    result = ObjectProperty(None)
    def search(self):
        self.result.text = ""
        name = self.tosearch.text
        cursor = db.execute("SELECT * FROM contacts WHERE first_name= ? ", (name,)).fetchall()
        if len(cursor) == 0:
            self.result.text = "No results"
        for i in cursor:
            self.result.text += str(i[1]) + " " + str(i[3]) + "\n"
        self.tosearch.text = ""

    def goBack(self):
        self.result.text = ""

class MainWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class PhonebookApp(App):
    def build(self):
        return kv

kv = Builder.load_file("phonebook.kv")

db = sqlite3.connect("contacts.db")

""" db.execute(CREATE TABLE contacts (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(255),
    surname VARCHAR(255),
    number INTEGER
)
) """

def deleteAll():
    db.execute("DELETE FROM contacts")

def search():
    name = input("Name: ")
    cursor = db.execute("SELECT * FROM contacts WHERE first_name= ? ", (name,)).fetchall()
    print(cursor)

if __name__ == "__main__":
    PhonebookApp().run()