# Jamie Smead
# 02/23/2021
# A Person Generator program that produces an input file for a Life Generator program to process and then
# displays those results on the GUI.

import csv
import random
from tkinter import *
from tkinter import ttk


class StateFile:
    """Represents the state csv file."""

    def __init__(self, state, num_people):
        """Initialize the StateFile object"""
        self.state = state[0:2].lower()
        self.num_people = int(num_people)
        self.state_file = open(f'{self.state}.csv', encoding="utf8")
        self.length = len(list(self.state_file))
        self.state_file.seek(0)
        self.reader = csv.reader(self.state_file)
        self.people = []

    def generate_random(self):
        """Returns an ascending sorted order list of randomly generated numbers with length of self.num_people """
        return sorted([random.randint(1, self.length + 1) for _ in range(self.num_people)])

    def read_line(self):
        """Reads the state csv file and returns a list of addresses"""
        num_list = self.generate_random()
        index = 0

        for row in self.reader:
            if self.reader.line_num - 1 == num_list[index]:
                self.people.append(row)
                if index < len(num_list) - 1: index += 1
        self.close_file()
        return self.people

    def close_file(self):
        """Close the state file"""
        self.state_file.close()


class OutFile:
    """Represents the output.csv file"""

    def __init__(self, address_list, num_people, category, num_toys):
        """Initialize the OutFile object."""
        self.address_list = address_list
        self.num_people = num_people
        self.category = category
        self.num_toys = num_toys

    def write_output_file(self):
        """Writes all address_list rows to the output.csv file."""

        header = ['input_item_type', 'input_item_category', 'input_number_to_generate', 'num_addresses', 'address']
        with open("request.csv", "w", newline='') as outfile:
            output_file = csv.writer(outfile)
            output_file.writerow(header)
            for address in self.address_list:
                output_file.writerow(self.format_address_data(address))

    def format_address_data(self, address):
        """Formats the address that gets written in the output.csv file."""
        # address format: LON,LAT,NUMBER,STREET,UNIT,CITY,DISTRICT,REGION,POSTCODE,ID,HASH
        addr = f"{(address[2].strip())} {address[3].strip()} {address[4].strip()} {address[5].strip()} " \
               f"{address[6].strip()} {address[7].strip()}{address[8].strip()} {address[9].strip()}"
        return ['Toys', self.category, self.num_toys, self.num_people, addr]


class InterfaceInput:
    """Represents the user interface"""

    # Based on the examples available at https://tkdocs.com/index.html

    def __init__(self, root):
        """Initialize the InterfaceInput object."""
        self.root = root
        self.root.title("Person Generator")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame_input, self.frame_output = self.make_frames()
        self.entry_num, self.combobox_state, self.entry_num_toys, self.combobox_category = self.make_and_place_widgets()

    def make_frames(self):
        """Create the content frames of the UI window"""
        frame_input = ttk.Frame(self.root, padding="3 3 12 12")
        frame_input.grid(column=0, row=0)
        frame_output = ttk.Frame(self.root, padding="3 3 12 12")
        frame_output.grid(column=0, row=5)
        return frame_input, frame_output

    def make_and_place_label_people(self):
        """Make and place number of people label."""
        label_people_num = ttk.Label(self.frame_input, text='How many people?')
        label_people_num.grid(column=2, row=1, sticky=(N, W))
        return label_people_num

    def make_and_place_entry_people_number(self):
        """Make and place number of people entry box."""
        num = StringVar()
        entry_num = ttk.Entry(self.frame_input, textvariable=num)
        entry_num.grid(column=3, row=1, sticky=(N, W))
        return entry_num

    def make_and_place_label_state(self):
        """Make and place state label."""
        label_state_choice = ttk.Label(self.frame_input, text='Choose a state')
        label_state_choice.grid(column=2, row=0, sticky=(N, W))
        return label_state_choice

    def make_and_place_combobox_state(self):
        """Make and place the state dropdown."""
        state = StringVar()
        combobox_state = ttk.Combobox(self.frame_input, textvariable=state)
        combobox_state.grid(column=3, row=0, sticky=(N, W))
        combobox_state['values'] = ['AK - Alaska', 'AZ - Arizona', 'CO - Colorado', 'HI - Hawaii', 'ID - Idaho',
                                    'CA - California', 'MT - Montana', 'NM - New Mexico', 'NV - Nevada',
                                    'OR - Oregon', 'UT - Utah', 'WA - Washington', 'WY - Wyoming']
        combobox_state.state(["readonly"])
        return combobox_state

    def make_and_place_label_toys(self):
        """Make and place number of toys label."""
        label_toys_num = ttk.Label(self.frame_input, text='How many top toys?')
        label_toys_num.grid(column=0, row=1, sticky=(N, W))
        return label_toys_num

    def make_and_place_entry_num_toys(self):
        """Make and place number of number of toys entry box."""
        num_toys = StringVar()
        entry_num_toys = ttk.Entry(self.frame_input, textvariable=num_toys)
        entry_num_toys.grid(column=1, row=1, sticky=(N, W))
        return entry_num_toys

    def make_and_place_label_category(self):
        """Make and place category label."""
        label_category_choice = ttk.Label(self.frame_input, text='Choose a category')
        label_category_choice.grid(column=0, row=0, sticky=(N, W))
        return label_category_choice

    def make_and_place_combobox_category(self):
        """Make and place the category dropdown."""
        category = StringVar()
        combobox_category = ttk.Combobox(self.frame_input, textvariable=category)
        combobox_category.grid(column=1, row=0, sticky=(N, W))
        combobox_category['values'] = self.get_categories()
        combobox_category.state(["readonly"])
        return combobox_category

    def make_and_place_button_send_request(self):
        """Make and place the send request button."""
        button_send_request = ttk.Button(self.frame_input, text='Send Request!', command=self.click_request_button)
        button_send_request.grid(column=1, row=2, columnspan=2, sticky=(E, W))
        return button_send_request

    def make_and_place_button_show_result(self):
        """Make and place the show result button."""
        button_show_result = ttk.Button(self.frame_input, text='Show Results!', command=self.click_results_button)
        button_show_result.grid(column=1, row=3, columnspan=2, sticky=(E, W))
        return button_show_result

    def get_categories(self):
        """Makes a list from the contents of the categories.txt file."""
        categories = []
        with open('categories.txt', 'r') as cat_file:
            for line in cat_file:
                categories.append(line.strip())
        return categories

    def make_and_place_widgets(self):
        """Calls the make_and_place methods for the widget."""

        # Widgets that do not need to be returned.
        self.make_and_place_label_people()
        self.make_and_place_label_state()
        self.make_and_place_label_category()
        self.make_and_place_label_toys()
        self.make_and_place_button_send_request()
        self.make_and_place_button_show_result()

        # Widgets that need to be returned.
        return self.make_and_place_entry_people_number(), self.make_and_place_combobox_state(), \
               self.make_and_place_entry_num_toys(), self.make_and_place_combobox_category()

    def click_results_button(self):
        """ Calls show_results when the results button is clicked."""
        self.show_results()

    def click_request_button(self):
        """
        Calls methods needed to populate the output file.
        """
        try:
            state = self.combobox_state.get()
            num_people = self.entry_num.get()
            category = self.combobox_category.get()
            num_toys = self.entry_num_toys.get()
            people = StateFile(state, num_people).read_line()
            OutFile(people, num_people, category, num_toys).write_output_file()
        except ValueError:
            error_msg = 'Enter all required information and try again.'
            print(error_msg)

    def show_results(self):
        """Show the results on the UI."""
        address_list = Text(self.frame_output)
        address_list.config(width=150)
        with open("response.csv", "r", newline='') as infile:
            response_file = csv.reader(infile)
            for address in response_file:
                address_list.insert(END, f'{address[0]} | {address[1]} \n')
                address_list.pack()


def main():
    """Start the program and determine if an input.csv file is used."""
    root = Tk()
    InterfaceInput(root)
    root.mainloop()


if __name__ == "__main__":
    main()


