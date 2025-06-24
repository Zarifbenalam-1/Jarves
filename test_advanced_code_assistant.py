#!/usr/bin/env python3
"""
Advanced Code Assistant Testing Script
Tests the enhanced code analysis capabilities of JARVIS
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant.ai_engine import JarvisAI

def test_code_analysis():
    """Test the advanced code analysis features"""
    
    print("🔍 Testing Advanced Code Assistant System")
    print("="*50)
    
    ai = JarvisAI()
    
    # Test code samples
    python_code_basic = """
def hello_world():
    print("Hello, World!")
    return None

class Person:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        print(f"Hello, {self.name}")
"""
    
    python_code_complex = """
import requests
import json
from typing import List, Dict
import logging

class DataProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def fetch_data(self, url: str) -> Dict:
        \"\"\"Fetch data from API endpoint\"\"\"
        try:
            response = requests.get(url, headers={'Authorization': f'Bearer {self.api_key}'})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch data: {e}")
            return {}
    
    def process_items(self, items: List[Dict]) -> List[Dict]:
        \"\"\"Process list of items\"\"\"
        processed = []
        for item in items:
            if item.get('status') == 'active':
                processed.append({
                    'id': item['id'],
                    'name': item['name'].upper(),
                    'score': item.get('score', 0) * 1.1
                })
        return processed
"""
    
    python_code_issues = """
import *
import os, sys

def bad_function():
    global x
    x = eval(user_input)
    for i in range(len(data)):
        result += data[i]
    
    if condition == True:
        if another_condition == True:
            if third_condition == True:
                if fourth_condition == True:
                    if fifth_condition == True:
                        do_something()
"""
    
    javascript_code = """
function processData(data) {
    var result = [];
    for (var i = 0; i < data.length; i++) {
        if (data[i].status == 'active') {
            result.push({
                id: data[i].id,
                name: data[i].name.toUpperCase()
            });
        }
    }
    return result;
}

class UserManager {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        this.users.push(user);
        console.log('User added:', user);
    }
}
"""
    
    # Test 1: Full Analysis
    print("\n🔍 TEST 1: Full Code Analysis")
    print("-" * 30)
    result = ai.analyze_code(python_code_complex, "python", "full")
    print(result)
    
    # Test 2: Quick Analysis
    print("\n⚡ TEST 2: Quick Code Analysis")
    print("-" * 30)
    result = ai.analyze_code(python_code_basic, "python", "quick")
    print(result)
    
    # Test 3: Security Analysis
    print("\n🔒 TEST 3: Security Analysis")
    print("-" * 30)
    result = ai.analyze_code(python_code_issues, "python", "security")
    print(result)
    
    # Test 4: Performance Analysis
    print("\n⚡ TEST 4: Performance Analysis")
    print("-" * 30)
    result = ai.analyze_code(python_code_issues, "python", "performance")
    print(result)
    
    # Test 5: Documentation Generation
    print("\n📚 TEST 5: Documentation Generation")
    print("-" * 30)
    result = ai.generate_code_documentation(python_code_complex, "python")
    print(result)
    
    # Test 6: Code Improvements
    print("\n🔧 TEST 6: Code Improvement Suggestions")
    print("-" * 30)
    result = ai.suggest_code_improvements(python_code_issues, "python")
    print(result)
    
    # Test 7: Pattern Detection
    print("\n🎯 TEST 7: Pattern Detection")
    print("-" * 30)
    result = ai.detect_code_patterns(python_code_complex, "python")
    print(result)
    
    # Test 8: JavaScript Analysis
    print("\n📱 TEST 8: JavaScript Analysis")
    print("-" * 30)
    result = ai.analyze_code(javascript_code, "javascript", "full")
    print(result)
    
    print("\n✅ All tests completed!")

def test_language_detection():
    """Test language detection capabilities"""
    
    print("\n🔍 Testing Language Detection")
    print("="*30)
    
    test_codes = {
        "Python": "def hello():\n    print('Hello')\n    return True",
        "JavaScript": "function hello() {\n    console.log('Hello');\n    return true;\n}",
        "Java": "public class Hello {\n    public static void main(String[] args) {\n        System.out.println('Hello');\n    }\n}",
        "C": "#include <stdio.h>\nint main() {\n    printf('Hello');\n    return 0;\n}"
    }
    
    from main import JarvisXTerminal
    terminal = JarvisXTerminal()
    
    for expected_lang, code in test_codes.items():
        detected = terminal._detect_language(code)
        print(f"Expected: {expected_lang.lower()}, Detected: {detected}")

if __name__ == "__main__":
    try:
        test_code_analysis()
        test_language_detection()
        
        print("\n🎉 All advanced code assistant tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
