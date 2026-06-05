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
pptx.defineLayout({ name: "COURSE_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "COURSE_WIDE";
pptx.author = "课程项目组";
pptx.company = "数据处理与可视化课程";
pptx.subject = "2024-2026 主流大语言模型数据处理与可视化";
pptx.title = "主流大模型数据可视化课程展示";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Noto Sans SC",
  bodyFontFace: "Noto Sans SC",
  lang: "zh-CN",
};

const C = {
  ink: "232B38",
  muted: "64748B",
  blue: "2563EB",
  teal: "0F766E",
  green: "16A34A",
  orange: "EA580C",
  red: "DC2626",
  purple: "7C3AED",
  bg: "F8FAFC",
  panel: "F1F5F9",
  line: "D8E0EA",
  white: "FFFFFF",
};

const figures = {
  bubble: "01_landscape_bubble.png",
  ranking: "02_provider_ranking.png",
  progression: "03_series_progression.png",
  heatmap: "04_architecture_heatmap.png",
  correlation: "05_correlation_matrix.png",
  pareto: "06_hardware_pareto.png",
};

function addTitle(slide, title, kicker = "数据处理与可视化课程项目") {
  slide.addText(kicker, {
    x: 0.55,
    y: 0.28,
    w: 12,
    h: 0.25,
    fontFace: "Noto Sans SC",
    fontSize: 10.5,
    bold: true,
    color: C.teal,
    margin: 0,
  });
  slide.addText(title, {
    x: 0.55,
    y: 0.63,
    w: 12,
    h: 0.55,
    fontFace: "Noto Sans SC",
    fontSize: 23,
    bold: true,
    color: C.ink,
    fit: "shrink",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, { x: 0.55, y: 1.27, w: 12.2, h: 0, line: { color: C.line, width: 1 } });
}

function addFooter(slide, page) {
  slide.addText(`主流大模型数据可视化分析 · ${page}`, {
    x: 0.55,
    y: 7.13,
    w: 12,
    h: 0.16,
    fontFace: "Noto Sans SC",
    fontSize: 8.5,
    color: "8A97A8",
    margin: 0,
  });
}

function addBullets(slide, items, x, y, w, color = C.teal, fontSize = 14.5, gap = 0.54) {
  items.forEach((item, i) => {
    const yy = y + i * gap;
    slide.addShape(pptx.ShapeType.ellipse, { x, y: yy + 0.07, w: 0.11, h: 0.11, fill: { color }, line: { color } });
    slide.addText(item, {
      x: x + 0.22,
      y: yy,
      w,
      h: 0.34,
      fontFace: "Noto Sans SC",
      fontSize,
      color: C.ink,
      fit: "shrink",
      margin: 0,
    });
  });
}

function addSectionBox(slide, title, body, x, y, w, h, color = C.teal) {
  slide.addShape(pptx.ShapeType.rect, { x, y, w, h, fill: { color: C.bg }, line: { color: C.line }, radius: 0.06 });
  slide.addText(title, {
    x: x + 0.22,
    y: y + 0.2,
    w: w - 0.44,
    h: 0.26,
    fontFace: "Noto Sans SC",
    fontSize: 13,
    bold: true,
    color,
    margin: 0,
  });
  slide.addText(body, {
    x: x + 0.22,
    y: y + 0.56,
    w: w - 0.44,
    h: h - 0.72,
    fontFace: "Noto Sans SC",
    fontSize: 13.5,
    color: C.ink,
    fit: "shrink",
    margin: 0,
    breakLine: false,
  });
}

function titleSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: "F8FAFC" };
  slide.addText("2024-2026 主流大语言模型", {
    x: 0.72,
    y: 0.82,
    w: 7.9,
    h: 0.55,
    fontFace: "Noto Sans SC",
    fontSize: 25,
    bold: true,
    color: C.teal,
    margin: 0,
  });
  slide.addText("数据处理与可视化分析", {
    x: 0.72,
    y: 1.42,
    w: 8.6,
    h: 0.9,
    fontFace: "Noto Sans SC",
    fontSize: 37,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  slide.addText("横向比较不同模型，纵向观察同一系列进步；用图表把复杂表格数据变成可解释结论。", {
    x: 0.75,
    y: 2.62,
    w: 8.4,
    h: 0.48,
    fontFace: "Noto Sans SC",
    fontSize: 16,
    color: C.muted,
    margin: 0,
  });
  [
    ["课程目标", "数据收集、清洗、特征工程、可视化表达"],
    ["数据范围", "68 个代表模型 · 17 个系列 · 截止 2026-06-05"],
    ["展示重点", "横向对比、纵向趋势、相关性、帕累托权衡"],
  ].forEach((row, i) => {
    addSectionBox(slide, row[0], row[1], 9.35, 0.95 + i * 1.55, 2.75, 1.05, i === 0 ? C.teal : i === 1 ? C.blue : C.orange);
  });
  addFooter(slide, 1);
}

function whySlide() {
  const slide = pptx.addSlide();
  addTitle(slide, "为什么选择这个项目：复杂模型数据适合做可视化");
  addSectionBox(slide, "数据问题", "主流模型数量快速增加，参数量、发布时间、基准分、Elo、速度和延迟分散在不同来源，单看表格很难比较。", 0.85, 1.85, 3.75, 3.8, C.blue);
  addSectionBox(slide, "课程价值", "这个主题天然包含分类变量、连续变量、时间变量和缺失值，适合展示清洗、归一化、插补、横纵向对比等课程方法。", 4.85, 1.85, 3.75, 3.8, C.teal);
  addSectionBox(slide, "展示目标", "不是简单罗列模型，而是通过图表回答：谁更强、进步有多快、哪些指标更接近体验、哪些模型更适合部署。", 8.85, 1.85, 3.75, 3.8, C.orange);
  slide.addText("这页的重点：项目选题服务于数据可视化课程本身，因为它有足够复杂的数据结构，也能产出清楚的图表结论。", {
    x: 1.0,
    y: 6.16,
    w: 11.4,
    h: 0.42,
    fontFace: "Noto Sans SC",
    fontSize: 16.5,
    bold: true,
    color: C.teal,
    align: "center",
    margin: 0,
  });
  addFooter(slide, 2);
}

function dataScopeSlide() {
  const slide = pptx.addSlide();
  addTitle(slide, "数据范围与字段设计");
  addBullets(slide, [
    "时间范围：2024-01-01 至 2026-06-05，按发布日期和采集截止日组织。",
    "模型范围：17 个主流系列，每个系列保留多个代表版本，支持纵向趋势分析。",
    "核心字段：模型名、公司、系列、架构、训练范式、参数量、发布时间、基准分、Elo、吞吐、首字延迟。",
    "质量标记：保留 benchmark_observed、arena_observed、hardware_observed，区分实测与插补。",
  ], 0.95, 1.78, 11.3, C.teal, 16, 0.68);
  slide.addShape(pptx.ShapeType.rect, { x: 0.95, y: 4.8, w: 11.45, h: 1.35, fill: { color: C.bg }, line: { color: C.line }, radius: 0.06 });
  slide.addText("数据可视化课程对应点", { x: 1.25, y: 5.08, w: 2.8, h: 0.28, fontFace: "Noto Sans SC", fontSize: 15, bold: true, color: C.blue, margin: 0 });
  slide.addText("本项目不是追求爬取长尾全集，而是构造可比较、可解释、可展示的代表性数据表；字段设计直接服务于后续图表编码。", {
    x: 1.25,
    y: 5.45,
    w: 10.6,
    h: 0.34,
    fontFace: "Noto Sans SC",
    fontSize: 15.5,
    color: C.ink,
    margin: 0,
  });
  addFooter(slide, 3);
}

function processSlide() {
  const slide = pptx.addSlide();
  addTitle(slide, "数据处理过程：从原始字段到可视化指标");
  const steps = [
    ["字段统一", "统一日期、系列、架构、训练范式和模型规模，保证横向比较口径一致。"],
    ["缺失处理", "保留观测标记；对 Elo、速度、延迟等缺失值用同系列均值和 KNN 插补。"],
    ["归一化", "将 MMLU、GPQA、IFEval 等不同量纲投射到统一尺度，避免视觉权重失真。"],
    ["复合指标", "构造 Average_Score、Composite_Score、Hardware_Pareto_Index，服务图表排序与筛选。"],
  ];
  steps.forEach((s, i) => {
    const x = 0.72 + i * 3.12;
    slide.addShape(pptx.ShapeType.rect, { x, y: 2.05, w: 2.68, h: 2.9, fill: { color: i % 2 ? "F1F5F9" : "ECFDF5" }, line: { color: C.line }, radius: 0.08 });
    slide.addText(`${i + 1}`, { x: x + 0.22, y: 2.32, w: 0.44, h: 0.44, fontFace: "Noto Sans SC", fontSize: 17, bold: true, color: C.white, align: "center", valign: "mid", fill: { color: i % 2 ? C.blue : C.teal }, margin: 0 });
    slide.addText(s[0], { x: x + 0.28, y: 3.0, w: 2.1, h: 0.33, fontFace: "Noto Sans SC", fontSize: 18, bold: true, color: C.ink, margin: 0 });
    slide.addText(s[1], { x: x + 0.28, y: 3.55, w: 2.12, h: 0.82, fontFace: "Noto Sans SC", fontSize: 13.2, color: C.muted, fit: "shrink", margin: 0 });
    if (i < 3) {
      slide.addShape(pptx.ShapeType.chevron, { x: x + 2.76, y: 3.35, w: 0.38, h: 0.38, fill: { color: C.orange }, line: { color: C.orange } });
    }
  });
  slide.addText("课程重点：所有图表都不是装饰，而是建立在清洗、变换和指标构造之后的分析表达。", {
    x: 1.1,
    y: 5.92,
    w: 11.1,
    h: 0.38,
    fontFace: "Noto Sans SC",
    fontSize: 16,
    bold: true,
    color: C.teal,
    align: "center",
    margin: 0,
  });
  addFooter(slide, 4);
}

function imageSlide(page, title, image, seen, professional, daily) {
  const slide = pptx.addSlide();
  addTitle(slide, title);
  slide.addImage({ path: path.join(FIG, image), x: 0.55, y: 1.55, w: 7.7, h: 4.82 });
  addSectionBox(slide, "图中看到了什么", seen, 8.62, 1.55, 3.6, 1.36, C.blue);
  addSectionBox(slide, "专业上说明什么", professional, 8.62, 3.1, 3.6, 1.55, C.teal);
  addSectionBox(slide, "生活中意味着什么", daily, 8.62, 4.85, 3.6, 1.35, C.orange);
  addFooter(slide, page);
}

function conclusionSlide() {
  const slide = pptx.addSlide();
  addTitle(slide, "项目结论：可视化让模型数据从“复杂”变成“可解释”");
  addSectionBox(slide, "课程层面的收获", "通过同一项目串起数据收集、缺失处理、归一化、特征工程、视觉编码和图表解读，完整覆盖数据可视化课程的核心要求。", 0.8, 1.65, 3.75, 3.75, C.teal);
  addSectionBox(slide, "数据分析层面的发现", "主流模型能力持续上升，开放权重模型追赶很快；但参数量、考试分数、Elo 和部署体验并不是同一个维度。", 4.75, 1.65, 3.75, 3.75, C.blue);
  addSectionBox(slide, "直觉层面的理解", "好的图表能把抽象指标翻译成真实感受：等多久、写得顺不顺、能否本地运行、成本是否可接受。", 8.7, 1.65, 3.75, 3.75, C.orange);
  slide.addText("最终意义：这个项目的重点不是展示模型有多强，而是展示如何用数据可视化方法把多维数据整理成可比较、可解释、可讨论的结论。", {
    x: 1.0,
    y: 6.05,
    w: 11.4,
    h: 0.5,
    fontFace: "Noto Sans SC",
    fontSize: 16.5,
    bold: true,
    color: C.teal,
    align: "center",
    margin: 0,
  });
  addFooter(slide, 11);
}

function assertAssets() {
  Object.values(figures).forEach((file) => {
    const p = path.join(FIG, file);
    if (!fs.existsSync(p)) throw new Error(`缺少图表文件：${p}`);
  });
}

async function main() {
  assertAssets();
  titleSlide();
  whySlide();
  dataScopeSlide();
  processSlide();
  imageSlide(
    5,
    "横向比较：主流模型能力气泡图",
    figures.bubble,
    "每个点是一个模型，位置展示参数量和综合能力，颜色区分开放权重与闭源 API。",
    "这是多变量散点图：X/Y/颜色/大小共同表达模型规模、能力、人类偏好和开放性。",
    "不是所有大模型都必须很大才好用，一些中小模型也能在日常任务中表现顺手。"
  );
  imageSlide(
    6,
    "横向比较：头部系列代表模型排名",
    figures.ranking,
    "每个模型系列取综合分最高的代表模型，用横条比较不同系列的位置。",
    "这是排序条形图，适合表达类别之间的整体差异，比散点图更利于快速读排名。",
    "使用者可以快速判断不同模型家族的大致水平，而不是陷入一长串表格。"
  );
  imageSlide(
    7,
    "纵向比较：同一系列模型的进步轨迹",
    figures.progression,
    "折线展示 GPT、Claude、Gemini、Llama、Qwen、DeepSeek 等系列随时间的能力变化。",
    "这是时间序列可视化，回答同一系列模型是否持续进步、进步速度是否一致。",
    "新版本常带来更少追问、更少返工，聊天、写作和编程体验会更连贯。"
  );
  imageSlide(
    8,
    "结构比较：架构生态与训练范式热力图",
    figures.heatmap,
    "矩阵展示不同架构和训练方式组合下的平均综合能力。",
    "这是分类变量与连续变量的联合编码，可以同时看结构分布和性能强弱。",
    "模型进步不只是参数变大，也可能来自微调、蒸馏、MoE 和推理训练。"
  );
  imageSlide(
    9,
    "关系分析：客观基准与人类偏好相关矩阵",
    figures.correlation,
    "矩阵展示多个基准指标、Elo、速度和延迟之间的相关关系。",
    "这是相关性热力图，用来判断哪些指标更接近真实偏好，哪些指标只是局部能力。",
    "考试分数高不一定代表用起来最好，是否听懂要求、回复是否快也很重要。"
  );
  imageSlide(
    10,
    "权衡分析：本地部署帕累托图",
    figures.pareto,
    "散点展示模型吞吐、首字延迟和能力之间的权衡，红线表示较优前沿。",
    "这是多目标权衡图，适合寻找高能力、低延迟、高吞吐的候选模型。",
    "等待时间越短，长文总结、代码生成和资料整理越像连续协作。"
  );
  conclusionSlide();
  await pptx.writeFile({ fileName: OUT });
  console.log(`wrote ${OUT}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
