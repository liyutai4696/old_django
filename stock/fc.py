from old_django.settings import SQLITE_ENGINE

import pandas as pd

def load_stock_csv(data):

    d = pd.DataFrame(data,index=[0])
    d.to_sql('stock_list',SQLITE_ENGINE,index=False,if_exists='append')
