# CyberEval-Seed

CyberEval-Seed 是 CyberEval 网络安全大模型通用测评集的种子项目，用于展示 CyberEval 正式测评集的核心设计、数据结构、样例组织和轻量评测流程。

本项目聚焦三个问题：

- SEU（Security Evaluation Unit）统一数据结构能否承载选择题、填空题、简答题和动态交互任务。
- 网络安全知识领域能否形成可扩展覆盖矩阵，支撑不少于 1000 条正式样本建设。
- 轻量评测脚本能否实现数据校验、覆盖统计和静态题型自动评分。

## 项目定位

CyberEval-Seed 是 CyberEval 网络安全大模型通用测评集的种子项目，展示从领域调研、数据结构设计、样例组织、覆盖矩阵、评测脚本到可视化说明的完整方法链路。后续可在该基础上扩展为正式的网络安全大模型测评数据集与评测框架。

## 项目结构

```text
CyberEval-Seed/
├── data/
│   ├── seu_schema.json          # SEU 统一数据结构草案
│   ├── seed_samples.jsonl       # 预研种子样例
│   ├── coverage_matrix.csv      # 领域/认知层级覆盖矩阵
│   └── project_summary.json     # 项目摘要，供展示网页读取
├── docs/
│   ├── prestudy_plan.md         # 预研计划
│   ├── annotation_guide.md      # 标注与质量控制规范
│   └── security_policy.md       # 内容边界与脱敏策略
├── scripts/
│   ├── evaluate_seed.py         # 覆盖统计与轻量评分
│   └── validate_dataset.py      # Schema 与字段完整性校验
└── showcase/
    ├── app.py                   # 方法展示网页后端
    └── static/                  # 可静态部署的网页资源
```

## 核心设计

SEU 五元组：

```text
SEU = (Q, O, A, M, E)
```

- Q, Question：题目内容，包括题干、题型、答题要求。
- O, Options：选项集合，选择题使用，填空题、简答题和动态任务可为空。
- A, Answer：标准答案、解析和评分规则。
- M, Metadata：领域、知识点、难度、认知层级、内容边界和来源说明。
- E, Evaluation：评测指标、评分方式和模型作答记录。

## 覆盖范围

- 漏洞分析：CVE、CWE、CVSS、漏洞影响评估和修复建议。
- 密码学：对称/非对称加密、哈希、数字签名、密钥管理。
- 网络协议安全：TCP/IP、HTTP、DNS、TLS 和常见协议风险。
- Web 安全：OWASP Top 10、SQL 注入、XSS、CSRF、认证授权。
- 恶意代码分析：病毒、蠕虫、木马、勒索软件和沙箱分析基础。
- 安全合规与治理：等保 2.0、ISO 27001、GDPR、安全审计和应急响应。

## 快速运行

```bash
python scripts/validate_dataset.py
python scripts/evaluate_seed.py
```

## 输出示例

```text
samples=4
domains={'漏洞分析': 1, '密码学': 1, 'Web安全': 1, '威胁情报与攻击链': 1}
cognitive_levels={'C1': 1, 'C2': 1, 'C3': 1, 'C4': 1}
scorable_static_samples=2
```

## 后续扩展

- 扩展至不少于 1000 条结构化样本。
- 接入 lm-eval-harness 和 OpenCompass。
- 增加动态交互沙箱任务。
- 建设模型能力画像和评测报告生成模块。
- 建设面向展示和复现的项目网页，集中说明方法链路、样例结构和扩展路线。
