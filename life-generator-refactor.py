# Name: Steinar Jennings
# Course: CS 361
# Description: Life Generator - GUI and main program logic

from tkinter import *
from tkinter import ttk
from csv_logic import *
from instructions import *
import sys
import time
import random

# basic setup logic and detail taken from stackexchange for using "grid"
root=Tk()
root.wm_title("Life Generator")
mainframe = ttk.Frame(root, padding="10 10 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# This is used to pull our "entry" values
category=StringVar() 
quantity=StringVar() 

# variable definitions 
item_type = "Toys"
valid = 0   # this is used to evaluate whether or not we can run based on the user input we were provided.
cat_value = None    # this value is defaulted to "None" 
quantity_value = None
num_addresses = []
addresses = []

# stores and updates the values of the input
def search_and_output():
    delete_table()  # we are deleting the table everytime we run a new search_and_output so it doesn't overwrite
    global cat_value
    global item_type
    global quantity_value
    global valid
    global num_addresses
    global addresses
    # checks to see if we need to get our inputs from the text entry GUI or files
    if valid == 1 or valid == 2:
        quantity_value = int(quantity_value)
        pass
    else:
        cat_value = category.get()
        quantity_value = int(quantity.get())
    res = search_database(item_type, cat_value, quantity_value) # parses the DB for our information
    if valid == 2:  # if this is an address call, we execute this logic
        toys_list = get_toys_from_res(res)
        rand_toys = generate_address_table(res,item_type, cat_value, quantity_value, num_addresses, addresses, toys_list)
        create_csv_response(res, addresses, rand_toys)
        valid = 0
    else:
        # warning to check for existing CSV file overwrite
        if path.exists("response.csv") or path.exists("output.csv"):
            popupmsg("Warning", "CSV file in current directory has been overwritten, please rename file to avoid overwriting.")
        create_csv_pd(res, item_type, cat_value, quantity_value)
        generate_table(res,item_type,cat_value,quantity_value)
    return

# this is used to store JUST the toys in a data structure to have a random choice performed
def get_toys_from_res(res):
    toys = []
    for i in range(len(res)):
        toys.append(res[i][1])
    return toys     # our original results item was stored in a larger structure, this will help us randomize toys

# This function will parse the Address CSV input and strip the key information to be used by the main program
# Note: although this code is similar to the other parse function it requires enough differring logic to justify its own function
def parse_address_file():
    # global declarations to be populated by input
    global cat_value
    global item_type
    global quantity_value
    global num_addresses
    global valid
    filename = "request.csv"
    with open(filename, encoding='utf8') as input_file:
        csv_reader = csv.reader(input_file, delimiter=',')    # our delimiter is set as a "," since it's a csv file
        line_count = 0   # mostly used to track the first line of processing, but a good piece of data nonetheless
        for row in csv_reader:
            #checks to make sure we are evaluating the header row
            if line_count == 0:
                line_count += 1
                continue
            # otherwise, we will be parsing for our specific category, and pulling the data we need from the CSV.
            else:
                input_item_type = row[0]    # stores "Toys" for now
                user_category = row[1]      # process the category provided
                cat_value = user_category
                num_to_generate = row[2]    # process the number of entries to generate
                quantity_value = num_to_generate
                num_addresses.append(row[3])
                addresses.append(row[4])
        valid = 2
    return search_and_output()

# This function will parse the Input CSV and strip the key information to be used by the main program
# Note: This parse function checks to see if an arg was recieved when the program was run the other runs off a button command
def parse_input():
    global cat_value
    global item_type
    global quantity_value
    if len(sys.argv) == 2:
        filename = (sys.argv)[1]
        with open(filename, encoding='utf8') as input_file:
            csv_reader = csv.reader(input_file, delimiter=',')    #our delimiter is set as a "," since it's a csv file
            line_count = 0   # mostly used to track the first line of processing, but a good piece of data nonetheless
            for row in csv_reader:
                #checks to make sure we are evaluating the header row
                if line_count == 0:
                    line_count += 1
                    continue
                # otherwise, we will be parsing for our specific category, and pulling the data we need from the CSV.
                else:
                    input_item_type = row[0]   # stores "Toys" for now
                    user_category = row[1]      # process the category provided
                    cat_value = user_category
                    num_to_generate = row[2]     # process the number of entries to generate
                    quantity_value = num_to_generate
                    return True
    return False

# generates a table for information that includes addresses, since we are storing the
# the rand_toys in here and the row headers are not consistent, it would make a conveluted funciton with if statements, it is 
# easier to just generate a separate table
def generate_address_table(res,item_type,cat_value,quantity_value,num_addresses, addresses, toys_list):
    processed_rows = 0      # used to track where to put new table cells
    # Table Headers
    ttk.Label(mainframe, text="input_item_type", foreground="cyan", background="grey",width=15, anchor="center", borderwidth=2, relief="groove").grid(column=1, row=16)
    ttk.Label(mainframe, text="input_item_category", foreground="cyan", background="grey", width=25, anchor="center", borderwidth=2, relief="groove").grid(column=2, row=16)
    ttk.Label(mainframe, text="num_addresses", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=3, row=16)
    ttk.Label(mainframe, text="address", foreground="cyan", background="grey",width=40, anchor="center", borderwidth=2, relief="groove").grid(column=4, row=16)
    ttk.Label(mainframe, text="output_item_name", foreground="cyan", background="grey",width=40, anchor="center", borderwidth=2, relief="groove").grid(column=5, row=16)
    rangeVal = int(num_addresses[0])        # used to iterate over the range of the addresses, not the range of the toys
    rand_toys = [random.choice(toys_list) for _ in range(rangeVal)]         # stores a random toy rangeVal times in a list
    # Fill Table Cells
    for i in range(rangeVal):
        ttk.Label(mainframe, text=item_type, foreground="black", background="grey",width=15, anchor="center", borderwidth=2, relief="groove").grid(column=(1), row=(17+processed_rows))
        ttk.Label(mainframe, text=cat_value, foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(2), row=(17+processed_rows))
        ttk.Label(mainframe, text=str(num_addresses[0]), foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(3), row=(17+processed_rows))
        ttk.Label(mainframe, text=addresses[i], foreground="black", background="grey",width=40, anchor="w", borderwidth=2, relief="groove").grid(column=(4), row=(17+processed_rows))
        ttk.Label(mainframe, text=rand_toys[i], foreground="black", background="grey",width=40, anchor="w", borderwidth=2, relief="groove").grid(column=(5), row=(17+processed_rows))
        processed_rows += 1
    return rand_toys    # return this value to be used in the csv generation. Since we are randomizing, we need one copy of the rand vals

# This function generates the table for the traditional use (non-address)
def generate_table(res,item_type,cat_value,quantity_value):
    processed_rows = 0    # used to track where to put new table cells
    # Table Headers
    ttk.Label(mainframe, text="input_item_type", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=1, row=16)
    ttk.Label(mainframe, text="input_item_category", foreground="cyan", background="grey", width=25, anchor="center", borderwidth=2, relief="groove").grid(column=2, row=16)
    ttk.Label(mainframe, text="input_number_to_generate", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=3, row=16)
    ttk.Label(mainframe, text="output_item_name", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=4, row=16)
    ttk.Label(mainframe, text="output_item_rating", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=5, row=16)
    ttk.Label(mainframe, text="output_item_num_reviews", foreground="cyan", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=6, row=16)
    # Fill Table Cells
    for ele in res:
        ttk.Label(mainframe, text=item_type, foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(1), row=(17+processed_rows))
        ttk.Label(mainframe, text=cat_value, foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(2), row=(17+processed_rows))
        ttk.Label(mainframe, text=str(quantity_value), foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(3), row=(17+processed_rows))
        for i in range(1,len(ele)):
            ttk.Label(mainframe, text=ele[i], foreground="black", background="grey",width=25, anchor="center", borderwidth=2, relief="groove").grid(column=(i+3), row=(17+processed_rows))
        processed_rows += 1
    # nothing is returned here since we aren't randomizing values

# when we update our screen, we need to clear the current table fully.
def delete_table():
    for label in mainframe.grid_slaves():
        if int(label.grid_info()["row"]) >= 16:      # all rows above grid area 16 are table values
            label.grid_forget()

# pop-up help/instructions window
def popupmsg(name="Instructions", message=returnInstructions()):
    popup = Tk()
    popup.wm_title(name)
    mainframe1 = ttk.Frame(popup, padding="10 10 12 12")
    mainframe1.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe1.columnconfigure(0, weight=1)
    mainframe1.rowconfigure(0, weight=1)
    ttk.Label(mainframe1, text=message).grid(column=1, row=1)
    B1 = ttk.Button(mainframe1, text="Okay", command = mainframe1.destroy)
        
# adds tkinter logic to accept input from the user, will be autopopulated if we have valid input
ttk.Entry(mainframe, width=20, text=category).grid(column=2, row=1)
ttk.Label(mainframe, text="Category").grid(column=1, row=1)
ttk.Entry(mainframe, width=20, text=quantity).grid(column=2, row=2)
ttk.Label(mainframe, text="# Of Results").grid(column=1, row=2)

# submit button to run the program and update our variables
ttk.Button(mainframe, text="Run Screen", command = search_and_output).grid(column=1, row=15)
ttk.Button(mainframe, text="Use Address Input", command = parse_address_file).grid(column=2, row=15)
ttk.Button(mainframe, text="Help", command = popupmsg).grid(column=5, row=1)

# runs our parse input function and checks to see if it's viable (wasn't just a header)
if parse_input() == True:
    valid = 1

# using this instead of a mainloop
while True:
    root.update_idletasks()
    root.update()
    # check to see if the program was run with user provided input
    if valid == 1:
        search_and_output()
        valid = 0
    
        