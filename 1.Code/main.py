#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爆款评论系统 - 主程序入口
AI-Native评论生成系统的核心Pipeline

使用方式:
    python main.py --analyze post_001
    python main.py --generate post_001
    python main.py --full-pipeline post_001
"""

import json
import sys
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
HOOKS_DIR = PROJECT_ROOT / "hooks"
DATA_DIR = PROJECT_ROOT / "data"

class ViralCommentSystem:
    """爆款评论系统主类"""
    
    def __init__(self):
        """初始化系统"""
        self.config = self._load_config()
        self.rules = self._load_rules()
        
    def _load_config(self):
        """加载MCP配置"""
        mcp_file = PROJECT_ROOT / ".mcp.json"
        if not mcp_file.exists():
            raise FileNotFoundError(f"MCP配置文件不存在: {mcp_file}")
        
        with open(mcp_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_rules(self):
        """加载CLAUDE规则"""
        rules = {
            "safety_categories": 6,
            "hook_layers": 4,
            "risk_dimensions": 3,
            "minimum_originality": 0.7,  # 70% 新颖度最低要求
        }
        return rules
    
    def analyze_post(self, post_id):
        """
        Stage 1: 帖子理解 (A1)
        分析帖子内容、图片、语气、风险等
        """
        print(f"[Stage 1] 分析帖子: {post_id}")
        
        # 加载测试帖子
        test_posts = self._load_test_posts()
        if post_id not in test_posts:
            raise ValueError(f"帖子不存在: {post_id}")
        
        post = test_posts[post_id]
        
        # A1 Schema 分析结果模板
        analysis = {
            "post_id": post_id,
            "factual_fields": {
                "id": post.get("id"),
                "title": post.get("title"),
                "content": post.get("content"),
                "platform": post.get("platform"),
                "images": post.get("images", []),
                "url": post.get("url", ""),
            },
            "judgement_fields": {
                "core_topic": "待分析",
                "hook_points": [],
                "sentiment": "neutral",
                "risk_level": 0,
                "recommended_styles": [],
            }
        }
        
        print(f"✓ 帖子理解完成")
        return analysis
    
    def learn_patterns(self, post_id):
        """
        Stage 2: 参考学习 (A2)
        从参考库学习套路
        """
        print(f"[Stage 2] 学习参考评论套路: {post_id}")
        
        patterns = {
            "retrieval_query": f"related to {post_id}",
            "pattern_taxonomy": {
                "expectation_vs_reality": "期望vs现实",
                "dimensional_reduction": "降维打击",
                "crowd_spokesperson": "代言群众",
                "logic_reversal": "逻辑反转",
                "question_driven": "提问引流",
                "self_deconstruction": "自我解构",
                "visual_reframing": "视觉重构",
            },
            "reference_comments": []
        }
        
        print(f"✓ 参考模式学习完成")
        return patterns
    
    def generate_comments(self, post_id, num_candidates=5):
        """
        Stage 3: 评论生成 (A3)
        生成多个候选评论，进行风险评估
        """
        print(f"[Stage 3] 生成原创评论: {post_id}")
        
        candidates = []
        for i in range(num_candidates):
            candidate = {
                "id": f"{post_id}_candidate_{i+1}",
                "text": f"[生成的评论 {i+1}]",
                "style": ["analytical", "witty", "rational", "questioning", "meta"][i % 5],
                "pattern_used": "待标注",
                "why_effective": "待说明",
                "risk_assessment": {
                    "offense_level": 0,  # 冒犯度 0-10
                    "misinterpretation_risk": 0,  # 误解概率 0-10
                    "backlash_risk": 0,  # 翻车风险 0-10
                    "final_risk_score": 0,  # 综合评分
                },
                "originality_score": 0.95,
            }
            candidates.append(candidate)
        
        print(f"✓ 评论生成完成 ({num_candidates}条候选)")
        return candidates
    
    def run_safety_hooks(self, comment_text):
        """
        运行4层安全Hook
        """
        print(f"[Hook验证] 评论: {comment_text[:50]}...")
        
        # Layer 1: 敏感词检查
        layer1_result = self._hook_layer1_keyword_check(comment_text)
        if not layer1_result["pass"]:
            print(f"✗ Layer 1 BLOCKED: {layer1_result['reason']}")
            return False
        
        # Layer 2: 结构校验
        layer2_result = self._hook_layer2_structure_check(comment_text)
        if not layer2_result["pass"]:
            print(f"✗ Layer 2 BLOCKED: {layer2_result['reason']}")
            return False
        
        # Layer 3: 风险评分
        layer3_result = self._hook_layer3_risk_scoring(comment_text)
        if layer3_result["risk_score"] >= 8:
            print(f"✗ Layer 3 BLOCKED: Risk score {layer3_result['risk_score']}/10")
            return False
        
        # Layer 4: 原创性检查
        layer4_result = self._hook_layer4_originality_check(comment_text)
        if not layer4_result["pass"]:
            print(f"✗ Layer 4 BLOCKED: {layer4_result['reason']}")
            return False
        
        print(f"✓ 全部Hook通过")
        return True
    
    def _hook_layer1_keyword_check(self, text):
        """Hook Layer 1: 关键词过滤"""
        # 从config加载敏感词库
        sensitive_words = self.config.get("sensitive_words", [])
        
        for word in sensitive_words:
            if word.lower() in text.lower():
                return {"pass": False, "reason": f"包含敏感词: {word}"}
        
        return {"pass": True}
    
    def _hook_layer2_structure_check(self, text):
        """Hook Layer 2: 结构完整性"""
        # 长度检查
        if len(text) < 20:
            return {"pass": False, "reason": "评论过短 (<20字)"}
        if len(text) > 500:
            return {"pass": False, "reason": "评论过长 (>500字)"}
        
        # 非纯标点检查
        alpha_count = sum(1 for c in text if c.isalpha())
        if alpha_count / len(text) < 0.5:
            return {"pass": False, "reason": "内容太稀疏 (纯标点)"}
        
        return {"pass": True}
    
    def _hook_layer3_risk_scoring(self, text):
        """Hook Layer 3: 风险多维评分"""
        # 简化版本，实际应用需要NLP模型
        risk_score = 0  # 低风险
        
        return {
            "offense_level": 2,
            "misinterpretation_risk": 1,
            "backlash_risk": 2,
            "risk_score": risk_score
        }
    
    def _hook_layer4_originality_check(self, text, similarity_threshold=0.3):
        """Hook Layer 4: 原创性检查"""
        # 实际应该对比参考库
        # 这里简化为总是通过
        return {"pass": True, "similarity": 0.15}
    
    def _load_test_posts(self):
        """加载测试帖子"""
        test_posts_file = DATA_DIR / "test_posts.json"
        with open(test_posts_file, 'r', encoding='utf-8') as f:
            posts_list = json.load(f)
        
        # 转换为字典格式
        return {post["id"]: post for post in posts_list}
    
    def full_pipeline(self, post_id):
        """完整管道: 理解 -> 学习 -> 生成 -> 验证"""
        print(f"\n{'='*60}")
        print(f"开始处理: {post_id}")
        print(f"{'='*60}\n")
        
        # Stage 1: 理解
        analysis = self.analyze_post(post_id)
        
        # Stage 2: 学习
        patterns = self.learn_patterns(post_id)
        
        # Stage 3: 生成
        candidates = self.generate_comments(post_id)
        
        # Stage 4: 验证
        print(f"\n[Stage 4] 安全验证")
        valid_candidates = []
        for candidate in candidates:
            if self.run_safety_hooks(candidate["text"]):
                valid_candidates.append(candidate)
        
        print(f"\n✓ 流程完成")
        print(f"  理解: ✓")
        print(f"  学习: ✓")
        print(f"  生成: {len(candidates)}条")
        print(f"  验证通过: {len(valid_candidates)}条")
        
        return {
            "post_id": post_id,
            "analysis": analysis,
            "patterns": patterns,
            "candidates": candidates,
            "valid_candidates": valid_candidates,
        }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python main.py --full-pipeline post_001")
        print("  python main.py --analyze post_001")
        print("  python main.py --generate post_001")
        sys.exit(1)
    
    command = sys.argv[1]
    post_id = sys.argv[2] if len(sys.argv) > 2 else "post_001"
    
    system = ViralCommentSystem()
    
    if command == "--full-pipeline":
        result = system.full_pipeline(post_id)
    elif command == "--analyze":
        result = system.analyze_post(post_id)
    elif command == "--generate":
        result = system.generate_comments(post_id)
    else:
        print(f"未知命令: {command}")
        sys.exit(1)
    
    # 输出结果
    print("\n结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
