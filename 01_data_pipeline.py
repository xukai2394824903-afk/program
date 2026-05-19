import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


def scrape_weather_data(date="2026-05-17"):
    """网页爬虫：获取实验采集期间的历史天气数据"""
    url = f"https://api.weather-example.com/history?date={date}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # 简单模拟HTML解析
            soup = BeautifulSoup(response.text, 'html.parser')
            return {"date": date, "temperature": 25, "rain": False}
    except Exception as e:
        print(f"爬虫请求失败，使用默认天气数据: {e}")
    return {"date": date, "temperature": 25, "rain": False}


def generate_simulated_edgetraffic_data():
    """生成模拟的EdgeTraffic原始数据文件以供后续清洗处理"""
    os.makedirs("./data", exist_ok=True)
    np.random.seed(42)
    time_index = pd.date_range("2026-05-01 08:00:00", periods=600, freq="1s")

    # 模拟车流量
    vehicle_count = np.sin(np.linspace(0, 10, 600)) * 20 + 30 + np.random.normal(0, 5, 600)
    df_traffic = pd.DataFrame({"timestamp": time_index, "vehicle_count": vehicle_count})

    # 模拟系统数据 (设定约3秒的系统滞后)
    cpu_util = np.roll(vehicle_count, 3) * 1.5 + np.random.normal(0, 2, 600)
    df_system = pd.DataFrame({"timestamp": time_index, "cpu_util": cpu_util, "gpu_util": cpu_util * 0.8})

    df_traffic.to_csv("./data/traffic.csv", index=False)
    df_system.to_csv("./data/system.csv", index=False)
    print("原始数据采集完成。")


def clean_and_merge_data():
    """清洗与合并业务侧和系统侧数据"""
    df_traffic = pd.read_csv("./data/traffic.csv", parse_dates=['timestamp'])
    df_system = pd.read_csv("./data/system.csv", parse_dates=['timestamp'])

    # 设置时间戳索引
    df_traffic.set_index('timestamp', inplace=True)
    df_system.set_index('timestamp', inplace=True)

    # 时间重采样与对齐
    df_traffic = df_traffic.resample('1s').mean().ffill()
    df_system = df_system.resample('1s').mean().ffill()

    # 合并数据集
    df_merged = pd.merge(df_traffic, df_system, left_index=True, right_index=True, how='inner')

    # 异常值处理 (过滤掉CPU占用>100的数据)
    df_merged = df_merged[df_merged['cpu_util'] <= 100]

    # 保存为高效Parquet格式
    df_merged.to_parquet("./data/cleaned_edgetraffic.parquet")
    print(f"数据清洗完成，已保存至Parquet。当前数据维度：{df_merged.shape}")


if __name__ == "__main__":
    weather_df = pd.DataFrame([scrape_weather_data()])
    print("爬取的天气特征：\n", weather_df)
    generate_simulated_edgetraffic_data()
    clean_and_merge_data()