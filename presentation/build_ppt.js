const fs = require("fs");
const path = require("path");
const Module = require("module");

const bundledNodeModules = "C:\\Users\\HBZuo\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules";
const bundledPnpmModules = path.join(bundledNodeModules, ".pnpm", "node_modules");
process.env.NODE_PATH = [process.env.NODE_PATH, bundledNodeModules, bundledPnpmModules].filter(Boolean).join(path.delimiter);
Module._initPaths();

const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "LLM项目课堂展示.pptx");
const FIG = path.join(ROOT, "dashboard", "assets", "figures");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Codex";
pptx.subject = "开源大语言模型性能演进与架构特征可视化分析";
pptx.title = "LLM项目课堂展示";
pptx.company = "课程项目";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Noto Sans SC",
  bodyFontFace: "Noto Sans SC",
  lang: "zh-CN",
};
pptx.defineLayout({ name: "COURSE_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "COURSE_WIDE";

const C = {
  ink: "232B38",
  muted: "667085",
  blue: "2563EB",
  teal: "0F766E",
  green: "16A34A",
  orange: "EA580C",
  bg: "F7FAFC",
  line: "D8E0EA",
  white: "FFFFFF",
};

function addTitle(slide, title, kicker) {
  slide.addText(kicker || "数据处理与可视化课程项目", {
    x: 0.55,
    y: 0.32,
    w: 12,
    h: 0.28,
    fontFace: "Noto Sans SC",
    fontSize: 11,
    bold: true,
    color: C.teal,
    margin: 0,
  });
  slide.addText(title, {
    x: 0.55,
    y: 0.68,
    w: 12,
    h: 0.56,
    fontFace: "Noto Sans SC",
    fontSize: 24,
    bold: true,
    color: C.ink,
    breakLine: false,
    fit: "shrink",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, { x: 0.55, y: 1.34, w: 12.2, h: 0, line: { color: C.line, width: 1 } });
}

function addFooter(slide, page) {
  slide.addText(`开源大模型性能演进可视化分析 · ${page}`, {
    x: 0.55,
    y: 7.14,
    w: 12,
    h: 0.18,
    fontFace: "Noto Sans SC",
    fontSize: 8.5,
    color: "8A97A8",
    margin: 0,
  });
}

function bullet(slide, items, x, y, w) {
  items.forEach((item, i) => {
    slide.addShape(pptx.ShapeType.ellipse, { x, y: y + i * 0.58 + 0.08, w: 0.13, h: 0.13, fill: { color: C.teal }, line: { color: C.teal } });
    slide.addText(item, {
      x: x + 0.24,
      y: y + i * 0.58,
      w,
      h: 0.34,
      fontFace: "Noto Sans SC",
      fontSize: 15,
      color: C.ink,
      fit: "shrink",
      margin: 0,
    });
  });
}

function addImageSlide(title, image, insight, page) {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addTitle(slide, title);
  slide.addImage({ path: path.join(FIG, image), x: 0.58, y: 1.55, w: 8.35, h: 4.95 });
  slide.addShape(pptx.ShapeType.rect, { x: 9.25, y: 1.55, w: 3.15, h: 4.95, fill: { color: C.bg }, line: { color: C.line }, radius: 0.06 });
  slide.addText("课堂讲解要点", {
    x: 9.55,
    y: 1.9,
    w: 2.55,
    h: 0.32,
    fontFace: "Noto Sans SC",
    fontSize: 17,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  bullet(slide, insight, 9.55, 2.45, 2.5);
  addFooter(slide, page);
}

function titleSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: "F8FAFC" };
  slide.addText("开源大语言模型性能演进与架构特征分析", {
    x: 0.75,
    y: 0.72,
    w: 8.1,
    h: 1.3,
    fontFace: "Noto Sans SC",
    fontSize: 34,
    bold: true,
    color: C.ink,
    fit: "shrink",
    margin: 0,
  });
  slide.addText("本地数据处理 · KNN 插补 · 归一化 · 五类可视化证据", {
    x: 0.78,
    y: 2.15,
    w: 7.6,
    h: 0.38,
    fontFace: "Noto Sans SC",
    fontSize: 16,
    color: C.muted,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, { x: 9.15, y: 0.78, w: 2.85, h: 5.6, fill: { color: C.white }, line: { color: C.line }, radius: 0.06 });
  [
    ["数据对象", "2024-2026 LLM 基准、Elo、架构与硬件延迟"],
    ["处理重点", "参数修正、Elo 插补、Min-Max 归一化"],
    ["展示方式", "本地网页 + 中文 PPT + PNG 图表"],
  ].forEach((row, i) => {
    slide.addText(row[0], { x: 9.45, y: 1.18 + i * 1.55, w: 2.2, h: 0.26, fontFace: "Noto Sans SC", fontSize: 12, bold: true, color: C.teal, margin: 0 });
    slide.addText(row[1], { x: 9.45, y: 1.55 + i * 1.55, w: 2.2, h: 0.62, fontFace: "Noto Sans SC", fontSize: 15, color: C.ink, fit: "shrink", margin: 0 });
  });
  addFooter(slide, 1);
}

function processSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addTitle(slide, "数据处理流程与特征工程");
  const steps = [
    ["异常识别", "参数量 -1/空值 → 从模型名提取 7B/72B 等信息"],
    ["KNN 插补", "用六类客观基准估算缺失的 Chatbot Arena Elo"],
    ["归一化", "将 GPQA、IFEval、MATH 等投射到统一尺度"],
    ["复合指标", "构造参数效率与 Hardware Pareto Index"],
  ];
  steps.forEach((step, i) => {
    const x = 0.78 + i * 3.05;
    slide.addShape(pptx.ShapeType.rect, { x, y: 2.18, w: 2.55, h: 2.45, fill: { color: i % 2 ? "F1F5F9" : "ECFDF5" }, line: { color: C.line }, radius: 0.08 });
    slide.addText(`${i + 1}`, { x: x + 0.2, y: 2.42, w: 0.45, h: 0.45, fontFace: "Noto Sans SC", fontSize: 18, bold: true, color: C.white, align: "center", valign: "mid", fill: { color: i % 2 ? C.blue : C.teal }, margin: 0 });
    slide.addText(step[0], { x: x + 0.28, y: 3.02, w: 2.0, h: 0.34, fontFace: "Noto Sans SC", fontSize: 18, bold: true, color: C.ink, margin: 0 });
    slide.addText(step[1], { x: x + 0.28, y: 3.55, w: 2.0, h: 0.74, fontFace: "Noto Sans SC", fontSize: 13.5, color: C.muted, fit: "shrink", margin: 0 });
    if (i < 3) {
      slide.addShape(pptx.ShapeType.chevron, { x: x + 2.63, y: 3.2, w: 0.42, h: 0.42, fill: { color: C.orange }, line: { color: C.orange } });
    }
  });
  slide.addText("输出物：清洗后 CSV、5 张中文 PNG 可视化图片、本地网页与课堂展示 PPT。", {
    x: 1.15,
    y: 5.55,
    w: 10.8,
    h: 0.42,
    fontFace: "Noto Sans SC",
    fontSize: 17,
    bold: true,
    color: C.teal,
    align: "center",
    margin: 0,
  });
  addFooter(slide, 2);
}

function conclusionSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addTitle(slide, "课堂结论：从刷榜到可部署能力");
  const claims = [
    ["能力密度", "高质量数据微调让 7B-9B 模型逼近更大模型的可用体验。"],
    ["架构收敛", "开源生态在 Llama/Qwen 等底座上进行二次开发，创新转向微调、蒸馏与融合。"],
    ["评估鸿沟", "客观基准与人类 Elo 并非完全一致，指令遵循与响应延迟更贴近日常使用。"],
    ["本地部署", "高吞吐、低延迟的小模型降低端侧应用门槛，推动算力平民化。"],
  ];
  claims.forEach((claim, i) => {
    const y = 1.65 + i * 1.15;
    slide.addShape(pptx.ShapeType.rect, { x: 0.9, y, w: 11.25, h: 0.78, fill: { color: i % 2 ? "F8FAFC" : "ECFDF5" }, line: { color: C.line }, radius: 0.06 });
    slide.addText(claim[0], { x: 1.18, y: y + 0.18, w: 1.55, h: 0.25, fontFace: "Noto Sans SC", fontSize: 16, bold: true, color: i % 2 ? C.blue : C.teal, margin: 0 });
    slide.addText(claim[1], { x: 2.75, y: y + 0.18, w: 8.85, h: 0.33, fontFace: "Noto Sans SC", fontSize: 15.5, color: C.ink, fit: "shrink", margin: 0 });
  });
  addFooter(slide, 7);
}

function assertAssets() {
  ["01_scaling_bubble.png", "02_radar_profile.png", "03_architecture_heatmap.png", "04_correlation_matrix.png", "05_hardware_jointplot.png"].forEach((file) => {
    const p = path.join(FIG, file);
    if (!fs.existsSync(p)) throw new Error(`缺少图表文件：${p}`);
  });
}

async function main() {
  assertAssets();
  titleSlide();
  processSlide();
  addImageSlide("证据 1：缩放定律与参数效率", "01_scaling_bubble.png", ["log 参数轴处理长尾分布", "趋势线显示边际收益趋缓", "小模型通过微调获得高能力密度"], 3);
  addImageSlide("证据 2：能力轮廓与偏科检测", "02_radar_profile.png", ["7B-9B 模型横向比较", "GPQA/MATH 放大真实差距", "均值线提供课堂解读参照"], 4);
  addImageSlide("证据 3：架构生态与训练范式", "03_architecture_heatmap.png", ["底层架构呈现收敛", "微调、蒸馏和 MoE 推动二次开发", "热力矩阵同时表达类别与强度"], 5);
  addImageSlide("证据 4：偏好相关性与硬件帕累托", "04_correlation_matrix.png", ["Elo 与客观测试存在评估鸿沟", "指令遵循更贴近日常体验", "延迟指标解释部署体验损耗"], 6);
  conclusionSlide();
  await pptx.writeFile({ fileName: OUT });
  console.log(`wrote ${OUT}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
