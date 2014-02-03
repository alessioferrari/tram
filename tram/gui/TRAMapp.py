'''
Created on Jan 29, 2014

@author: alessioferrari


'''
from ModelIndexManager import ModelIndexManager
from ModelTransformer import ModelTransformer
from QueryManager import QueryManager
from RequirementsModelLoader import RequirementsModelLoader
from Tkconstants import W, E, N, S, END
from Tkinter import Tk, BOTH, Text, StringVar, Listbox
from UserManager import UserManager
from gui.ObjectChangeWizard import ObjectChangeWizard
from ttk import Frame, Button, Style, Label, Entry, Combobox, LabelFrame

class TRAMapp(Frame):
    '''
    classdocs
    '''
  
    def __init__(self, parent, userManager):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.userManager = userManager
        
        self.searchQuery = StringVar()
        self.recommendationList = list()
        
        
        self.initUI()
        
    def __findModels(self):
        '''
        The function finds the models and the transformations associated 
        to the specification query written in the searchQuery variable.
        the results are rendered according to the structure of
        the QueryResultList class  
        '''
        self.recommendationList = self.userManager.issueQuery(self.searchQuery.get())
        
        for recommendation in self.recommendationList:
            
            item = recommendation.getModelInfo().getName() + ' (' \
            + ', '.join(recommendation.getTransformationList()) + ') ' \
            + ' SCORE: ' + str(recommendation.getScore())
            
            self.l.insert(END, item)
            
    def __transformModel(self):
        '''
        The function takes the item that has been selected from the list
        of recommended models and transformations and applies the
        transformation to the model
        '''
        print self.l.get(self.l.curselection()[0])
        o = ObjectChangeWizard(self)
        
    def __loadSelectedModel(self):
        '''
        The function loads the model currently selected.
        The model is identified according to its position in the recommendationList
        '''
        selected = self.l.curselection()[0]
        modelPath = self.recommendationList[int(selected)].getModelInfo().getLocation()
        
        # here we load the actual input file
        fp = open(modelPath, 'r')
        file_text = fp.read()
        self.t.insert('0.0', file_text)
        fp.close()
        
        
    def initUI(self):
      
        self.parent.title("TRAM")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        #Model Text
        self.t = Text(self, borderwidth=3, relief="sunken")
        self.t.config(font=("consolas", 12), undo=True, wrap='word')
        self.t.grid(row=0, column=0, padx=2, pady=2, sticky=(N, W, E, S))
        
        
        
        #Search Panel
        searchPanel = LabelFrame(self, text="Find your model")
        searchPanel.grid(row=0, column=1, padx=2, pady=2, sticky=N) 
        
        Label(searchPanel, text="Model name").grid(row=0, column=0, padx=2, pady=2, sticky=W)
        
        searchQueryEntry = Entry(searchPanel, textvariable=self.searchQuery)
        searchQueryEntry.grid(row=0, column=1, padx=2, pady=2, sticky=W)
        
        Label(searchPanel, text="Transformation").grid(row=1, column=0, padx=2, pady=2, sticky=W)
        preferredTransformation = StringVar()
        box = Combobox(searchPanel, textvariable=preferredTransformation, state='readonly')
        box['values'] = ('Any...', 'Object Change', 'Object Extension', 'Specialization', 'Functionality Extension', 'System Extension', 'Soft Simplification', 'Hard Simplification')
        box.current(0)
        box.grid(row=1, column=1, padx=2, pady=2, sticky=W)
        
        findButton = Button(searchPanel, text="Find", command = self.__findModels)
        findButton.grid(row=2, column=1, padx=2, pady=2, sticky=E)
        
        #Listbox with recommendations
        recommendationPanel = LabelFrame(self, text="Recommended models (transformations)")
        recommendationPanel.grid(row=0, column=1, padx=2, pady=2, sticky=(W,E,S))
        self.l = Listbox(recommendationPanel)
        self.l.pack(fill=BOTH, expand=1)
        
        #Button frame
        transformButtonPanel = Frame(recommendationPanel)
        transformButtonPanel.pack(fill=BOTH, expand=1)
        
        viewButton = Button(transformButtonPanel, text="View", command = self.__loadSelectedModel)
        viewButton.grid(row=1, column=0, padx=2, pady=2)
        
        transformButton = Button(transformButtonPanel, text="Transform", command = self.__transformModel)
        transformButton.grid(row=1, column=2, padx=2, pady=2)

        
def main():
  
    f = RequirementsModelLoader('../models')  
    modelIndexManager = ModelIndexManager(f)        
    q = QueryManager(modelIndexManager)
    m = ModelTransformer(f)
    u = UserManager(q, m)  
    root = Tk()
    app = TRAMapp(root, u)
    root.mainloop()  


if __name__ == '__main__':
    main()  
    