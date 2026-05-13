import json
import unittest
import sys
import os

# 将项目根目录加入 path 以便导入 hooks
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from safety_checker import run_safety_check

class TestSafetyChecker(unittest.TestCase):
    def test_passed_comment(self):
        comment_data = {
            "candidates": [
                {"text": "这是一条非常有意思的评论！", "style": "humor"}
            ]
        }
        result = run_safety_check(json.dumps(comment_data))
        self.assertEqual(result["status"], "PASSED")

    def test_blocked_forbidden_keyword(self):
        comment_data = {
            "candidates": [
                {"text": "这是一条包含歧视的评论", "style": "hate"}
            ]
        }
        result = run_safety_check(json.dumps(comment_data))
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("forbidden keyword", result["reason"])

    def test_blocked_too_short(self):
        comment_data = {
            "candidates": [
                {"text": "!", "style": "short"}
            ]
        }
        result = run_safety_check(json.dumps(comment_data))
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("too short", result["reason"])

    def test_invalid_json(self):
        result = run_safety_check("invalid json")
        self.assertEqual(result["status"], "ERROR")

if __name__ == "__main__":
    unittest.main()
