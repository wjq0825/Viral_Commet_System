# 神评论系统核心规则文档 (CLAUDE.md - COMPLETE)

## 项目愿景与核心使命

构建一个 **AI 原生的、风险可控的、高质量产出的"神评论"生成系统**。

通过深度多模态理解、检索增强学习和严格的程序化约束，生成原创的、高互动的、低翻车风险的社交媒体评论。

---

## 核心规则 (Core Rules)

### Rule 1：多模态优先原则

**强制要求**：所有帖子分析必须结合图片内容（如果存在），不可仅依赖文字。

**具体执行**：
- 若帖子包含图片，必须输出 `image_text_synergy` 字段
- 若图片识别失败，必须显性化标注为 `text-only mode`
- 图片内容权重 ≥ 文字内容

### Rule 2：原创性保证

**强制要求**：禁止直接复制参考评论，必须提取模式并重新创作。

**具体执行**：
- 从参考评论提取通用模式（如：期望vs现实）
- 用新的词汇、例子、角度进行组合创作
- 词汇重合率 < 30%

**失败处置**：
- 相似度 > 0.5 → BLOCKED: Plagiarism detected
- 相似度 0.3-0.5 → HIGH_RISK: Review required

---

### Rule 3：安全红线 - 6大绝对禁区

#### Category A：身份攻击（Identity Attacks）
- ❌ 基于种族、民族、肤色的贬低性表述
- ❌ 性别歧视或刻板印象强化
- ❌ 宗教或信仰的冒犯性评论
- ❌ 性取向或性别认同的歧视

#### Category B：人身攻击（Harassment）
- ❌ 直接辱骂或贬低特定个人
- ❌ 强调他人的生理缺陷或私人信息
- ❌ 暗示或明示的人身威胁

#### Category C：暴力或自伤（Violence & Self-Harm）
- ❌ 鼓励或提供伤害自己或他人的方法
- ❌ 美化或浪漫化暴力和自杀
- ❌ 将暴力视为正当的解决方案

#### Category D：隐私泄露（Privacy Violation）
- ❌ 暴露未成年人的信息或图片
- ❌ 泄露个人私密信息（电话、地址）
- ❌ 分享非公开的个人信息

#### Category E：违法内容（Illegal Content）
- ❌ 鼓励或协助非法活动
- ❌ 知识产权侵犯
- ❌ 宣传恐怖主义或极端主义

#### Category F：虚假信息与阴谋论（Misinformation）
- ❌ 故意散布已证实错误的信息
- ❌ 推广没有科学依据的阴谋论
- ❌ 否认公认的历史事实

---

### Rule 4：结构化输出要求

所有中间结果必须符合定义的 JSON Schema。

**Post Analysis 必需字段**：
```json
{
  "id": "帖子ID",
  "factual_fields": {"title": "", "content": "", "platform": "", "images": ""},
  "judgement_fields": {
    "core_topic": "",
    "hook_points": ["≥1项"],
    "risk_profile": {"level": "1-10", "description": ""},
    "comment_strategy": {"suggested_vibe": [], "best_interaction_angle": ""}
  }
}
```

**Comment Generation 必需字段**：
```json
{
  "candidates": [{"text": "", "style": "", "pattern_used": "", "why_effective": "", "risk_evaluation": ""}],
  "best_pick": {"index": "", "reason": ""}
}
```

---

### Rule 5：风险等级多维度评估

**冒犯度等级**：1-2无害，3-4轻微，5-6中等，7-8高，9-10极高→阻断

**原帖误解概率**：1-2清晰，3-4有歧义，5-6易曲解，7-8高曲解，9-10肯定误解

**舆论翻车概率**：1-2极低，3-4低，5-6中等，7-8高，9-10极高

**综合评估**：
```
Final_Risk = (Offense × 0.5) + (Misinterpretation × 0.2) + (Backlash × 0.3)
≥ 8 → BLOCKED，6-8 → FLAGGED，< 6 → PASSED
任一维度 ≥ 9 → 直接 BLOCKED
```

---

## 验证方式 (Validation Methods)

### V1：4层Hook强制校验

[Hook 1] 敏感词拦截 → 触发则BLOCKED
[Hook 2] 结构完整性 → 长度 ≥ 5字符，不符则BLOCKED
[Hook 3] 风险等级 → ≥8则BLOCKED，6-8则FLAGGED
[Hook 4] 原创性 → 相似度 < 30%

### V2：逻辑溯源

每条评论必须标注traceability，说明来源、使用的套路、参考评论、生成理由。

---

## 禁区与限制 (Non-goals & Constraints)

### NG1：高度敏感个人隐私
- 涉及未成年人 + 个人信息 → 直接拒绝
- ✅ 可处理：公开的公众讨论

### NG2：极端政治讨论
- ✅ 可处理：理性分析、多角度讨论
- ❌ 不可处理：极端立场

### NG3：系统能力边界
- 评论需人工审查才可发布
- 所有输出标注"AI Generated"
- 系统不连接任何社交媒体API
- 图片识别失败必须显性标注

---

## 新人接手项目必知 (Onboarding)

### 3件必做
```
□ 1. 完整阅读 CLAUDE.md
□ 2. 理解 DESIGN.md 中的假设和工具编排
□ 3. 跑通 main.py，理解完整数据流
```

### 5件绝对不能做
```
✗ 1. 修改 Hook 的严格程度
✗ 2. 移除"风险评估"步骤
✗ 3. 生成的评论不标注"AI Generated"
✗ 4. 在未经人工审查前自动发布
✗ 5. 对种族/性别/宗教话题掉以轻心
```

---

## 常用命令

```bash
python main.py --analyze <post_id>      # 分析单条帖子
python main.py --generate <post_id>     # 生成评论
python main.py --pipeline <post_id>     # 完整管道
pytest tests/                           # 运行所有测试
pytest tests/test_safety_checker.py     # Hook测试
```

---

## 版本历史

| 版本 | 日期 | 主要更新 |
|---|---|---|
| v2.0 | 2026-05-13 | 完整规则体系、6大风险分类、4层Hook验证、工程化落地 |
