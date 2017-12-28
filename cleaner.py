""" Python coding solution for the OYO ROOMS problem set -- submitted by MALYAJ SRIVASTAV"""

import pandas as pd
import numpy as np

path = "/Users/malyajsrivastav/Desktop/"



def return_pivot(table_name, file_path, file_type = ".csv", status_value = 2):
    """Returns:
    1) a dataframe of amount, count of bookings, and stayed room_nights for each customer
    2) a set of unique customer ids
    """
    #columns to be parsed as dates
    columns_as_dates = ['checkin', 'checkout', 'date']
    #reading the csv file to a pandas dataframe
    table_df = pd.read_csv(path + table_name + file_type, parse_dates=columns_as_dates)
    #unique customers set
    unique_customers = set(table_df['customer_id'].unique())
    # calculation to compute room_nights as product of oyo_rooms, and checkout minus checkin for rows with status as 2, for rest it is assigned 0
    table_df['room_nights_with_status_2'] = np.where(table_df['status'] == status_value, table_df['oyo_rooms'] * (table_df['checkout'] - table_df['checkin']), 0)
    # applying pivot: to compute total number of bookings for each unique customer,
    # amount spent by each customer, number of room_nights per customer, and stayed room nights
    pivot = table_df.pivot_table(values=["booking_id", "amount", "room_nights_with_status_2"], index=["customer_id"],aggfunc={"booking_id": 'count', "amount": np.sum, "room_nights_with_status_2": np.sum})
    return  pivot, unique_customers

## determining the 3 tables for Jan, Feb, and March months
pivot_A, unique_customers_A = return_pivot(table_name = "TableA", file_path = path)
pivot_B, unique_customers_B = return_pivot(table_name = "TableB", file_path = path)
pivot_C, unique_customers_C = return_pivot(table_name = "TableC", file_path = path)

## merging these 3 dataframes
table = pd.concat([pivot_A, pivot_B, pivot_C], axis=1)
#writing the data to a csv file
table.to_csv("python_out.csv", sep=',')
print("The output is saved as a csv file")

## Repeat customers for month of February = common customers for the month of Feb and Jan
Feb_repeat = len(unique_customers_B.intersection(unique_customers_A))
print("Number of repeat customers in February: ", Feb_repeat)

## Top 3 revenue earning hotels for each city (for the entire period of time)
