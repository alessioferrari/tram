'''
Created on Feb 3, 2014

@author: alessioferrari
'''
from Tkconstants import END
from Tkinter import Tk
from gui import tkSimpleDialog
from ttk import Label, Entry, Button



class ObjectChangeWizard(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Object Change transformation").grid(row=0)
        Label(master, text="Old Object is").grid(row=1)
        Label(master, text="New Object is").grid(row=2)

        self.e1 = Entry(master)
        self.e1.delete(0, END)
        self.e1.insert(0, self.data[0])
        self.e2 = Entry(master)

        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = str(self.e1.get())
        second = str(self.e2.get())
        self.result['oldObjectString'] = first
        self.result['newObjectString'] = second

    #def getResult(self):
    #    return self.result
#root = Tk()
#Button(root, text="Hello!").pack()
#root.update()

#d = ObjectChangeWizard(root)

#root.wait_window(d)