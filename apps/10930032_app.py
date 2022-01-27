import streamlit as st
import io
import yfinance as yf
import pandas as pd


def app():
    st.markdown(
        """# 這是股票查詢小工具٩(●˙▿˙●)۶…⋆ฺ
Hello~我是**Mina** 現在是高二生。這是這次資管營的小作業，難到瘋掉的那種。
功能：
1. 查詢股票目前的股價
2. 查詢股票的成交量
3. 查詢股票的資訊
4. 查詢股票特定時間區間下來的報酬率
"""
    )

    st.write("\n")

    symbol = st.text_input("輸入欲查詢的股票", "APPL")

    stock_obj = yf.Ticker(symbol)

    st.write(f"## 分析 {symbol} ({stock_obj.info['longName']})")
    period = st.selectbox(
        "選擇時間區間", ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=4
    )  # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max

    stock_df = stock_obj.history(period=period, auto_adjust=False)  # period="max"
    try:
        st.markdown(f'### 最新成交價格：**{stock_obj.info["regularMarketPrice"]}**')
    except:
        st.markdown(
            f"### 最新成交價格：**{stock_obj.history(period='1d', interval='1m', auto_adjust=False).sort_index(ascending=False).head(1).iloc[0, 0]}**"
        )

    st.markdown(f"### 市場走勢圖")
    st.line_chart(stock_df.Close)
    st.markdown(f"### 月成交量")
    st.bar_chart(stock_df.resample("MS").sum().Volume)

    p_1_year_ago = stock_df["Adj Close"][0]
    p_now = stock_df["Adj Close"][-1]
    return_rate = (p_now - p_1_year_ago) / p_1_year_ago
    # daily_returns = stock_df["Adj Close"].pct_change()
    # cum_returns = (daily_returns + 1).cumprod()
    # return_rate2 = (cum_returns[-1] - 1) / 1

    st.markdown(
        f"從 {stock_df['Adj Close'].index[0].strftime('%Y 年 %m 月 %d 日')} 到 {stock_df['Adj Close'].index[-1].strftime('%Y 年 %m 月 %d 日')}，{symbol} 的累積報酬率為 {round(return_rate * 100, 2)}%。"
    )

app()