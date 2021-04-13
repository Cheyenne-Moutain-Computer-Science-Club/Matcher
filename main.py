
# =====================
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import tkinter as tk
# import random


class Main():
    profiles = {}
    output_csv = None

    def __init__(self, input_csv, pay_csv):
        self.inputs = pd.DataFrame(pd.read_csv(input_csv))


class Lint(Main):
    def __init__(self, convertions):
        super().__init__()
        self.convertions = convertions

    def convert(self, key):
        convert = []

        for index, row in Main.inputs.iterrows():
            if convertions.key[0] == row[key]:
                convert.append(0)
            elif convertions.key[1] == row[key]:
                convert.append(1)
            elif convertions.key[2] == row[key]:
                convert.append(2)
            elif convertions.key[3] == row[key]:
                convert.append(3)
            else:
                raise TypeError

        inputs[key] = convert

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            profiles[index] = {
                'id': index,
                'coords': [],
                'matchs': []
            }


class Graph(Main):
    def __init__(self):
        super().__init__()

    def create_coordinates(self, id):
        pass


class Distance(Main):
    def __init__(self):
        super().__init__()
        self.in_range = []
        self.range = [0,0]
        self.apothem = 0

    def calc_distance(self, id1, id2):
        return ((Main.profiles[id1]['coords'][0] + Main.profiles[id2]['coords'][0])**2 + (Main.profiles[id1]['coords'][1] + Main.profiles[id2]['coords'][1])**2) **(1/2)

    def get_people(self, id):
        # Get coords from id
        # Go through dict and if in range, add to self.in_range
        # If self.in_range.length() < 5, do over again with larger apothem
        # Else, grab five random people from that range and order by distance
        # Append this array to profile from id
        pass


class Compile(Main):
    def __init__(self):
        pass


# class MailMerge(Main):
#     def __init__(self):
#         pass


class GUI(Main):
    def __init__(self):
        # Sets up the main window
        self.root = ThemedTk(theme="arc")
        self.root.title('DECA Project')
        self.root.geometry('650x300')
        # self.root.iconbitmap(r'')
        self.tab_control = ttk.Notebook(self.root)

        self.menu = ttk.Frame(self.tab_control)
        self.log = ttk.Frame(self.tab_control)
        self.output = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu, text="Import Values")
        self.tab_control.add(self.log, text="Log")
        self.tab_control.add(self.output, text="Output")

        self.tab_control.pack(expand=1, fill="both")


        self.test = ttk.Label(self.log, text="TEST!!!")
        # self.textbox = ttk.Frame(self.menu)
        # self.textbox.pack()
        # self.name_label = ttk.Label(self.textbox, text="Name your Head:")
        # self.name_label.pack(side="left")
        # self.name_text = ttk.Entry(self.textbox, width=50)
        # self.name_text.pack(side="left")
        #
        # self.idbox = ttk.Frame(self.menu)
        # self.idbox.pack()
        # self.id_label = ttk.Label(self.idbox, text="Head id:")
        # self.id_label.pack(side="left")
        # self.id_text = ttk.Entry(self.idbox, width=50)
        # self.id_text.pack(side="left")

        self.file_open_inputs = ttk.Frame(self.menu)
        self.file_open_inputs.pack()
        self.file_open_inputs_button = ttk.Button(self.file_open_inputs, command=self.set_inputs, text="Select Responses CSV")
        self.file_open_inputs_button.pack()

        self.paid = ttk.Frame(self.menu)
        self.paid.pack()
        self.paid_text = ttk.Label(self.paid, text="Paid List Settings:")
        self.paid_text.pack(side='top')
        self.paid_active = tk.IntVar()
        self.pay_checkbox = ttk.Checkbutton(self.paid, text="Use Paid List?", variable=self.paid_active)
        self.pay_checkbox.pack(side='left')
        # self.file_open_model = ttk.Frame(self.paid)
        # self.file_open_model.pack()
        self.file_open_button_model = ttk.Button(self.paid, command=self.set_paid, text="Select Paid List CSV")
        self.file_open_button_model.pack(side='right')

        # self.catagories = ['Please select a category', 'concrete', 'dim', 'dirt', 'logs', 'misc', 'natural', 'ores', 'redstone', 'stone', 'terracotta', 'utility', 'water', 'wool', 'mob']
        # self.display_catagories = ['Please select a category', 'Concrete', 'Dimensions', 'Dirt', 'Logs', 'Miscellaneous', 'Natural', 'Ores', 'Redstone', 'Stone', 'Terracotta', 'Utility', 'Water', 'Wool', 'Mob']
        # self.var = tk.StringVar(self.menu)
        # self.var.set("Please select a category")
        # self.option = ttk.OptionMenu(self.menu, self.var, *self.display_catagories)
        # self.option.pack(side=tk.LEFT)

        self.start_button = ttk.Button(self.menu, text='Run', command=self.start)
        self.start_button.pack(side= tk.RIGHT)

        self.root.mainloop()

    def start(self):
        # super().__init__()
        self.name = self.name_text.get()
        self.id = self.id_text.get()
        self.catagory = self.catagories[self.display_catagories.index(self.var.get())]
        if (self.name == None) or (self.name == ""):
            tk.messagebox.showinfo("Error", "Please enter a head name!")
            return
        elif (self.id == None) or (self.id == ""):
            messagebox.showinfo("Error", "Please enter an id!")
            return
        elif self.item == None:
            messagebox.showinfo("Error", "Please select art for the Item!")
            return
        elif self.model == None:
            messagebox.showinfo("Error", "Please select art for the Model!")
            return
        elif self.catagory == 'Please select a category':
            messagebox.showinfo("Error", "Please select a Category!")
            return

        self.menu.pack_forget()
        self.add()

        # Clears all test boxes and file labels
        self.name_text.delete(0, len(self.name_text.get()))
        self.id_text.delete(0, len(self.id_text.get()))
        self.file_label_item.destroy()
        self.file_label_model.destroy()
        self.menu.pack()


    # setters for the filepaths
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


    def set_paid(self):
        self.model = filedialog.askopenfilename(initialdir = r"C:",title = "Select file",filetypes = (("png files","*.png"),("all files", "*.*")))
        self.render_model = ImageTk.PhotoImage(Image.open(self.model).resize((64,32)))
        self.file_label_model = ttk.Label(self.file_open_model, text=self.model)
        self.file_label_model_image = ttk.Label(self.file_open_model, image=self.render_model)
        self.file_label_model_image.image = self.render_model
        self.file_label_model.pack(side= "bottom")
        self.file_label_model_image.pack(side="bottom")


if __name__ == "__main__":
    GUI = GUI()
