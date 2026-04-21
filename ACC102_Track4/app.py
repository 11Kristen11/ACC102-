import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 页面配置
st.set_page_config(page_title="ACC102 Track 4 - Offline Stock Tool", layout="wide")
st.title("Interactive Stock Price Analysis Tool (Offline Demo)")
st.caption("Data Source: Simulated Example Data | ACC102 Mini Assignment")

# 用户输入界面
ticker = st.text_input("Stock Ticker (Demo Mode)", "AAPL")
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2024-01-01"))

# 加载按钮（关键）
if st.button("🔄 Load & Analyze Data"):
    with st.spinner("Loading example data..."):
        # ----------------------
        # 这里用代码生成模拟数据，完全不需要网络
        # ----------------------
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        base_price = 150  # 基础股价
        # 生成趋势+随机波动
        trend = np.linspace(0, 40, len(dates))
        noise = np.random.normal(0, 3, len(dates))
        prices = base_price + trend + noise

        # 构建完整的股票数据框
        data = pd.DataFrame({
            "Open": prices,
            "High": prices + 1.5,
            "Low": prices - 1.5,
            "Close": prices,
            "Adj Close": prices,
            "Volume": np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)

        st.success(f"✅ Example data loaded for {ticker}!")
        st.subheader("📊 Raw Historical Data (Latest 10 Rows)")
        st.dataframe(data.tail(10))

        # 数据处理（和真实分析完全一样）
        data["Daily Return"] = data["Close"].pct_change()
        data["MA50"] = data["Close"].rolling(50).mean()
        data["MA200"] = data["Close"].rolling(200).mean()

        # 价格+均线图
        st.subheader(f"📈 {ticker} Price Trend (MA50 + MA200)")
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        ax1.plot(data["Close"], label="Close Price", color="#1f77b4", linewidth=2)
        ax1.plot(data["MA50"], label="MA50", color="#ff7f0e", linestyle="--")
        ax1.plot(data["MA200"], label="MA200", color="#2ca02c", linestyle="--")
        ax1.set_title(f"{ticker} Stock Price Analysis (Demo)")
        ax1.legend()
        ax1.grid(alpha=0.3)
        st.pyplot(fig1)

        # 日收益率图
        st.subheader("📉 Daily Return Volatility")
        st.line_chart(data["Daily Return"].dropna(), color="#d62728")

        # 关键指标（和真实分析一样）
        st.subheader("💡 Key Financial Insights")
        latest_close = data["Close"].iloc[-1]
        mean_return = data["Daily Return"].mean()
        volatility = data["Daily Return"].std()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Latest Close Price", value=f"${latest_close:.2f}")
        with col2:
            st.metric(label="Avg Daily Return", value=f"{mean_return:.4f}", delta=f"{mean_return*100:.2f}%")
        with col3:
            st.metric(label="Return Volatility", value=f"{volatility:.4f}")

        st.info("ℹ️ Note: This is simulated example data for demonstration purposes.")