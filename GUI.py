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
# =====================
# Module imports
# =====================
from main import Main
# =====================
# Script
# =====================

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
        self.root.geometry('650x550')
        self.root.resizable(False, True)
        self.style = ttk.Style(self.root)
        # self.root.configure(bg='#464646')

        # IntVar setup
        self.use_tsv_inputs = tk.IntVar()
        self.use_tsv_paid = tk.IntVar()
        self.use_paid_list = tk.BooleanVar()
        self.only_include_paid = tk.BooleanVar()
        self.output_option = tk.StringVar()
        self.scale_x_enabled = tk.BooleanVar()
        self.scale_y_enabled = tk.BooleanVar()
        self.scale_y_enabled.set(True)
        self.theme_selection = tk.StringVar()

        # *Maybe Change to Main????
        # Other variable setup
        self.inputs_path = None
        self.paid_path = None
        self.output_path = None

        # Tab control
        self.tab_control = ttk.Notebook(self.root, width = 650)

        self.menu = ttk.Frame(self.tab_control)
        self.options = ttk.Frame(self.tab_control)
        self.log = ttk.Frame(self.tab_control)
        self.output = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu, text="Import Values")
        self.tab_control.add(self.options, text="Advanced Options")
        # self.tab_control.add(self.log, text="Log")
        self.tab_control.add(self.output, text="Output")

        self.tab_control.pack()

        # ============================
        # Main Menu
        # ============================

        # Inputs CSV
        self.inputs = ttk.Frame(self.menu)
        self.inputs.pack(pady=5)
        self.input_header = ttk.Label(self.inputs, 
                                        text="Input CSV Settings",
                                        font = ("Microsoft JhengHei UI", 12))
        self.input_header.pack()
        self.input_spacer = ttk.Label(self.inputs, text="")
        self.input_spacer.pack()
        self.inputs_button = ttk.Button(self.inputs, text="Select Responses CSV", command=self.set_inputs)
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

        # Paid List
        self.paid = ttk.Frame(self.menu)
        self.paid.pack(pady=5)
        self.paid_header = ttk.Label(self.paid, 
                                        text="Paid List Settings",
                                        font = ("Microsoft JhengHei UI", 12))
        self.paid_header.pack()
        self.paid_spacer = ttk.Label(self.paid, text="")
        self.paid_spacer.pack()
        self.paid_frame = ttk.Frame(self.paid)
        self.use_paid_checkbox = ttk.Checkbutton(self.paid,
                                                text="Use Paid List", 
                                                variable=self.use_paid_list,
                                                command= self.paid_manager)
        self.use_paid_checkbox.pack()
        # Hidden Frame
        self.paid_spacer2 = ttk.Label(self.paid_frame, text="")
        self.paid_spacer2.pack(side="top")
        # Button and Breadcrumbs
        self.paid_button_frame = ttk.Frame(self.paid_frame)
        self.paid_button_frame.pack()
        self.paid_button = ttk.Button(self.paid_button_frame, text="Select Paid List", command=self.set_paid)
        self.paid_button.pack()
        self.paid_breadcrumbs = ttk.Frame(self.paid_button_frame)
        self.paid_breadcrumbs.pack()
        # Checkbox
        self.only_include_paid_checkbox = ttk.Checkbutton(self.paid_frame,
                                                text="Only include paid users in match lists", 
                                                variable=self.only_include_paid)
        self.only_include_paid_checkbox.pack()
        # Radio Buttons
        self.use_csv_radio = ttk.Radiobutton(self.paid_frame,
                                                value=0,
                                                text="Use Comma Seperated Values (*.csv)", 
                                                variable=self.use_tsv_paid)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_inputs_radio = ttk.Radiobutton(self.paid_frame,
                                                value=1,
                                                text="Use Tab Seperated Values (*.tsv)", 
                                                variable=self.use_tsv_paid)
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


        
        self.root.mainloop()

    # ============================
    # Methods
    # ============================
    def update_appearance(self, *args):
        self.root.resizable(self.scale_x_enabled.get(), self.scale_y_enabled.get())
        if args:
            self.style.theme_use(args[0].lower())
            if args[0] == 'Equilux':
                self.root.configure(bg='#464646')

    def paid_manager(self):
        if self.use_paid_list.get():
            self.paid_frame.pack()
        else:
            self.paid_frame.pack_forget()
            self.only_include_paid.set(False)
            if self.paid_path:
                self.paid_breadcrumbs_txt.pack_forget()
                self.paid_path = None

    def set_inputs(self):
        if self.inputs_path != None:
            self.inputs_breadcrumbs.destroy()
        self.inputs_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("tsv files","*.tsv"),("all files", "*.*")))
        self.inputs_breadcrumbs_txt = ttk.Label(self.inputs_breadcrumbs, text=self.inputs_path)
        self.inputs_breadcrumbs_txt.pack()


    def set_paid(self):
        if self.paid_path != None:
            self.paid_breadcrumbs.destroy()
        self.paid_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("tsv files","*.tsv"),("all files", "*.*")))
        self.paid_breadcrumbs_txt = ttk.Label(self.paid_breadcrumbs, text=self.paid_path)
        self.paid_breadcrumbs_txt.pack()

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
        elif ((self.paid_path == None) or (self.paid_path == "")) and self.use_paid_list.get():
            tk.messagebox.showerror("Error", "Please enter a paid list file path")
            return
        elif (self.output_path == None) or (self.output_path == ""):
            tk.messagebox.showerror("Error", "Please select an output file path!")
            return
        elif self.output_option.get() == 'Please select an output format':
            tk.messagebox.showerror("Error", "Please select an output format!")
            return
        

        Main.input_csv = self.inputs_path
        Main.output_csv = self.output_path
        Main.pay_csv = self.paid_path

        Main.use_tsv_inputs = self.use_tsv_inputs.get()
        Main.use_tsv_paid = self.use_tsv_paid.get()
        Main.use_paid_list = self.use_paid_list.get()
        Main.only_include_paid = self.only_include_paid.get()
        Main.output_option = self.output_option.get()

        Main.convert(Main)

        self.tab_control.hide(0)
        self.tab_control.hide(1)
        self.tab_control.select(2)
            

if __name__ == "__main__":
    Gui = GUI()
