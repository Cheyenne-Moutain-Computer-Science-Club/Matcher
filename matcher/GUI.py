# =====================
# Package imports
# =====================
import sys
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter as tk
import time
import threading
from tkinter import messagebox
import json
import os
# =====================
# Module imports
# =====================
from matcher.core import Core
from matcher.data import Data
# =====================
# Script
# =====================


class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, borderwidth=0, height=600)
        self.viewPort = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.viewPort, anchor="nw",
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.on_frame_configure(None)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


class GUI(Data):
    def __init__(self):
        # ============================
        # Setup
        # ============================
        # Class setup
        self.Core = Core()
        super().__init__()

        # # Os setup
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        # Tkinter setup
        self.root = ThemedTk(theme="breeze")
        self.root.title('Matcher')
        self.root.geometry('650x600')
        self.root.iconbitmap(resource_path(r'assets/radio.ico'))
        # self.root.iconbitmap(r'assets/radio.ico')
        self.root.resizable(False, True)
        self.style = ttk.Style(self.root)

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

        # *Maybe Change to Data????
        # Other variable setup
        self.inputs_path = None
        self.filtered_path = None
        self.output_path = None
        self.convert_path = None

        # Tab control
        self.tab_control = ttk.Notebook(self.root, width=650)

        self.menu = ttk.Frame(self.tab_control)
        self.options = ttk.Frame(self.tab_control)
        self.log = ttk.Frame(self.tab_control)
        self.output_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu, text="Import Values")
        self.tab_control.add(self.options, text="Advanced Options")
        # self.tab_control.add(self.log, text="Log")
        self.tab_control.add(self.output_tab, text="Output")

        self.tab_control.pack(expand = True)

        # Canvas and Scrollbar setup
        self.scrollFrame = ScrollFrame(self.menu)

        # ============================
        # Data Menu
        # ============================

        # Inputs
        self.inputs = ttk.Frame(self.scrollFrame.viewPort)
        self.inputs.pack(pady=5)
        self.input_header = ttk.Label(self.inputs,
                                      text="Input Settings",
                                      font=("Microsoft JhengHei UI", 12))
        self.input_header.pack()
        self.input_spacer = ttk.Label(self.inputs, text="")
        self.input_spacer.pack()
        self.inputs_button = ttk.Button(self.inputs, text="Select Responses", command=self.set_inputs)
        self.inputs_button.pack()
        self.inputs_breadcrumbs = ttk.Frame(self.inputs)
        self.inputs_breadcrumbs_txt = ttk.Label(self.inputs_breadcrumbs)
        self.inputs_breadcrumbs.pack()
        self.use_csv_radio = ttk.Radiobutton(self.inputs,
                                             value=0,
                                             text="Use Comma Separated Values (*.csv)",
                                             variable=self.use_tsv_inputs)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_inputs_radio = ttk.Radiobutton(self.inputs,
                                                    value=1,
                                                    text="Use Tab Separated Values (*.tsv)",
                                                    variable=self.use_tsv_inputs)
        self.use_tsv_inputs_radio.pack(side="right")
        # Separator
        self.separator1 = ttk.Separator(self.scrollFrame.viewPort, orient='horizontal')
        self.separator1.pack(fill='x')

        # filtered List
        self.filtered = ttk.Frame(self.scrollFrame.viewPort)
        self.filtered.pack(pady=5)
        self.filtered_header = ttk.Label(self.filtered,
                                         text="Filter List Settings",
                                         font=("Microsoft JhengHei UI", 12))
        self.filtered_header.pack()
        self.filtered_spacer = ttk.Label(self.filtered, text="")
        self.filtered_spacer.pack()
        self.filtered_frame = ttk.Frame(self.filtered)
        self.use_filtered_checkbox = ttk.Checkbutton(self.filtered,
                                                     text="Use Filter List",
                                                     variable=self.use_filtered_list,
                                                     command=self.filtered_manager)
        self.use_filtered_checkbox.pack()
        # Hidden Frame
        self.filtered_spacer2 = ttk.Label(self.filtered_frame, text="")
        self.filtered_spacer2.pack(side="top")
        # Button and Breadcrumbs
        self.filtered_button_frame = ttk.Frame(self.filtered_frame)
        self.filtered_button_frame.pack()
        self.filtered_button = ttk.Button(self.filtered_button_frame, text="Select Filter", command=self.set_filtered)
        self.filtered_button.pack()
        self.filtered_breadcrumbs = ttk.Label(self.filtered_button_frame)
        self.filtered_breadcrumbs_txt = ttk.Label(self.filtered_breadcrumbs)
        self.filtered_breadcrumbs.pack()
        # Checkbox
        self.only_include_filtered_checkbox = ttk.Checkbutton(self.filtered_frame,
                                                              text="Only include filtered users in match lists",
                                                              variable=self.only_include_filtered)
        self.only_include_filtered_checkbox.pack()
        # Radio Buttons
        self.use_csv_radio = ttk.Radiobutton(self.filtered_frame,
                                             value=0,
                                             text="Use Comma Separated Values (*.csv)",
                                             variable=self.use_tsv_filtered)
        self.use_csv_radio.pack(side="left")
        self.use_tsv_inputs_radio = ttk.Radiobutton(self.filtered_frame,
                                                    value=1,
                                                    text="Use Tab Separated Values (*.tsv)",
                                                    variable=self.use_tsv_filtered)
        self.use_tsv_inputs_radio.pack(side="right")
        # Separator
        self.separator2 = ttk.Separator(self.scrollFrame.viewPort, orient='horizontal')
        self.separator2.pack(fill='x')

        # Output List
        self.output = ttk.Frame(self.scrollFrame.viewPort)
        self.output.pack(pady=5)
        self.output_header = ttk.Label(self.output,
                                       text="Output Settings",
                                       font=("Microsoft JhengHei UI", 12))
        self.output_header.pack()
        self.output_spacer = ttk.Label(self.output, text="")
        self.output_spacer.pack()

        # Dropdown
        self.display_categories = ['Please select an output format', 'Comma Separated Values (*.csv)',
                                   'Tab Separated Values (*.tsv)', 'Text File (*.txt)']
        self.output_option.set("Please select an output format")
        self.option = ttk.OptionMenu(self.output, self.output_option, *self.display_categories)
        self.option_label = ttk.Label(self.output, text="Output format:")
        self.option_label.pack(side=tk.LEFT)
        self.option.pack(side=tk.RIGHT)
        # Separator
        self.separator3 = ttk.Separator(self.scrollFrame.viewPort, orient='horizontal')
        self.separator3.pack(fill='x')

        # Conversions
        self.conversions = ttk.Frame(self.scrollFrame.viewPort)
        self.conversions.pack()
        self.conversions_label = ttk.Label(self.conversions, text="Question Conversion Options",
                                           font=("Microsoft JhengHei UI", 12))
        self.conversions_label.pack(pady=5)
        self.conversions_spacer = ttk.Label(self.inputs, text="")
        self.conversions_spacer.pack()
        self.convert_button = ttk.Button(self.conversions, text="Select conversion JSON", command=self.set_conversions)
        self.convert_button.pack(pady=5)
        self.convert_breadcrumbs = ttk.Frame(self.conversions)
        self.convert_breadcrumbs_txt = ttk.Label(self.convert_breadcrumbs)
        self.convert_breadcrumbs.pack()

        self.separator6 = ttk.Separator(self.scrollFrame.viewPort, orient='horizontal')
        self.separator6.pack(fill='x')

        # Run
        self.start_button = ttk.Button(self.scrollFrame.viewPort, text='Run', command=self.start)
        self.start_button.pack(pady=10)

        # ============================
        # Advanced Menu
        # ============================

        # Appearance Menu
        self.appearance = ttk.Frame(self.options)
        self.appearance.pack()
        self.appearance_label = ttk.Label(self.appearance, text="Appearance Options",
                                          font=("Microsoft JhengHei UI", 12))
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
        self.display_themes = ["", 'Breeze', 'Adapta', 'Arc', 'Equilux']
        self.theme_selection.set("Breeze")
        self.theme_dropdown = ttk.OptionMenu(self.appearance, self.theme_selection, *self.display_themes,
                                             command=self.update_appearance)
        self.theme_label = ttk.Label(self.appearance, text="Theme:")
        self.theme_label.pack(side=tk.LEFT)
        self.theme_dropdown.pack(side=tk.RIGHT, pady=5)
        # Separator
        self.separator4 = ttk.Separator(self.options, orient='horizontal')
        self.separator4.pack(fill='x')

        # Logging settings
        self.log = ttk.Frame(self.options)
        self.log.pack()
        self.log_label = ttk.Label(self.log, text="Logging Options", font=("Microsoft JhengHei UI", 12))
        self.log_label.pack(pady=5)
        self.log_coming_soon = ttk.Label(self.log, text="Coming Soon!").pack(pady=5)
        # Separator
        self.separator5 = ttk.Separator(self.options, orient='horizontal')
        self.separator5.pack(fill='x')

        # Subsampling options
        self.sub = ttk.Frame(self.options)
        self.sub.pack()
        self.sub_label = ttk.Label(self.sub, text="Subsampling Options", font=("Microsoft JhengHei UI", 12))
        self.sub_label.pack(pady=5)
        self.sub_coming_soon = ttk.Label(self.sub, text="Coming Soon!").pack(pady=5)

        # ============================
        # Output
        # ============================
        self.output_tab_label = ttk.Label(self.output_tab, text="Output:", font=("Microsoft JhengHei UI", 12))
        self.output_tab_label.pack(pady=5)
        self.save_output_button = ttk.Button(self.output_tab, text="Save Output File", command=self.save)
        self.progress_bar = ttk.Progressbar(self.output_tab, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack()

        self.info = ttk.Label(self.output_tab, text="Thank you for using the Matcher program! Designed with ❤ by CMCSC",
                              font=("Microsoft JhengHei UI", 9)).pack(anchor='s')

        self.scrollFrame.pack(side="top", fill="both", expand=True)

        self.root.mainloop()

    # ============================
    # Methods
    # ============================
    def save(self):
        Data.save_output_as = filedialog.asksaveasfilename(initialdir=self.output_path, title="Save File", filetypes=(
            ('CSV file', "*.csv"), ('TSV file', "*.tsv"), ('TXT file', "*.txt"), ("all files", "*.*")))
        if Data.output_option == 'Comma Separated Values (*.csv)':
            Data.output.to_csv(f'{Data.save_output_as}.csv', index=False)
        elif Data.output_option == 'Tab Separated Values (*.tsv)':
            Data.output.to_csv(f'{Data.save_output_as}.tsv', index=False, sep="\t")
        elif Data.output_option == 'Text File (*.txt)':
            Data.output.to_csv(f'{Data.save_output_as}.txt', header=None, index=None, sep=' ', mode='a')
        self.root.destroy()

    def update_appearance(self, *args):
        self.root.resizable(self.scale_x_enabled.get(), self.scale_y_enabled.get())
        if args:
            self.style.theme_use(args[0].lower())
            if args[0] == 'Equilux':
                self.root.configure(bg='#464646')
            elif args[0] != 'Equilux':
                self.root.configure(bg='#fff')

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
        if self.inputs_path is not None:
            self.inputs_breadcrumbs_txt.pack_forget()
        self.inputs_path = filedialog.askopenfilename(initialdir=r"C:", title="Select file", filetypes=(
            ("csv files", "*.csv"), ("tsv files", "*.tsv"), ("all files", "*.*")))
        self.inputs_breadcrumbs_txt.config(text=self.inputs_path)
        self.inputs_breadcrumbs_txt.pack()

    def set_conversions(self):
        if self.convert_path is not None:
            self.convert_breadcrumbs_txt.pack_forget()
        self.convert_path = filedialog.askopenfilename(initialdir=r"C:", title="Select file", filetypes=(
            ("JSON files", "*.json"), ("all files", "*.*")))
        self.convert_breadcrumbs_txt.config(text=self.convert_path)
        self.convert_breadcrumbs_txt.pack()

    def set_filtered(self):
        if self.filtered_path is not None:
            self.filtered_breadcrumbs_txt.pack_forget()
        self.filtered_path = filedialog.askopenfilename(initialdir=r"C:", title="Select file", filetypes=(
            ("csv files", "*.csv"), ("tsv files", "*.tsv"), ("all files", "*.*")))
        self.filtered_breadcrumbs_txt.config(text=self.filtered_path)
        self.filtered_breadcrumbs_txt.pack()

    def start(self):
        if (self.inputs_path is None) or (self.inputs_path == ""):
            tk.messagebox.showerror("Error", "Please enter an input list file path")
            return
        elif ((self.filtered_path is None) or (self.filtered_path == "")) and self.use_filtered_list.get():
            tk.messagebox.showerror("Error", "Please enter a filtered list file path")
            return
        # elif (self.output_path is None) or (self.output_path == ""):
        #     tk.messagebox.showerror("Error", "Please select an output file path!")
        #     return
        elif self.output_option.get() == 'Please select an output format':
            tk.messagebox.showerror("Error", "Please select an output format!")
            return
        elif (self.convert_path is None) or (self.convert_path == ""):
            tk.messagebox.showerror("Error", "Please enter a conversions JSON!")
            return

        # self.Data = Data()

        Data.input_csv = self.inputs_path
        Data.filter_csv = self.filtered_path
        with open(self.convert_path) as f:
            Data.conversions = json.load(f)
        Data.use_tsv_inputs = self.use_tsv_inputs.get()
        Data.use_tsv_filtered = self.use_tsv_filtered.get()
        Data.use_filtered_list = self.use_filtered_list.get()
        Data.only_include_filtered = self.only_include_filtered.get()
        Data.output_option = self.output_option.get()
        
        x: None = threading.Thread(target=self.Core.run).start()
        y: None = threading.Thread(target=self.progress_bar_func).start()
        # self.Core.run()
        # self.progress_bar_func()

    def progress_bar_func(self) -> None:

        self.tab_control.hide(0)
        self.tab_control.hide(1)
        self.tab_control.select(2)

        while True:
            self.progress_bar['value'] = Data.status
            self.root.update_idletasks()
            if self.progress_bar['value'] >= 100:
                self.save_output_button.pack(pady=5)


if __name__ == "__main__":
    GUI = GUI()