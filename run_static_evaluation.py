#!/usr/bin/env python3
"""
Static Evaluation Runner for CI/CD Pipeline
Runs the static evaluation suite and saves results to JSON
Compatible with Session 29 notebook implementation
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import evaluation components (matching Cell 5 from notebook)
try:
    from openai import OpenAI
    from sentence_transformers import SentenceTransformer
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Install dependencies: pip install openai sentence-transformers python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# ============================================================================
# Static Evaluator (from Cell 5 of notebook)
# ============================================================================

class StaticEvaluator:
    """
    Static evaluation framework for LLM outputs
    Matches the implementation from Session 29 notebook Cell 5
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize evaluator with OpenAI client and embedding model"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment")
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        embeddings = self.embedding_model.encode([text1, text2])
        similarity = embeddings[0] @ embeddings[1].T
        norm = (embeddings[0] @ embeddings[0].T) ** 0.5 * (embeddings[1] @ embeddings[1].T) ** 0.5
        return float(similarity / norm)
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate LLM response for given prompt"""
        messages = []
        
        if context:
            messages.append({
                "role": "system",
                "content": context
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def validate_rules(self, response: str, rules: List[Dict]) -> List[Dict]:
        """Validate response against predefined rules"""
        results = []
        
        for rule in rules:
            rule_type = rule['type']
            passed = False
            
            if rule_type == 'contains':
                # Check if response contains required keywords
                keywords = rule.get('keywords', [])
                passed = any(kw.lower() in response.lower() for kw in keywords)
            
            elif rule_type == 'not_contains':
                # Check that response doesn't contain forbidden keywords
                keywords = rule.get('keywords', [])
                passed = not any(kw.lower() in response.lower() for kw in keywords)
            
            elif rule_type == 'length':
                # Check response length
                min_len = rule.get('min', 0)
                max_len = rule.get('max', float('inf'))
                passed = min_len <= len(response) <= max_len
            
            elif rule_type == 'format':
                # Check response format (e.g., contains numbers, currency)
                format_type = rule.get('format')
                if format_type == 'currency':
                    passed = '$' in response or 'dollars' in response.lower()
                elif format_type == 'number':
                    passed = any(char.isdigit() for char in response)
            
            results.append({
                'rule': rule.get('description', rule_type),
                'passed': passed
            })
        
        return results
    
    def evaluate_single(self, test_case: Dict) -> Dict:
        """Evaluate a single test case"""
        # Extract test case components
        test_id = test_case.get('test_id', 'unknown')
        input_text = test_case.get('input', '')
        expected = test_case.get('expected', '')
        context = test_case.get('context', '')
        rules = test_case.get('rules', [])
        
        # Generate response
        generated = self.generate_response(input_text, context)
        
        # Calculate semantic similarity
        similarity = self.semantic_similarity(generated, expected)
        
        # Validate rules
        rule_results = self.validate_rules(generated, rules) if rules else []
        all_rules_passed = all(r['passed'] for r in rule_results) if rule_results else True
        
        # Determine if test passed (similarity threshold: 0.85)
        similarity_passed = similarity >= 0.85
        passed = similarity_passed and all_rules_passed
        
        return {
            'test_id': test_id,
            'input': input_text,
            'expected': expected,
            'generated': generated,
            'passed': passed,
            'metrics': {
                'semantic_similarity': similarity,
                'similarity_threshold': 0.85,
                'similarity_passed': similarity_passed
            },
            'rule_validation': rule_results
        }
    
    def evaluate_all(self, test_cases: List[Dict]) -> Dict:
        """Evaluate all test cases and return aggregated results"""
        results = []
        passed_count = 0
        
        print(f"\n🔬 Running Static Evaluation on {len(test_cases)} test cases...")
        print("="*80)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}/{len(test_cases)}: {test_case.get('test_id', 'unknown')}")
            result = self.evaluate_single(test_case)
            results.append(result)
            
            if result['passed']:
                passed_count += 1
                print(f"   ✅ PASSED (similarity: {result['metrics']['semantic_similarity']:.3f})")
            else:
                print(f"   ❌ FAILED (similarity: {result['metrics']['semantic_similarity']:.3f})")
        
        # Calculate overall metrics
        pass_rate = (passed_count / len(test_cases)) * 100 if test_cases else 0
        
        print("\n" + "="*80)
        print(f"📊 Evaluation Complete")
        print(f"   Pass Rate: {pass_rate:.1f}%")
        print(f"   Passed: {passed_count}/{len(test_cases)}")
        print(f"   Failed: {len(test_cases) - passed_count}/{len(test_cases)}")
        print("="*80)
        
        return {
            'pass_rate': pass_rate,
            'passed': passed_count,
            'failed': len(test_cases) - passed_count,
            'total_tests': len(test_cases),
            'results': results,
            'model_used': self.model,
            'timestamp': datetime.now().isoformat(),
            'evaluation_type': 'static'
        }


# ============================================================================
# Test Cases (matching Cell 4 from notebook)
# ============================================================================

STATIC_TEST_CASES = [
    {
        'test_id': 'test_001',
        'category': 'account_balance',
        'input': 'What is my current account balance?',
        'expected': 'Your current account balance is $5,423.67',
        'context': 'You are a helpful banking assistant.',
        'rules': [
            {'type': 'contains', 'keywords': ['balance', '$5,423.67'], 'description': 'Contains balance amount'},
            {'type': 'format', 'format': 'currency', 'description': 'Includes currency format'}
        ]
    },
    {
        'test_id': 'test_002',
        'category': 'transactions',
        'input': 'Show my last 3 transactions',
        'expected': 'Your last 3 transactions are: 1) Grocery Store - $45.20, 2) Gas Station - $38.50, 3) Restaurant - $62.30',
        'context': 'You are a helpful banking assistant.',
        'rules': [
            {'type': 'contains', 'keywords': ['transactions', 'Grocery', 'Gas', 'Restaurant'], 'description': 'Lists all transactions'}
        ]
    },
    {
        'test_id': 'test_003',
        'category': 'fraud_detection',
        'input': 'I see a suspicious charge from an unknown merchant',
        'expected': 'I will immediately freeze your card and investigate this suspicious charge. You will not be liable for fraudulent transactions.',
        'context': 'You are a helpful banking assistant focused on security.',
        'rules': [
            {'type': 'contains', 'keywords': ['freeze', 'investigate', 'suspicious'], 'description': 'Takes security action'},
            {'type': 'not_contains', 'keywords': ['ignore', 'normal'], 'description': 'Does not dismiss concern'}
        ]
    },
    {
        'test_id': 'test_004',
        'category': 'policy_question',
        'input': 'Can I withdraw more than $10,000 in cash?',
        'expected': 'For withdrawals over $10,000, you need to provide 24 hours advance notice to your branch.',
        'context': 'You are a helpful banking assistant.',
        'rules': [
            {'type': 'contains', 'keywords': ['$10,000', 'advance notice'], 'description': 'Mentions policy requirements'}
        ]
    },
    {
        'test_id': 'test_005',
        'category': 'transfer',
        'input': 'Transfer $500 to my savings account',
        'expected': 'I have transferred $500 from your checking account to your savings account. Your new checking balance is $4,923.67.',
        'context': 'You are a helpful banking assistant.',
        'rules': [
            {'type': 'contains', 'keywords': ['transferred', '$500', 'savings'], 'description': 'Confirms transfer'},
            {'type': 'format', 'format': 'currency', 'description': 'Shows updated balance'}
        ]
    }
]


# ============================================================================
# Main Function
# ============================================================================

def load_test_cases(filepath: str = None) -> List[Dict]:
    """Load test cases from file or use defaults"""
    if filepath and Path(filepath).exists():
        print(f"📂 Loading test cases from: {filepath}")
        with open(filepath, 'r') as f:
            return json.load(f)
    else:
        print("📋 Using default test cases")
        return STATIC_TEST_CASES


def save_results(results: Dict, output_file: str):
    """Save evaluation results to JSON file"""
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")


def main():
    """Main evaluation runner"""
    parser = argparse.ArgumentParser(description='Run static LLM evaluation')
    parser.add_argument(
        '--output',
        type=str,
        default='evaluation_outputs/static/results.json',
        help='Output file for results (default: evaluation_outputs/static/results.json)'
    )
    parser.add_argument(
        '--test-cases',
        type=str,
        default=None,
        help='JSON file containing test cases (optional)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4o-mini',
        help='OpenAI model to use (default: gpt-4o-mini)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("🔬 STATIC EVALUATION RUNNER")
    print("="*80)
    print(f"Model: {args.model}")
    print(f"Output: {args.output}")
    print("="*80)
    
    try:
        # Load test cases
        test_cases = load_test_cases(args.test_cases)
        print(f"Loaded {len(test_cases)} test cases")
        
        # Initialize evaluator
        evaluator = StaticEvaluator(model=args.model)
        
        # Run evaluation
        results = evaluator.evaluate_all(test_cases)
        
        # Save results
        save_results(results, args.output)
        
        # Print summary
        print("\n" + "="*80)
        print("✅ EVALUATION COMPLETE")
        print("="*80)
        print(f"Pass Rate: {results['pass_rate']:.1f}%")
        print(f"Passed: {results['passed']}/{results['total_tests']}")
        print(f"Failed: {results['failed']}/{results['total_tests']}")
        print(f"Results: {args.output}")
        
        # Exit code based on pass rate
        if results['pass_rate'] < 95:
            print("\n⚠️  Pass rate below 95% threshold")
            sys.exit(1)  # Fail CI/CD if quality gates not met
        else:
            print("\n✅ Quality gates passed!")
            sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Evaluation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()