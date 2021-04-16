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

        # IntVar Setup
        self.use_tsv = tk.IntVar()
        self.use_paid_list = tk.BooleanVar()
        self.only_include_paid = tk.BooleanVar()
        self.output_option = tk.StringVar()

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
        self.inputs_button = ttk.Button(self.inputs, text="Select Responses CSV")
        self.inputs_button.pack()
        self.inputs_breadcrumbs = ttk.Frame(self.inputs)
        self.inputs_breadcrumbs.pack()
        self.use_csv_radio = ttk.Radiobutton(self.inputs,
                                                value=0,
                                                text="Use Comma Seperated Values", 
                                                variable=self.use_tsv)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_radio = ttk.Radiobutton(self.inputs,
                                                value=1,
                                                text="Use Tab Seperated Values", 
                                                variable=self.use_tsv)
        self.use_tsv_radio.pack(side="right")

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
        self.paid_button = ttk.Button(self.paid, text="Select Paid List")
        # self.paid_button.pack()
        self.paid_breadcrumbs = ttk.Frame(self.paid)
        # self.paid_breadcrumbs.pack()
        self.use_paid_checkbox = ttk.Checkbutton(self.paid,
                                                text="Use Paid List", 
                                                variable=self.use_paid_list,
                                                command= self.paid_manager)
        self.use_paid_checkbox.pack(side="left")
        self.only_include_paid_checkbox = ttk.Checkbutton(self.paid,
                                                text="Only include paid users in match lists", 
                                                variable=self.only_include_paid)
        # self.only_include_paid_checkbox.pack(side="right")

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
        self.output_button = ttk.Button(self.output, text="Select Output Location")
        self.output_button.pack()
        self.output_breadcrumbs = ttk.Frame(self.output)
        self.output_breadcrumbs.pack()

        self.catagories = ['Please select an output format', 'csv', 'tsv', 'individually']
        self.display_catagories = ['Please select an output format', 'Comma Seperated Values', 'Tab Seperated Values', 'Individual Text Files']
        self.output_option.set("Please select an output format")
        self.option = ttk.OptionMenu(self.output, self.output_option, *self.display_catagories)
        self.option_label = ttk.Label(self.output, text="Output format:")
        self.option_label.pack(side=tk.LEFT)
        self.option.pack(side=tk.RIGHT)

        self.seperator3 = ttk.Separator(self.menu, orient='horizontal')
        self.seperator3.pack(fill='x')
        



        self.root.mainloop()

    def paid_manager(self):
        if self.use_paid_list.get():
            self.only_include_paid_checkbox.pack(side="right")
            self.paid_button.pack()
            self.paid_breadcrumbs.pack()
        else:
            self.only_include_paid_checkbox.pack_forget()
            self.only_include_paid.set(False)
            self.paid_button.pack_forget()
            self.paid_breadcrumbs.pack_forget()

    def set_inputs(self):
        if self.item != None:
            self.file_label_item.destroy()
            self.file_label_item_image.destroy()
        self.item = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("png files","*.png"),("all files", "*.*")))
        self.render_item = ImageTk.PhotoImage(Image.open(self.item).resize((16,16)))
        self.file_label_item = ttk.Label(self.file_open_item, text=self.item)
        self.file_label_item_image = ttk.Label(self.file_open_item, image=self.render_item)
        self.file_label_item_image.image = self.render_item
        self.file_label_item.pack(side= "bottom")
        self.file_label_item_image.pack(side="bottom")


    def set_paid_list(self):
        self.model = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("png files","*.png"),("all files", "*.*")))
        self.render_model = ImageTk.PhotoImage(Image.open(self.model).resize((64,32)))
        self.file_label_model = ttk.Label(self.file_open_model, text=self.model)
        self.file_label_model_image = ttk.Label(self.file_open_model, image=self.render_model)
        self.file_label_model_image.image = self.render_model
        self.file_label_model.pack(side= "bottom")
        self.file_label_model_image.pack(side="bottom")
            

Gui = GUI()
