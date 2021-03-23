# Name: Steinar Jennings
# Course: CS 361
# Description: Life Generator - Processing Functions for handling csv database and creation

import csv
import sys
import pandas as pd
import os.path
from os import path

# searches the CSV (locally for the file)
def search_database(input_item_type, user_category, num_to_generate):
    output_array = []
    # logic taken largely from real python (processing csv in python)
    with open('amazon_co-ecommerce_sample.csv', encoding='utf8') as csv_file:    # had to specify UTF-8 because I was getting an encoding error.
        csv_reader = csv.reader(csv_file, delimiter=',')    #our delimiter is set as a "," since it's a csv file
        line_count = 0   # mostly used to track the first line of processing, but a good piece of data nonetheless
        for row in csv_reader:
            #checks to make sure we are evaluating the header row
            if line_count == 0:
                line_count += 1
            # otherwise, we will be parsing for our specific category, and pulling the data we need from the CSV.
            else:
                if row[8].partition(' >')[0] == user_category:
                    row_5 = row[5]
                    if row_5 == "":
                        row_5 = "0"
                    output_array.append([row[0], row[1], row_5, row[7]])    # appends uniq_id, product_name, number_of_reviews, average_review_rating to output array
                line_count += 1          
        # naming convenstions are clear here, but we are doing multisorts using a lambda key
        by_id_then_reviews = sorted(sorted(output_array, key=lambda x: x[0]), key = lambda x: int(x[2]), reverse=True)
        gen_num_times_ten = by_id_then_reviews[0:(num_to_generate*10)]
        by_id_then_rating = sorted(sorted(gen_num_times_ten, key=lambda x: x[0]), key = lambda x: float(x[3].partition(' ')[0]), reverse=True)
        res = by_id_then_rating[0:(num_to_generate)]
        return res    # res contains the data that we got from the database ONLY

# logic for handling the csv files using pandas dataframes (did this to handle cases where cells had commas)      
def create_csv_pd(res, input_item_type, user_category, num_to_generate):
    column_1, column_2, column_3, column_4, column_5, column_6 = [], [], [], [], [], []
    for ele in res:
        column_1.append(input_item_type)
        column_2.append(user_category)
        column_3.append(num_to_generate)
        column_4.append(ele[1])
        column_5.append(ele[3])
        column_6.append(ele[2])
    df = pd.DataFrame({'input_item_type': column_1, 'input_item_category': column_2, 'input_number_to_generate': column_3, 'output_item_name': column_4, 'output_item_rating': column_5, 'output_item_num_reviews': column_6})
    df.to_csv('output.csv', index=False)
    
# request address logic for handling the csv files using pandas dataframes
# this is would create a longer, more confusing function to consolidate   
def create_csv_response(res, addresses, toys_list):
    column_1, column_2 = [], []
    for i in range(len(toys_list)):
        column_1.append(addresses[i])
        column_2.append(toys_list[i])
    df = pd.DataFrame({'address': column_1, 'output_item_name': column_2})
    df.to_csv('response.csv', index=False)
