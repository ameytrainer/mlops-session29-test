# Session 29: Advanced LLM Evaluation & CI/CD Integration

**MLOps with Agentic AI - Advanced Certification Course**  
**Final Session** 🎓

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Learning Objectives](#learning-objectives)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [What You'll Build](#what-youll-build)
6. [Session Structure](#session-structure)
7. [Evaluation Tools Covered](#evaluation-tools-covered)
8. [Troubleshooting](#troubleshooting)
9. [Additional Resources](#additional-resources)

---

## 🎯 Overview

This is the **final and most comprehensive session** of the MLOps with Agentic AI course. You'll learn how to build production-grade LLM evaluation pipelines that prevent catastrophic failures like the $2.4M disaster scenario we'll explore.

**Duration:** 4 hours (240 minutes)  
**Format:** 100% hands-on, disaster-first methodology  
**Outcome:** Complete evaluation pipeline integrated with CI/CD

---

## 🎓 Learning Objectives

By the end of this session, you will:

1. ✅ **Build complete LLM evaluation pipelines** covering all evaluation types
2. ✅ **Master Static, Dynamic, and Hybrid evaluation** strategies  
3. ✅ **Implement PromptLayer, Promptfoo, and OpenAI Evals** for comprehensive testing
4. ✅ **Integrate evaluations with CI/CD** for automated regression testing
5. ✅ **Create production-grade evaluation workflows** with alerting and monitoring
6. ✅ **Understand how to prevent catastrophic LLM failures** in production

---

## 📚 Prerequisites

### Required Knowledge:
- Session 27: Agentic Frameworks (LangChain, CrewAI, LangGraph)
- Session 28: Evaluation Tools (RAGAS, LangSmith, TruLens)
- Basic Python programming
- Understanding of APIs and JSON

### Required Software:
- Python 3.10 or higher
- Node.js 18+ (for Promptfoo)
- Git
- OpenAI API key (required)
- PromptLayer account (recommended, free tier available)

### Recommended:
- GitHub account (for CI/CD examples)
- VS Code or Jupyter Notebook environment
- Basic Docker knowledge (helpful but not required)

---

## 🚀 Setup Instructions

### Step 1: Clone Repository (if applicable)
```bash
git clone <repository-url>
cd session-29-evaluation
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv session29_env

# Activate virtual environment
# On macOS/Linux:
source session29_env/bin/activate
# On Windows:
session29_env\Scripts\activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Promptfoo (Node.js Tool)
```bash
npm install -g promptfoo

# Verify installation
promptfoo --version
```

### Step 5: Configure API Keys
```bash
# Copy template to .env
cp .env.template .env

# Edit .env with your actual API keys
nano .env  # or use your favorite editor
```

**Required API Keys:**
1. **OpenAI API Key** (REQUIRED)
   - Get from: https://platform.openai.com/api-keys
   - Cost: ~$2-5 for entire session

2. **PromptLayer API Key** (RECOMMENDED)
   - Get from: https://promptlayer.com
   - FREE for first 1,000 requests
   - Provides tracking and annotation capabilities

### Step 6: Verify Setup
```bash
# Run verification script
python verify_setup.py
```

Expected output:
```
✅ Python 3.11.0 detected
✅ OpenAI API key configured
✅ PromptLayer API key configured
✅ Promptfoo installed (version 0.x.x)
✅ All dependencies installed
🎉 You're ready to start!
```

### Step 7: Launch Jupyter Notebook
```bash
jupyter notebook Session_29_Advanced_LLM_Evaluation_CICD.ipynb
```

---

## 🛠️ What You'll Build

### 1. Static Evaluation Engine
- Complete test suite with ground truth labels
- Multiple evaluation metrics (exact match, semantic similarity, custom rules)
- Production-ready evaluation engine with logging
- Automated pass/fail criteria

### 2. Dynamic Evaluation System
- PromptLayer integration for request tracking
- Production sampling strategy (1% review)
- Human review interface with structured scoring
- Multi-dimensional quality assessment

### 3. Hybrid Evaluation Pipeline
- Promptfoo for comprehensive testing
- OpenAI Evals for model comparison
- Automated metrics + human feedback loop
- Scalable evaluation framework

### 4. CI/CD Integration
- GitHub Actions workflow for automated testing
- Quality gate checker (deployment decisions)
- Regression testing for prompts
- Auto-rollback mechanism
- Slack alerting on quality drops

---

## 📖 Session Structure

### Part 1: The $2.4 Million Disaster (30 min)
- Real production failure case study
- Why evaluation matters
- Types of evaluation needed

### Part 2: Understanding Evaluation Types (20 min)
- Static evaluation (ground truth)
- Dynamic evaluation (human-in-loop)
- Hybrid evaluation (best of both)
- When to use each type

### Part 3: Static Evaluation (45 min)
- Building test suites
- Implementing evaluation engine
- Quality metrics and thresholds
- **Hands-on:** Run complete static evaluation

### Part 4: Dynamic Evaluation (40 min)
- PromptLayer setup and tracking
- Production sampling strategy
- Human review simulation
- **Hands-on:** Collect and analyze human feedback

### Part 5: Hybrid Evaluation (50 min)
- Promptfoo comprehensive testing
- OpenAI Evals for model comparison
- Combining automated + human
- **Hands-on:** Run multi-tool evaluation

### Part 6: CI/CD Integration (45 min)
- GitHub Actions workflow
- Quality gate automation
- Alerting and rollback
- **Hands-on:** Test deployment pipeline

### Part 7: Course Conclusion (30 min)
- Reflection on entire course
- Capstone project guidance
- Continued learning resources
- Q&A and wrap-up

**Total: 240 minutes (4 hours)**

---

## 🔧 Evaluation Tools Covered

### Tool Comparison Matrix

| Tool | Type | Best For | Complexity | Cost |
|------|------|----------|------------|------|
| **PromptLayer** | Tracking | Request logging & annotation | Low | Free tier available |
| **Promptfoo** | Testing | Multi-prompt comparison | Medium | Free & Open Source |
| **OpenAI Evals** | Benchmarking | Model comparison | High | Free & Open Source |
| **Custom Static** | Testing | Domain-specific validation | Medium | Development time |
| **Human Review** | Quality | Subjective assessment | Low | Human time cost |

### When to Use Each Tool:

```python
# Your Evaluation Strategy:

1. PromptLayer     → Track EVERY production request
2. Static Tests    → Run on EVERY code commit (CI/CD)
3. Promptfoo       → Test BEFORE deployment
4. Human Reviews   → Sample 1-5% of production
5. OpenAI Evals    → Quarterly model comparison
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions:

#### Issue: OpenAI API Rate Limits
```
Error: Rate limit exceeded
```
**Solution:**
- Use gpt-4o-mini instead of gpt-4 (cheaper, faster)
- Add delays between requests: `time.sleep(1)`
- Implement exponential backoff
- Upgrade to Tier 2 if needed

#### Issue: Promptfoo Not Found
```
Error: promptfoo: command not found
```
**Solution:**
```bash
# Reinstall globally
npm install -g promptfoo

# Check PATH
echo $PATH

# Try with npx
npx promptfoo --version
```

#### Issue: Import Errors
```
ModuleNotFoundError: No module named 'promptlayer'
```
**Solution:**
```bash
# Verify virtual environment is activated
which python  # Should show session29_env/bin/python

# Reinstall requirements
pip install -r requirements.txt

# Install specific package
pip install promptlayer
```

#### Issue: PromptLayer Not Tracking
```
Requests not appearing in dashboard
```
**Solution:**
- Verify API key in .env
- Check you're using `promptlayer.openai.OpenAI()` wrapper
- Allow 2-3 minutes for dashboard to update
- Check PromptLayer status page

#### Issue: Jupyter Kernel Crashes
```
Kernel died, restarting
```
**Solution:**
- Reduce batch size in evaluation
- Add memory management:
  ```python
  import gc
  gc.collect()
  ```
- Restart kernel: Kernel → Restart
- Use Colab if local memory insufficient

---

## 📚 Additional Resources

### Documentation:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [PromptLayer Docs](https://docs.promptlayer.com)
- [Promptfoo Docs](https://www.promptfoo.dev/docs)
- [OpenAI Evals GitHub](https://github.com/openai/evals)

### Related Sessions:
- **Session 27:** Agentic Frameworks (LangChain, CrewAI, LangGraph)
- **Session 28:** Evaluation Tools (RAGAS, LangSmith, TruLens)
- **Session 1-5:** MLOps Foundations (MLflow, CI/CD)

### Further Learning:
- [MLOps Community](https://mlops.community)
- [LangChain Documentation](https://python.langchain.com)
- [Hugging Face Evaluate](https://huggingface.co/docs/evaluate)
- [Chip Huyen's MLOps Blog](https://huyenchip.com/blog/)

### Books:
- "Designing Machine Learning Systems" by Chip Huyen
- "Building Machine Learning Pipelines" by Hannes Hapke
- "Machine Learning Design Patterns" by Lakshmanan et al.

---

## 🎯 Success Criteria

You've successfully completed this session when you can:

- [ ] Explain the three types of LLM evaluation (Static, Dynamic, Hybrid)
- [ ] Build a static evaluation suite with >95% pass rate threshold
- [ ] Implement PromptLayer tracking for production monitoring
- [ ] Use Promptfoo to compare multiple prompt versions
- [ ] Create a GitHub Actions workflow for automated LLM testing
- [ ] Set up quality gates that block bad deployments
- [ ] Implement auto-rollback on quality drops
- [ ] Understand when to use each evaluation tool
- [ ] Build a complete evaluation pipeline for your use case

---

## 🏆 Final Capstone Challenge

**Build Your Own Evaluation Pipeline:**

Choose a domain (e.g., customer support, content generation, medical Q&A) and:

1. Create 50+ test cases with ground truth
2. Implement static evaluation with quality gates
3. Set up PromptLayer tracking
4. Configure Promptfoo for regression testing
5. Build GitHub Actions CI/CD pipeline
6. Document your evaluation strategy
7. Present results showing deployment decision

**Deliverables:**
- GitHub repository with complete code
- Evaluation results (static, dynamic, hybrid)
- CI/CD workflow that blocks bad deployments
- README explaining your approach
- Presentation slides (10 minutes)

---

## 📞 Support

**Need Help?**

1. **During Session:** Ask instructor immediately
2. **After Session:** 
   - Post in course Slack/Discord
   - Office Hours: Fridays 6-7 PM IST
   - Email: [instructor-email]

**Found a Bug?**
- Open GitHub issue
- Include error message and environment details
- Share relevant code snippet

---

## 🎉 Congratulations!

You're about to complete the most comprehensive MLOps + Agentic AI course available. This final session ties everything together and equips you with production-grade evaluation skills that prevent million-dollar disasters.

**Let's build evaluation pipelines that make LLM deployments safe and reliable!** 🚀

---

**Last Updated:** February 2026  
**Course:** MLOps with Agentic AI (Advanced Certification)  
**Instructor:** [Your Name]  
**Contact:** [Your Contact Info]

---
