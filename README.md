# 2024-2026 主流大语言模型数据处理与可视化分析

这是一个面向《数据处理与可视化》课程的本地化项目。项目围绕 2024 年 1 月至 2026 年 6 月 5 日前发布的主流大语言模型，整理模型基准、参数规模、开放性、架构、训练范式、人类偏好 Elo、吞吐和首字延迟等字段，并通过横向比较和纵向趋势图展示数据规律。

项目重点不是单纯介绍大模型，而是完整呈现数据可视化课程中的关键能力：数据收集、字段统一、缺失标记、插补、归一化、复合指标构造、图表编码、图表解读和结论表达。

## 项目结构

```text
.
├── AI项目设计：数据处理与可视化.pdf
├── data/
│   ├── raw/                         # 主流代表模型原始整理数据
│   └── processed/                   # 清洗、插补、归一化后的数据
├── dashboard/
│   ├── index.html                   # 本地网页展示
│   ├── styles.css
│   └── assets/
│       ├── figures/                 # 生成后的 6 张 PNG 可视化图片
│       └── data/                    # 前端可读取的处理后数据
├── outputs/
│   └── figures/                     # 图表脚本输出
├── presentation/
│   ├── build_ppt.js                 # 生成中文课堂展示 PPT
│   └── LLM项目课堂展示.pptx
├── scripts/
│   ├── generate_sample_data.py      # 构建主流代表模型数据集
│   └── process_and_visualize.py     # 清洗、插补、特征工程、绘图
├── requirements.txt
└── run_local.ps1
```

## 本地运行

在 PowerShell 中运行：

```powershell
.\run_local.ps1
```

脚本会依次完成：

1. 生成 `data/raw/llm_mainstream_2024_2026.csv`
2. 清洗数据、标记观测/估算字段、插补缺失值、归一化指标
3. 生成 6 张大画布中文 PNG 可视化图片
4. 生成 `presentation/LLM项目课堂展示.pptx`
5. 启动本地网页服务

启动后访问：

```text
http://localhost:8000/dashboard/
```

## 数据口径

当前项目采用“公开资料 + 离线主流代表集”的课程项目口径，不依赖 API key。数据覆盖 71 个主流代表模型、17 个模型系列，截止日期为 2026-06-05。覆盖系列包括 GPT/GPT-o、Claude、Gemini、Gemma、Llama、Qwen、DeepSeek、Mistral、Grok、Command、GLM、Kimi、ERNIE、Hunyuan、Phi、Yi、MiniMax 等。

最新旗舰代表已纳入头部横向比较，包括 Gemini 3.1 Pro、Claude Opus 4.6、GPT-5.5。对于这些较新的模型，若公开资料没有完全对应本项目字段的 MMLU_PRO、IFEval、BBH、GPQA、MATH、MuSR、Arena Elo、吞吐或首字延迟，则在 CSV 中保留估算值并将对应 `*_observed` 标记为 `False`。

主要字段包括：

- 模型身份字段：`model_name`、`provider`、`family`、`release_date`
- 模型属性字段：`availability`、`architecture`、`training_paradigm`、`parameter_count_B`
- 能力基准字段：`MMLU_PRO`、`GPQA`、`IFEval`、`BBH`、`MATH_Lvl_5`、`MuSR`
- 人类偏好字段：`chatbot_arena_elo`、`arena_votes`
- 部署体验字段：`output_tokens_per_second`、`time_to_first_token_s`
- 数据质量字段：`source_url`、`source_note`、`*_observed`

缺失指标会保留观测标记，并在处理阶段进行同系列或 KNN 插补。插补结果用于课堂可视化展示，不被当作原始实测事实。

## 处理逻辑

项目实现了以下数据处理步骤：

- 日期标准化：将发布日期统一为 `release_date`，并生成 `release_year_month` 供纵向趋势图使用。
- 缺失标记：保留 `chatbot_arena_elo_observed`、`hardware_metrics_observed` 等字段，区分观测值和插补值。
- 缺失插补：优先使用同系列邻近模型均值；同系列不足时使用基准指标 KNN 插补。
- 指标归一化：对不同量纲的基准分、Elo、吞吐和延迟进行标准化处理。
- 复合指标：构造 `Average_Score`、`Composite_Score`、`Score_per_Billion_Params`、`Hardware_Pareto_Index`。

## 可视化图片

生成的 6 张图表位于 `outputs/figures/` 和 `dashboard/assets/figures/`：

1. `01_landscape_bubble.png`：主流模型横向能力气泡图
2. `02_provider_ranking.png`：头部模型横向排名条形图
3. `03_series_progression.png`：同一系列模型纵向进步折线图
4. `04_architecture_heatmap.png`：架构生态与训练范式热力图
5. `05_correlation_matrix.png`：客观基准与人类偏好相关矩阵
6. `06_hardware_pareto.png`：本地部署帕累托图

图表统一使用约 `2000×1250` 的大画布，减少文字遮挡，并通过固定图例区、说明框、少量关键标注和更大的坐标留白增强可读性。

## 课堂 PPT

PPT 文件：

```text
presentation/LLM项目课堂展示.pptx
```

PPT 主题围绕数据可视化课程本身展开：为什么需要整理这些数据、如何进行数据处理、如何设计横向和纵向图表、每张图展示了什么、图表结论如何服务于模型比较。每张图片页都包含三段短说明：

- 图中看到了什么
- 专业上说明什么
- 生活中意味着什么

其中“生活中意味着什么”只作为图表解读的直觉补充，例如响应是否等待、长文生成是否流畅、普通电脑是否可能本地运行等，不脱离数据可视化课程主线。

## GitHub

项目仓库：

```text
https://github.com/Heleen-z/digitalvlsual
```

更新后可使用：

```powershell
git add .
git commit -m "扩展主流模型数据并重构可视化展示"
git push
```
