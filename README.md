# 开源大语言模型性能演进与架构特征可视化分析

这是一个面向课堂展示的数据处理与可视化项目，围绕 2024-2026 年大语言模型的基准性能、参数规模、开源架构、训练范式与本地硬件响应指标展开分析。

项目已设计为本地化部署优先：无需外部 CDN，无需联网即可生成教学样例数据、完成数据清洗、输出 5 张中文可视化图片，并在本地网页与中文 PPT 中展示结果。

## 项目结构

```text
.
├── AI项目设计：数据处理与可视化.pdf
├── data/
│   ├── raw/                         # 原始或教学样例数据
│   └── processed/                   # 清洗后的数据
├── dashboard/
│   ├── index.html                   # 本地可视化网页
│   ├── styles.css
│   └── assets/
│       ├── figures/                 # PNG/SVG 可视化图片
│       └── data/                    # 前端可读取的数据
├── outputs/
│   └── figures/                     # 脚本生成的图表输出
├── presentation/
│   ├── build_ppt.js                 # 生成课堂展示 PPT
│   └── LLM项目课堂展示.pptx
├── scripts/
│   ├── generate_sample_data.py      # 生成教学样例数据
│   └── process_and_visualize.py     # 清洗、插补、特征工程、绘图
├── requirements.txt
└── run_local.ps1
```

## 本地运行

推荐在 PowerShell 中运行：

```powershell
.\run_local.ps1
```

脚本会依次完成：

1. 生成 `data/raw/llm_benchmark_sample_2024_2026.csv`
2. 清洗数据、KNN 插补 Elo、归一化指标、构造复合特征
3. 生成 5 张中文 PNG 可视化图片
4. 生成 `presentation/LLM项目课堂展示.pptx`
5. 启动本地网页服务

启动后访问：

```text
http://localhost:8000/dashboard/
```

## 数据说明

当前仓库包含的是课程演示用教学样例数据，字段设计参考项目说明 PDF 中给出的 Kaggle 数据集结构，包括：

- `parameter_count_B`
- `architecture`
- `training_paradigm`
- `MMLU_PRO`
- `GPQA`
- `IFEval`
- `BBH`
- `MATH_Lvl_5`
- `MuSR`
- `chatbot_arena_elo`
- `arena_votes`
- `output_tokens_per_second`
- `time_to_first_token_s`

如需使用真实 Kaggle 数据，可将 CSV 放入 `data/raw/`，并按上述字段命名或在 `scripts/process_and_visualize.py` 中调整字段映射。

## 处理逻辑

项目实现了课程说明中的核心处理要求：

- 参数量异常值处理：将 `-1` 或缺失参数识别为异常，并从模型名称中提取 `7B`、`72B`、`405B` 等信息自动修正。
- Elo 缺失值插补：使用手写 KNN 逻辑，基于 MMLU-PRO、GPQA、IFEval、BBH、MATH、MuSR 等客观基准估算缺失的 `chatbot_arena_elo`。
- Min-Max 归一化：将多学科指标统一投射到 0-1 尺度，减少不同测试难度带来的视觉偏差。
- 复合特征工程：构造 `Average_Score`、`Score_per_Billion_Params`、`Hardware_Pareto_Index` 等分析字段。

## 可视化图片

生成的 5 张 PNG 图表位于 `outputs/figures/` 和 `dashboard/assets/figures/`：

1. `01_scaling_bubble.png`：参数规模与 Elo 的气泡散点图
2. `02_radar_profile.png`：同参数量级模型能力雷达图
3. `03_architecture_heatmap.png`：架构与训练范式热力图
4. `04_correlation_matrix.png`：客观基准与人类偏好相关性矩阵
5. `05_hardware_jointplot.png`：吞吐、延迟与帕累托前沿图

图表生成脚本会优先使用 Windows 中的 `Noto Sans SC`、`Source Han Sans CN`、`SimHei`、`Microsoft YaHei` 等中文字体，保证中文标题、坐标轴和注释正常显示。

## 课堂 PPT

PPT 文件：

```text
presentation/LLM项目课堂展示.pptx
```

PPT 为简短课堂展示版本，包含项目目标、数据处理流程、五类图表证据和结论页。中文字体优先使用 `Noto Sans SC`，并直接嵌入生成的 PNG 图表，降低跨设备乱码风险。

## GitHub 发布建议

推荐仓库名：

```text
llm-performance-visualization
```

首次发布命令示例：

```powershell
git init
git add .
git commit -m "完成本地化数据可视化项目"
gh repo create llm-performance-visualization --public --source . --remote origin --push
```

如果未安装或未登录 GitHub CLI，可先运行：

```powershell
gh auth login
```
