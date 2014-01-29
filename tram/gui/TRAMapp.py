'''
Created on Jan 29, 2014

@author: alessioferrari


'''
from Tkconstants import W, E, N, S, END
from Tkinter import Tk, BOTH, Text, StringVar, Listbox
from ttk import Frame, Button, Style, Label, Entry, Combobox, \
    LabelFrame

class TRAMapp(Frame):
    '''
    classdocs
    '''
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("TRAM")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        #Model Text
        t = Text(self, borderwidth=3, relief="sunken")
        t.config(font=("consolas", 12), undo=True, wrap='word')
        t.grid(row=0, column=0, padx=2, pady=2, sticky=(N, W, E, S))
        
        
        
        #Search Panel
        searchPanel = LabelFrame(self, text="Find your model")
        searchPanel.grid(row=0, column=1, padx=2, pady=2, sticky=N) 
        
        Label(searchPanel, text="Model name").grid(row=0, column=0, padx=2, pady=2, sticky=W)
        searchQuery = Entry(searchPanel)
        searchQuery.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        
        Label(searchPanel, text="Transformation").grid(row=1, column=0, padx=2, pady=2, sticky=W)
        preferredTransformation = StringVar()
        box = Combobox(searchPanel, textvariable=preferredTransformation, state='readonly')
        box['values'] = ('Any...', 'Object Change', 'Object Extension', 'Specialization', 'Functionality Extension', 'System Extension', 'Soft Simplification', 'Hard Simplification')
        box.current(0)
        box.grid(row=1, column=1, padx=2, pady=2, sticky=W)
        
        findButton = Button(searchPanel, text="Find")
        findButton.grid(row=2, column=1, sticky=E)
        
        #Listbox with recommendations
        recommendationPanel = LabelFrame(self, text="Recommended models")
        recommendationPanel.grid(row=0, column=1, padx=2, pady=2, sticky=(W,E,S))
        l = Listbox(recommendationPanel)
        l.pack(fill=BOTH, expand=1)
        l.insert(END, 'Model | Transformation')
        
def main():
  
    root = Tk()
    app = TRAMapp(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
    