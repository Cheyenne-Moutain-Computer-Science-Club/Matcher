from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import tkinter as tk


class GUI():
    def __init__(self):
        # Setup
        self.root = ThemedTk(theme="arc")
        self.root.title('DECA Project')
        self.root.geometry('650x500')
        self.root.resizable(False, False)

        # IntVar setup
        self.use_tsv_inputs = tk.IntVar()
        self.use_tsv_paid = tk.IntVar()
        self.use_paid_list = tk.BooleanVar()
        self.only_include_paid = tk.BooleanVar()
        self.output_option = tk.StringVar()

        # *Maybe Change to Main????
        # Other variable setup
        self.inputs_path = None
        self.paid_path = None
        self.output_path = None

        # Grid setup
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.columnconfigure(2, weight=1)

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
        self.catagories = ['Please select an output format', 'csv', 'tsv', 'txt']
        self.display_catagories = ['Please select an output format', 'Comma Seperated Values (*.csv)', 'Tab Seperated Values (*.tsv)', 'Text File (*.txt)']
        self.output_option.set("Please select an output format")
        self.option = ttk.OptionMenu(self.output, self.output_option, *self.display_catagories)
        self.option_label = ttk.Label(self.output, text="Output format:")
        self.option_label.pack(side=tk.LEFT)
        self.option.pack(side=tk.RIGHT)
        # Seperator
        self.seperator3 = ttk.Separator(self.menu, orient='horizontal')
        self.seperator3.pack(fill='x')
        



        self.root.mainloop()

    def paid_manager(self):
        # if self.use_paid_list.get():
        #     self.only_include_paid_checkbox.pack()
        #     self.paid_button.pack()
        #     self.paid_breadcrumbs.pack()
        # else:
        #     self.only_include_paid_checkbox.pack_forget()
        #     self.only_include_paid.set(False)
        #     self.paid_button.pack_forget()
        #     self.paid_breadcrumbs.pack_forget()
        #     if self.paid_path:
        #         self.paid_breadcrumbs_txt.pack_forget()
        #         self.paid_path = None
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
        self.inputs_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("all files", "*.*")))
        self.inputs_breadcrumbs_txt = ttk.Label(self.inputs_breadcrumbs, text=self.inputs_path)
        self.inputs_breadcrumbs_txt.pack()


    def set_paid(self):
        if self.paid_path != None:
            self.paid_breadcrumbs.destroy()
        self.paid_path = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("csv files","*.csv"),("all files", "*.*")))
        self.paid_breadcrumbs_txt = ttk.Label(self.paid_breadcrumbs, text=self.paid_path)
        self.paid_breadcrumbs_txt.pack()

    def set_output(self):
        if self.output_path != None:
            self.output_breadcrumbs.destroy()
        self.output_path = filedialog.askdirectory()
        self.output_breadcrumbs_txt = ttk.Label(self.output_breadcrumbs, text=self.output_path)
        self.output_breadcrumbs_txt.pack()
            

Gui = GUI()
