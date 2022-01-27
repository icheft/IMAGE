import streamlit as st
import io
import yfinance as yf
import pandas as pd

from bs4 import BeautifulSoup
import time
from datetime import datetime
import requests 
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 新的套件
import streamlit as st
from dateutil.relativedelta import relativedelta # 日期上的運算

st.write ('這是我做的小網站')
st.write('我是羅憶寧')

def get_price(stock_id="0050.TW"):
    url = f"https://tw.stock.yahoo.com/d/s/dividend_{stock_id.split('.')[0]}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    price = soup.find("div", {"class": "D(f) Ai(fe) Mb(4px)"}).find("span").text
    return price

def get_dividend_yield(stock_id="0050.TW", year=None):
    url = f"https://tw.stock.yahoo.com/d/s/dividend_{stock_id.split('.')[0]}.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div_table = soup.find_all("div", {"class": "table-body-wrapper"})[0].find("ul")

    all_years_raw = div_table.find_all("li")
    first_date = all_years_raw[0].find_all("div")[6].text
    if year == None:
        first_year = first_date.split("/")[0]
    else:
        first_year = str(year)

    total_div = 0
    for year_raw in all_years_raw:
        tmp_year = year_raw.find_all("div")[6].text.split("/")[0]
        if tmp_year == first_year:
            total_div += float(year_raw.find_all("div")[3].text)

    div_yield = total_div / float(get_price(stock_id))
    return first_year, div_yield, total_div


def app(stock_id='0050.TW'):
    stock_obj = yf.Ticker(stock_id)

   
    st.title (f'分析 {stock_obj.info["longName"]}')

    current_price = get_price(stock_id)
    year, div_yield, total_div = get_dividend_yield(stock_id)
    

    st.write(f'參考時價：{current_price}｜殖利率：{div_yield * 100}%')

    stock_df = stock_obj.history(
        start='2011-3-12', end='2021-3-12', auto_adjust=False)  # period="max"

    stock_df = stock_obj.history(
        start='2011-3-12', end='2021-3-12', auto_adjust=False)  # period="max"

    st.write('股市回測線：')
    stock_df['Adj Close'].plot.line()
    st.line_chart(stock_df['Adj Close'])

    plt.show()

    stock_monthly_returns = stock_df['Adj Close'].resample('M').ffill().pct_change() * 100
    stock_yearly_returns = stock_df['Adj Close'].resample('Y').ffill().pct_change() * 100

    stock_yearly_returns.index = stock_yearly_returns.index.strftime('%Y') #將 index 的 dateformat 改成‘年’
    st.write('年度報酬率：')
    #stock_yearly_returns.dropna().plot(kind='bar')
    #plt.show()
    st.bar_chart(stock_tearly_returns.dropna())

    stock_daily_return = stock_df['Adj Close'].ffill().pct_change()

    start = stock_daily_return.index[0]
    end = stock_daily_return.index[-1] 

    year_difference = relativedelta(end, start).years + \
        (relativedelta(end, start).months)/12 + \
        (relativedelta(end, start).days)/365.2425


    init_balance = balance = 3000
    total_balance = stock_daily_return.copy()
    total_balance[0] = 0

    for i in range(len(stock_daily_return)):
        balance = balance * (1+total_balance[i])
        total_balance[i] = balance

    total_balance.rename('成長變化', inplace=True)

    return_rate = (total_balance[-1] - total_balance[0])/total_balance[0]

    cgar = (((1+return_rate)**(1/year_difference))-1)

    st.write(f'經過 {year_difference} 年後，變成 {total_balance[-1]} 元｜年化報酬率為 {cgar * 100}%')
    
    stock_info = stock_obj.info
    
app()


