
import os
import time
import wx
import networkx as nx
import matplotlib.pyplot as plt

from kanonymity import *
#-------------------------------------------------------------------------------
# Define booleans until Python ver 2.3
True=1
False=0

APP_NAME = "IMS Data Privacy Demo"

# --- Menu and control ID's
ID_NEW=101
ID_OPEN=102
ID_SAVE=103
ID_SAVEAS=104
ID_EXIT=109
ID_ABOUT=141

ID_LOAD=142
ID_DRAW=143
ID_ANALYZE=144
ID_KANON=145
ID_DEGREE=146
ID_CLUSTER=147

ID_RTB=201

SB_INFO = 0
SB_ROWCOL = 1
SB_DATETIME = 2
#-------------------------------------------------------------------------------
class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None
 
    def __call__(cls, *args, **kw):
        if not cls.instance:
            # Not created or has been Destroyed
            obj = super(Singleton, cls).__call__(*args, **kw)
            cls.instance = obj
            cls.instance.SetupWindow()
 
        return cls.instance

class SingletonDialog(wx.Dialog):
    __metaclass__ = Singleton

    def SetupWindow(self):
        """Hook method for initializing window"""
        self.field = wx.TextCtrl(self)
        self.check = wx.CheckBox(self, label="Enable Foo")

        # Layout
        vsizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, label="FooBar")
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([(label, 0, wx.ALIGN_CENTER_VERTICAL),
                        ((5, 5), 0),
                        (self.field, 0, wx.EXPAND)])
        btnsz = self.CreateButtonSizer(wx.OK)
        btnsc = self.CreateButtonSizer(wx.CANCEL)
        vsizer.AddMany([(hsizer, 0, wx.ALL|wx.EXPAND, 10),
                        (self.check, 0, wx.ALL, 10),(btnsc, 0, wx.EXPAND|wx.ALL, 10),
                        (btnsz, 0, wx.EXPAND|wx.ALL, 10)])
        self.SetSizer(vsizer)
        self.SetInitialSize()

        

# --- our frame class
class dpFrame(wx.Frame):
    """ Derive a new class of wxFrame. """
    
    
    def __init__(self, parent, id, title):
        # --- a basic window frame/form
        wx.Frame.__init__(self, parent = None, id = -1,
                         title = APP_NAME +  "wxPython App",
                         pos = wx.Point(200, 200), size = wx.Size(379, 207),
                         name = '', style = wx.DEFAULT_FRAME_STYLE)

        # --- real windows programs have icons, so here's ours!
        # XXX see about integrating this into our app or a resource file
        try:            # - don't sweat it if it doesn't load
            self.SetIcon(wx.Icon("face-monkey.png", wx.BITMAP_TYPE_PNG))
            pass
        finally:
            pass

        # --- add a menu, first build the menus (with accelerators
        fileMenu = wx.Menu()

        fileMenu.Append(ID_NEW, "&New\tCtrl+N", "Creates a new file")
        wx.EVT_MENU(self, ID_NEW, self.OnFileNew)
        fileMenu.Append(ID_OPEN, "&Open\tCtrl+O", "Opens an existing file")
        wx.EVT_MENU(self, ID_OPEN, self.OnFileOpen)
        fileMenu.Append(ID_SAVE, "&Save\tCtrl+S", "Save the active file")
        wx.EVT_MENU(self, ID_SAVE, self.OnFileSave)
        fileMenu.Append(ID_SAVEAS, "Save &As...", "Save the active file with a new name")
        wx.EVT_MENU(self, ID_SAVEAS, self.OnFileSaveAs)

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, "E&xit\tAlt+Q", "Exit the program")
        wx.EVT_MENU(self, ID_EXIT, self.OnFileExit)
        
        graphMenu=wx.Menu()
        graphMenu.Append(ID_LOAD,"&Load\tCtrl+L","Load a new data file")
        wx.EVT_MENU(self,ID_LOAD,self.OnLoadFile)
        graphMenu.Append(ID_DRAW,"&Draw\tCtrl+D","Draw the graph")
        wx.EVT_MENU(self,ID_DRAW,self.OnDrawGraph)

        protectMenu=wx.Menu()
        protectMenu.Append(ID_KANON,"&Kanony\tCtrl+K","k-Anonymity")
        wx.EVT_MENU(self,ID_KANON,self.OnKanon)
 
        analyzeMenu=wx.Menu()
        analyzeMenu.Append(ID_ANALYZE,"&Analyze\tCtrl+A","Analyze")
        wx.EVT_MENU(self,ID_ANALYZE,self.OnAnalyze)
        analyzeMenu.Append(ID_DEGREE,"&Degree\tCtrl+D","Degree")
        wx.EVT_MENU(self,ID_DEGREE,self.OnDegree)


        helpMenu = wx.Menu()
        helpMenu.Append(ID_ABOUT, "&About", "Display information about the program")
        wx.EVT_MENU(self, ID_ABOUT, self.OnHelpAbout)


        # --- now add them to a menubar & attach it to the frame
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(graphMenu,"&Graph")
        menuBar.Append(protectMenu, "&Protect")
        menuBar.Append(analyzeMenu, "&Analyze")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)
        
        #  Not needed!, just put them in text form after tab in menu item!
        # --- add accelerators to the menus
        #self.SetAcceleratorTable(wx..AcceleratorTable([(wxACCEL_CTRL, ord('O'), ID_OPEN), 
        #                          (wxACCEL_ALT, ord('Q'), ID_EXIT)]))

        # --- add a statusBar (with date/time panel)
        sb = self.CreateStatusBar(3)
        sb.SetStatusWidths([-1, 65, 150])
        sb.PushStatusText("Ready", SB_INFO)
        # --- set up a timer to update the date/time (every 5 seconds)
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(5000)
        self.Notify()       # - call it once right away

        # --- add a control (a RichTextBox) & trap KEY_DOWN event
        self.rtb = wx.TextCtrl(self, ID_RTB, size=wx.Size(400,200),
                              style=wx.TE_MULTILINE | wx.TE_RICH2)
        ### - NOTE: binds to the control itself!
        wx.EVT_KEY_UP(self.rtb, self.OnRtbKeyUp)

        # --- need to add a sizer for the control - yuck!
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.SetMinSize(200,400)
        self.sizer.Add(self.rtb, 1, wx.EXPAND)
        # --- now add it to the frame (at least this auto-sizes the control!)
        self.SetSizer(self.sizer)
        self.SetAutoLayout(True)
        self.sizer.SetSizeHints(self)

        # --- initialize other settings
        self.dirName = ""
        self.fileName = ""
        self.g=nx.Graph()

        # - this is ugly, but there's no static available 
        #   once we build a class for RTB, move this there
        self.oldPos = -1
        self.ShowPos()

        # --- finally - show it!
        self.Show(True)

#---------------------------------------
    def __del__(self):
        """ Class delete event: don't leave timer hanging around! """
        self.timer.stop()
        del self.timer

#---------------------------------------
    def Notify(self):
        """ Timer event """
        t = time.localtime(time.time())
        st = time.strftime(" %b-%d-%Y  %I:%M %p", t)
        # --- could also use self.sb.SetStatusText
        self.SetStatusText(st, SB_DATETIME)

#---------------------------------------
    def OnFileExit(self, e):
        """ File|Exit event """
        self.Close(True)

#---------------------------------------
    def OnFileNew(self, e):
        """ File|New event - Clear rtb. """
        self.fileName = ""
        self.dirName = ""
        self.rtb.SetValue("")
        self.PushStatusText("Starting new file", SB_INFO)
        self.ShowPos()

#---------------------------------------
    def OnFileOpen(self, e):
        """ File|Open event - Open dialog box. """
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|Pajek File (*.net)|*.net|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            

            ### - this will read in Unicode files (since I'm using Unicode wxPython
            #if self.rtb.LoadFile(os.path.join(self.dirName, self.fileName)):
            #    self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
            #                       " characters.", SB_INFO)
            #    self.ShowPos()
            #else:
            #    self.SetStatusText("Error in opening file.", SB_INFO)

            ### - but we want just plain ASCII files, so:
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
        dlg.Destroy()

#---------------------------------------
    def OnFileSave(self, e):
        """ File|Save event - Just Save it if it's got a name. """
        if (self.fileName != "") and (self.dirName != ""):
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'w')
                f.write(self.rtb.GetValue())
                self.PushStatusText("Saved file: " + str(self.rtb.GetLastPosition()) +
                                    " characters.", SB_INFO)
                f.close()
                return True
            except:
                self.PushStatusText("Error in saving file.", SB_INFO)
                return False
        else:
            ### - If no name yet, then use the OnFileSaveAs to get name/directory
            return self.OnFileSaveAs(e)

#---------------------------------------
    def OnFileSaveAs(self, e):
        """ File|SaveAs event - Prompt for File Name. """
        ret = False
        dlg = wx.FileDialog(self, "Save As", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|All Files|*.*", wx.SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            ### - Use the OnFileSave to save the file
            if self.OnFileSave(e):
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                ret = True
        dlg.Destroy()
        return ret

#---------------------------------------
    def OnLoadFile(self,e):
        """ File|Open event - Open dialog box. """
        
        dlg = wx.FileDialog(self, "Open", self.dirName, self.fileName,
                           "Text Files (*.txt)|*.txt|Pajek File (*.net)|*.net|All Files|*.*", wx.OPEN)
        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()

            ### - this will read in Unicode files (since I'm using Unicode wxPython
            #if self.rtb.LoadFile(os.path.join(self.dirName, self.fileName)):
            #    self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) + 
            #                       " characters.", SB_INFO)
            #    self.ShowPos()
            #else:
            #    self.SetStatusText("Error in opening file.", SB_INFO)

            ### - but we want just plain ASCII files, so:
            try:
                f = file(os.path.join(self.dirName, self.fileName), 'r')
                self.rtb.SetValue(f.read())
                self.SetTitle(APP_NAME + " - [" + self.fileName + "]")
                self.SetStatusText("Opened file: " + str(self.rtb.GetLastPosition()) +
                                   " characters.", SB_INFO)
                self.ShowPos()
                f.close()
            except:
                self.PushStatusText("Error in opening file.", SB_INFO)
          
        dlg.Destroy()
        self.fileName=os.path.join(self.dirName, self.fileName)
        print self.fileName
        #try:
        #    if self.fileName!=self.dirName:
        #        g=readfile_net(g)
        #except:
        #    self.PushStatusText("Error in opening file.", SB_INFO)

        #print self.g.nodes()

        if self.fileName!=self.dirName:
            readfile_net(self.g,self.fileName)


    def OnDrawGraph(self,e):
        sh(self.g)
#---------------------------------------

    def OnKanon(self,e):
        self.rtb.SetValue("")
        self.PushStatusText("Starting anonymity", SB_INFO)
        self.ShowPos()
        k=3
        dlg=wx.NumberEntryDialog(self,message='Please enter k, default 3!',prompt='k:',caption='k-anonymity parameter',value=3,min=2,max=20)
        if (dlg.ShowModal() == wx.ID_OK):
            k=dlg.GetValue()
  
        if len(self.g.node)!=0:
                deglist=graphtodegree(self.g)
                deglist.sort(key=lambda deg:deg['deg'],reverse=True)
                degreee_anony(deglist,k)
                deglist=diffSelect(deglist)
                addEdge(self.g,deglist)
                addNode(self.g,deglist)
        else:
            print 'Grap is empty!! Please load data!'

    def OnAnalyze(self,e):
        print 'onananlyze'
 #---------------------------------------       
    def OnDegree(self,e):
        #dlg = wx.TextEntryDialog(None, 
        #    "What kind of text would you like to enter?",
        #    "Text Entry", "Default Value", style=wx.OK|wx.CANCEL)
        #if (dlg.ShowModal() == wx.ID_OK):
        #    print 'sssss'
        #dlg=wx.NumberEntryDialog(self,message='k-anonymity',prompt='k:',caption='k-anonymity parameter',value=3,min=2,max=20)
        #if (dlg.ShowModal() == wx.ID_OK):
        #    k=dlg.GetValue()
        #    print k
        #dlg = SingletonDialog(self, title="Singleton Dialog")
        #dlg.Show()
        #dlg.Raise()
        #if (dlg.ShowModal() == wx.ID_OK):
        #    print 'dlg show'
        #    t=dlg.field.GetValue()
        #    print t
        if len(self.g.node)!=0:
            print self.g.degree()
            x=self.g.degree().values()
            n, bins, patches =plt.hist(x)
            plt.xlabel('Degree')
            plt.ylabel('Number')
            plt.title(r'Histogram of Degree Distribution')

            plt.show()   

#---------------------------------------
    def OnHelpAbout(self, e):
        """ Help|About event """
        title = self.GetTitle()
        d = wx.MessageDialog(self, "About " + title, title, wx.ICON_INFORMATION | wx.OK)
        d.ShowModal()
        d.Destroy()
        wx.dialo

#---------------------------------------
    def OnRtbKeyUp(self, e):
        """ Update Row/Col indicator based on position """
        self.ShowPos()
        e.Skip()

#---------------------------------------
    def ShowPos(self):
        """ Update Row/Col indicator """
        (bPos,ePos) = self.rtb.GetSelection()
        if (self.oldPos != ePos):
            (c,r) = self.rtb.PositionToXY(ePos)
            self.SetStatusText(" " + str((r+1,c+1)), SB_ROWCOL)
        self.oldPos = ePos

# --- end [testFrame] class



#-------------------------------------------------------------------------------
# --- Program Entry Point
app = wx.App()
# --- note: Title never gets used!
frame = dpFrame("A Title", -1, "Small wxPython Application")
# frame.Show(True)  # - now shown in class __init__
app.MainLoop()
