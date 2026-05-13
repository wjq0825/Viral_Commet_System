# Skill: Comment Generator

## Description
结合帖子理解与学习到的模式，生成原创的神评论。

## Trigger
当完成帖子分析与模式提取后触发。

## Inputs
- `post_analysis`: `Post Analyzer` 的输出。
- `extracted_patterns`: `Pattern Extractor` 的输出。

## Steps
1. **多风格创作**：针对每个 `hook_point`，尝试应用不同的 `extracted_patterns`。
2. **原创性校验**：检查生成内容与参考评论的相似度，确保不是抄袭。
3. **互动预测**：为每条评论标注预期的互动效果（如：引发争论、博君一一笑）。
4. **风险自测**：进行初步的冒犯度评估。

## Output Template
```json
{
  "candidates": [
    {
      "text": "...",
      "style": "...",
      "pattern_used": "...",
      "why_effective": "...",
      "risk_evaluation": "..."
    }
  ],
  "best_pick": "..."
}
```
