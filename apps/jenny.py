import streamlit as st
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


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


def stock_price():
    symbol = st.text_input(label="輸入想要查詢的股票代碼", value="0050.TW")
    stock_obj = yf.Ticker(symbol)

    st.write(f"## 分析 {stock_obj.info['longName']}")
    st.write(f"### 目前成交價格為：**{get_price(symbol)}**")
    stock_df = stock_obj.history(
        start="2011-3-12", end="2021-3-12", auto_adjust=False
    )  # period="max"

    st.line_chart(stock_df.Close)
    st.bar_chart(stock_df.Volume)

    stock_daily_return = stock_df["Adj Close"].ffill().pct_change()
    start = stock_daily_return.index[0]
    end = stock_daily_return.index[-1]  # 以 stock 的最後一天為結束日期.

    year_difference = (
        relativedelta(end, start).years
        + (relativedelta(end, start).months) / 12
        + (relativedelta(end, start).days) / 365.2425
    )

    init_balance = balance = 3000
    total_balance = stock_daily_return.copy()
    total_balance[0] = 0

    for i in range(len(stock_daily_return)):
        balance = balance * (1 + total_balance[i])
        total_balance[i] = balance

    total_balance.rename("成長變化", inplace=True)

    st.line_chart(total_balance)

    return_rate = (total_balance[-1] - total_balance[0]) / total_balance[0]
    st.write(
        f"如果當初投資 {init_balance} 元，現在會有 {total_balance[-1]} 元。經過約 {year_difference:.2f} 年的變化，投資報酬率為 {return_rate * 100:.2f}%。"
    )

    st.write("股票基本資料：")
    stock_info = stock_obj.info

    st.write(stock_info)


def stock_range():
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
        (0.1, 2, 0.2, 1, 0.1)
    )

    row0_1.title("定期定額股票查詢系統")

    with row0_2:
        st.write("")

    row0_2.subheader(
        "A Simple Stock Analysis App by [Brian L. Chen](https://icheft.github.io) (CHINESE VER.)"
    )

    row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

    with row1_1:
        st.markdown("定期定額投資成果查詢。")
        st.markdown("**請按照格式要求輸入值。可以輸入不同於預設的投資標的唷！** 👇🏾")

    row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3 = st.columns(
        (0.1, 1.5, 0.1, 1.5, 0.1)
    )

    with row2_1:
        stock_id = st.text_input("輸入你的股票代碼*", "0050.TW")

        need_help = st.expander("需要幫忙嗎？ 👉")
        with need_help:
            st.markdown(
                """不知道您欲查詢的投資標的？只要搜尋「股票代碼.TW」就可以繼續查詢，如「0050.TW」。完整的台股代碼可以參考[本國上市證券國際證券辨識號碼一覽表](https://isin.twse.com.tw/isin/C_public.jsp?strMode=2)。
有些上櫃公司的代碼需要加上「.TWO」。如果出現錯誤，請至 [Yahoo! Finance](https://finance.yahoo.com) 搜尋。"""
            )

    with row2_2:
        installment = st.number_input("輸入定期定額金額", value=3000, step=1000, min_value=1000)

    (
        row3_spacer1,
        row3_1,
        row3_spacer2,
        row3_2,
        row3_spacer3,
        row3_3,
        row3_spacer4,
    ) = st.columns((0.1, 1, 0.05, 1, 0.05, 1, 0.1))

    with row3_1:
        start_date = st.date_input("開始日期", datetime.date(2000, 1, 1))

    with row3_2:
        end_date = st.date_input("結束日期", datetime.date.today())

    with row3_3:
        offset_day = int(
            st.selectbox("每月扣款日", ("6", "16", "26"))
        )  # multichoice to be added

    line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))


def app():
    st.write("# 成果 - 股票分析")
    st.write("本頁面僅使用台灣地區股票作為例子。")
    st.write(
        """### Stockie - 股票查詢小工具
            嗨，我是 Jenny。在這個簡單的小工具中，你可以達成以下事項：
            1. 查詢股票目前的股價
            2. 查詢股票的成交量
            3. 查詢股票的資訊
            4. 查詢股票特定時間區間下來的報酬率"""
    )

    stock_price()
    stock_range()
    st.button("重新整理")
