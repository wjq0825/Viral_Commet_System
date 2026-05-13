import json
import sys
import re

# 敏感词库 (Bilingual)
FORBIDDEN_KEYWORDS = [
    # English
    r"discrimination", r"violence", r"self-harm", r"drugs", r"pornography", 
    r"racial", r"hate speech", r"terrorist", r"API key",
    # Chinese
    r"歧视", r"暴力", r"自残", r"毒品", r"色情", r"恐怖主义", r"仇恨言论", r"赌博"
]

def run_safety_check(comment_json):
    """
    程序化强制校验：
    1. 敏感词拦截
    2. 结构完整性校验
    """
    try:
        data = json.loads(comment_json)
        candidates = data.get("candidates", [])
        
        for idx, cand in enumerate(candidates):
            text = cand.get("text", "")
            
            # 1. 敏感词正则匹配
            for pattern in FORBIDDEN_KEYWORDS:
                if re.search(pattern, text, re.IGNORECASE):
                    return {
                        "status": "BLOCKED",
                        "reason": f"Candidate {idx} contains forbidden keyword: {pattern}",
                        "item": text
                    }
            
            # 2. 最小长度校验 (防止 AI 敷衍)
            if len(text) < 2:
                return {
                    "status": "BLOCKED",
                    "reason": f"Candidate {idx} is too short.",
                    "item": text
                }

        return {"status": "PASSED"}
        
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}

if __name__ == "__main__":
    # 模拟从 stdin 读取生成的 JSON
    input_str = sys.stdin.read()
    result = run_safety_check(input_str)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["status"] != "PASSED":
        sys.exit(1)
