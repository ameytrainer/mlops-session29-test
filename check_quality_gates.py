#!/usr/bin/env python3
"""
Quality Gate Checker for CI/CD Pipeline
Validates evaluation results against quality thresholds
Compatible with Session 29 notebook implementation
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass

# ============================================================================
# Quality Configuration
# ============================================================================

@dataclass
class QualityConfig:
    """Quality gate configuration"""
    min_pass_rate: float = 95.0
    min_semantic_similarity: float = 0.85
    max_hallucination_rate: float = 0.02
    critical_categories: List[str] = None
    
    def __post_init__(self):
        if self.critical_categories is None:
            self.critical_categories = ['fraud_detection', 'security']


# ============================================================================
# Quality Gate Checker
# ============================================================================

class QualityGateChecker:
    """Check if evaluation results meet quality gates"""
    
    def __init__(self, config: QualityConfig = None):
        self.config = config or QualityConfig()
        self.failed = []
        self.warnings = []
        self.passed_checks = []
    
    def check_pass_rate(self, results: Dict) -> bool:
        """Check overall pass rate"""
        if 'pass_rate' in results:
            pass_rate = results['pass_rate']
        elif 'passed' in results and 'total_tests' in results:
            pass_rate = (results['passed'] / results['total_tests']) * 100
        else:
            self.failed.append("Cannot calculate pass rate - missing data")
            return False
        
        threshold = self.config.min_pass_rate
        
        if pass_rate >= threshold:
            self.passed_checks.append(f"Pass rate: {pass_rate:.1f}% >= {threshold}%")
            return True
        else:
            self.failed.append(
                f"Pass rate {pass_rate:.1f}% below threshold {threshold}%"
            )
            return False
    
    def check_critical_tests(self, results: Dict) -> bool:
        """Check that all critical tests passed"""
        test_results = results.get('results', [])
        if not test_results:
            self.warnings.append("No detailed results for critical test check")
            return True
        
        critical_categories = self.config.critical_categories
        all_critical_passed = True
        critical_count = 0
        
        for result in test_results:
            category = result.get('category', 'unknown')
            
            if category in critical_categories:
                critical_count += 1
                passed = result.get('passed', result.get('correct', False))
                
                if not passed:
                    test_id = result.get('test_id', 'unknown')
                    self.failed.append(
                        f"Critical test failed: {test_id} (category: {category})"
                    )
                    all_critical_passed = False
        
        if critical_count > 0:
            if all_critical_passed:
                self.passed_checks.append(f"All {critical_count} critical tests passed")
        else:
            self.warnings.append("No critical tests found")
        
        return all_critical_passed
    
    def check_semantic_similarity(self, results: Dict) -> bool:
        """Check average semantic similarity"""
        test_results = results.get('results', [])
        if not test_results:
            self.warnings.append("No detailed results for similarity check")
            return True
        
        similarities = []
        for result in test_results:
            if 'metrics' in result and 'semantic_similarity' in result['metrics']:
                sim = result['metrics']['semantic_similarity']
                similarities.append(sim)
            elif 'semantic_similarity' in result:
                sim = result['semantic_similarity']
                similarities.append(sim)
        
        if not similarities:
            self.warnings.append("No similarity scores found")
            return True
        
        avg_similarity = sum(similarities) / len(similarities)
        threshold = self.config.min_semantic_similarity
        
        if avg_similarity >= threshold:
            self.passed_checks.append(
                f"Avg semantic similarity: {avg_similarity:.3f} >= {threshold}"
            )
            return True
        else:
            self.failed.append(
                f"Avg semantic similarity {avg_similarity:.3f} below threshold {threshold}"
            )
            return False
    
    def check_hallucination_rate(self, results: Dict) -> bool:
        """Check hallucination rate"""
        test_results = results.get('results', [])
        if not test_results:
            self.warnings.append("No detailed results for hallucination check")
            return True
        
        hallucinations = 0
        total = len(test_results)
        
        for result in test_results:
            if 'metrics' in result:
                metrics = result['metrics']
                if 'hallucination' in metrics and metrics['hallucination']:
                    hallucinations += 1
            
            if 'rule_validation' in result:
                for rule in result['rule_validation']:
                    if 'hallucination' in str(rule).lower() and not rule.get('passed', True):
                        hallucinations += 1
                        break
        
        hallucination_rate = hallucinations / total if total > 0 else 0
        threshold = self.config.max_hallucination_rate
        
        if hallucination_rate <= threshold:
            self.passed_checks.append(
                f"Hallucination rate: {hallucination_rate:.1%} <= {threshold:.1%}"
            )
            return True
        else:
            self.failed.append(
                f"Hallucination rate {hallucination_rate:.1%} above threshold {threshold:.1%}"
            )
            return False
    
    def evaluate(self, results: Dict) -> bool:
        """Run all quality checks"""
        self.failed = []
        self.warnings = []
        self.passed_checks = []
        
        checks = [
            self.check_pass_rate(results),
            self.check_critical_tests(results),
            self.check_semantic_similarity(results),
            self.check_hallucination_rate(results)
        ]
        
        return all(checks)
    
    def get_decision(self) -> str:
        """Get deployment decision"""
        if not self.failed:
            return "✅ APPROVED"
        elif len(self.failed) <= 2:
            return "⚠️ CONDITIONAL"
        else:
            return "❌ BLOCKED"
    
    def report(self, verbose: bool = False) -> str:
        """Generate deployment decision report"""
        decision = self.get_decision()
        
        lines = [
            "="*80,
            "🚦 QUALITY GATE DECISION",
            "="*80,
            "",
            f"Decision: {decision}",
            ""
        ]
        
        if self.passed_checks and verbose:
            lines.append("✅ Passed Checks:")
            for check in self.passed_checks:
                lines.append(f"   • {check}")
            lines.append("")
        
        if self.failed:
            lines.append("❌ Failed Checks:")
            for issue in self.failed:
                lines.append(f"   • {issue}")
            lines.append("")
        
        if self.warnings and verbose:
            lines.append("⚠️  Warnings:")
            for warning in self.warnings:
                lines.append(f"   • {warning}")
            lines.append("")
        
        if not self.failed and not self.warnings:
            lines.append("✅ All quality gates passed!")
            lines.append("   Ready for production deployment")
            lines.append("")
        
        lines.append("="*80)
        
        return "\n".join(lines)


# ============================================================================
# Main Function
# ============================================================================

def load_results(filepath: str) -> Dict:
    """Load evaluation results from JSON file"""
    if not Path(filepath).exists():
        raise FileNotFoundError(f"Results file not found: {filepath}")
    
    with open(filepath, 'r') as f:
        return json.load(f)


def main():
    """Main quality gate checker"""
    parser = argparse.ArgumentParser(description='Check evaluation quality gates')
    parser.add_argument(
        '--results',
        type=str,
        required=True,
        help='Path to evaluation results JSON file'
    )
    parser.add_argument(
        '--min-pass-rate',
        type=float,
        default=95.0,
        help='Minimum pass rate threshold (default: 95.0)'
    )
    parser.add_argument(
        '--min-similarity',
        type=float,
        default=0.85,
        help='Minimum semantic similarity threshold (default: 0.85)'
    )
    parser.add_argument(
        '--max-hallucination',
        type=float,
        default=0.02,
        help='Maximum hallucination rate threshold (default: 0.02)'
    )
    parser.add_argument(
        '--critical-categories',
        type=str,
        nargs='+',
        default=['fraud_detection', 'security'],
        help='Critical test categories (default: fraud_detection security)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--output-report',
        type=str,
        default=None,
        help='Save report to file (optional)'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("🚦 QUALITY GATE CHECKER")
    print("="*80)
    print(f"Results file: {args.results}")
    print(f"Min pass rate: {args.min_pass_rate}%")
    print(f"Min similarity: {args.min_similarity}")
    print(f"Max hallucination: {args.max_hallucination}")
    print(f"Critical categories: {args.critical_categories}")
    print("="*80)
    
    try:
        # Load results
        print(f"\n📂 Loading results from: {args.results}")
        results = load_results(args.results)
        
        # Create quality configuration
        config = QualityConfig(
            min_pass_rate=args.min_pass_rate,
            min_semantic_similarity=args.min_similarity,
            max_hallucination_rate=args.max_hallucination,
            critical_categories=args.critical_categories
        )
        
        # Check quality gates
        print("🔍 Running quality gate checks...\n")
        checker = QualityGateChecker(config)
        passed = checker.evaluate(results)
        
        # Generate and print report
        report = checker.report(verbose=args.verbose)
        print(report)
        
        # Save report if requested
        if args.output_report:
            with open(args.output_report, 'w') as f:
                f.write(report)
            print(f"\n💾 Report saved to: {args.output_report}")
        
        # Print action items
        decision = checker.get_decision()
        
        if decision == "✅ APPROVED":
            print("\n✅ Next Steps:")
            print("   • Proceed with deployment")
            print("   • Monitor production metrics")
            print("   • Schedule next evaluation")
            sys.exit(0)  # Success
        
        elif decision == "⚠️ CONDITIONAL":
            print("\n⚠️  Next Steps:")
            print("   • Review failed checks")
            print("   • Get manual approval")
            print("   • Consider deploying with monitoring")
            sys.exit(1)  # Conditional failure
        
        else:  # BLOCKED
            print("\n❌ Next Steps:")
            print("   • Fix failed quality checks")
            print("   • Re-run evaluation")
            print("   • Do NOT deploy to production")
            sys.exit(1)  # Hard failure
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Quality gate check failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()