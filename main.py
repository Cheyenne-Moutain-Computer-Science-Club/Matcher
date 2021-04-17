# =====================
# Package imports
# =====================
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import tkinter as tk
import time
import threading
import concurrent.futures
import convertions as cv
import pandas as pd
import random as rd
# =====================
# Module imports
# =====================
# from main import Main
# =====================
# Script
# =====================
class Main():
    profiles = {}
    output = None
    input_csv = None
    filter_csv = None
    use_tsv_inputs = None
    use_tsv_filtered = None
    use_filtered_list = None
    only_include_filtered = None
    output_option = None
    convertions = cv.convertions
    finished = False

    def __init__(self):
        pass

    def convert(self):
        if self.use_tsv_inputs:
            self.inputs = pd.DataFrame(pd.read_csv(self.input_csv, sep='\t'))
        else:
            self.inputs = pd.DataFrame(pd.read_csv(self.input_csv))

        if self.use_filtered_list:
            if self.use_tsv_inputs:
                self.filtered = pd.DataFrame(pd.read_csv(self.filter_csv, sep='\t'))
            else:
                self.filtered = pd.DataFrame(pd.read_csv(self.filter_csv))
            if self.only_include_filtered:
                drop_list = []
                for index, row in self.inputs.iterrows():
                    if row['Email Address'] in pd.merge(self.inputs, self.filtered, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1).values:
                        drop_list.append(index)
                self.inputs = self.inputs.drop(drop_list)

        
        print('Convert')
            

class Lint(Main):

    def __init__(self):
        super().__init__()
        self.convert()
        self.create_profiles()

    def convert(self):
        heads = list(Main.inputs.columns)
        for col in heads:
            if col in Main.convertions:
                convert = []
                for index, row in Main.inputs.iterrows():
                    convert.append(Main.convertions[col][row[col]])
                Main.inputs[col] = convert
        print('Convert from Lint')
    

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            Main.profiles[index] = {
                'id': index,
                'coords': [],
                'matches': []
            }
        print('Profiles Created')


class Graph(Main):
    def __init__(self):
        super().__init__()
        self.create_coordinates()

    def create_coordinates(self):
        for index in list(Main.inputs.index.values):
            heads = list(Main.inputs.columns)
            total_x = 0
            total_y = 0
            for col in heads:
                if col in Main.convertions:
                    if Main.convertions[col]['axis'] == 'x':
                        total_x += Main.inputs.iloc[index][col]
                    elif Main.convertions[col]['axis'] == 'y':
                        total_y += Main.inputs.iloc[index][col]
                    else:
                        raise ValueError('Incorrect Axis Definition')
            Main.profiles[index]['coords'] = [total_x, total_y]
        
        print('Graphed')


class Distance(Main):
    def __init__(self):
        super().__init__()
        self.get_people()

    def get_people(self):
        for key, prof1 in Main.profiles.items():
            self.apothem = 15
            people = self.in_range(key)
            while len(people) < 13:
                self.apothem += 3
                people = self.in_range(key)
            Main.profiles[key]['matches'] = rd.sample(people, 10)
        print('Matches Made')

    def in_range(self, di):
        people = []
        dist = []
        for key, prof in Main.profiles.items():
            if ((Main.profiles[di]['coords'][0] - self.apothem) < prof['coords'][0] < (Main.profiles[di]['coords'][0] + self.apothem)) and ((Main.profiles[di]['coords'][1] - self.apothem) < prof['coords'][1] < (Main.profiles[di]['coords'][1] + self.apothem)):
                if key == di:
                    pass
                else:
                    dist.append(((Main.profiles[di]['coords'][0] + Main.profiles[key]['coords'][0])**2 + (Main.profiles[di]['coords'][1] + Main.profiles[key]['coords'][1])**2) **(1/2))
                    people.append(key)
        dist, people = zip(*sorted(zip(dist, people)))
        return people


class Compile(Main):
    def __init__(self):
        super().__init__()
        self.generate_output()
        if Main.use_filtered_list:
            self.filter_outputs()

    def generate_output(self):
        Main.output = pd.DataFrame({"Name": [], "Email Address": [], "Matches": []})
        for key, prof in Main.profiles.items():
            build_list = [Main.inputs.iloc[key]['Name'], Main.inputs.iloc[key]['Email Address'], [Main.inputs.iloc[x]['Name'] for x in prof['matches']]]
            # Main.output.loc[len(Main.inputs.index)] = build_list
            Main.output.loc[key] = build_list
    
        print('Compiled')

    def filter_outputs(self):
        drop_list = []
        for index, row in Main.output.iterrows():
            if row['Email Address'] in pd.merge(Main.output, Main.filtered, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1).values:
                drop_list.append(index)
        Main.output = Main.output.drop(drop_list)


class GUI(Main):
    def __init__(self):
        super().__init__()
        # ============================
        # Setup
        # ============================
        # self.root = ThemedTk(theme="arc")
        self.root = ThemedTk(theme="breeze")
        # self.root = ThemedTk(theme="equilux")
        self.root.title('Matcher')
        self.root.geometry('650x600')
        self.root.resizable(False, True)
        self.style = ttk.Style(self.root)
        # self.root.configure(bg='#464646')

        # IntVar setup
        self.use_tsv_inputs = tk.IntVar()
        self.use_tsv_filtered = tk.IntVar()
        self.use_filtered_list = tk.BooleanVar()
        self.only_include_filtered = tk.BooleanVar()
        self.output_option = tk.StringVar()
        self.scale_x_enabled = tk.BooleanVar()
        self.scale_y_enabled = tk.BooleanVar()
        self.scale_y_enabled.set(True)
        self.theme_selection = tk.StringVar()

        # *Maybe Change to Main????
        # Other variable setup
        self.inputs_path = None
        self.filtered_path = None
        self.output_path = None

        # Tab control
        self.tab_control = ttk.Notebook(self.root, width = 650)

        self.menu = ttk.Frame(self.tab_control)
        self.options = ttk.Frame(self.tab_control)
        self.log = ttk.Frame(self.tab_control)
        self.output_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu, text="Import Values")
        self.tab_control.add(self.options, text="Advanced Options")
        # self.tab_control.add(self.log, text="Log")
        self.tab_control.add(self.output_tab, text="Output")

        self.tab_control.pack()

        # ============================
        # Main Menu
        # ============================

        # Inputs CSV
        self.inputs = ttk.Frame(self.menu)
        self.inputs.pack(pady=5)
        self.input_header = ttk.Label(self.inputs, 
                                        text="Input Settings",
                                        font = ("Microsoft JhengHei UI", 12))
        self.input_header.pack()
        self.input_spacer = ttk.Label(self.inputs, text="")
        self.input_spacer.pack()
        self.inputs_button = ttk.Button(self.inputs, text="Select Responses", command=self.set_inputs)
        self.inputs_button.pack()
        self.inputs_breadcrumbs = ttk.Frame(self.inputs)
        self.inputs_breadcrumbs.pack()
        self.use_csv_radio = ttk.Radiobutton(self.inputs,
                                                value=0,
                                                text="Use Comma Seperated Values (*.csv)", 
                                                variable=self.use_tsv_inputs)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_inputs_radio = ttk.Radiobutton(self.inputs,
                                                value=1,
                                                text="Use Tab Seperated Values (*.tsv)", 
                                                variable=self.use_tsv_inputs)
        self.use_tsv_inputs_radio.pack(side="right")
        # Seperator
        self.seperator1 = ttk.Separator(self.menu, orient='horizontal')
        self.seperator1.pack(fill='x')

        # filtered List
        self.filtered = ttk.Frame(self.menu)
        self.filtered.pack(pady=5)
        self.filtered_header = ttk.Label(self.filtered, 
                                        text="Filter List Settings",
                                        font = ("Microsoft JhengHei UI", 12))
        self.filtered_header.pack()
        self.filtered_spacer = ttk.Label(self.filtered, text="")
        self.filtered_spacer.pack()
        self.filtered_frame = ttk.Frame(self.filtered)
        self.use_filtered_checkbox = ttk.Checkbutton(self.filtered,
                                                text="Use Filter List", 
                                                variable=self.use_filtered_list,
                                                command= self.filtered_manager)
        self.use_filtered_checkbox.pack()
        # Hidden Frame
        self.filtered_spacer2 = ttk.Label(self.filtered_frame, text="")
        self.filtered_spacer2.pack(side="top")
        # Button and Breadcrumbs
        self.filtered_button_frame = ttk.Frame(self.filtered_frame)
        self.filtered_button_frame.pack()
        self.filtered_button = ttk.Button(self.filtered_button_frame, text="Select Filter", command=self.set_filtered)
        self.filtered_button.pack()
        self.filtered_breadcrumbs = ttk.Frame(self.filtered_button_frame)
        self.filtered_breadcrumbs.pack()
        # Checkbox
        self.only_include_filtered_checkbox = ttk.Checkbutton(self.filtered_frame,
                                                text="Only include filtered users in match lists", 
                                                variable=self.only_include_filtered)
        self.only_include_filtered_checkbox.pack()
        # Radio Buttons
        self.use_csv_radio = ttk.Radiobutton(self.filtered_frame,
                                                value=0,
                                                text="Use Comma Seperated Values (*.csv)", 
                                                variable=self.use_tsv_filtered)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_inputs_radio = ttk.Radiobutton(self.filtered_frame,
                                                value=1,
                                                text="Use Tab Seperated Values (*.tsv)", 
                                                variable=self.use_tsv_filtered)
        self.use_tsv_inputs_radio.pack(side="right")
        # Seperator
        self.seperator2 = ttk.Separator(self.menu, orient='horizontal')
        self.seperator2.pack(fill='x')

        # Output List
        self.output = ttk.Frame(self.menu)
        self.output.pack(pady=5)
        self.output_header = ttk.Label(self.output, 
                                        text="Output Settings",
                                        font = ("Microsoft JhengHei UI", 12))
        self.output_header.pack()
        self.output_spacer = ttk.Label(self.output, text="")
        self.output_spacer.pack()
        self.output_button = ttk.Button(self.output, text="Select Output Location", command=self.set_output)
        self.output_button.pack()
        self.output_breadcrumbs = ttk.Frame(self.output)
        self.output_breadcrumbs.pack()
        # Dropdown
        self.display_catagories = ['Please select an output format', 'Comma Seperated Values (*.csv)', 'Tab Seperated Values (*.tsv)', 'Text File (*.txt)']
        self.output_option.set("Please select an output format")
        self.option = ttk.OptionMenu(self.output, self.output_option, *self.display_catagories)
        self.option_label = ttk.Label(self.output, text="Output format:")
        self.option_label.pack(side=tk.LEFT)
        self.option.pack(side=tk.RIGHT)
        # Seperator
        self.seperator3 = ttk.Separator(self.menu, orient='horizontal')
        self.seperator3.pack(fill='x')

        # Run
        self.start_button = ttk.Button(self.menu, text='Run', command=self.start)
        self.start_button.pack(pady=10)

        # ============================
        # Advanced Menu
        # ============================
        
        # Appearance Menu
        self.appearance = ttk.Frame(self.options)
        self.appearance.pack()
        self.appearance_label = ttk.Label(self.appearance, text="Appearance Options", font= ("Microsoft JhengHei UI", 12))
        self.appearance_label.pack(pady=5)
        # Scale checkboxes
        self.scale_x = ttk.Checkbutton(self.appearance,
                                                text="Allow X Scaling", 
                                                variable=self.scale_x_enabled,
                                                command=self.update_appearance)
        self.scale_y = ttk.Checkbutton(self.appearance,
                                                text="Allow Y Scaling", 
                                                variable=self.scale_y_enabled,
                                                command=self.update_appearance)
        self.scale_x.pack()
        self.scale_y.pack()
        # Theme dropdown
        self.display_themes = ["",'Breeze', 'Adapta', 'Arc', 'Equilux']
        self.theme_selection.set("Breeze")
        self.theme_dropdown = ttk.OptionMenu(self.appearance, self.theme_selection, *self.display_themes, command = self.update_appearance)
        self.theme_label = ttk.Label(self.appearance, text="Theme:")
        self.theme_label.pack(side=tk.LEFT)
        self.theme_dropdown.pack(side=tk.RIGHT, pady = 5)
        # Seperator
        self.seperator4 = ttk.Separator(self.options, orient='horizontal')
        self.seperator4.pack(fill='x')

        # Logging settings
        self.log = ttk.Frame(self.options)
        self.log.pack()
        self.log_label = ttk.Label(self.log, text="Logging Options", font= ("Microsoft JhengHei UI", 12))
        self.log_label.pack(pady=5)
        self.log_coming_soon = ttk.Label(self.log, text= "Coming Soon!").pack()


        # ============================
        # Output
        # ============================
        self.output_tab_label = ttk.Label(self.output_tab, text="Output:", font= ("Microsoft JhengHei UI", 12))
        self.output_tab_label.pack(pady=5)
        self.save_output_button = ttk.Button(self.output_tab, text="Save Output File", command = self.save)
        self.progress_bar = ttk.Progressbar(self.output_tab, orient='horizontal', length = 300, mode='determinate')
        self.progress_bar.pack()

        self.info = ttk.Label(self.output_tab, text="Thank you for using the Matcher program! Designed with ❤ by CMCSC", font=("Microsoft JhengHei UI", 9)).pack(anchor='s')

        
        self.root.mainloop()

    # ============================
    # Methods
    # ============================
    def save(self):
        Main.save_output_as = filedialog.asksaveasfilename(initialdir = self.output_path,title = "Save File", filetypes = (('CSV file', "*.csv"),('TSV file', "*.tsv"),('TXT file', "*.txt"),("all files","*.*")))
        if Main.output_option == 'Comma Seperated Values (*.csv)':
            Main.output.to_csv(f'{Main.save_output_as}.csv', index=False)
        elif Main.output_option == 'Tab Seperated Values (*.tsv)':
            Main.output.to_csv(f'{Main.save_output_as}.tsv', index=False, sep="\t")
        elif Main.output_option == 'Text File (*.txt)':
            Main.output.to_csv(f'{Main.save_output_as}.txt', header=None, index=None, sep=' ', mode='a')
        self.root.destroy()

    def update_appearance(self, *args):
        self.root.resizable(self.scale_x_enabled.get(), self.scale_y_enabled.get())
        if args:
            self.style.theme_use(args[0].lower())
            if args[0] == 'Equilux':
                self.root.configure(bg='#464646')

    def filtered_manager(self):
        if self.use_filtered_list.get():
            self.filtered_frame.pack()
        else:
            self.filtered_frame.pack_forget()
            self.only_include_filtered.set(False)
            if self.filtered_path:
                self.filtered_breadcrumbs_txt.pack_forget()
                self.filtered_path = None

    def set_inputs(self):
        if self.inputs_path != None:
            self.inputs_breadcrumbs.destroy()
        self.inputs_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("tsv files","*.tsv"),("all files", "*.*")))
        self.inputs_breadcrumbs_txt = ttk.Label(self.inputs_breadcrumbs, text=self.inputs_path)
        self.inputs_breadcrumbs_txt.pack()


    def set_filtered(self):
        if self.filtered_path != None:
            self.filtered_breadcrumbs.destroy()
        self.filtered_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("tsv files","*.tsv"),("all files", "*.*")))
        self.filtered_breadcrumbs_txt = ttk.Label(self.filtered_breadcrumbs, text=self.filtered_path)
        self.filtered_breadcrumbs_txt.pack()

    def set_output(self):
        if self.output_path != None:
            self.output_breadcrumbs.destroy()
        self.output_path = filedialog.askdirectory()
        self.output_breadcrumbs_txt = ttk.Label(self.output_breadcrumbs, text=self.output_path)
        self.output_breadcrumbs_txt.pack()

    def start(self):
        if (self.inputs_path == None) or (self.inputs_path == ""):
            tk.messagebox.showerror("Error", "Please enter an input list file path")
            return
        elif ((self.filtered_path == None) or (self.filtered_path == "")) and self.use_filtered_list.get():
            tk.messagebox.showerror("Error", "Please enter a filtered list file path")
            return
        elif (self.output_path == None) or (self.output_path == ""):
            tk.messagebox.showerror("Error", "Please select an output file path!")
            return
        elif self.output_option.get() == 'Please select an output format':
            tk.messagebox.showerror("Error", "Please select an output format!")
            return
        

        Main.input_csv = self.inputs_path
        # Main.output_csv = self.output_path
        Main.filter_csv = self.filtered_path

        Main.use_tsv_inputs = self.use_tsv_inputs.get()
        Main.use_tsv_filtered = self.use_tsv_filtered.get()
        Main.use_filtered_list = self.use_filtered_list.get()
        Main.only_include_filtered = self.only_include_filtered.get()
        Main.output_option = self.output_option.get()

        self.x = threading.Thread(target=self.progress_bar_func)
        self.x.start()

        Main.convert()

        self.Lint = Lint()
        self.Graph = Graph()
        self.Distance = Distance()
        self.Compile = Compile()


    def progress_bar_func(self):

        self.tab_control.hide(0)
        self.tab_control.hide(1)
        self.tab_control.select(2)

        while True:
            self.progress_bar['value'] += 1
            self.root.update_idletasks()
            if self.progress_bar['value'] >= 100 and not Main.finished:
                self.save_output_button.pack(pady=5)
                break
            elif self.progress_bar['value'] >= 100 and Main.finished:
                self.progress_bar['value'] = 0
            time.sleep(0.1)


if __name__ == "__main__":
    Main = Main()
    GUI = GUI()
