# Skill: Post Analyzer (Bilingual & Multimodal)

## Description
对社交媒体帖子进行深度多模态理解，提取核心事实并进行跨语言、跨文化的逻辑判断。

## Trigger
当输入新的帖子内容（文本和/或图片）时触发。

## Inputs
- `post_text`: 帖子正文（支持中英文）
- `post_images`: 图片描述或视觉分析结果
- `platform`: 来源平台上下文 (Reddit, X, Weibo, Zhihu, Xiaohongshu, HN, 9GAG)

## Steps
1. **视觉分析**：识别图片中的关键物体、文字、人物表情、环境氛围，特别关注视觉笑点 (Visual Hooks)。
2. **语言识别与意图提取**：
    - 识别语言（中/英）。
    - 识别平台特有口语（如：小红书的"家人们谁懂啊"、Reddit 的 "ELI5"、Zhihu 的 "谢邀"）。
3. **文化语境分析**：
    - 识别特定文化的梗（如：中文的"粘土滤镜"、"空巢老人"；英文的"American Dream"、"Shrinkflation"）。
    - 寻找图文之间的"张力"或"反差"。
4. **风险预判**：识别跨语言的政治、种族、宗教、暴力等敏感点。
5. **结构化输出**：按照 `DESIGN.md` 中的 Schema 生成 JSON。

## Output Template
```json
{
  "id": "{{post_id}}",
  "language": "zh/en",
  "topic": "...",
  "cultural_context": "分析该帖子背后的文化背景或流行趋势",
  "hook_points": ["...", "..."],
  "risk_profile": {
    "level": 0-10,
    "description": "..."
  },
  "suggested_vibe": "讽刺/共情/专业/脑洞..."
}
```

## Failure Handling
- 若图片读取失败，记录错误并降级为 `Text-Only` 模式。
- 若内容违反安全策略，直接中断流程并返回 `BLOCKED` 状态。
