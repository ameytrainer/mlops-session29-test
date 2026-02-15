# 🚀 Quick Start Guide - Session 29

**Get up and running in 10 minutes!**

---

## ⚡ Speed Setup (Minimal)

If you just want to start learning immediately:

```bash
# 1. Install Python packages (2 min)
pip install openai pandas numpy scikit-learn matplotlib loguru python-dotenv

# 2. Set OpenAI API key
export OPENAI_API_KEY="sk-your-key-here"

# 3. Launch notebook
jupyter notebook Session_29_Advanced_LLM_Evaluation_CICD.ipynb
```

**That's it!** You can start with the first few parts of the session.

---

## 📋 Full Setup (Recommended)

For complete experience with all tools:

### 1️⃣ Prerequisites (5 min)
```bash
# Check Python version (need 3.10+)
python --version

# Check if Node.js installed (need 18+)
node --version

# If not installed:
# - Python: https://www.python.org/downloads/
# - Node.js: https://nodejs.org/
```

### 2️⃣ Environment Setup (3 min)
```bash
# Create and activate virtual environment
python -m venv session29_env
source session29_env/bin/activate  # macOS/Linux
# session29_env\Scripts\activate   # Windows

# Install all dependencies
pip install -r requirements.txt
```

### 3️⃣ Install Promptfoo (1 min)
```bash
npm install -g promptfoo
```

### 4️⃣ Configure API Keys (2 min)
```bash
# Copy template
cp .env.template .env

# Edit with your keys
nano .env  # or use any text editor
```

Add your keys:
```
OPENAI_API_KEY=sk-your-actual-key-here
PROMPTLAYER_API_KEY=pl-your-key-here  # optional
```

### 5️⃣ Verify Setup (1 min)
```bash
python verify_setup.py
```

Should see:
```
🎉 ALL CHECKS PASSED! You're ready to start Session 29!
```

### 6️⃣ Start Learning! (0 min to ∞)
```bash
jupyter notebook Session_29_Advanced_LLM_Evaluation_CICD.ipynb
```

---

## 🆘 Quick Troubleshooting

### Issue: "Module not found"
```bash
# Make sure virtual environment is activated
which python  # should show: .../session29_env/bin/python

# Reinstall
pip install -r requirements.txt
```

### Issue: "OpenAI API key invalid"
```bash
# Check .env file exists
ls -la .env

# Check key format (should start with 'sk-')
cat .env | grep OPENAI

# Test manually
python -c "import openai; print(openai.api_key)"
```

### Issue: "Promptfoo command not found"
```bash
# Reinstall globally
npm install -g promptfoo

# Or use npx
npx promptfoo --version
```

### Issue: "Rate limit exceeded"
- Use gpt-4o-mini instead of gpt-4 (cheaper)
- Add `time.sleep(1)` between API calls
- Upgrade OpenAI tier if needed

---

## 💰 Cost Estimate

**For entire session:**
- OpenAI API: $2-5 (using gpt-4o-mini)
- PromptLayer: FREE (first 1,000 requests)
- Promptfoo: FREE (open source)
- Total: ~$2-5

**Tips to reduce cost:**
- Use gpt-4o-mini everywhere
- Start with smaller test suites
- Comment out expensive evaluations initially
- Use provided results to understand concepts

---

## 📚 What You Need to Know

### Must Know (from previous sessions):
- Basic Python syntax
- How to use Jupyter notebooks
- What an API is
- Session 27 & 28 content (recommended)

### Nice to Know:
- Git basics
- Docker concepts
- CI/CD fundamentals
- AWS/Cloud basics

### Don't Worry About:
- Advanced Python - we'll explain everything
- Deep learning theory - not needed
- Complex math - minimal required

---

## 🎯 Session Flow

**Part 1-2 (50 min):** Theory + Disaster scenario  
→ No coding, just understanding

**Part 3 (45 min):** Static evaluation  
→ First hands-on coding

**Part 4 (40 min):** Dynamic evaluation  
→ PromptLayer integration

**Part 5 (50 min):** Hybrid evaluation  
→ Multiple tools

**Part 6 (45 min):** CI/CD integration  
→ GitHub Actions

**Part 7 (30 min):** Wrap-up  
→ Course conclusion

**Total: 4 hours with breaks**

---

## 💡 Pro Tips

### Save Money:
```python
# Use cheaper model
model = "gpt-4o-mini"  # instead of "gpt-4"

# Reduce max_tokens
max_tokens = 100  # instead of 500
```

### Debug Faster:
```python
# Add verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print intermediate results
print(f"Debug: {variable}")
```

### Work Offline:
- Download notebook first
- Use provided sample results
- Run expensive evaluations later
- Focus on understanding concepts

---

## 📞 Getting Help

### During Session:
1. Raise hand / unmute
2. Ask in chat
3. Flag instructor

### After Session:
1. Check README.md (detailed docs)
2. Review Troubleshooting section
3. Post in course Slack/Discord
4. Office hours: Fridays 6-7 PM IST
5. Email instructor

---

## ✅ Pre-Session Checklist

Before starting the session, verify:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Promptfoo installed (`promptfoo --version` works)
- [ ] OpenAI API key configured in .env
- [ ] PromptLayer account created (optional)
- [ ] Notebook opens successfully
- [ ] verify_setup.py passes all checks
- [ ] $5-10 credit in OpenAI account
- [ ] Quiet workspace ready
- [ ] Notebook + pen for notes

---

## 🎓 Learning Mode Selection

Choose your learning path:

### 🐰 **Fast Track** (2 hours)
- Skip detailed explanations
- Run all code cells quickly
- Focus on outputs and results
- Good for: Experienced developers

### 🐢 **Deep Dive** (4 hours)
- Read all explanations carefully
- Understand every line of code
- Try modifying examples
- Good for: Thorough understanding

### 🎯 **Hands-On** (3 hours)
- Light reading, heavy coding
- Modify examples as you go
- Build custom evaluations
- Good for: Practical learners

---

## 🚦 Ready to Start?

**Final check:**
```bash
python verify_setup.py && echo "✅ READY!" || echo "❌ FIX ISSUES"
```

If you see `✅ READY!`, you're all set!

**Launch notebook:**
```bash
jupyter notebook Session_29_Advanced_LLM_Evaluation_CICD.ipynb
```

**Let's build production-grade LLM evaluation pipelines!** 🚀

---

**Questions before starting?** Ask now!

**Having issues?** Check README.md or ask instructor.

**Excited?** Let's go! 🎉

---
