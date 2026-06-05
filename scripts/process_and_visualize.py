from __future__ import annotations

import math
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "llm_mainstream_2024_2026.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_PATH = PROCESSED_DIR / "llm_mainstream_processed.csv"
FIGURE_DIR = ROOT / "outputs" / "figures"
DASHBOARD_FIGURE_DIR = ROOT / "dashboard" / "assets" / "figures"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "assets" / "data"

COLLECTION_CUTOFF = "2026-06-05"
BENCHMARKS = ["MMLU_PRO", "IFEval", "BBH", "GPQA", "MATH_Lvl_5", "MuSR"]
FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\NotoSansSC-VF.ttf"),
    Path(r"C:\Windows\Fonts\SourceHanSansCN-Normal.ttf"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
    Path(r"C:\Windows\Fonts\simsun.ttc"),
]

W, H = 2000, 1250
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
    "gold": (202, 138, 4),
    "cyan": (8, 145, 178),
}
SERIES_COLORS = {
    "GPT-o": PALETTE["blue"],
    "Claude": PALETTE["purple"],
    "Gemini": PALETTE["green"],
    "Llama": PALETTE["teal"],
    "Qwen": PALETTE["orange"],
    "DeepSeek": PALETTE["red"],
}


def ensure_dirs() -> None:
    for path in [PROCESSED_DIR, FIGURE_DIR, DASHBOARD_FIGURE_DIR, DASHBOARD_DATA_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    for folder in [FIGURE_DIR, DASHBOARD_FIGURE_DIR]:
        for old in folder.glob("*.png"):
            old.unlink()


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = FONT_CANDIDATES.copy()
    if bold:
        candidates.insert(0, Path(r"C:\Windows\Fonts\Dengb.ttf"))
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def text(draw: ImageDraw.ImageDraw, xy, content: str, size=28, fill=None, bold=False, anchor=None, align="left") -> None:
    draw.text(xy, str(content), font=load_font(size, bold), fill=fill or PALETTE["ink"], anchor=anchor, align=align)


def text_box(draw, xy, content: str, width: int, size=28, fill=None, bold=False, line_gap=8) -> int:
    font = load_font(size, bold)
    words = list(str(content))
    lines: list[str] = []
    line = ""
    for ch in words:
        trial = line + ch
        if font.getbbox(trial)[2] - font.getbbox(trial)[0] <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = ch
    if line:
        lines.append(line)
    x, y = xy
    line_h = size + line_gap
    for i, ln in enumerate(lines):
        draw.text((x, y + i * line_h), ln, font=font, fill=fill or PALETTE["ink"])
    return len(lines) * line_h


def text_width(content: str, size=28, bold=False) -> int:
    box = load_font(size, bold).getbbox(str(content))
    return box[2] - box[0]


def canvas(title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 150], fill=(245, 248, 252))
    text(draw, (70, 38), title, size=46, bold=True)
    if subtitle:
        text(draw, (70, 98), subtitle, size=24, fill=PALETTE["muted"])
    return img, draw


def save_chart(img: Image.Image, name: str) -> None:
    png_path = FIGURE_DIR / f"{name}.png"
    img.save(png_path, quality=96)
    shutil.copy2(png_path, DASHBOARD_FIGURE_DIR / png_path.name)


def minmax(series: pd.Series) -> pd.Series:
    lo = series.min()
    hi = series.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(np.zeros(len(series)), index=series.index)
    return (series - lo) / (hi - lo)


def impute_numeric(df: pd.DataFrame, target: str, features: list[str]) -> pd.Series:
    result = pd.to_numeric(df[target], errors="coerce").copy()
    known = result.notna()
    if known.sum() == 0:
        return result
    feature_df = df[features].apply(pd.to_numeric, errors="coerce")
    feature_df = feature_df.fillna(feature_df.mean())
    norm = feature_df.apply(minmax)
    known_x = norm[known].to_numpy()
    known_y = result[known].to_numpy()
    for idx in df.index[~known]:
        family = df.loc[idx, "family"]
        same = df.index[(df["family"] == family) & known]
        if len(same) >= 2:
            result.loc[idx] = result.loc[same].mean()
            continue
        x = norm.loc[idx].to_numpy()
        distances = np.sqrt(((known_x - x) ** 2).sum(axis=1))
        nearest = np.argsort(distances)[:5]
        weights = 1 / (distances[nearest] + 1e-6)
        result.loc[idx] = float(np.average(known_y[nearest], weights=weights))
    return result.round(2)


def process_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError("请先运行 scripts/generate_sample_data.py 生成主流模型数据。")
    df = pd.read_csv(RAW_PATH)
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["release_year_month"] = df["release_date"].dt.strftime("%Y-%m")
    df["collected_through"] = COLLECTION_CUTOFF

    numeric_cols = BENCHMARKS + [
        "parameter_count_B",
        "chatbot_arena_elo",
        "arena_votes",
        "output_tokens_per_second",
        "time_to_first_token_s",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["parameter_count_observed"] = df["parameter_count_B"].notna()
    df["chatbot_arena_elo_observed"] = df["chatbot_arena_elo"].notna()
    df["hardware_metrics_observed"] = df["output_tokens_per_second"].notna() & df["time_to_first_token_s"].notna()

    df["chatbot_arena_elo"] = impute_numeric(df, "chatbot_arena_elo", BENCHMARKS)
    df["output_tokens_per_second"] = impute_numeric(df, "output_tokens_per_second", BENCHMARKS + ["chatbot_arena_elo"])
    df["time_to_first_token_s"] = impute_numeric(df, "time_to_first_token_s", BENCHMARKS + ["chatbot_arena_elo"])

    for col in BENCHMARKS:
        df[f"{col}_norm"] = minmax(df[col])
    df["Average_Score"] = df[BENCHMARKS].mean(axis=1).round(2)
    df["Average_Score_norm"] = minmax(df["Average_Score"])
    df["Elo_norm"] = minmax(df["chatbot_arena_elo"])
    df["Composite_Score"] = (0.55 * df["Average_Score_norm"] + 0.35 * df["Elo_norm"] + 0.10 * minmax(df["IFEval"])).round(3)
    df["Score_per_Billion_Params"] = (df["Average_Score"] / df["parameter_count_B"]).replace([np.inf, -np.inf], np.nan).round(3)

    elo_norm = minmax(df["chatbot_arena_elo"])
    tps_norm = minmax(df["output_tokens_per_second"])
    ttft_norm = minmax(df["time_to_first_token_s"])
    df["Hardware_Pareto_Index"] = np.sqrt((1 - elo_norm) ** 2 + (1 - tps_norm) ** 2 + ttft_norm**2).round(3)

    df = df.sort_values(["release_date", "provider", "model_name"])
    df.to_csv(PROCESSED_PATH, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    shutil.copy2(PROCESSED_PATH, DASHBOARD_DATA_DIR / PROCESSED_PATH.name)
    return df


def map_value(value, src_min, src_max, dst_min, dst_max):
    if src_max == src_min:
        return (dst_min + dst_max) / 2
    return dst_min + (value - src_min) / (src_max - src_min) * (dst_max - dst_min)


def draw_axes(draw, left, top, right, bottom, x_label, y_label, y_ticks=5):
    draw.line([left, bottom, right, bottom], fill=PALETTE["ink"], width=3)
    draw.line([left, top, left, bottom], fill=PALETTE["ink"], width=3)
    for i in range(y_ticks + 1):
        y = top + i * (bottom - top) / y_ticks
        draw.line([left, y, right, y], fill=PALETTE["grid"], width=1)
    text(draw, ((left + right) / 2, bottom + 62), x_label, size=26, fill=PALETTE["muted"], anchor="mm")
    text(draw, (left, top - 35), y_label, size=26, fill=PALETTE["muted"], anchor="lm")


def chart_landscape_bubble(df: pd.DataFrame) -> None:
    img, draw = canvas("图表一：主流模型横向能力气泡图", "横向比较参数规模、综合能力、人类偏好与开放性；仅标注关键模型，避免遮挡。")
    left, top, right, bottom = 140, 230, 1510, 1030
    draw_axes(draw, left, top, right, bottom, "参数量 parameter_count_B（log10；API 模型放在右侧参考区）", "综合能力分 Average_Score")
    plot = df.copy()
    open_plot = plot[plot["parameter_count_B"].notna()].copy()
    x_log = np.log10(open_plot["parameter_count_B"])
    x_min, x_max = x_log.min(), x_log.max()
    y_min, y_max = plot["Average_Score"].min() - 3, plot["Average_Score"].max() + 3
    colors = {"开放权重": PALETTE["teal"], "API/闭源": PALETTE["orange"]}
    for _, row in open_plot.iterrows():
        x = map_value(math.log10(row["parameter_count_B"]), x_min, x_max, left, right)
        y = map_value(row["Average_Score"], y_min, y_max, bottom, top)
        radius = 10 + row["Elo_norm"] * 28
        color = colors.get(row["availability"], PALETTE["blue"])
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color, outline="white", width=3)

    api_x = right + 115
    for _, row in plot[plot["parameter_count_B"].isna()].iterrows():
        y = map_value(row["Average_Score"], y_min, y_max, bottom, top)
        radius = 10 + row["Elo_norm"] * 28
        draw.ellipse([api_x - radius, y - radius, api_x + radius, y + radius], fill=PALETTE["orange"], outline="white", width=3)
    draw.line([right + 42, top, right + 42, bottom], fill=PALETTE["grid"], width=2)
    text(draw, (api_x, bottom + 62), "API/闭源参考区", size=24, fill=PALETTE["muted"], anchor="mm")

    notable = plot.sort_values("Composite_Score", ascending=False).head(10)
    panel_x = 1700
    draw.rounded_rectangle([panel_x - 35, 230, 1940, 1030], radius=18, fill=PALETTE["panel"], outline=PALETTE["grid"], width=2)
    text(draw, (panel_x, 270), "关键观察", size=32, bold=True)
    notes = [
        "闭源旗舰仍在高分区密集分布。",
        "Qwen、DeepSeek、Llama 等开放模型快速逼近。",
        "参数更大通常更强，但小模型的能力密度正在上升。",
    ]
    y = 330
    for note in notes:
        draw.ellipse([panel_x, y + 8, panel_x + 12, y + 20], fill=PALETTE["teal"])
        y += text_box(draw, (panel_x + 24, y), note, 210, size=22, fill=PALETTE["ink"]) + 18
    text(draw, (panel_x, y + 10), "综合分前十", size=26, bold=True, fill=PALETTE["muted"])
    y += 52
    for i, (_, row) in enumerate(notable.iterrows(), 1):
        text(draw, (panel_x, y), f"{i}. {row['model_name']}", size=20, fill=PALETTE["ink"])
        y += 34
    for i, (label, color) in enumerate(colors.items()):
        x0 = left + i * 150
        draw.ellipse([x0, 175, x0 + 24, 199], fill=color)
        text(draw, (x0 + 34, 171), label, size=24)
    save_chart(img, "01_landscape_bubble")


def chart_provider_ranking(df: pd.DataFrame) -> None:
    img, draw = canvas("图表二：头部模型横向排名", "每个系列取综合分最高的代表模型，比较不同公司/系列的当前能力位置。")
    text(draw, (1900, 102), "* 含非完全实测/口径映射指标", size=21, fill=PALETTE["muted"], anchor="ra")
    rep = df.sort_values("Composite_Score", ascending=False).groupby("family", as_index=False).head(1).sort_values("Composite_Score", ascending=True)
    left, top, right, row_h = 520, 218, 1770, 45
    max_score = rep["Composite_Score"].max()
    min_score = rep["Composite_Score"].min() - 0.04
    for i, (_, row) in enumerate(rep.iterrows()):
        y = top + i * row_h
        bar_w = map_value(row["Composite_Score"], min_score, max_score, 80, right - left)
        color = SERIES_COLORS.get(row["family"], PALETTE["blue"])
        text(draw, (70, y + 6), row["family"], size=21, bold=True)
        text(draw, (230, y + 6), row["model_name"], size=19, fill=PALETTE["muted"])
        draw.rounded_rectangle([left, y, left + bar_w, y + 29], radius=8, fill=color)
        has_estimated_metric = not bool(row.get("benchmark_observed", True)) or not bool(row.get("arena_observed", True)) or not bool(row.get("hardware_observed", True))
        suffix = "*" if has_estimated_metric else ""
        text(draw, (left + bar_w + 14, y + 1), f"{row['Composite_Score']:.3f}{suffix}", size=19)
    save_chart(img, "02_provider_ranking")


def chart_series_progression(df: pd.DataFrame) -> None:
    img, draw = canvas("图表三：同一系列模型的纵向进步", "按发布日期追踪系列内代表模型的能力变化，观察 2024 到 2026 年 6 月前的演进速度。")
    families = list(SERIES_COLORS.keys())
    plot = df[df["family"].isin(families)].copy()
    plot["date_ord"] = plot["release_date"].map(pd.Timestamp.toordinal)
    left, top, right, bottom = 140, 235, 1660, 1030
    draw_axes(draw, left, top, right, bottom, "发布日期", "综合能力分 Average_Score")
    x_min, x_max = plot["date_ord"].min(), pd.Timestamp(COLLECTION_CUTOFF).toordinal()
    y_min, y_max = plot["Average_Score"].min() - 2, plot["Average_Score"].max() + 2
    tick_dates = pd.to_datetime(["2024-01-01", "2024-07-01", "2025-01-01", "2025-07-01", "2026-01-01", COLLECTION_CUTOFF])
    for dt in tick_dates:
        x = map_value(dt.toordinal(), x_min, x_max, left, right)
        draw.line([x, bottom, x, top], fill=(236, 240, 245), width=1)
        text(draw, (x, bottom + 26), dt.strftime("%Y-%m"), size=20, fill=PALETTE["muted"], anchor="mm")
    for fam in families:
        sub = plot[plot["family"] == fam].sort_values("release_date")
        pts = [(map_value(r["date_ord"], x_min, x_max, left, right), map_value(r["Average_Score"], y_min, y_max, bottom, top)) for _, r in sub.iterrows()]
        color = SERIES_COLORS[fam]
        if len(pts) >= 2:
            draw.line(pts, fill=color, width=5)
        for x, y in pts:
            draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=color, outline="white", width=2)
        if pts:
            text(draw, (pts[-1][0] + 12, pts[-1][1] - 12), fam, size=23, fill=color, bold=True)
    text(draw, (1710, 300), "专业含义", size=30, bold=True)
    text_box(draw, (1710, 350), "推理强化、蒸馏和 MoE 让多个系列在一年内明显上移。", 220, size=23, fill=PALETTE["ink"])
    text(draw, (1710, 500), "生活感受", size=30, bold=True)
    text_box(draw, (1710, 550), "同样是聊天或写代码，新版本更像“少追问、少返工”的助手。", 220, size=23, fill=PALETTE["muted"])
    save_chart(img, "03_series_progression")


def heat_color(value: float, lo: float, hi: float) -> tuple[int, int, int]:
    t = 0 if hi == lo else (value - lo) / (hi - lo)
    return int(232 - 180 * t), int(245 - 90 * t), int(233 - 130 * t)


def chart_architecture_heatmap(df: pd.DataFrame) -> None:
    img, draw = canvas("图表四：架构生态与训练范式热力图", "单元格为平均综合能力分，观察主流模型依靠哪些架构和训练策略取得提升。")
    open_df = df[df["availability"] == "开放权重"].copy()
    arch_map = {
        "LlamaForCausalLM": "Llama",
        "Qwen2ForCausalLM": "Qwen2",
        "Qwen3ForCausalLM": "Qwen3",
        "DeepseekForCausalLM": "DeepSeek",
        "MistralForCausalLM": "Mistral",
        "MixtralForCausalLM": "Mixtral",
        "GemmaForCausalLM": "Gemma",
        "PhiForCausalLM": "Phi",
        "ChatGLMForCausalLM": "GLM",
    }
    open_df["arch_short"] = open_df["architecture"].map(arch_map).fillna(open_df["architecture"])
    paradigms = ["指令微调", "MoE/模型融合", "混合推理", "推理强化", "蒸馏/推理微调", "蒸馏/小模型"]
    arches = open_df["arch_short"].value_counts().head(8).index.tolist()
    matrix = open_df.pivot_table(index="arch_short", columns="training_paradigm", values="Average_Score", aggfunc="mean").reindex(arches)
    vals = matrix.to_numpy().astype(float)
    lo, hi = np.nanmin(vals), np.nanmax(vals)
    left, top = 330, 250
    cell_w, cell_h = 230, 84
    for j, col in enumerate(paradigms):
        text_box(draw, (left + j * cell_w + 8, top - 72), col, 190, size=20, fill=PALETTE["ink"])
    for i, arch in enumerate(arches):
        text(draw, (left - 28, top + i * cell_h + 24), arch, size=24, bold=True, anchor="ra")
        for j, col in enumerate(paradigms):
            value = matrix.loc[arch, col] if col in matrix.columns else np.nan
            x0, y0 = left + j * cell_w, top + i * cell_h
            fill = (241, 245, 249) if np.isnan(value) else heat_color(float(value), lo, hi)
            label = "—" if np.isnan(value) else f"{value:.1f}"
            draw.rectangle([x0, y0, x0 + cell_w - 8, y0 + cell_h - 8], fill=fill, outline="white", width=3)
            text(draw, (x0 + cell_w / 2 - 4, y0 + cell_h / 2 - 6), label, size=26, bold=not np.isnan(value), anchor="mm")
    text(draw, (330, 1080), "结论：主流提升不只来自更大参数，也来自 MoE、蒸馏和推理训练等工程策略。", size=28, fill=PALETTE["teal"], bold=True)
    save_chart(img, "04_architecture_heatmap")


def corr_color(value: float) -> tuple[int, int, int]:
    t = (value + 1) / 2
    if t < 0.5:
        p = t / 0.5
        return int(220 + (255 - 220) * p), int(38 + (255 - 38) * p), int(38 + (255 - 38) * p)
    p = (t - 0.5) / 0.5
    return int(255 + (37 - 255) * p), int(255 + (99 - 255) * p), int(255 + (235 - 255) * p)


def chart_correlation(df: pd.DataFrame) -> None:
    img, draw = canvas("图表五：客观基准与人类偏好的相关矩阵", "下三角热力图比较知识、推理、数学、指令遵循、速度与人类 Elo 的关系。")
    cols = BENCHMARKS + ["chatbot_arena_elo", "output_tokens_per_second", "time_to_first_token_s"]
    labels = ["MMLU", "IFEval", "BBH", "GPQA", "MATH", "MuSR", "Elo", "TPS", "TTFT"]
    corr = df[cols].corr()
    left, top, cell = 320, 230, 92
    for i, label in enumerate(labels):
        text(draw, (left - 18, top + i * cell + 32), label, size=23, anchor="ra")
        text(draw, (left + i * cell + 42, top - 35), label, size=21, anchor="mm")
    for i, row in enumerate(cols):
        for j, col in enumerate(cols):
            x0, y0 = left + j * cell, top + i * cell
            if j > i:
                draw.rectangle([x0, y0, x0 + cell - 6, y0 + cell - 6], fill=(248, 250, 252), outline="white")
                continue
            value = float(corr.loc[row, col])
            draw.rectangle([x0, y0, x0 + cell - 6, y0 + cell - 6], fill=corr_color(value), outline="white", width=3)
            fill = "white" if abs(value) > 0.62 else PALETTE["ink"]
            text(draw, (x0 + cell / 2 - 3, y0 + cell / 2 - 5), f"{value:.2f}", size=22, bold=True, fill=fill, anchor="mm")
    text(draw, (1260, 305), "专业含义", size=32, bold=True)
    text_box(draw, (1260, 360), "Elo 与指令遵循、综合推理高度相关，但并不等于某一个考试分数。", 520, size=26, fill=PALETTE["ink"])
    text(draw, (1260, 535), "生活直觉", size=32, bold=True)
    text_box(draw, (1260, 590), "一个模型“分数高”不一定“用起来顺手”；是否听懂要求、回复是否快，也会影响真实体验。", 520, size=26, fill=PALETTE["muted"])
    save_chart(img, "05_correlation_matrix")


def chart_hardware_pareto(df: pd.DataFrame) -> None:
    img, draw = canvas("图表六：本地部署帕累托图", "右下区域代表高吞吐、低延迟；点的颜色区分开放权重与 API/闭源模型。")
    left, top, right, bottom = 140, 240, 1450, 1030
    draw_axes(draw, left, top, right, bottom, "输出速度 output_tokens_per_second", "首字延迟 time_to_first_token_s")
    x = df["output_tokens_per_second"]
    y = df["time_to_first_token_s"]
    x_min, x_max = x.min() - 5, x.max() + 5
    y_min, y_max = 0, y.max() + 0.3
    colors = {"开放权重": PALETTE["teal"], "API/闭源": PALETTE["orange"]}
    for _, row in df.iterrows():
        px = map_value(row["output_tokens_per_second"], x_min, x_max, left, right)
        py = map_value(row["time_to_first_token_s"], y_min, y_max, bottom, top)
        color = colors.get(row["availability"], PALETTE["blue"])
        radius = 8 + row["Elo_norm"] * 14
        draw.ellipse([px - radius, py - radius, px + radius, py + radius], fill=color, outline="white", width=2)
    pareto = df.sort_values("output_tokens_per_second", ascending=False)
    best = []
    min_ttft = float("inf")
    for _, row in pareto.iterrows():
        if row["time_to_first_token_s"] < min_ttft:
            best.append(row)
            min_ttft = row["time_to_first_token_s"]
    pts = [(map_value(r["output_tokens_per_second"], x_min, x_max, left, right), map_value(r["time_to_first_token_s"], y_min, y_max, bottom, top)) for r in best]
    if len(pts) > 1:
        draw.line(pts, fill=PALETTE["red"], width=5)
    top_models = df.nsmallest(7, "Hardware_Pareto_Index")
    panel_x = 1580
    draw.rounded_rectangle([panel_x - 35, 245, 1940, 1030], radius=18, fill=PALETTE["panel"], outline=PALETTE["grid"], width=2)
    text(draw, (panel_x, 285), "黄金候选", size=32, bold=True)
    draw.ellipse([panel_x, 330, panel_x + 20, 350], fill=PALETTE["teal"])
    text(draw, (panel_x + 30, 324), "开放权重", size=20, fill=PALETTE["ink"])
    draw.ellipse([panel_x + 150, 330, panel_x + 170, 350], fill=PALETTE["orange"])
    text(draw, (panel_x + 180, 324), "API/闭源", size=20, fill=PALETTE["ink"])
    y0 = 390
    for i, (_, row) in enumerate(top_models.iterrows(), 1):
        text(draw, (panel_x, y0), f"{i}. {row['model_name']}", size=22)
        text(draw, (panel_x, y0 + 28), f"TPS {row['output_tokens_per_second']:.0f} · TTFT {row['time_to_first_token_s']:.2f}s", size=18, fill=PALETTE["muted"])
        y0 += 72
    text_box(draw, (panel_x, 922), "生活含义：等待更少，长文、代码、资料整理更连贯。", 300, size=22, fill=PALETTE["teal"], bold=True)
    save_chart(img, "06_hardware_pareto")


def main() -> None:
    ensure_dirs()
    df = process_data()
    chart_landscape_bubble(df)
    chart_provider_ranking(df)
    chart_series_progression(df)
    chart_architecture_heatmap(df)
    chart_correlation(df)
    chart_hardware_pareto(df)
    print(f"processed rows: {len(df)}")
    print(f"families: {df['family'].nunique()}")
    print(f"processed data: {PROCESSED_PATH}")
    print(f"figures: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
