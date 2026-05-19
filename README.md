# 🚗 车载边缘计算 (VEC) 资源动态映射与前摄性调度研究
**(Dynamic Mapping and Proactive Scheduling of Business and System Resources in VEC Scenarios)**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-brightgreen)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange)

## 📌 项目简介

本项目为《车载边缘计算场景下业务与系统资源的动态映射及前摄性调度研究》课程论文的配套开源代码与分析库。

随着智能交通系统的演进，真实场景中车流量的动态波动给路侧单元（RSU）的资源调度带来了巨大挑战。本项目基于真实的 **EdgeTraffic 多模态数据集**，构建了从数据采集、清洗、持久化到可视化与预测分析的完整数据管道（Data Pipeline）。

### 🎯 核心研究目标 (Research Questions)
1. 定量分析车流量（业务特征）变化对边缘节点系统开销（CPU/GPU）的映射关系。
2. 挖掘业务波动传导至系统层面的物理与计算**时滞（Time Lag）特征**。
3. 验证基于时序预测（Random Forest）的**前摄性调度策略（Proactive Scheduling）**在降低响应滞后性方面的有效性。

---

## 📂 仓库结构 (Repository Structure)

本项目采用模块化的 Python 脚本架构，确保全流程的可复现性：

```text
├── 01_data_pipeline.py         # 数据采集、辅助特征爬虫、对齐与 Parquet 持久化
├── 02_visualization.py         # 业务-系统映射关系与交叉相关性时滞分析图表生成
├── 03_predictive_scheduling.py # 基于随机森林的时序预测与前摄性调度策略评估
├── .gitignore                  # Git 忽略配置（忽略原始数据集与本地缓存）
├── README.md                   # 项目说明文档
└── data/                       # (本地运行生成) 存放清洗后的 Parquet 数据集

```

---

## 🚀 快速开始 (Getting Started)

### 1. 环境依赖

请确保您的环境中安装了以下基础库：

```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy requests beautifulsoup4 pyarrow

```

*(注：`pyarrow` 用于支持高效的 Parquet 数据格式读写)*

### 2. 运行顺序

请在终端中按以下顺序执行脚本以完整复现论文实验：

```bash
# Step 1: 采集辅助天气特征，生成模拟/拉取原始数据，清洗并输出为 Parquet 格式
python 01_data_pipeline.py

# Step 2: 运行数据可视化模块，生成论文 Fig 1 ~ Fig 4
python 02_visualization.py

# Step 3: 训练联合预测模型，评估调度策略，生成论文 Fig 5 ~ Fig 6
python 03_predictive_scheduling.py

```

---

## 📊 核心发现与实验结论 (Key Findings)

运行上述脚本后，将自动生成 6 张核心分析图表，支撑了本论文的以下结论：

1. **定量映射关系挖掘：** 业务负载与系统开销呈强烈的正相关线性映射。回归分析表明，车流量每增加 1 辆/秒，边缘节点的 CPU 占用率平均刚性上升约 **1.35%**。
2. **"3秒"刚性时滞发现：** 交叉相关性（Cross-Correlation）分析证明，从车流激增到系统触发满载警报，存在约 **3.0秒** 的物理与计算传导延迟。这也是传统被动调度频繁失效的核心盲区。
3. **前摄性调度大幅提升 SLA：** 引入基于 Random Forest 的联合预测模型后，系统资源调度的响应时滞被压缩至 **0.4秒**（降幅 86.7%），使得由算力不足导致的 SLA 违约次数暴跌 **85.6%**。

---

## 📝 声明与致谢

* 本项目数据处理流程及部分基础分析代码的重构，参考了部分开源社区规范，并借助 AI 编程助手优化了数据管道的执行效率与图表美观度。
* 本仓库仅用于课程论文答辩与学术交流，相关模拟数据与分析结论仅供参考。
