#!/usr/bin/env python3
"""
Post PR Results - Post evaluation results as PR comment
For use in GitHub Actions CI/CD pipeline
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict


def normalize_results(results: Dict) -> Dict:
    """Normalize results to expected format"""
    normalized = {
        'model_used': results.get('model_used', 'gpt-4o-mini'),
        'timestamp': results.get('timestamp', datetime.now().isoformat()),
    }
    
    # Calculate pass_rate if not present
    if 'pass_rate' in results:
        normalized['pass_rate'] = results['pass_rate']
    elif 'passed' in results and 'total_tests' in results:
        normalized['pass_rate'] = (results['passed'] / results['total_tests']) * 100
    else:
        normalized['pass_rate'] = 0
    
    # Get counts
    normalized['passed'] = results.get('passed', 0)
    normalized['failed'] = results.get('failed', 0)
    normalized['total_tests'] = results.get('total_tests', 
                                           normalized['passed'] + normalized['failed'])
    
    return normalized


def create_pr_comment(results: Dict, run_url: str = None) -> str:
    """Create PR comment from evaluation results"""
    norm = normalize_results(results)
    
    pass_rate = norm['pass_rate']
    passed = norm['passed']
    total = norm['total_tests']
    
    # Determine status
    if pass_rate >= 95:
        status = "✅ PASSED"
        emoji = "🎉"
    elif pass_rate >= 90:
        status = "⚠️ WARNING"
        emoji = "⚠️"
    else:
        status = "❌ FAILED"
        emoji = "🚨"
    
    comment = f"""## {emoji} LLM Evaluation Results

**Status:** {status}

### Summary
| Metric | Value |
|--------|-------|
| Pass Rate | {pass_rate:.1f}% |
| Tests Passed | {passed}/{total} |
| Tests Failed | {total - passed}/{total} |
| Model | {norm['model_used']} |
| Timestamp | {norm['timestamp']} |

### Quality Gate Decision
"""
    
    if pass_rate >= 95:
        comment += """
✅ **APPROVED FOR MERGE**

This PR passes all quality gates and is approved for deployment.

**Next Steps:**
- Review code changes
- Merge when ready
- Monitor production deployment
"""
    elif pass_rate >= 90:
        comment += """
⚠️ **CONDITIONAL APPROVAL**

Pass rate is below 95% threshold. Please review failed tests before merging.

**Action Required:**
- Review failed test cases
- Determine if failures are acceptable
- Get manual approval before merging
"""
    else:
        comment += """
❌ **BLOCKED FROM MERGE**

Pass rate is critically low. This PR cannot be merged until evaluation passes.

**Action Required:**
1. Review failed test cases in evaluation logs
2. Fix issues causing failures
3. Push new commits to re-run evaluation
4. Ensure pass rate >= 95%
"""
    
    if run_url:
        comment += f"\n📊 [View detailed results]({run_url})\n"
    
    comment += """
---
*Automated evaluation by MLOps CI/CD pipeline*
"""
    
    return comment


def post_comment_to_pr(repo: str, pr_number: int, comment: str, token: str) -> bool:
    """Post comment to GitHub PR"""
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {"body": comment}
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 201:
            print(f"✅ Comment posted to PR #{pr_number}")
            return True
        else:
            print(f"⚠️ Failed to post comment: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error posting comment: {str(e)}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Post evaluation results to PR')
    parser.add_argument(
        '--results',
        type=str,
        required=True,
        help='Path to evaluation results JSON file'
    )
    parser.add_argument(
        '--pr-number',
        type=int,
        required=True,
        help='Pull request number'
    )
    parser.add_argument(
        '--repo',
        type=str,
        default=None,
        help='Repository (owner/repo). Defaults to GITHUB_REPOSITORY env var'
    )
    parser.add_argument(
        '--token',
        type=str,
        default=None,
        help='GitHub token. Defaults to GITHUB_TOKEN env var'
    )
    parser.add_argument(
        '--run-url',
        type=str,
        default=None,
        help='URL to GitHub Actions run (optional)'
    )
    
    args = parser.parse_args()
    
    # Get repo and token from args or environment
    repo = args.repo or os.getenv('GITHUB_REPOSITORY')
    token = args.token or os.getenv('GITHUB_TOKEN')
    
    if not repo:
        print("❌ Error: --repo not provided and GITHUB_REPOSITORY not set")
        sys.exit(1)
    
    if not token:
        print("❌ Error: --token not provided and GITHUB_TOKEN not set")
        sys.exit(1)
    
    print("="*80)
    print("📝 POST PR RESULTS")
    print("="*80)
    print(f"Repository: {repo}")
    print(f"PR Number: #{args.pr_number}")
    print(f"Results: {args.results}")
    print("="*80)
    
    try:
        # Load results
        if not Path(args.results).exists():
            print(f"❌ Results file not found: {args.results}")
            sys.exit(1)
        
        with open(args.results, 'r') as f:
            results = json.load(f)
        
        print(f"\n✅ Loaded results:")
        print(f"   Pass Rate: {results.get('pass_rate', 'N/A'):.1f}%")
        print(f"   Passed: {results.get('passed', 0)}/{results.get('total_tests', 0)}")
        
        # Create comment
        print("\n📝 Creating PR comment...")
        comment = create_pr_comment(results, args.run_url)
        
        # Post comment
        print(f"📤 Posting comment to PR #{args.pr_number}...")
        success = post_comment_to_pr(repo, args.pr_number, comment, token)
        
        if success:
            print("\n✅ Comment posted successfully!")
            sys.exit(0)
        else:
            print("\n❌ Failed to post comment")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()