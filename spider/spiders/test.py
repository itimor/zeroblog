# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import easyquotation as eq


# ts初始化
ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
df = ts_data.daily(ts_code='000001.SZ,600000.SH', start_date='20210113', end_date='20210113')
print(df)
