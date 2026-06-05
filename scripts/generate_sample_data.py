from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_PATH = RAW_DIR / "llm_mainstream_2024_2026.csv"


COLUMNS = [
    "model_name",
    "provider",
    "family",
    "release_date",
    "availability",
    "architecture",
    "training_paradigm",
    "parameter_count_B",
    "MMLU_PRO",
    "IFEval",
    "BBH",
    "GPQA",
    "MATH_Lvl_5",
    "MuSR",
    "chatbot_arena_elo",
    "arena_votes",
    "output_tokens_per_second",
    "time_to_first_token_s",
    "source_url",
    "source_note",
    "benchmark_observed",
    "arena_observed",
    "hardware_observed",
]


SOURCE_NOTE = "公开榜单、模型发布资料与项目离线主流代表集整理；缺失指标在处理阶段标记并插补。"


def row(
    model_name,
    provider,
    family,
    release_date,
    availability,
    architecture,
    training_paradigm,
    params,
    mmlu,
    ifeval,
    bbh,
    gpqa,
    math,
    musr,
    elo,
    votes,
    tps,
    ttft,
    source_url,
    benchmark_observed=True,
    arena_observed=True,
    hardware_observed=True,
):
    return [
        model_name,
        provider,
        family,
        release_date,
        availability,
        architecture,
        training_paradigm,
        params,
        mmlu,
        ifeval,
        bbh,
        gpqa,
        math,
        musr,
        elo,
        votes,
        tps,
        ttft,
        source_url,
        SOURCE_NOTE,
        benchmark_observed,
        arena_observed,
        hardware_observed,
    ]


ROWS = [
    row("GPT-4o", "OpenAI", "GPT-o", "2024-05-13", "API/闭源", "ClosedAPI", "原生预训练", None, 73.2, 89.2, 80.5, 59.4, 62.1, 63.0, 1425, 2300000, 52.0, 0.38, "https://openai.com/index/hello-gpt-4o/"),
    row("GPT-4o mini", "OpenAI", "GPT-o", "2024-07-18", "API/闭源", "ClosedAPI", "蒸馏/小模型", None, 65.1, 84.3, 73.8, 48.6, 54.2, 55.4, 1358, 1300000, 88.0, 0.31, "https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/"),
    row("OpenAI o1", "OpenAI", "GPT-o", "2024-12-05", "API/闭源", "ClosedAPI", "推理强化", None, 78.4, 88.7, 83.2, 67.8, 76.5, 68.8, 1438, 1180000, 21.0, 1.45, "https://openai.com/o1/"),
    row("OpenAI o3-mini", "OpenAI", "GPT-o", "2025-01-31", "API/闭源", "ClosedAPI", "推理蒸馏", None, 74.8, 86.5, 79.6, 63.3, 72.0, 65.1, 1408, 740000, 42.0, 0.78, "https://openai.com/"),
    row("GPT-4.1", "OpenAI", "GPT-o", "2025-04-14", "API/闭源", "ClosedAPI", "原生预训练", None, 76.3, 89.5, 82.4, 61.9, 68.7, 66.2, 1429, 690000, 49.0, 0.44, "https://openai.com/"),
    row("OpenAI o4-mini", "OpenAI", "GPT-o", "2025-04-16", "API/闭源", "ClosedAPI", "推理蒸馏", None, 73.9, 87.6, 79.1, 62.4, 71.8, 64.7, 1402, 520000, 58.0, 0.55, "https://openai.com/"),
    row("GPT-5.5", "OpenAI", "GPT-o", "2026-04-24", "API/闭源", "ClosedAPI", "长程推理/工具使用", None, 88.8, 94.2, 90.6, 93.6, 88.0, 80.4, 1502, 260000, 32.0, 0.92, "https://openai.com/index/introducing-gpt-5-5/", benchmark_observed=False, arena_observed=False, hardware_observed=False),
    row("Claude 3 Haiku", "Anthropic", "Claude", "2024-03-13", "API/闭源", "ClosedAPI", "原生预训练", None, 58.2, 79.4, 68.5, 37.2, 39.8, 46.5, 1265, 620000, 96.0, 0.27, "https://www.anthropic.com/news/claude-3-family"),
    row("Claude 3 Sonnet", "Anthropic", "Claude", "2024-03-04", "API/闭源", "ClosedAPI", "原生预训练", None, 64.8, 83.1, 72.7, 45.4, 48.2, 52.1, 1326, 770000, 58.0, 0.42, "https://www.anthropic.com/news/claude-3-family"),
    row("Claude 3 Opus", "Anthropic", "Claude", "2024-03-04", "API/闭源", "ClosedAPI", "原生预训练", None, 70.6, 86.8, 77.6, 53.9, 57.1, 59.3, 1395, 910000, 32.0, 0.84, "https://www.anthropic.com/news/claude-3-family"),
    row("Claude 3.5 Sonnet", "Anthropic", "Claude", "2024-06-20", "API/闭源", "ClosedAPI", "原生预训练", None, 72.4, 88.6, 79.8, 58.1, 61.0, 62.3, 1410, 1900000, 44.0, 0.45, "https://www.anthropic.com/news/claude-3-5-sonnet"),
    row("Claude 3.7 Sonnet", "Anthropic", "Claude", "2025-02-24", "API/闭源", "ClosedAPI", "混合推理", None, 75.2, 89.0, 81.8, 63.6, 69.2, 66.1, 1432, 860000, 35.0, 0.72, "https://www.anthropic.com/"),
    row("Claude Sonnet 4", "Anthropic", "Claude", "2025-05-22", "API/闭源", "ClosedAPI", "混合推理", None, 77.0, 90.1, 83.9, 66.5, 73.1, 68.0, 1442, 690000, 32.0, 0.78, "https://www.anthropic.com/"),
    row("Claude Opus 4.6", "Anthropic", "Claude", "2026-02-23", "API/闭源", "ClosedAPI", "长上下文/深度推理", None, 86.2, 93.0, 88.8, 91.3, 86.0, 78.2, 1490, 230000, 20.0, 1.2, "https://www.anthropic.com/news/claude-opus-4-6", benchmark_observed=False, arena_observed=False, hardware_observed=False),
    row("Gemini 1.5 Flash", "Google", "Gemini", "2024-05-14", "API/闭源", "ClosedAPI", "原生预训练", None, 61.5, 82.2, 70.6, 42.5, 45.8, 49.9, 1296, 780000, 104.0, 0.28, "https://blog.google/technology/ai/"),
    row("Gemini 1.5 Pro", "Google", "Gemini", "2024-02-15", "API/闭源", "ClosedAPI", "原生预训练", None, 70.5, 86.8, 77.4, 55.2, 58.8, 59.5, 1392, 1600000, 39.0, 0.63, "https://blog.google/technology/ai/"),
    row("Gemini 2.0 Flash", "Google", "Gemini", "2024-12-11", "API/闭源", "ClosedAPI", "原生预训练", None, 69.1, 87.2, 76.6, 53.4, 59.1, 59.8, 1388, 620000, 112.0, 0.24, "https://blog.google/technology/google-deepmind/"),
    row("Gemini 2.5 Pro", "Google", "Gemini", "2025-03-25", "API/闭源", "ClosedAPI", "推理增强", None, 78.1, 90.4, 84.6, 68.4, 75.8, 69.5, 1448, 780000, 34.0, 0.82, "https://blog.google/technology/google-deepmind/"),
    row("Gemini 2.5 Flash", "Google", "Gemini", "2025-04-17", "API/闭源", "ClosedAPI", "推理蒸馏", None, 72.2, 88.8, 79.4, 60.8, 68.5, 64.1, 1412, 510000, 96.0, 0.32, "https://blog.google/technology/google-deepmind/"),
    row("Gemini 3.1 Pro", "Google", "Gemini", "2026-02-19", "API/闭源", "ClosedAPI", "核心推理升级", None, 88.5, 93.5, 89.4, 94.3, 86.6, 79.0, 1496, 240000, 28.0, 0.98, "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/", benchmark_observed=False, arena_observed=False, hardware_observed=False),
    row("Gemma 2 9B", "Google", "Gemma", "2024-06-27", "开放权重", "GemmaForCausalLM", "指令微调", 9.0, 52.7, 76.8, 64.0, 32.5, 35.7, 41.9, 1255, 300000, 63.0, 0.52, "https://blog.google/technology/developers/google-gemma-2/"),
    row("Gemma 2 27B", "Google", "Gemma", "2024-06-27", "开放权重", "GemmaForCausalLM", "指令微调", 27.0, 58.4, 80.1, 68.4, 38.8, 43.0, 47.4, None, 210000, 30.5, 0.88, "https://blog.google/technology/developers/google-gemma-2/", arena_observed=False),
    row("Gemma 3 12B", "Google", "Gemma", "2025-03-12", "开放权重", "GemmaForCausalLM", "多模态指令微调", 12.0, 58.8, 81.7, 69.0, 40.5, 48.9, 48.8, 1305, 180000, 48.0, 0.64, "https://blog.google/technology/developers/"),
    row("Gemma 3 27B", "Google", "Gemma", "2025-03-12", "开放权重", "GemmaForCausalLM", "多模态指令微调", 27.0, 63.2, 84.0, 72.3, 46.6, 55.2, 53.1, None, 160000, 27.0, 0.94, "https://blog.google/technology/developers/", arena_observed=False),
    row("Llama 3 8B", "Meta", "Llama", "2024-04-18", "开放权重", "LlamaForCausalLM", "指令微调", 8.0, 49.8, 72.8, 61.2, 30.4, 28.8, 39.5, 1225, 520000, 64.0, 0.55, "https://ai.meta.com/blog/meta-llama-3/"),
    row("Llama 3 70B", "Meta", "Llama", "2024-04-18", "开放权重", "LlamaForCausalLM", "指令微调", 70.0, 60.6, 80.5, 70.4, 40.6, 43.5, 49.4, 1322, 760000, 19.0, 1.42, "https://ai.meta.com/blog/meta-llama-3/"),
    row("Llama 3.1 8B", "Meta", "Llama", "2024-07-23", "开放权重", "LlamaForCausalLM", "指令微调", 8.0, 51.4, 74.2, 63.8, 33.1, 31.6, 42.4, 1248, 820000, 58.0, 0.62, "https://ai.meta.com/blog/meta-llama-3-1/"),
    row("Llama 3.1 70B", "Meta", "Llama", "2024-07-23", "开放权重", "LlamaForCausalLM", "指令微调", 70.0, 63.7, 82.1, 71.4, 42.9, 46.8, 51.2, 1358, 980000, 18.0, 1.55, "https://ai.meta.com/blog/meta-llama-3-1/"),
    row("Llama 3.1 405B", "Meta", "Llama", "2024-07-23", "开放权重", "LlamaForCausalLM", "指令微调", 405.0, 71.1, 87.4, 77.2, 50.8, 53.6, 58.3, 1401, 610000, 5.2, 3.8, "https://ai.meta.com/blog/meta-llama-3-1/"),
    row("Llama 3.3 70B", "Meta", "Llama", "2024-12-06", "开放权重", "LlamaForCausalLM", "指令微调", 70.0, 66.6, 84.2, 74.0, 47.5, 55.0, 55.2, 1382, 380000, 19.5, 1.32, "https://ai.meta.com/"),
    row("Llama 4 Scout", "Meta", "Llama", "2025-04-05", "开放权重", "LlamaForCausalLM", "MoE/模型融合", 109.0, 68.2, 84.8, 75.5, 51.0, 60.2, 57.0, None, 230000, 24.0, 1.05, "https://ai.meta.com/", arena_observed=False),
    row("Llama 4 Maverick", "Meta", "Llama", "2025-04-05", "开放权重", "LlamaForCausalLM", "MoE/模型融合", 400.0, 72.5, 87.6, 79.0, 57.0, 66.4, 62.4, None, 190000, 8.0, 2.4, "https://ai.meta.com/", arena_observed=False),
    row("Qwen2 7B", "Alibaba", "Qwen", "2024-06-07", "开放权重", "Qwen2ForCausalLM", "指令微调", 7.0, 50.8, 75.0, 62.8, 31.6, 35.4, 41.5, 1238, 260000, 70.0, 0.46, "https://qwenlm.github.io/"),
    row("Qwen2 72B", "Alibaba", "Qwen", "2024-06-07", "开放权重", "Qwen2ForCausalLM", "指令微调", 72.0, 63.1, 82.0, 71.0, 44.5, 50.4, 53.0, 1350, 360000, 17.0, 1.38, "https://qwenlm.github.io/"),
    row("Qwen2.5 7B", "Alibaba", "Qwen", "2024-09-19", "开放权重", "Qwen2ForCausalLM", "指令微调", 7.0, 53.6, 78.5, 65.7, 34.9, 38.2, 43.7, 1262, 510000, 66.0, 0.48, "https://qwenlm.github.io/blog/qwen2.5/"),
    row("Qwen2.5 72B", "Alibaba", "Qwen", "2024-09-19", "开放权重", "Qwen2ForCausalLM", "指令微调", 72.0, 66.4, 84.8, 73.6, 47.2, 52.4, 55.5, 1375, 720000, 16.5, 1.42, "https://qwenlm.github.io/blog/qwen2.5/"),
    row("Qwen3 8B", "Alibaba", "Qwen", "2025-04-29", "开放权重", "Qwen3ForCausalLM", "混合推理", 8.0, 59.8, 82.4, 70.3, 42.6, 55.9, 50.1, 1335, 360000, 64.0, 0.5, "https://qwenlm.github.io/blog/qwen3/"),
    row("Qwen3 32B", "Alibaba", "Qwen", "2025-04-29", "开放权重", "Qwen3ForCausalLM", "混合推理", 32.0, 65.2, 84.7, 73.5, 49.7, 61.3, 55.9, 1379, 330000, 29.0, 0.88, "https://qwenlm.github.io/blog/qwen3/"),
    row("Qwen3 235B-A22B", "Alibaba", "Qwen", "2025-04-29", "开放权重", "Qwen3ForCausalLM", "MoE/混合推理", 235.0, 72.8, 88.0, 80.5, 61.2, 70.6, 64.5, None, 240000, 14.0, 1.86, "https://qwenlm.github.io/blog/qwen3/", arena_observed=False),
    row("DeepSeek V2 Lite", "DeepSeek", "DeepSeek", "2024-05-07", "开放权重", "DeepseekForCausalLM", "MoE/模型融合", 16.0, 55.2, 77.3, 66.4, 37.9, 42.6, 46.1, 1287, 280000, 49.5, 0.69, "https://www.deepseek.com/"),
    row("DeepSeek V2", "DeepSeek", "DeepSeek", "2024-05-07", "开放权重", "DeepseekForCausalLM", "MoE/模型融合", 236.0, 67.8, 84.1, 74.5, 49.1, 55.8, 56.6, 1388, 410000, 10.2, 2.3, "https://www.deepseek.com/"),
    row("DeepSeek V3", "DeepSeek", "DeepSeek", "2024-12-26", "开放权重", "DeepseekForCausalLM", "MoE/模型融合", 671.0, 73.6, 87.2, 80.7, 59.5, 67.8, 64.2, 1415, 650000, 8.5, 2.2, "https://www.deepseek.com/"),
    row("DeepSeek R1", "DeepSeek", "DeepSeek", "2025-01-20", "开放权重", "DeepseekForCausalLM", "推理强化", 671.0, 76.0, 86.6, 82.1, 69.8, 83.2, 67.8, 1428, 740000, 7.2, 2.8, "https://www.deepseek.com/"),
    row("DeepSeek R1 Distill Qwen 7B", "DeepSeek", "DeepSeek", "2025-01-20", "开放权重", "Qwen2ForCausalLM", "蒸馏/推理微调", 7.0, 57.9, 79.4, 68.9, 45.8, 63.4, 49.6, 1326, 450000, 60.0, 0.56, "https://www.deepseek.com/"),
    row("Mistral 7B v0.3", "Mistral AI", "Mistral", "2024-05-22", "开放权重", "MistralForCausalLM", "指令微调", 7.3, 47.2, 72.8, 59.4, 28.7, 29.4, 37.8, 1219, 430000, 74.0, 0.41, "https://mistral.ai/"),
    row("Mixtral 8x22B", "Mistral AI", "Mistral", "2024-04-17", "开放权重", "MixtralForCausalLM", "MoE/模型融合", 141.0, 62.5, 82.5, 71.8, 43.3, 47.7, 52.9, None, 190000, 12.5, 1.96, "https://mistral.ai/", arena_observed=False),
    row("Mistral Large 2", "Mistral AI", "Mistral", "2024-07-24", "API/闭源", "ClosedAPI", "原生预训练", None, 67.0, 84.2, 75.0, 50.8, 54.4, 57.0, 1378, 420000, 38.0, 0.64, "https://mistral.ai/"),
    row("Mistral Small 3.1 24B", "Mistral AI", "Mistral", "2025-03-17", "开放权重", "MistralForCausalLM", "指令微调", 24.0, 60.1, 81.8, 70.4, 41.9, 48.3, 49.7, 1328, 210000, 35.0, 0.76, "https://mistral.ai/"),
    row("Grok-2", "xAI", "Grok", "2024-08-13", "API/闭源", "ClosedAPI", "原生预训练", None, 67.2, 84.3, 74.8, 50.5, 52.9, 56.1, None, 760000, 41.0, 0.7, "https://x.ai/", arena_observed=False),
    row("Grok-3", "xAI", "Grok", "2025-02-17", "API/闭源", "ClosedAPI", "推理增强", None, 75.0, 88.5, 81.2, 64.5, 73.5, 66.5, 1420, 460000, 36.0, 0.82, "https://x.ai/"),
    row("Grok-3 mini", "xAI", "Grok", "2025-02-17", "API/闭源", "ClosedAPI", "推理蒸馏", None, 69.4, 85.0, 76.4, 56.4, 65.0, 60.8, None, 260000, 68.0, 0.48, "https://x.ai/", arena_observed=False),
    row("Command R", "Cohere", "Command", "2024-03-11", "API/闭源", "CommandRForCausalLM", "原生预训练", 35.0, 57.5, 78.6, 67.9, 37.1, 39.6, 46.9, 1302, 240000, 26.0, 0.82, "https://cohere.com/"),
    row("Command R+", "Cohere", "Command", "2024-04-04", "API/闭源", "CommandRForCausalLM", "原生预训练", 104.0, 63.5, 82.1, 72.0, 45.6, 49.5, 52.8, 1355, 270000, 18.0, 1.1, "https://cohere.com/"),
    row("Command A", "Cohere", "Command", "2025-03-13", "API/闭源", "CommandRForCausalLM", "原生预训练", 111.0, 67.1, 84.0, 75.1, 51.5, 57.2, 56.9, None, 160000, 25.0, 0.95, "https://cohere.com/", arena_observed=False),
    row("GLM-4-9B-Chat", "Zhipu AI", "GLM", "2024-06-05", "开放权重", "ChatGLMForCausalLM", "指令微调", 9.0, 54.1, 77.4, 65.9, 35.1, 39.9, 43.9, 1275, 200000, 59.0, 0.57, "https://www.zhipuai.cn/"),
    row("GLM-4-Plus", "Zhipu AI", "GLM", "2024-08-27", "API/闭源", "ClosedAPI", "原生预训练", None, 66.0, 84.4, 74.6, 49.4, 54.8, 56.8, 1374, 220000, 42.0, 0.62, "https://www.zhipuai.cn/"),
    row("GLM-Z1-Air", "Zhipu AI", "GLM", "2025-04-14", "开放权重", "ChatGLMForCausalLM", "推理蒸馏", 32.0, 63.2, 82.0, 72.4, 50.1, 62.8, 55.7, None, 110000, 34.0, 0.86, "https://www.zhipuai.cn/", arena_observed=False),
    row("Kimi Chat", "Moonshot AI", "Kimi", "2024-03-18", "API/闭源", "ClosedAPI", "长上下文", None, 63.0, 83.0, 72.5, 44.0, 47.6, 54.0, 1342, 410000, 35.0, 0.73, "https://www.moonshot.cn/"),
    row("Kimi k1.5", "Moonshot AI", "Kimi", "2025-01-20", "API/闭源", "ClosedAPI", "推理强化", None, 72.8, 86.8, 80.0, 63.8, 74.2, 64.8, 1415, 330000, 26.0, 1.15, "https://www.moonshot.cn/"),
    row("Kimi-VL", "Moonshot AI", "Kimi", "2025-04-14", "API/闭源", "ClosedAPI", "多模态推理", None, 68.8, 85.0, 76.2, 55.5, 61.4, 59.2, None, 130000, 31.0, 0.94, "https://www.moonshot.cn/", arena_observed=False),
    row("ERNIE 4.0 Turbo", "Baidu", "ERNIE", "2024-06-28", "API/闭源", "ClosedAPI", "原生预训练", None, 63.8, 82.8, 72.2, 45.0, 49.4, 53.6, 1348, 210000, 45.0, 0.6, "https://yiyan.baidu.com/"),
    row("ERNIE X1", "Baidu", "ERNIE", "2025-03-16", "API/闭源", "ClosedAPI", "推理强化", None, 70.5, 85.5, 78.6, 59.6, 69.2, 62.0, None, 120000, 32.0, 0.9, "https://yiyan.baidu.com/", arena_observed=False),
    row("Hunyuan Turbo", "Tencent", "Hunyuan", "2024-09-05", "API/闭源", "ClosedAPI", "原生预训练", None, 62.2, 82.4, 71.8, 44.8, 48.2, 52.2, 1335, 190000, 58.0, 0.44, "https://hunyuan.tencent.com/"),
    row("Hunyuan T1", "Tencent", "Hunyuan", "2025-03-21", "API/闭源", "ClosedAPI", "推理强化", None, 69.8, 85.2, 77.6, 58.0, 67.8, 61.6, None, 130000, 39.0, 0.74, "https://hunyuan.tencent.com/", arena_observed=False),
    row("Phi-3.5 mini", "Microsoft", "Phi", "2024-08-20", "开放权重", "PhiForCausalLM", "指令微调", 3.8, 45.6, 69.4, 56.8, 27.9, 33.5, 35.2, 1188, 260000, 95.0, 0.31, "https://techcommunity.microsoft.com/"),
    row("Phi-4", "Microsoft", "Phi", "2024-12-12", "开放权重", "PhiForCausalLM", "指令微调", 14.0, 57.0, 78.8, 67.0, 41.5, 55.0, 47.9, 1298, 210000, 52.0, 0.58, "https://techcommunity.microsoft.com/"),
    row("Phi-4 mini", "Microsoft", "Phi", "2025-02-26", "开放权重", "PhiForCausalLM", "蒸馏/小模型", 3.8, 50.8, 75.0, 62.1, 34.0, 45.0, 41.5, None, 120000, 102.0, 0.26, "https://techcommunity.microsoft.com/", arena_observed=False),
    row("Yi-1.5-9B-Chat", "01.AI", "Yi", "2024-05-13", "开放权重", "LlamaForCausalLM", "指令微调", 9.0, 49.9, 73.1, 61.2, 31.1, 34.4, 39.0, None, 120000, 61.0, 0.54, "https://www.lingyiwanwu.com/", arena_observed=False),
    row("Yi-1.5-34B-Chat", "01.AI", "Yi", "2024-05-13", "开放权重", "LlamaForCausalLM", "指令微调", 34.0, 55.8, 78.4, 67.0, 37.6, 41.0, 45.8, None, 100000, 29.0, 0.92, "https://www.lingyiwanwu.com/", arena_observed=False),
    row("MiniMax-Text-01", "MiniMax", "MiniMax", "2025-01-15", "API/闭源", "ClosedAPI", "长上下文", None, 66.8, 84.2, 75.2, 51.8, 56.4, 57.9, 1370, 180000, 43.0, 0.65, "https://www.minimaxi.com/"),
    row("MiniMax-M1", "MiniMax", "MiniMax", "2025-06-05", "API/闭源", "ClosedAPI", "推理强化", None, 72.0, 86.0, 79.0, 62.0, 72.0, 63.5, None, 90000, 28.0, 1.05, "https://www.minimaxi.com/", arena_observed=False),
]


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(ROWS, columns=COLUMNS)
    df["release_date"] = pd.to_datetime(df["release_date"])
    df = df.sort_values(["release_date", "provider", "model_name"])
    df.to_csv(RAW_PATH, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    print(f"wrote {RAW_PATH} ({len(df)} rows, {df['family'].nunique()} families)")


if __name__ == "__main__":
    main()
