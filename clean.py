# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

mac_path = "/Users/malyajsrivastav/Desktop/"
windows_path = "D:/Users/703143501/Documents/Genpact Internal/oye/"
path = windows_path

def make_hotel_city(path, TableD="TableD", file_type = ".xlsx"):
    file_name = path + TableD + file_type
    mapping = pd.read_excel(file_name)
    hotel_city = dict(zip(mapping['hotel_id'], mapping['city']))
    return hotel_city

hotel_city_dict = make_hotel_city(path)

def return_df(table_name, path, file_type = ".csv", columns_as_dates = ['checkin', 'checkout', 'date']):
    """takes the csv file, and return the dataframe"""
    file_name = path + table_name + file_type
    table_df = pd.read_csv(file_name, parse_dates=columns_as_dates)
    return table_df
    
def subset_df(table_df, hotel_city_dict):
    """return columns for hotel_id and amount"""
    sub = table_df[['hotel_id', 'amount']]
    sub['city'] = np.where(sub['hotel_id'] in hotel_city_dict, hotel_city_dict['hotel_id'], np.NaN)
    return sub
    
def return_pivot(table_df, status_value = 2):
    """takes the data, and return the pivot of customers against
    count of bookings, amount spent, and stayed room_nights"""
    # calculation to compute room_nights as product of oyo_rooms, and checkout minus checkin for rows with status as 2, for rest it is assigned 0
    table_df['room_nights_with_status_2'] = np.where(table_df['status'] == status_value, table_df['oyo_rooms'] * (table_df['checkout'] - table_df['checkin']), 0)
    # applying pivot
    pivot = table_df.pivot_table(values=["booking_id", "amount", "room_nights_with_status_2"], index=["customer_id"],aggfunc={"booking_id": 'count', "amount": np.sum, "room_nights_with_status_2": np.sum})
    return pivot

def unique_cust(table_df):
    """Return the number of unique customers for the month"""
    unique_customers = set(table_df['customer_id'].unique())
    return unique_customers

    
def run(table_name, path, hotel_city_dict):
    table_x = return_df(table_name, path)
    hotel_amount_x = subset_df(table_x, hotel_city_dict)
    pivot_x = return_pivot(table_x)
    unique_cust_x = unique_cust(table_x)
    return unique_cust_x, hotel_amount_x, pivot_x
 
unique_cust_A, hotel_amount_A, pivot_A = run("tableA",path, hotel_city_dict)
unique_cust_B, hotel_amount_B, pivot_B = run("tableB",path, hotel_city_dict)
unique_cust_C, hotel_amount_C, pivot_C = run("tableC",path, hotel_city_dict)


print(hotel_amount_A)
## merging these 3 dataframes
table = pd.concat([pivot_A, pivot_B, pivot_C], axis=1)
#writing the data to a csv file
table.to_csv("python_out.csv", sep=',')
#print("The output is saved as a csv file")

## Repeat customers for month of February = common customers for the month of Feb and Jan
Feb_repeat = len(unique_cust_B.intersection(unique_cust_A))
#print("Number of repeat customers in February: ", Feb_repeat)

## Top 3 revenue earning hotels for each city (for the entire period of time)
# 

