<h1 align="center">IMAGE 2022</h1>

<h2 align="center">Stockie - Building a Stock Analysis Web App in Python</h2>

<div align="center">
<em>This repository is affiliated under NTU IM 2022 IMAGE Camp</em>
</div>

<hr/>

+ [學員請看此](#學員請看此)
    + [這是啥？](#這是啥)
    + [怎麼使用？](#怎麼使用)
+ [助教請看此](#助教請看此)
    + [收到 `app.py` 時該怎麼做？](#收到-apppy-時該怎麼做)
    + [還有其他問題？](#還有其他問題)

## 學員請看此

### 這是啥？

你/妳正在看的頁面為 Building a Stock Analysis Web App in Python 的成果展示首頁。你可以在左側的菜單中選擇查看其他同學所做的成果。

如果你不想要你的網頁在網站上顯示，煩請聯絡我們。也先在此致上十二萬分的歉意。

### 怎麼使用？

1. 每個人當初繳交的時有請同學填寫一個英文 ID
2. 此 ID 即為你的 app 名稱，你有兩種存取方式：
    + 直接透過網址訪問，例如：`https://share.streamlit.io/icheft/image-st?p=<your-app-id>`
    + 將左邊的 sidebar 點開來，在成果展示的搜尋欄位中輸入你/妳的 ID 

至於為什麼是 `image-st` 呢？*IMAGE* 顧名思義就是我們營隊的名稱，而 *st* 則是因為我們使用 Streamlit 來幫助我們部署成網站。此命名只是為了方便日後查看原始碼時，有更好的判斷。

## 助教請看此

### 收到 `app.py` 時該怎麼做？

1. 首先，你應該在自己的電腦上面跑一遍同學的 `app.py`，並且將分數記錄下來。
2. 評分標準可以參考此 [demo](https://share.streamlit.io/icheft/image2021-stock-analysis-tutorial/main?p=metrics)，上面有動態紀錄了評分的依據。
3. 評分完之後，請在 GitHub 以你/妳的帳號為名的 branch 中裡的 `apps/` 資料夾中上傳同學的 `app.py` 檔案。**上傳前有幾個步驟需要請你幫忙：**
    + 將同學的 `app.py` 改成 `他的 id.py`（中間不要用空格）
    + 把檔案中散亂各處的 code 包成一個 `app()` function（如果沒有包的話）
    
    ```py
    import streamlit as st
    import yfinance as yf

    def app():
        ...
    
    if __name__ == '__main__':
        app()
    ```

    + 確定該同學的 code 可以用 `app()` 執行。用 `streamlit run <id>.py` 要可以看到同學的網頁。

You're all set!
    
### 還有其他問題？

請直接來找我！感恩 ^^

