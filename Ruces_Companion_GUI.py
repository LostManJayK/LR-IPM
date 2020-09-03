'''
#To change window colour, edit the set_clearcolor_by_theme_style function in kivymd/theming.py

#callback function added in menus.py and in the dropdown menu class in python in order to run functions from dropdown menu selections

#menus.py in kivymd has the c value edited in displayMenu sso that the DropdownMenu appears correctly, default is c = caller.to_window(caller.center_X, caller.center_y_)

#button.py BaseRectangularButton edited with font_name
'''

import kivy
import kivymd
kivy.require('1.11.1')
import sys, os

import Ruces_Companion_New_Format as rc

from kivymd.theming import ThemeManager
from kivymd.menus import MDDropdownMenu
from kivymd.label import MDLabel
from kivymd.button import MDRaisedButton
from kivymd.navigationdrawer import NavigationLayout

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput


from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner, SpinnerOption, DropDown
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout

#Class for loading jobs        
class LoadDialog(BoxLayout):
    
    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
#        self.chooserlayout.loadchooser.path = "D:\\Python\\RUCES AUTO\\Saves"
        
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    

#Class for saving jobs
class SaveDialog(BoxLayout):
    
    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)
#        self.chooserlayout.savechooser.path = "D:\\Python\\RUCES AUTO\\Saves"
    
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

widget_ids = {}
rc_gui = None

#Main app class
class RcGUIApp(App):
    
    theme_cls = ThemeManager()
    title='RUCES'
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.sm = ScreenManager()
        self.sm.add_widget(IntroPage(name="intro_page"))
        self.sm.add_widget(NewJobPage(name="new_job_page"))
        self.sm.add_widget(IPMConfirmPage(name = "ipm_confirm_page"))
        self.sm.add_widget(ResultPages(name="result_pages"))
        self.nav = Navigator()
        self.nav.nav_layout.add_widget(self.sm)
        rc.retrieveDatabase()
        self.nav.menu_items[4]['text'] = "Locate Database: " + rc.retrieveDatabase()
        return self.nav

#Class for navigation Box layout
class NavigatorBox(BoxLayout):
    orientation = 'vertical'


#Class for main navigation Drawer
class Navigator(NavigatorBox):
    
    loaded = False
    
    toolbar = ObjectProperty(None)
    
    menu_items = [
                  {'viewclass': 'MDMenuItem', 'text': 'New', 'id': 'new'},
                  {'viewclass': 'MDMenuItem', 'text': 'Save'},
                  {'viewclass': 'MDMenuItem', 'text': 'Load'},
                  {'viewclass': 'MDMenuItem', 'text': 'Export'},
                  {'viewclass': 'MDMenuItem', 'text': 'Locate Database', 'font_color': (1, 0.6, 0, 1)},
                  {'viewclass': 'MDMenuItem', 'text': 'Settings'}
                 ]
        
    
    def buildOptionsMenu(self):
        self.options_menu = MyDropdownMenu(items=self.menu_items, pos_hint={'left': 1})
        self.options_menu.open(self.toolbar)
        
    def returnCDPath(self):
        global rc
        return str(rc.cd_path)
    
    def dismiss_popup(self):
        self._popup.dismiss()
    
    def show_save(self):
        
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        content.id = "savedialog"
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
    
    def show_load(self):
        
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        content.id = "loaddialog"
        self._popup = Popup(title="Select Job", content=content, size_hint=(0.9, 0.9))
        self._popup.open()
        
    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.loaded = stream.read()
            print(self.loaded)

        self.dismiss_popup()
        
    def save(self, path, filename):
        
        self.store = JsonStore(str(filename)+'_params.json')
        
        globals()[str(filename)+"_vars"].put('rc_params', parts = rc.parts_list, pole = rc.pole_list,)
        
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write("yoyoyo")

        self.dismiss_popup()

class MyDropdownMenu(MDDropdownMenu):
    
    def __init__(self, **kwargs):
        super(MyDropdownMenu, self).__init__(**kwargs)
        self.width_mult = 4
     
    #Function for actions when option is clicked
    def callback(self, choice):
        
        if choice == "New":
            self.new()
        elif "Locate Database" in choice:
            self.locateDatabase()
            
        elif choice == "Load":
            print('load')
        else:
            print('dummy')
            
    def new(self):
        
        rc.cd_list = {}
        rc.cd_counter = {}
        rc.cd_list_names = {}
        rc.missing_cd = {}
        rc.part_list = {}
        rc.pole_list = {}
        rc.ipm_list = {}
        
        print('new')
        if rc_gui.sm.get_screen('result_pages').active == True:
        
            self.result_list = rc_gui.sm.get_screen('result_pages').grid
            for w in range(0, len(self.result_list.children)):
                self.result_list.remove_widget(self.result_list.children[0])
            
        if rc_gui.sm.get_screen('ipm_confirm_page').active == True:
            
            self.confirm_list = rc_gui.sm.get_screen('ipm_confirm_page').grid
            
            for w in range(0, len(self.confirm_list.children)):
                self.confirm_list.remove_widget(self.confirm_list.children[0])
                
        rc_gui.sm.current = "new_job_page"
        
        rc_gui.sm.get_screen('ipm_confirm_page').active = False
        rc_gui.sm.get_screen('result_pages').active = False
        
    def locateDatabase(self):
        global rc
        rc_gui.nav.menu_items[4]['text'] = "Locate Database: " + rc.retrieveDatabase()
        rc_gui.nav.loaded = True        

#Class for introduction page
class IntroPage(Screen):

    global rc_gui
    
    def checkLoaded(self):
        if not rc_gui.nav.loaded == True:
            pass


    def openJob(self):
        #Go to open job page
        pass

#Class for starting a new job
class NewJobPage(Screen):
        
    global rc_gui
    
    def changeToGreen(self, wid):
        if not wid.text == '':
            wid.line_color_normal=(0,1,0,1)
        else:
            wid.line_color_normal=(1,0,0,1)
    
    def newJob(self):
        global rc
        self.ipm_label.text = "IPM file path: " + str(rc.openIPM())
        
        if rc.ipm_loaded:
            rc.makePartList()
            rc.makePoleList()
    
    def returnCDPath(self):
        global rc
        return str(rc.cd_path)
    
    def locateDatabase(self):
        global rc
        self.data_label.text = "Locate Database: " + rc.retrieveDatabase()

    def retrieve(self):
        global rc
        rc.getIPM(self.ipm_header.text.upper())
        rc.buildIPM(self.pole_header.text.upper(), self.cd_header.text.upper(), self.conductor_header.text.upper())
        rc_gui.sm.get_screen("ipm_confirm_page").displayIPM()
        
        rc_gui.sm.get_screen('ipm_confirm_page').active = True

class OpenJobPage(Screen):
    pass

#Class for the page containg a modifiable table of the IPMs and their CD#s and conductors
#   Add functionality for adding/deleting entries                 
class IPMConfirmPage(Screen):
    grid = ObjectProperty(None)
    global widget_ids
    active = False
            
    
    def displayIPM(self):
        global rc
        
        for ipm in rc.ipm_list:
            try:
                widget_ids.update({rc.ipm_list[ipm].name+"_name": CustLabel(text=rc.ipm_list[ipm].name, id = rc.ipm_list[ipm].name+"_name")})
                widget_ids.update({rc.ipm_list[ipm].name+"_cd": MySpinner(text=rc.ipm_list[ipm].CD, id = rc.ipm_list[ipm].name+"_cd", values=self.cdLister())})
                widget_ids.update({rc.ipm_list[ipm].name+"_conductor": MySpinner(text=rc.ipm_list[ipm].conductor, id = rc.ipm_list[ipm].name+"_conductor", values=self.condLister())})
            except Exception as e:
                print(e)
                break
            
        for widget in widget_ids:
            try:
                self.grid.add_widget(widget_ids[widget])
            except Exception:
                print(sys.exc_info())
        
        self.active = True
            

    def cdLister(self):
        cd_arr = []
        for sheet in rc.cd_data.sheetnames:
            if sheet == "PARTS":
                break
            ws = rc.cd_data[sheet]
            for col in ws.iter_cols(min_row=2, max_row=ws.max_row, min_col=1, max_col=1):
                for cell in col:
                    cd_arr.append(str(cell.value))
        return cd_arr
    
    def condLister(self):
        cond_arr = []
        ws = rc.cd_data["CONDUCTORS"]
        for row in ws.iter_rows(min_row=1, max_row=1, min_col=1, max_col=ws.max_column):
            for cell in row:
                cond_arr.append(str(cell.value))
        return cond_arr

    def estimate(self):
        
        for ipm in rc.ipm_list:
            if not rc.ipm_list[ipm].CD == widget_ids[rc.ipm_list[ipm].name+"_cd"].text:
                rc.ipm_list[ipm].CD = widget_ids[rc.ipm_list[ipm].name+"_cd"].text
            if not rc.ipm_list[ipm].conductor == widget_ids[rc.ipm_list[ipm].name+"_conductor"].text:
                rc.ipm_list[ipm].conductor = widget_ids[rc.ipm_list[ipm].name+"_conductor"].text
                        
        for ipm in rc.ipm_list:
            rc.ipm_list[ipm].scanCD()
        
        rc_gui.sm.get_screen("result_pages").displayParts()
        
#Class for page containing quantities of required parts
#   Add functionality for adding/subtracting quantities by a predefined step
#   Add cost estimate functionality
#   Implement save/load functions
class ResultPages(Screen):  
    
    grid = ObjectProperty(None)
    active = False
    
    def displayParts(self):
            for part in rc.part_list:
                try:
                    if type(rc.part_list[part]) is dict:
                        for entry in rc.part_list[part]:
                            #nav_layout.main_grid.nav_box.
                            self.grid.add_widget(CustLabel(text=str(part) + " "+ entry, id = part+entry+"_name"))
                            self.grid.add_widget(TextInput(text=str(rc.part_list[part][entry]), id = part+entry+"_count"))
                    else:
                        self.grid.add_widget(CustLabel(text=str(part), id = part+"_name"))
                        self.grid.add_widget(TextInput(text=str(rc.part_list[part]), id = part+"_count"))
                except Exception as e:
                    print(e)
            
            self.active = True

                    
#Class for Material Design Labels
class CustLabel(MDLabel):
    font_size = 20
    color = (.051,.596,.729,1)
    font_name = 'D:\DOCUMENTS\Coding\Python\Anaconda\Lib\site-packages\kivymd/fonts/Roboto-Medium'
 
             
#Class for creating spinner options    
class SpinnerOptions(SpinnerOption):

    def __init__(self, **kwargs):
        super(SpinnerOptions, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [.4, .4, 1, 1]    # blue colour
        self.height = 30

#Class for spinner dropdown
class SpinnerDropdown(DropDown):

    def __init__(self, **kwargs):
        super(SpinnerDropdown, self).__init__(**kwargs)
        self.auto_width = False
        self.height = 50
        self.width = 200    

#Class for creating main spinner button    
class MySpinner(Spinner):
    
    def __init__(self, **kwargs):
        super(MySpinner, self).__init__(**kwargs)
        self.dropdown_cls = SpinnerDropdown
        self.option_cls = SpinnerOptions
        self.background_normal = ''
        self.background_color = [0,0,1,1]

#Class for creating material design buttons
class MyButton(MDRaisedButton):
    
    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        
    font_name = 'D:\DOCUMENTS\Coding\Python\Anaconda\Lib\site-packages\kivymd/fonts/Roboto-MediumItalic'
    font_size = 25


#Class for creating a grid layout for a ScrollView        
class ScrollGrid(GridLayout):
    
    def __init__(self, **kwargs):
        super(ScrollGrid, self).__init__(**kwargs)
        
#Main function
def main():
    
        global rc_gui
        rc_gui = RcGUIApp()
        rc_gui.run()
        
if __name__ == "__main__":
        main()
quit()        

