# main.py
# created by Jeremy C. Adams
# created: 2023-03-07

# NOTE: Franklin County Auditor files 1997-07, 1997-10, and all of 1998 except month 10
#       have no data in the CSV file provided on the Auditor's FTP server.
# NOTE2: Consistent problem in 1997 and 1998: one line that contains a comma between two
#        people's names, which messes up the CSV structure: "LEACH JOSEPH T &","JOSEPH T JR &"

import os
import csv
import pandas as pd
import datetime

PARCELS_PATH = 'D:\\Raw_Data\\Franklin_County\\Parcel_CSV\\'


def read_parcel_csv(path):
    df = pd.read_csv(path,
                     encoding='cp1252',
                     on_bad_lines='warn',
                     low_memory=False)
    return df


def clean_dataframe(df, year, month, last_modified_timestamp):
    df.insert(0, 'sys_add_date', pd.to_datetime(datetime.date.today(), yearfirst=True))
    df.insert(1, 'sys_last_mod_ts', pd.to_datetime(last_modified_timestamp))
    df.insert(2, 'appr_year', year)
    df.insert(3, 'appr_month', month)
    return df


def load_db(df):
    x = []
    return True

def traverse_dirs(path, year='1997', month='01'):
    list_of_years = ['1997', '1998', '1999']
    list_of_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for entry in os.scandir(path):
        if entry.is_dir() and entry.path[len(entry.path) - 4:] in list_of_years:
            yr = entry.path[len(entry.path) - 4:]
            traverse_dirs(entry.path, year=yr)
        elif entry.is_dir() and entry.path[len(entry.path) - 2:] in list_of_months:
            yr = year
            mo = entry.path[len(entry.path) - 2:]
            traverse_dirs(entry.path, year=yr, month=mo)
        elif not entry.name.startswith('.') and entry.is_file():
            yr = year
            mo = month
            print(yr, mo, entry.name, entry.path, os.stat(entry.path).st_ctime_ns)
            if entry.name == 'parcel_mod.csv':
                df = read_parcel_csv(entry.path)
                df_clean = clean_dataframe(df, yr, mo, os.stat(entry.path).st_ctime_ns)
                load_db(clean_df)
            else:
                # at this point, don't write to db, but do attempt to put data into a df
                # to find out what needs corrected in original csv
                df = read_parcel_csv(entry.path)
        elif entry.is_dir() and entry.path[len(entry.path) - 4:] not in list_of_years:
            yr = "NA"
            mo = "NA"
            print(yr, mo, entry.name, entry.path, os.stat(entry.path).st_ctime_ns)
            return yr, mo, entry.name, entry.path, os.stat(entry.path).st_ctime_ns


if __name__ == '__main__':
    pd.set_option('display.max_column', 200)
    yr, mo, f_name, f_path, st_ctime_ns = traverse_dirs(PARCELS_PATH)

