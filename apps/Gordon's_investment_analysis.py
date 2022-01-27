from bs4 import BeautifulSoup
import time
from datetime import datetime
import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import pws
import streamlit as st

def app(stock_id='2330.TW'):
    st.write("""Gordon的股票查詢小工具
             嗨，我是Gordon。在這個簡單的小工具中，你可以達成以下事項：
             1. 查詢股票目前的股價
             2. 查詢股票的成交量
             3. 查詢股票的資訊
             4. 查詢股票特定時間區間下來的報酬率""")
             
    symbol = st.text_input("輸入欲查詢的股票")

    stock_obj = yf.Ticker(symbol)

    st.write(f"## 分析 {symbol} ({stock_obj.info['longName']})")
    
    # 印出我們的標題

    current_price = pws.get_price(stock_id)
    year, div_yield, total_div = pws.get_dividend_yield(stock_id)

    st.write(f'參考時價：{current_price}｜殖利率：{div_yield * 100}%')

    stock_df = stock_obj.history(
        start='2011-3-12', end='2021-3-12', auto_adjust=False)  # period="max"

    ock_df = stock_obj.history(
        start='2011-3-12', end='2021-3-12', auto_adjust=False)  # period="max"

    st.write('股市回測線：')
    st.line_chart(stock_df['Adj Close'])
#     plt.show()

    stock_monthly_returns = stock_df['Adj Close'].resample(
        'M').ffill().pct_change() * 100
    stock_yearly_returns = stock_df['Adj Close'].resample(
        'Y').ffill().pct_change() * 100

    stock_yearly_returns.index = stock_yearly_returns.index.strftime(
        '%Y')  # 將 index 的 dateformat 改成‘年’
    st.write('年度報酬率：')
#     stock_yearly_returns.dropna().plot(kind='bar')
#     plt.show()
    st.bar_chart(stock_yearly_returns.dropna())

    stock_daily_return = stock_df['Adj Close'].ffill().pct_change()

    start = stock_daily_return.index[0]
    end = stock_daily_return.index[-1]  # 以 stock 的最後一天為結束日期.

    year_difference = relativedelta(end, start).years + (relativedelta(
        end, start).months)/12 + (relativedelta(end, start).days)/365.2425

    # 假設一開始我們有 3000 元

    init_balance = balance = 3000
    total_balance = stock_daily_return.copy()
    total_balance[0] = 0

    for i in range(len(stock_daily_return)):
        balance = balance * (1+total_balance[i])
        total_balance[i] = balance

    total_balance.rename('成長變化', inplace=True)
    st.line_chart(total_balance)

    return_rate = (total_balance[-1] - total_balance[0])/total_balance[0]

    cgar = (((1+return_rate)**(1/year_difference))-1)

    st.write(
        f'經過 {year_difference} 年後，變成 {total_balance[-1]} 元｜年化報酬率為 {cgar * 100}%')

    # 股票基本資料
    stock_info = stock_obj.info


app()