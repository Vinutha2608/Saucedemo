import os

import pandas as pd


def get_excel_data(sheet_name):
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "test_data",
        "testdata.xlsx"
    )
    data = pd.read_excel(file_path,sheet_name=sheet_name)
    print(data.values.tolist())
    return data.values.tolist()