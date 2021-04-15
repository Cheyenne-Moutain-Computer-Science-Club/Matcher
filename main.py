
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
            if self.convertions[key][0] == row[key]:
                convert.append(0)
            elif self.convertions[key][1] == row[key]:
                convert.append(1)
            elif self.convertions[key][2] == row[key]:
                convert.append(2)
            elif self.convertions[key][3] == row[key]:
                convert.append(3)
            else:
                raise TypeError

        Main.inputs[key] = convert

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            Main.profiles[index] = {
                'id': index,
                'coords': [],
                'matches': []
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
        self.apothem = 15

    def calc_distance(self, id1, id2):
        return ((Main.profiles[id1]['coords'][0] + Main.profiles[id2]['coords'][0])**2 + (Main.profiles[id1]['coords'][1] + Main.profiles[id2]['coords'][1])**2) **(1/2)

    # TODO: Write Harry's Function
    def get_people(self, id):
        for key, prof1 in Main.profiles.items():
            apothem = 15
            people = self.in_range()
            while len(people) < 7:
                apothem += 3
                people = self.in_range()
        Main.profile[key]['matchs'] = people

            
    
    def in_range(self):
        people = []
        for key, prof in self.profiles.items():
            if ((self.profiles[di]['coords'][0] - self.apothem) < prof['coords'][0] < (self.profiles[di]['coords'][0] + self.apothem)) and ((self.profiles[di]['coords'][1] - self.apothem) < prof['coords'][1] < (self.profiles[di]['coords'][1] + self.apothem)):
                people.append(key)
        return people

# TODO: Write Compilation script
class Compile(Main):
    def __init__(self):
        pass

    # TODO: Generate output CSV
    def generate_output(self):
        pass

# ! Should separate in case of errors
# class MailMerge(Main):
#     def __init__(self):
#         pass

# TODO: Update GUI from heads
class GUI(Main):
    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)
        # Sets up the main window
        self.root = ThemedTk(theme="arc")
        self.root.title('DECA Project')
        self.root.geometry('650x300')
        # self.root.iconbitmap(r'')
        self.tab_control = ttk.Notebook(self.root)

        # self.grid_rowconfigure(0, weight=1) # this needed to be added
        # self.grid_columnconfigure(0, weight=1) # as did this

        # self.columnconfigure(0, weight = 1)
        # self.rowconfigure(0, weight = 1)
        # self.rowconfigure(1, weight = 1)
        # self.rowconfigure(2, weight = 1)
        # self.rowconfigure(3, weight = 1)

        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.menu = ttk.Frame(self.tab_control)
        self.log = ttk.Frame(self.tab_control)
        self.output = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu, text="Import Values")
        self.tab_control.add(self.log, text="Log")
        self.tab_control.add(self.output, text="Output")

        # self.tab_control.pack(expand=1, fill="both")
        self.tab_control.grid(column = 1, row = 1, columnspan = 10, sticky = tk.N)


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
        # self.file_open_inputs.pack()
        self.paid_text = ttk.Label(self.file_open_inputs, text="Input List Settings:")
        # self.paid_text.pack(side='top')
        self.paid_text.grid(row=1, column=2, sticky=tk.N)
        self.input_spacer = ttk.Label(self.file_open_inputs, text="")
        self.input_spacer.grid(row=2, column=2)
        self.file_open_inputs.grid(row=3, column=2, sticky='n')
        self.file_open_inputs_button = ttk.Button(self.file_open_inputs, command=self.set_inputs, text="Select Responses CSV")
        # self.file_open_inputs_button.pack()
        self.file_open_inputs_button.grid(row=3, column=2, sticky='n')

        self.frame_spacer = ttk.Label(self.menu, text="")
        self.frame_spacer.grid(row=6, column=2)

        self.paid = ttk.Frame(self.menu)
        # self.paid.pack()
        self.paid.grid(row=7, column=2, sticky=tk.N)
        self.paid_text = ttk.Label(self.paid, text="Paid List Settings:")
        # self.paid_text.pack(side='top')
        self.paid_text.grid(row=7, column=2)
        self.paid_active = tk.IntVar()
        self.pay_checkbox = ttk.Checkbutton(self.paid, text="Use Paid List?", variable=self.paid_active)
        self.paid_spacer = ttk.Label(self.paid, text="")
        self.paid_spacer.grid(row=8, column=2)
        # self.pay_checkbox.pack(side='left')
        self.pay_checkbox.grid(row=9, column=1)
        # self.file_open_model = ttk.Frame(self.paid)
        # self.file_open_model.pack()
        self.file_open_button_model = ttk.Button(self.paid, command=self.set_paid, text="Select Paid List CSV")
        # self.file_open_button_model.pack(side='right')
        self.file_open_button_model.grid(row=9, column=2)

        # self.catagories = ['Please select a category', 'concrete', 'dim', 'dirt', 'logs', 'misc', 'natural', 'ores', 'redstone', 'stone', 'terracotta', 'utility', 'water', 'wool', 'mob']
        # self.display_catagories = ['Please select a category', 'Concrete', 'Dimensions', 'Dirt', 'Logs', 'Miscellaneous', 'Natural', 'Ores', 'Redstone', 'Stone', 'Terracotta', 'Utility', 'Water', 'Wool', 'Mob']
        # self.var = tk.StringVar(self.menu)
        # self.var.set("Please select a category")
        # self.option = ttk.OptionMenu(self.menu, self.var, *self.display_catagories)
        # self.option.pack(side=tk.LEFT)

        self.start_button = ttk.Button(self.menu, text='Run', command=self.start)
        # self.start_button.pack(side= tk.RIGHT)
        self.start_button.grid(row=10, column = 3)

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
