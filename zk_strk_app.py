
import streamlit as st
import requests
from datetime import datetime

# 幣種配置
TOKENS = {
    "ZK": {"symbol": "zksync", "weight": 0.6},
    "STRK": {"symbol": "starknet", "weight": 0.4}
}

# 讀取價格資料
def fetch_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()[symbol]["usd"]
    return None

# 布林通道模擬（簡化假設）
def estimate_entry(price):
    return round(price * 0.96, 4)

# Streamlit UI
st.title("ZK × STRK 每日DCA助手")
st.markdown("策略：穩健偏激進，預算預設每日 10 USDT，可自定")

# 預算輸入
daily_budget = st.number_input("每日總預算（USDT）", min_value=1.0, max_value=100.0, value=10.0, step=1.0)

# 當前時間
st.markdown(f"⏱️ 今日：{datetime.now().strftime('%Y-%m-%d')}")

# 顯示價格與建議下單點位
st.subheader("📊 幣價與建議下單")
for token, data in TOKENS.items():
    price = fetch_price(data["symbol"])
    if price:
        amount = round(daily_budget * data["weight"], 2)
        entry = estimate_entry(price)
        st.markdown(f"### {token}")
        st.write(f"目前價格：${price}")
        st.write(f"建議下單點位（布林通道近似下緣）：${entry}")
        st.write(f"建議投入金額：${amount}")
    else:
        st.error(f"無法取得 {token} 價格資料。")

st.caption("資料來源：CoinGecko API，非即時布林值，僅作參考。")
