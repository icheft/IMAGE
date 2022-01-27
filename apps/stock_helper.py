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

    # 開始進行加總
    total_div = 0
    for year_raw in all_years_raw:
        tmp_year = year_raw.find_all("div")[6].text.split("/")[0]
        if tmp_year == first_year:
            total_div += float(year_raw.find_all("div")[3].text)

    # 利用剛剛的函式幫我們取得現價
    div_yield = total_div / float(get_price(stock_id))
    return first_year, div_yield, total_div

def app(stock_id='0050.TW'):
    st.write("HELLO:)))) Welcome to stock_helper")
    st.write("我是徐皓揚！！")
    st.write("這個網站主要是想要幫助我查到yahoo finance的股市")
    st.write("可以快速地查到資料")
    st.write(">>:33")
    st.write("更新：")
    st.write("yfinance程式好像有問題")
    st.write("只要使用history的語法就會出現'Index' object has no attribute 'tz_localize'的錯誤")
    st.write("可惡只能拿一點點分>:(")
    st.write("")
    stock_id = st.text_input(label="輸入想要查詢的股票代碼", value="2330.TW")

    stock_id = stock_id
    stock_obj = yf.Ticker(stock_id)


    st.write(f'分析 {stock_obj.info["longName"]}')

    current_price = get_price(stock_id)
    year, div_yield, total_div = get_dividend_yield(stock_id)

    st.write(f'參考時價：{current_price}｜殖利率：{div_yield * 100}%')


def main():


    app()
    st.button("reset")


if __name__ == "__main__":
    main()
