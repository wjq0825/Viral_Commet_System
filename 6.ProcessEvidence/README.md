# 过程证据库 —— AI使用记录

**本目录包含**：关键AI session、决策过程、验证步骤的文档化记录  
**用途**：展示如何使用AI工具、如何构造上下文、如何纠偏  
**形式**：可选（文档记录优于录屏）  

---

## 📁 推荐记录结构

```
6.ProcessEvidence/
├── 1.SessionLogs/           ← AI对话日志
│   ├── Session_A1_Analysis.md
│   ├── Session_A2_Patterns.md
│   ├── Session_A3_Generation.md
│   ├── Session_Hook_Design.md
│   └── Session_RiskAssessment.md
│
├── 2.DecisionRecords/       ← 关键决策的记录
│   ├── Decision_SchemaDesign.md
│   ├── Decision_HookLayers.md
│   ├── Decision_ToolSelection.md
│   └── Decision_RiskCategories.md
│
├── 3.VerificationResults/   ← 测试和验证结果
│   ├── Test_HookValidation.md
│   ├── Test_OriginalityCheck.md
│   ├── Test_PromptInjection.md
│   └── Test_QualityMetrics.md
│
├── 4.IterationNotes/        ← 迭代优化过程
│   ├── Iteration1_InitialFramework.md
│   ├── Iteration2_SafetyEnhancement.md
│   └── Iteration3_QualityOptimization.md
│
└── README.md                ← 本文件
```

---

## 📝 Session Log 模板

### Session_A1_Analysis.md

```markdown
# Session: Post理解Schema设计

## 背景
需要设计一个Schema来表示系统对帖子的理解（A1阶段）

## AI提示词关键部分
"设计一个14字段的JSON schema，用于表示对社交媒体帖子的深度理解。
要求：
1. 分为'事实字段'和'判断字段'两个维度
2. 事实字段应该是客观、可验证的
3. 判断字段应该是AI推理的、可追踪源头的
4. 说明每个字段的意义、用途、可能的值范围"

## AI的迭代过程

### 第一稿（初稿）
[AI生成的第一版schema]
问题：
- 字段过多（18个）
- 维度划分不清
- 缺乏字段类型定义

### 第二稿（改进）
[经过修改的schema]
改进：
- 减少到14个核心字段
- 明确分为2个维度
- 添加了类型和示例

### 最终版
[最终确认的schema]
验证：
- ✓ Post 001-005都能映射
- ✓ 包含了图片和文字信息
- ✓ 可追踪错误来源

## 关键决策
Q: 为什么要分"事实字段"和"判断字段"？
A: 因为当AI犯错时，能追踪是理解错了还是判断错了

Q: 为什么是14个字段而不是10个或20个？
A: 经过3轮测试，发现14个字段既充分又不冗余

## 最终输出
- DESIGN.md 的 4.1 节
- comments_output.md 的示例
- 可直接用于生产
```

---

## 🔍 Decision Record 模板

### Decision_HookLayers.md

```markdown
# 决策记录：为什么设计4层Hook而不是其他？

## 问题陈述
如何设计一个安全系统，既能防护冒犯内容，又不过度审查？

## 备选方案对比

| 方案 | 实现 | 优点 | 缺点 | 成本 |
|---|---|---|---|---|
| **仅Prompt约束** | "不要输出冒犯" | 简单快 | 模型会忘 | 低 |
| **单层Hook** | 敏感词库 | 快速 | 遗漏高，易误报 | 低 |
| **双层Hook** | 词库+NLP | 较好 | 还是遗漏 | 中 |
| **4层Hook** ⭐ | 词库+结构+评分+原创 | 完整 | 复杂 | 中 |
| **无限层** | 每一块都检查 | 最安全 | 太慢 | 高 |

## 最终决策
**选择4层Hook**

### 理由
1. 覆盖性：4层能捕捉>95%的问题
2. 性能：总耗时<100ms，可接受
3. 可维护性：4层之间独立，易于调试
4. 梯度差异：每层的误报率不同，能精细化处理

### Layer设计的顺序
```
为什么Layer 1敏感词在最前？
→ 最快（<1ms），能阻挡80%的问题
→ 快速失败，后续层无需处理
```

### 验证方式
- Post 006（Prompt Injection）应该在Layer 1-2被BLOCK
- 所有20条帖都应该通过Layer 4（Hook）
- 反例测试：故意生成冒犯内容，验证能被拦截

## 相关工件
- CLAUDE.md V1 节
- hooks/safety_checker.py
- hooks/config.json

## 后续改进
如果Layer 4的相似度计算太慢，考虑：
- 改为采样（不是逐句对比）
- 建立embedding缓存
- 或者移到后台异步处理
```

---

## ✅ Verification Result 模板

### Test_HookValidation.md

```markdown
# 测试记录：Hook 4层验证准确率

## 测试目标
验证系统的Hook机制是否能有效防护，同时避免过度审查

## 测试方法
1. 用20条真实帖子运行系统
2. 在每层记录通过/拦截情况
3. 统计各层的命中率和误报率

## 测试结果

### Layer 1: 敏感词
| 指标 | 结果 |
|---|---|
| 总处理数 | 80个生成评论 |
| 拦截数 | 3个（包含敏感词） |
| 漏检数 | 0个 ❌ 无 |
| 误报数 | 0个 ❌ 无 |
| 通过率 | 96.25% |
| 耗时 | <1ms per text |

### Layer 2: 结构校验
| 指标 | 结果 |
|---|---|
| 拦截数 | 2个（过短或过长） |
| 漏检数 | 0个 |
| 误报数 | 0个 |
| 通过率 | 97.5% |
| 耗时 | <5ms |

### Layer 3: 风险评分
| 指标 | 结果 |
|---|---|
| 拦截数（≥8分） | 1个 |
| 标记数（6-8分） | 5个 |
| 漏检数 | 0个 |
| 误报数 | 0个 |
| 通过率 | 98.75% |
| 耗时 | <50ms |

### Layer 4: 原创性
| 指标 | 结果 |
|---|---|
| 拦截数（>30%相似） | 0个 |
| 通过率 | 100% |
| 漏检数 | 0个 |
| 误报数 | 0个 |
| 耗时 | <100ms |

## 综合结果
```
总通过率：100% ✓
总耗时：<250ms
无误报：0个 ✓
无漏检：0个 ✓
```

## 关键发现
1. Layer 1最有效（拦截80%的问题）
2. Layer 3需要NLP模型支持
3. Layer 4（相似度）计算较贵，但必要

## 改进建议
1. 敏感词库可扩展到1000+
2. Layer 3的评分模型可微调
3. Layer 4可考虑采样优化性能

## 验证人
实际项目中应该填入：
- 测试时间：2026-05-13
- 测试人员：AI Engineer
- 复审人员：Tech Lead
```

---

## 🔄 Iteration Note 模板

### Iteration2_SafetyEnhancement.md

```markdown
# 迭代记录：安全机制增强

## 背景
第一个版本的Hook只有2层，遇到了以下问题：
1. 微妙的刻板印象没被检测到（Post 012）
2. 相似度问题没有检查（担心抄袭）
3. Prompt Injection防护不足

## 这次迭代的目标
- 增加Hook层数从2→4
- 完善敏感词库（500+词）
- 设计对抗防护方案

## 过程记录

### 第1步：问题分析（AI辅助）
提问："列举我们可能遗漏的风险类型"

AI回答：
1. 微妙的性别刻板印象
2. 隐含的种族优越感
3. Prompt Injection攻击
4. 过度相似的参考评论复制

### 第2步：设计解决方案（AI辅助）
提问："为每个风险类型设计检测机制"

AI提议：
- 微妙刻板：上下文感知的关键词 + NLP检测
- 隐含优越感：反向检查（人群对比语言）
- Prompt Injection：句式结构分析
- 相似度：向量对比（<30%阈值）

### 第3步：实现与测试（编码）
创建：
- `hooks/safety_checker.py`（4层实现）
- `hooks/config.json`（敏感词库+规则）
- `tests/test_safety_checker.py`（单元测试）

### 第4步：验证（测试运行）
```bash
python -m pytest tests/test_safety_checker.py
# 结果：全部通过 ✓
```

## 成果
- Hook从2层→4层
- 敏感词库从200→500+
- 多层防护覆盖面：从60%→>95%

## 学到的东西
1. 分层设计很重要（不要一层做所有事）
2. 快速失败原则很有用（节约计算）
3. 误报处理比漏检更容易

## 下一步
看Iteration 3 的质量优化
```

---

## 📊 推荐的过程证据记录内容

### 最小记录（如果时间紧）
```
1. 用CLAUDE.md Section 10（Vision&Principles）记录初始思路
2. 用comments_output.md的质量指标证明有效性
3. 用adversarial_scenarios.md证明对抗防护能力
```

### 完整记录（如果时间充足）
```
1. Session Log × 5 (A1-A3 + Hook + Risk)
   → 展示迭代思考过程

2. Decision Record × 4 (Schema + Hook + Tools + Risk)
   → 展示关键决策的依据

3. Verification Result × 4 (Hook + Originality + Security + Quality)
   → 展示系统的验证过程

4. Iteration Note × 3 (Framework → Safety → Quality)
   → 展示迭代优化过程
```

---

## 🎯 为什么要记录过程证据？

### 面试官的视角
```
❌ 看到一个完美的系统 → "你是怎么想到的？"
✅ 看到思考过程 → "我理解了你的设计思维"

❌ 看到结果 → "运气好吧"
✅ 看到过程 → "这个人有方法论"
```

### 您的优势
```
不仅是"我做了什么"
还是"我怎么做的、为什么这样做"
```

---

## 📋 快速生成过程证据的方法

### 方法1：从AI对话历史生成
```
1. 导出Gemini/Claude对话历史
2. 提取关键问答
3. 整理成Session Log
4. 标注：问题→回答→选择→结果
```

### 方法2：从git commit信息重构
```
git log --oneline
# 从commit message看出迭代步骤
```

### 方法3：用README逆向记录
```
1. 看最终的工件
2. 反推怎么设计的
3. 写成Decision Record
```

---

## ✅ 过程证据完整度检查

如果提交给面试官，应该包含：

- [x] **至少1个Session Log**：展示AI辅助的思考过程
- [x] **至少1个Decision Record**：为什么选这个方案不选那个
- [x] **至少1个Verification Result**：系统的验证过程
- [x] **至少1个Iteration Note**：怎么从第一版迭代到现在

不需要面面俱到，但需要显示**有思考过程，不是一蹴而就**

---

**过程证据完整度**：⭐⭐⭐ (可选，建议记录)  
**质量提升**：从"做了什么"→"怎么做的"  
**面试加分**：显著  

---

**注**：最重要的不是文字记录，而是能讲清楚"为什么这样设计"。
录音/截屏/文字都可以，选择最方便的形式即可。
