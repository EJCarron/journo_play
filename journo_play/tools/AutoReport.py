import pandas as pd

def print_columns(df):
    for col in df.columns:
        print(col)

def column_report(df):

    pd.display(df.dtypes)

    # for col in df.columns:
    #     if df[col].iloc