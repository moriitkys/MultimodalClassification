import tkinter
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
import glob
import os

# https://denno-sekai.com/tkinter-pack/
# https://www.kihilog.net/python_tkinter_label/
# list box
# https://www.stjun.com/entry/2019/07/14/215812


class CreatePanel():
    '''
    This class creates UI panel for setting parameters especially for Deep Lerning
    Usage:
    import mylib.create_panel_for_mask as create_panel
    setting_panel = create_panel.CreatePanel()
    setting_panel.create_buttons()

    ~
    Notes:

    '''

    def __init__(self, key_for_searching_foldername):
        self.tki = tkinter.Tk()
        self.tki.geometry('500x465')
        self.tki.title('Settings')

        self.var_sp_trainvalratio = tkinter.StringVar()
        self.var_sp_epochs = tkinter.StringVar()

        self.flag_train = False

        self.list_selected_folders = []
        self.dict_selected_folders = {}

        self.target_folder = os.getcwd().replace("\\", '/')
        self.target_folder = self.target_folder.replace(
            "/mylib", "") + '/DataSource/rgbdt'

        self.key_for_searching_foldername = key_for_searching_foldername
        # Prepare self.dict_object_class_number
        self.prepare_dict_object_class_number()

        
    def prepare_dict_object_class_number(self):
        # Prepare self.dict_object_class_number
        self.dict_object_class_number = {}
        list_object_class_path = glob.glob(self.target_folder + "/*")
        #print(self.target_folder, list_object_class_path)
        for object_class_path in list_object_class_path:
            object_class_path = object_class_path.replace("\\", "/")
            object_class_name = object_class_path[object_class_path.rfind(
                '/')+1:]
            list_object_class_number_path = glob.glob(
                self.target_folder + "/" + object_class_name + "/*")
            for object_class_number_path in list_object_class_number_path:
                object_class_number_path = object_class_number_path.replace(
                    "\\", "/")
                object_class_number_name = object_class_number_path[object_class_number_path.rfind(
                    '/')+1:]
                # I want to list only the folders that are the target of data expansion
                # Like "/0001", "/0002", ...
                for filepath in glob.glob(object_class_number_path + "/*"):
                    if self.key_for_searching_foldername in filepath:
                        self.dict_object_class_number[object_class_name +
                                                        "/"+object_class_number_name] = object_class_number_path
                        break

    def change_parent_direstory(self,):
        self.target_folder = tkinter.filedialog.askdirectory(
            initialdir=self.target_folder)
        self.text_datasource.set(self.target_folder)
        #print("cpd", self.target_folder)

        # Update self.dict_object_class_number
        self.prepare_dict_object_class_number()

        list_object_class_number_name = [
            i for i in self.dict_object_class_number]
        self.list_object_class_number_name_tk.set(
            list_object_class_number_name)

    def select_class_number_folders(self):
        self.list_selected_folders = []
        self.dict_selected_folders = {}
        list_selected_folders_name = []
        # print(self.listbox.curselection())
        for selected_name in self.listbox.curselection():
            for i, key in enumerate(self.dict_object_class_number):
                if i == selected_name:
                    self.list_selected_folders.append(
                        self.dict_object_class_number[key])
                    self.dict_selected_folders[key] = self.dict_object_class_number[key]
                    list_selected_folders_name.append(key)

        # self.print_folders_value.set(list_selected_folders_name)
        self.print_folders.delete("1.0", "end")
        self.print_folders.insert(1.0, '\n'.join(list_selected_folders_name))

    def tkinter_callback(self, event):
        if event.widget["bg"] == "SystemButtonFace":
            event.widget["bg"] = "blue"
        else:
            event.widget["bg"] = "SystemButtonFace"

    def click_flag_train(self,):
        if self.flag_train == True:
            self.label_var['text'] = 'Mode: Inference'
            self.flag_train = False
        else:
            self.label_var['text'] = 'Mode: Train'
            self.flag_train = True

    def click_start(self,):
        # print("start")
        self.tki.destroy()

    def create_buttons(self):
        # Create labels and buttons
        y_axis_step = 25
        y_axis = 10
        self.radio_value_split = tkinter.IntVar()

        fontStyle = tkFont.Font(family="System", size=10, weight="bold")
        self.label_title = tkinter.Label(
            self.tki, text='DeepLearning Classification', font=fontStyle)
        self.label_title.place(x=25, y=y_axis)
        y_axis += y_axis_step

        self.label_explain1 = tkinter.Label(
            self.tki, text='Default targets are all folders in ')
        self.label_explain1.place(x=50, y=y_axis)
        self.text_datasource = tkinter.StringVar()
        self.text_datasource.set('./DataSource/rgbdt')
        self.label_explain2 = tkinter.Label(
            self.tki, textvariable=self.text_datasource)
        self.label_explain2.place(x=250, y=y_axis)
        y_axis += y_axis_step

        self.label_explain3 = tkinter.Label(
            self.tki, text='Click to change target folder ->')
        self.label_explain3.place(x=50, y=y_axis)

        btn_listbox = tkinter.Button(
            self.tki, text="Change Parent Directory", command=self.change_parent_direstory)
        btn_listbox.place(x=250,  y=y_axis)

        y_axis += y_axis_step + 10

        #file_path = tkinter.filedialog.askdirectory(initialdir=idir)
        # print(file_path)
        # self.label_explain2 = tkinter.Label(
        #    self.tki, text=files_dir)
        #self.label_explain2.place(x=50, y=y_axis)
        #y_axis += y_axis_step

        y_axis_step = 30
        # --- Show target folders ---
        list_target_folder_children_name = [
            name for name in self.dict_object_class_number]
        self.list_object_class_number_name_tk = tkinter.StringVar()
        self.list_object_class_number_name_tk.set(
            list_target_folder_children_name)  # dict_tk?

        # スクロールバーの作成
        self.scroll = tkinter.Scrollbar(self.tki)
        # スクロールバーの配置を決める
        #self.scroll.pack(side=tkinter.RIGHT, fill="y")
        self.listbox = tkinter.Listbox(self.tki, listvariable=self.list_object_class_number_name_tk,
                                       height=14, width=35, selectmode='multiple',
                                       yscrollcommand=self.scroll.set)

        self.listbox.place(x=25,  y=y_axis)
        #self.listbox.pack(side="left", fill="both")
        self.scroll.config(command=self.listbox.yview)

        btn_listbox = tkinter.Button(
            self.tki, text="Select Target Folders", command=self.select_class_number_folders)
        btn_listbox.place(x=250,  y=y_axis)
        btn_listbox.bind("<1>", self.tkinter_callback)

        #y_axis += y_axis_step

        #entry_value_folders = tkinter.StringVar()
        # print_folders = tkinter.Entry(
        #    self.tki, textvariable=entry_value_folders)
        #print_folders.place(x=200,  y=y_axis)
        # print(entry_value_folders.get())

        y_axis += y_axis_step

        #self.print_folders_value = tkinter.StringVar()
        # self.print_folders_value.set("")
        # self.print_folders = tkinter.Entry(
        #    self.tki, textvariable=self.print_folders_value)
        #self.print_folders.place(x=300,  y=y_axis, height=60, width=250)

        self.print_folders = tkinter.Text(self.tki)
        self.print_folders.insert(1.0, '\n'.join(self.list_selected_folders))
        self.print_folders.place(x=250,  y=y_axis, height=100, width=220)

        y_axis += y_axis_step + 180

        label5 = tkinter.Label(
            self.tki, text="Change the proportion of\n train data ")
        label5.place(x=25, y=y_axis)
        y_axis += y_axis_step

        self.var_sp_trainvalratio.set(0.7)
        spinbox = tkinter.Spinbox(
            self.tki, from_=0.0, to=1.0, textvariable=self.var_sp_trainvalratio, increment=0.05)
        spinbox.place(x=25, y=y_axis)

        y_axis -= y_axis_step

        label6 = tkinter.Label(
            self.tki, text="How many epochs the network trains ")
        label6.place(x=280, y=y_axis)
        y_axis += y_axis_step

        self.var_sp_epochs.set(30)
        self.sp_epochs = tkinter.Spinbox(
            self.tki, from_=1, to=1000, textvariable=self.var_sp_epochs, increment=5)
        self.sp_epochs.place(x=275, y=y_axis)
        y_axis += y_axis_step

        " ----- Train or Inference ----- "
        y_axis_step = 20

        btn_flag_train = tkinter.Button(self.tki, text='Train', command = self.click_flag_train)
        btn_start = tkinter.Button(self.tki, text='Start', command = self.click_start)
        label1 = tkinter.Label(self.tki,text="1. Select Train or Inference")
        label1.place(x=25, y=y_axis)
        y_axis += y_axis_step
        btn_flag_train.place(x=25, y=y_axis)
        btn_flag_train.bind("<1>",self.tkinter_callback)

        self.label_var = tkinter.Label(self.tki, text='Mode: Inference')
        self.label_var.place(x=75, y=y_axis)

        y_axis -= y_axis_step

        # ----- Start -----
        label_start = tkinter.Label(self.tki, text="Start (Close this window)")
        label_start.place(x=200, y=y_axis)
        y_axis += y_axis_step
        btn_start = tkinter.Button(
            self.tki, text="Start", command=self.click_start)
        btn_start.place(x=200, y=y_axis)

        # Display the button window
        btn_start.bind("<1>", self.tkinter_callback)
        self.tki.mainloop()
