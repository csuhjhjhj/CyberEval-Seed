# CyberEval Showcase

CyberEval Showcase 是 CyberEval 网络安全大模型通用测评集的方法展示网页，集中呈现调研结论、测评集构建流程、SEU 统一数据结构、样例覆盖、内容边界与脱敏策略、CyberEval-Seed 预研项目和实施路线。

## 本地运行

```bash
python app.py
```

默认地址：

```text
http://127.0.0.1:8060/
```

## 静态部署

`static/` 目录可以直接由 Nginx 等 Web 服务托管。静态部署时建议将 `CyberEval-Seed/data/project_summary.json` 汇总为 `static/data/summary.json`，页面会优先读取 `/api/summary`，不可用时读取 `/data/summary.json`。
