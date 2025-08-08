import streamlit as st
import requests
import time

st.set_page_config(page_title="ZK-STRK Combo App V2", layout="centered")
st.title("ZK-STRK Combo App V2")

st.markdown("🟢 已整合未成交偵測與自動加碼邏輯")
st.markdown("🔄 幣價來源：Binance（ZKUSDT / STRKUSDT）")
st.markdown("⚠️ 本 App 僅作為提示示範，不連接真實下單")

def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()["price"])

def run_combo(symbol, base_amount, gap, max_times, multiplier):
    prices = []
    last_price = fetch_price(symbol)
    prices.append(last_price)

    st.write(f"📌 初始價格：{last_price:.4f}")
    executed = [False] * max_times
    levels = [round(last_price * (1 - gap)**i, 4) for i in range(max_times)]

    with st.expander("📊 加碼級距與掛單狀態"):
        for i, price in enumerate(levels):
            st.write(f"第{i+1}層：{price}（{base_amount * multiplier**i:.4f}）")

    placeholder = st.empty()

    while True:
        now = fetch_price(symbol)
        prices.append(now)

        with placeholder.container():
            st.write(f"⏱️ 最新價格：{now:.4f}")
            for i, target in enumerate(levels):
                if now <= target and not executed[i]:
                    st.success(f"✅ 第{i+1}層達成，加碼金額：{base_amount * multiplier**i:.4f}")
                    executed[i] = True
                elif not executed[i]:
                    st.info(f"🔄 第{i+1}層等待中（觸發價 {target}）")

        if all(executed):
            st.balloons()
            st.success("🎉 所有加碼層數已執行完畢！")
            break

        time.sleep(5)

# ==== 使用者介面 ====
st.subheader("💰 參數設定")

symbol = st.selectbox("選擇幣種", ["ZKUSDT", "STRKUSDT"])
base_amount = st.number_input("初始加碼金額（例如 100）", value=100.0)
gap = st.number_input("每層下跌幅度（例如 0.02 代表 -2%）", value=0.02)
max_times = st.number_input("最大加碼次數", value=5, step=1)
multiplier = st.number_input("每次加碼倍率（例如 1.5）", value=1.5)

if st.button("🚀 開始追蹤與加碼模擬"):
    run_combo(symbol, base_amount, gap, max_times, multiplier)

