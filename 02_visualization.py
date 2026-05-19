import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def run_visualizations():
    # 加载清洗后的数据
    df = pd.read_parquet("./data/cleaned_edgetraffic.parquet")
    plt.style.use('seaborn-v0_8-whitegrid')

    # ================= Q1 图表 =================
    # 图表1：双Y轴时间序列图
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()
    ax1.plot(df.index, df['vehicle_count'], 'b-', label='Vehicle Count', alpha=0.7)
    ax2.plot(df.index, df['cpu_util'], 'r-', label='CPU Utilization', alpha=0.7)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Vehicle Count', color='b')
    ax2.set_ylabel('CPU Util (%)', color='r')
    plt.title("Fig 1: Dynamic Time Series Mapping (Traffic vs System Load)")
    plt.savefig("fig1_timeseries.png", bbox_inches='tight')
    plt.close()

    # 图表2：散点回归图 (定量映射关系)
    plt.figure(figsize=(8, 6))
    sns.regplot(x='vehicle_count', y='cpu_util', data=df,
                scatter_kws={'alpha': 0.3, 'color': 'gray'}, line_kws={'color': 'red'})
    plt.title("Fig 2: Regression Analysis of Traffic Flow and CPU Impact")
    plt.xlabel("Vehicle Count")
    plt.ylabel("CPU Utilization (%)")
    plt.savefig("fig2_regression.png", bbox_inches='tight')
    plt.close()

    # ================= Q2 图表 =================
    # 图表3：交叉相关性时滞分析
    cpu_norm = df['cpu_util'] - df['cpu_util'].mean()
    veh_norm = df['vehicle_count'] - df['vehicle_count'].mean()
    ccov = np.correlate(cpu_norm, veh_norm, mode='full')
    lags = np.arange(-len(df) + 1, len(df))

    plt.figure(figsize=(10, 4))
    plt.plot(lags, ccov, color='purple')
    plt.xlim(-20, 20)
    plt.axvline(3, color='red', linestyle='--', label='Peak at Lag = +3s')  # 标出3秒时滞
    plt.title("Fig 3: Cross-Correlation (Proving the 3-Second Time Lag)")
    plt.xlabel("Lag (Seconds)")
    plt.ylabel("Correlation Coefficient")
    plt.legend()
    plt.savefig("fig3_crosscorr.png", bbox_inches='tight')
    plt.close()

    # 图表4：局部峰值放大对比图 (直观展示时滞)
    df_zoom = df.iloc[100:150].reset_index()  # 截取50秒的数据观察一个完整的波峰
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax2 = ax1.twinx()
    ax1.plot(df_zoom.index, df_zoom['vehicle_count'], 'b-o', label='Traffic Peak', alpha=0.8)
    ax2.plot(df_zoom.index, df_zoom['cpu_util'], 'r-s', label='CPU Peak', alpha=0.8)

    # 添加标注 (假设波峰在相对索引20和23附近)
    ax1.axvline(20, color='blue', linestyle=':', alpha=0.5)
    ax2.axvline(23, color='red', linestyle=':', alpha=0.5)
    plt.title("Fig 4: Zoomed Peak Analysis (Visualizing the 3s Delay Window)")
    ax1.set_xlabel('Relative Time (Seconds)')
    ax1.set_ylabel('Vehicle Count', color='b')
    ax2.set_ylabel('CPU Util (%)', color='r')
    plt.savefig("fig4_zoomed_lag.png", bbox_inches='tight')
    plt.close()

    print("图表1~4生成完毕。")


if __name__ == "__main__":
    run_visualizations()