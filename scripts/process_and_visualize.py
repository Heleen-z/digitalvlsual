from __future__ import annotations

import math
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "llm_benchmark_sample_2024_2026.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "llm_benchmark_processed.csv"
FIGURE_DIR = ROOT / "outputs" / "figures"
DASHBOARD_FIGURE_DIR = ROOT / "dashboard" / "assets" / "figures"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "assets" / "data"

BENCHMARKS = ["MMLU_PRO", "IFEval", "BBH", "GPQA", "MATH_Lvl_5", "MuSR"]
FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
    Path(r"C:\Windows\Fonts\SourceHanSansCN-Normal.ttf"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\simsun.ttc"),
]

PALETTE = {
    "ink": (35, 43, 56),
    "muted": (96, 108, 124),
    "grid": (226, 232, 240),
    "panel": (248, 250, 252),
    "blue": (37, 99, 235),
    "teal": (15, 118, 110),
    "green": (22, 163, 74),
    "orange": (234, 88, 12),
    "red": (220, 38, 38),
    "purple": (124, 58, 237),
}


def ensure_dirs() -> None:
    for path in [PROCESSED_DIR, FIGURE_DIR, DASHBOARD_FIGURE_DIR, DASHBOARD_DATA_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = FONT_CANDIDATES.copy()
    if bold:
        candidates.insert(0, Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"))
        candidates.insert(1, Path(r"C:\Windows\Fonts\Dengb.ttf"))
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def text(draw: ImageDraw.ImageDraw, xy, content: str, size=28, fill=None, bold=False, anchor=None) -> None:
    draw.text(xy, content, font=load_font(size, bold), fill=fill or PALETTE["ink"], anchor=anchor)


def text_size(content: str, size=28, bold=False) -> tuple[int, int]:
    font = load_font(size, bold)
    box = font.getbbox(content)
    return box[2] - box[0], box[3] - box[1]


def canvas(title: str, subtitle: str = "", width=1280, height=760) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, 92], fill=(245, 248, 252))
    text(draw, (48, 26), title, size=34, bold=True)
    if subtitle:
        text(draw, (48, 66), subtitle, size=18, fill=PALETTE["muted"])
    return img, draw


def save_chart(img: Image.Image, name: str) -> None:
    png_path = FIGURE_DIR / f"{name}.png"
    img.save(png_path, quality=96)
    shutil.copy2(png_path, DASHBOARD_FIGURE_DIR / png_path.name)


def extract_params_from_name(name: str) -> float | None:
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*[bB]", str(name))
    if not matches:
        return None
    return float(matches[-1])


def minmax(series: pd.Series) -> pd.Series:
    lo = series.min()
    hi = series.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return (series - lo) / (hi - lo)


def impute_elo_with_knn(df: pd.DataFrame, k: int = 5) -> pd.Series:
    features = df[BENCHMARKS].astype(float)
    features = features.fillna(features.mean())
    norm = features.apply(minmax)
    known_mask = df["chatbot_arena_elo"].notna()
    known_x = norm[known_mask].to_numpy()
    known_y = df.loc[known_mask, "chatbot_arena_elo"].astype(float).to_numpy()
    result = df["chatbot_arena_elo"].astype(float).copy()

    for idx in df.index[~known_mask]:
        x = norm.loc[idx].to_numpy()
        distances = np.sqrt(((known_x - x) ** 2).sum(axis=1))
        nearest = np.argsort(distances)[:k]
        weights = 1 / (distances[nearest] + 1e-6)
        result.loc[idx] = float(np.average(known_y[nearest], weights=weights))

    return result.round(1)


def process_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError("请先运行 scripts/generate_sample_data.py 生成教学样例数据。")

    df = pd.read_csv(RAW_PATH)
    df["parameter_count_B"] = pd.to_numeric(df["parameter_count_B"], errors="coerce")
    bad_params = df["parameter_count_B"].isna() | (df["parameter_count_B"] <= 0)
    df.loc[bad_params, "parameter_count_B"] = df.loc[bad_params, "model_name"].map(extract_params_from_name)
    df["parameter_count_B"] = df["parameter_count_B"].replace({0: np.nan})

    for col in BENCHMARKS + ["arena_votes", "output_tokens_per_second", "time_to_first_token_s"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["chatbot_arena_elo_observed"] = df["chatbot_arena_elo"].notna()
    df["chatbot_arena_elo"] = pd.to_numeric(df["chatbot_arena_elo"], errors="coerce")
    df["chatbot_arena_elo"] = impute_elo_with_knn(df)

    for col in BENCHMARKS:
        df[f"{col}_norm"] = minmax(df[col])

    df["Average_Score"] = df[BENCHMARKS].mean(axis=1).round(2)
    df["Average_Score_norm"] = minmax(df["Average_Score"])
    df["Score_per_Billion_Params"] = (df["Average_Score"] / df["parameter_count_B"]).replace([np.inf, -np.inf], np.nan).round(3)

    elo_norm = minmax(df["chatbot_arena_elo"])
    tps_norm = minmax(df["output_tokens_per_second"])
    ttft_norm = minmax(df["time_to_first_token_s"])
    df["Hardware_Pareto_Index"] = np.sqrt((1 - elo_norm) ** 2 + (1 - tps_norm) ** 2 + ttft_norm**2).round(3)

    df.to_csv(PROCESSED_PATH, index=False, encoding="utf-8-sig")
    shutil.copy2(PROCESSED_PATH, DASHBOARD_DATA_DIR / PROCESSED_PATH.name)
    return df


def draw_axes(draw, left, top, right, bottom, x_label, y_label):
    draw.line([left, bottom, right, bottom], fill=PALETTE["ink"], width=2)
    draw.line([left, top, left, bottom], fill=PALETTE["ink"], width=2)
    for i in range(6):
        y = top + i * (bottom - top) / 5
        draw.line([left, y, right, y], fill=PALETTE["grid"], width=1)
    text(draw, ((left + right) / 2, bottom + 42), x_label, size=20, fill=PALETTE["muted"], anchor="mm")
    text(draw, (left, top - 22), y_label, size=20, fill=PALETTE["muted"], anchor="lm")


def chart_scaling_bubble(df: pd.DataFrame) -> None:
    img, draw = canvas("图表一：参数规模与人类偏好 Elo 的气泡散点图", "X 轴采用 log10 参数量；气泡大小代表 Arena 投票数，颜色区分开放权重与闭源 API。")
    left, top, right, bottom = 100, 140, 1160, 620
    draw_axes(draw, left, top, right, bottom, "参数量 parameter_count_B（log10）", "Chatbot Arena Elo")
    plot_df = df[df["parameter_count_B"].notna()].copy()
    x_log = np.log10(plot_df["parameter_count_B"])
    y = plot_df["chatbot_arena_elo"]
    x_min, x_max = x_log.min(), x_log.max()
    y_min, y_max = y.min() - 20, y.max() + 20

    colors = {"开放权重": PALETTE["teal"], "API/闭源": PALETTE["orange"]}
    for _, row in plot_df.iterrows():
        x = left + (math.log10(row["parameter_count_B"]) - x_min) / (x_max - x_min) * (right - left)
        yy = bottom - (row["chatbot_arena_elo"] - y_min) / (y_max - y_min) * (bottom - top)
        radius = 8 + math.sqrt(row["arena_votes"] / plot_df["arena_votes"].max()) * 26
        color = colors.get(row["availability"], PALETTE["blue"])
        draw.ellipse([x - radius, yy - radius, x + radius, yy + radius], fill=color + (90,), outline=color, width=2)
        if row["model_name"] in ["GPT-4o", "Qwen2.5-7B-Instruct", "DeepSeek-R1-Distill-Qwen-7B", "Llama-3.1-405B-Instruct"]:
            label = row["model_name"]
            label_w, _ = text_size(label, size=15)
            label_x = x + radius + 4
            anchor = "lm"
            if label_x + label_w > right:
                label_x = x - radius - 4
                anchor = "rm"
            text(draw, (label_x, yy), label, size=15, fill=PALETTE["ink"], anchor=anchor)

    bins = np.linspace(x_min, x_max, 7)
    pts = []
    for i in range(len(bins) - 1):
        b = plot_df[(x_log >= bins[i]) & (x_log <= bins[i + 1])]
        if len(b) >= 2:
            bx = (bins[i] + bins[i + 1]) / 2
            by = b["chatbot_arena_elo"].mean()
            pts.append((left + (bx - x_min) / (x_max - x_min) * (right - left), bottom - (by - y_min) / (y_max - y_min) * (bottom - top)))
    if len(pts) > 1:
        draw.line(pts, fill=PALETTE["purple"], width=4)
        text(draw, (pts[-1][0] - 150, pts[-1][1] - 34), "分段趋势线：边际增益趋缓", size=18, fill=PALETTE["purple"])

    for label, color in colors.items():
        x0 = 930 if label == "开放权重" else 1050
        draw.ellipse([x0, 112, x0 + 18, 130], fill=color, outline=color)
        text(draw, (x0 + 26, 113), label, size=18)
    save_chart(img, "01_scaling_bubble")


def chart_radar(df: pd.DataFrame) -> None:
    img, draw = canvas("图表二：7B-9B 量级模型能力雷达图", "同等参数规模下比较六类基准能力，并加入样本均值作为虚线参照。")
    cx, cy, radius = 620, 390, 245
    metrics = BENCHMARKS
    angles = [2 * math.pi * i / len(metrics) - math.pi / 2 for i in range(len(metrics))]

    for r in [0.25, 0.5, 0.75, 1.0]:
        pts = [(cx + math.cos(a) * radius * r, cy + math.sin(a) * radius * r) for a in angles]
        draw.line(pts + [pts[0]], fill=PALETTE["grid"], width=2)
    for a, label in zip(angles, ["MMLU", "IFEval", "BBH", "GPQA", "MATH", "MuSR"]):
        x = cx + math.cos(a) * (radius + 48)
        y = cy + math.sin(a) * (radius + 34)
        draw.line([cx, cy, cx + math.cos(a) * radius, cy + math.sin(a) * radius], fill=PALETTE["grid"], width=1)
        text(draw, (x, y), label, size=20, fill=PALETTE["ink"], anchor="mm")

    candidates = df[(df["parameter_count_B"] >= 7) & (df["parameter_count_B"] <= 9.5)].nlargest(3, "Average_Score")
    colors = [PALETTE["blue"], PALETTE["orange"], PALETTE["green"]]

    mean_vals = [df[f"{m}_norm"].mean() for m in metrics]
    mean_pts = [(cx + math.cos(a) * radius * v, cy + math.sin(a) * radius * v) for a, v in zip(angles, mean_vals)]
    draw.line(mean_pts + [mean_pts[0]], fill=PALETTE["muted"], width=3)

    legend_y = 145
    text(draw, (890, legend_y - 34), "排名模型", size=22, bold=True)
    for i, (_, row) in enumerate(candidates.iterrows()):
        vals = [row[f"{m}_norm"] for m in metrics]
        pts = [(cx + math.cos(a) * radius * v, cy + math.sin(a) * radius * v) for a, v in zip(angles, vals)]
        draw.polygon(pts, fill=colors[i] + (55,), outline=colors[i])
        draw.line(pts + [pts[0]], fill=colors[i], width=4)
        y = legend_y + i * 40
        draw.rectangle([890, y, 914, y + 18], fill=colors[i])
        text(draw, (924, y - 2), row["model_name"], size=18)
    draw.line([890, legend_y + 132, 914, legend_y + 132], fill=PALETTE["muted"], width=4)
    text(draw, (924, legend_y + 120), "全样本均值线", size=18)
    save_chart(img, "02_radar_profile")


def heat_color(value: float, lo: float, hi: float) -> tuple[int, int, int]:
    t = 0 if hi == lo else (value - lo) / (hi - lo)
    r = int(232 - 180 * t)
    g = int(245 - 90 * t)
    b = int(233 - 130 * t)
    return r, g, b


def chart_architecture_heatmap(df: pd.DataFrame) -> None:
    img, draw = canvas("图表三：开源架构与训练范式热力矩阵", "单元格数值为平均 MMLU-PRO；用于识别高产出的“架构 + 训练方式”组合。")
    open_df = df[df["availability"] == "开放权重"].copy()
    top_arch = open_df["architecture"].value_counts().head(6).index.tolist()
    paradigms = ["指令微调", "领域微调", "MoE/模型融合", "蒸馏/推理微调", "端侧微调"]
    matrix = open_df.pivot_table(index="architecture", columns="training_paradigm", values="MMLU_PRO", aggfunc="mean").reindex(top_arch)
    vals = matrix.to_numpy().astype(float)
    lo, hi = np.nanmin(vals), np.nanmax(vals)
    left, top = 255, 165
    cell_w, cell_h = 160, 72

    for j, col in enumerate(paradigms):
        text(draw, (left + j * cell_w + cell_w / 2, top - 42), col, size=17, fill=PALETTE["ink"], anchor="mm")
    for i, arch in enumerate(top_arch):
        text(draw, (left - 14, top + i * cell_h + cell_h / 2), arch.replace("ForCausalLM", ""), size=18, fill=PALETTE["ink"], anchor="rm")
        for j, col in enumerate(paradigms):
            value = matrix.loc[arch, col] if col in matrix.columns else np.nan
            x0 = left + j * cell_w
            y0 = top + i * cell_h
            if np.isnan(value):
                fill = (241, 245, 249)
                label = "—"
            else:
                fill = heat_color(float(value), lo, hi)
                label = f"{value:.1f}"
            draw.rectangle([x0, y0, x0 + cell_w - 4, y0 + cell_h - 4], fill=fill, outline="white", width=2)
            text(draw, (x0 + cell_w / 2, y0 + cell_h / 2 - 2), label, size=22, bold=not np.isnan(value), anchor="mm")

    text(draw, (255, 675), "结论：Llama/Qwen 系列覆盖多数高分组合，蒸馏与 MoE 让中小模型获得更高能力密度。", size=22, fill=PALETTE["teal"], bold=True)
    save_chart(img, "03_architecture_heatmap")


def corr_color(value: float) -> tuple[int, int, int]:
    t = (value + 1) / 2
    if t < 0.5:
        p = t / 0.5
        return int(220 + (255 - 220) * p), int(38 + (255 - 38) * p), int(38 + (255 - 38) * p)
    p = (t - 0.5) / 0.5
    return int(255 + (37 - 255) * p), int(255 + (99 - 255) * p), int(255 + (235 - 255) * p)


def chart_correlation(df: pd.DataFrame) -> None:
    img, draw = canvas("图表四：客观基准与人类偏好 Pearson 相关矩阵", "下三角热力图显示不同能力、速度和延迟指标之间的关系。")
    cols = BENCHMARKS + ["chatbot_arena_elo", "output_tokens_per_second", "time_to_first_token_s"]
    labels = ["MMLU", "IFEval", "BBH", "GPQA", "MATH", "MuSR", "Elo", "TPS", "TTFT"]
    corr = df[cols].corr()
    left, top, cell = 245, 145, 66
    for i, label in enumerate(labels):
        text(draw, (left - 10, top + i * cell + cell / 2), label, size=18, anchor="rm")
        text(draw, (left + i * cell + cell / 2, top - 22), label, size=17, anchor="mm")
    for i, row in enumerate(cols):
        for j, col in enumerate(cols):
            x0 = left + j * cell
            y0 = top + i * cell
            if j > i:
                draw.rectangle([x0, y0, x0 + cell - 4, y0 + cell - 4], fill=(248, 250, 252), outline="white")
                continue
            value = float(corr.loc[row, col])
            draw.rectangle([x0, y0, x0 + cell - 4, y0 + cell - 4], fill=corr_color(value), outline="white", width=2)
            fill = "white" if abs(value) > 0.65 else PALETTE["ink"]
            text(draw, (x0 + cell / 2, y0 + cell / 2 - 1), f"{value:.2f}", size=17, bold=True, fill=fill, anchor="mm")
    text(draw, (835, 205), "阅读重点", size=24, bold=True)
    text(draw, (835, 250), "Elo 与 IFEval、MMLU、GPQA 相关性较高，说明真实偏好并非只由数学刷榜决定。", size=20, fill=PALETTE["muted"])
    text(draw, (835, 332), "TTFT 与体验呈反向压力：延迟越高，本地部署价值越受限制。", size=20, fill=PALETTE["muted"])
    save_chart(img, "04_correlation_matrix")


def chart_hardware_jointplot(df: pd.DataFrame) -> None:
    img, draw = canvas("图表五：本地硬件性能联合分布与帕累托前沿", "右下区域代表高吞吐、低首字延迟；红线圈出部署体验更优的模型。")
    left, top, right, bottom = 110, 175, 920, 620
    draw_axes(draw, left, top, right, bottom, "输出速度 output_tokens_per_second", "首字延迟 time_to_first_token_s")
    x = df["output_tokens_per_second"]
    y = df["time_to_first_token_s"]
    x_min, x_max = x.min() - 5, x.max() + 5
    y_min, y_max = 0, y.max() + 0.5

    for _, row in df.iterrows():
        px = left + (row["output_tokens_per_second"] - x_min) / (x_max - x_min) * (right - left)
        py = bottom - (row["time_to_first_token_s"] - y_min) / (y_max - y_min) * (bottom - top)
        color = PALETTE["teal"] if row["availability"] == "开放权重" else PALETTE["orange"]
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=color, outline="white", width=2)
        if row["Hardware_Pareto_Index"] <= df["Hardware_Pareto_Index"].quantile(0.18):
            text(draw, (px + 10, py - 8), row["model_name"].split("-Instruct")[0], size=14)

    pareto = df.sort_values("output_tokens_per_second", ascending=False)
    best = []
    min_ttft = float("inf")
    for _, row in pareto.iterrows():
        if row["time_to_first_token_s"] < min_ttft:
            best.append(row)
            min_ttft = row["time_to_first_token_s"]
    pts = []
    for row in best:
        pts.append((left + (row["output_tokens_per_second"] - x_min) / (x_max - x_min) * (right - left), bottom - (row["time_to_first_token_s"] - y_min) / (y_max - y_min) * (bottom - top)))
    if len(pts) > 1:
        draw.line(pts, fill=PALETTE["red"], width=4)

    hist_x0, hist_y0 = left, 125
    bins = np.histogram(x, bins=12)
    max_count = bins[0].max()
    for count, edge0, edge1 in zip(bins[0], bins[1][:-1], bins[1][1:]):
        bx0 = left + (edge0 - x_min) / (x_max - x_min) * (right - left)
        bx1 = left + (edge1 - x_min) / (x_max - x_min) * (right - left)
        h = 60 * count / max_count
        draw.rectangle([bx0, hist_y0 + 60 - h, bx1 - 3, hist_y0 + 60], fill=(191, 219, 254))

    y_bins = np.histogram(y, bins=10)
    max_y_count = y_bins[0].max()
    for count, edge0, edge1 in zip(y_bins[0], y_bins[1][:-1], y_bins[1][1:]):
        by0 = bottom - (edge0 - y_min) / (y_max - y_min) * (bottom - top)
        by1 = bottom - (edge1 - y_min) / (y_max - y_min) * (bottom - top)
        w = 90 * count / max_y_count
        draw.rectangle([right + 18, by1, right + 18 + w, by0 - 3], fill=(254, 215, 170))

    top_models = df.nsmallest(5, "Hardware_Pareto_Index")[["model_name", "Hardware_Pareto_Index"]]
    text(draw, (1010, 190), "黄金模型候选", size=24, bold=True)
    for i, (_, row) in enumerate(top_models.iterrows(), 1):
        text(draw, (1010, 232 + i * 34), f"{i}. {row['model_name']}", size=17)
    save_chart(img, "05_hardware_jointplot")


def main() -> None:
    ensure_dirs()
    df = process_data()
    chart_scaling_bubble(df)
    chart_radar(df)
    chart_architecture_heatmap(df)
    chart_correlation(df)
    chart_hardware_jointplot(df)
    print(f"processed rows: {len(df)}")
    print(f"processed data: {PROCESSED_PATH}")
    print(f"figures: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
