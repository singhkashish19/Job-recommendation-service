# Python Virtual Environment Setup Guide

## ✅ Yes, You Need a Virtual Environment

Before running the application locally, you **must** create and activate a **Python Virtual Environment**. Here's why and how:

---

## 🤔 Why Virtual Environment?

A virtual environment is an **isolated Python environment** that allows you to:

✅ **Install dependencies without affecting system Python**
✅ **Have different Python packages for different projects**
✅ **Easily replicate your setup on another machine**
✅ **Avoid version conflicts**
✅ **Keep your system Python clean**

Think of it as a **sandbox for your project**.

---

## 🔧 Step-by-Step Setup (Windows)

### Step 1: Open PowerShell/Command Prompt

Navigate to your project folder:
```bash
cd c:\workspace\job-recommendation-service
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

**What this does:**
- Creates a `venv` folder in your project
- Contains a complete isolated Python environment
- Takes ~30 seconds to create

**Expected output:**
```
(No output = success!)
```

### Step 3: Activate Virtual Environment

```bash
.\venv\Scripts\activate
```

**Your prompt should change to show:**
```
(venv) C:\workspace\job-recommendation-service>
```

The `(venv)` prefix means the virtual environment is **active**.

### Step 4: Verify Installation

Check that you're using the virtual environment's Python:
```bash
python --version
where python
```

**Should show:**
```
Python 3.x.x
C:\workspace\job-recommendation-service\venv\Scripts\python.exe
```

### Step 5: Upgrade pip (Important!)

```bash
python -m pip install --upgrade pip
```

### Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

**This will:**
- Download and install all required packages
- Takes 2-5 minutes depending on your internet
- Shows progress bar

**Expected output:**
```
Successfully installed fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv passlib python-jose pydantic sentence-transformers numpy pytest...
```

### Step 7: Verify Installation

```bash
pip list
```

Should show all installed packages. Look for:
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- sentence-transformers
- pytest

---

## 🚀 Running the Application

Once virtual environment is activated and dependencies installed:

### 1. Ensure venv is Active
```bash
# You should see (venv) in your prompt
# If not, run: .\venv\Scripts\activate
```

### 2. Start the Application
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Open in Browser
```
http://localhost:8000/docs
```

---

## 🛑 Deactivating Virtual Environment

When you're done developing:

```bash
deactivate
```

Your prompt returns to normal without `(venv)` prefix.

---

## 📚 Setup for Mac/Linux (Alternative)

If you're on Mac or Linux (for reference):

### Step 1: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 2: Activate
```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
uvicorn app.main:app --reload --port 8000
```

### Step 5: Deactivate
```bash
deactivate
```

---

## ✨ Quick Reference

| Action | Command |
|--------|---------|
| Create venv | `python -m venv venv` |
| Activate (Windows) | `.\venv\Scripts\activate` |
| Activate (Mac/Linux) | `source venv/bin/activate` |
| Install dependencies | `pip install -r requirements.txt` |
| Update pip | `python -m pip install --upgrade pip` |
| Check packages | `pip list` |
| Run app | `uvicorn app.main:app --reload --port 8000` |
| Run tests | `pytest -v` |
| Deactivate | `deactivate` |

---

## 🐛 Troubleshooting

### Issue: Python command not found
**Solution:** Python not installed or not in PATH
```bash
# Download from python.org and reinstall
# Or check if you have Python installed:
python --version
```

### Issue: "No module named 'venv'"
**Solution:** Python venv module missing
```bash
# Reinstall Python with venv support
```

### Issue: Cannot find pip
**Solution:** Upgrade pip first
```bash
python -m pip install --upgrade pip
```

### Issue: "venv is not activated"
**Solution:** You forgot to activate
```bash
# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Issue: Packages won't install
**Solution:** Upgrade pip and try again
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "Permission denied" on Mac/Linux
**Solution:** Run with proper permissions
```bash
pip install --user -r requirements.txt
# Or fix permissions:
chmod +x venv/bin/activate
source venv/bin/activate
```

---

## 🔄 Resuming Work Later

Every time you open a new terminal/PowerShell for this project:

### 1. Navigate to Project
```bash
cd c:\workspace\job-recommendation-service
```

### 2. Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### 3. Continue Development
```bash
# Now you can run any command
uvicorn app.main:app --reload
# or
pytest -v
```

---

## 📊 What's In Your Virtual Environment

```
venv/
├── Scripts/  (Windows) or bin/ (Mac/Linux)
│   ├── python.exe
│   ├── pip.exe
│   ├── uvicorn
│   └── pytest
├── Lib/ (Windows) or lib/ (Mac/Linux)
│   └── site-packages/
│       ├── fastapi/
│       ├── sqlalchemy/
│       ├── psycopg2/
│       └── ...
└── pyvenv.cfg
```

This is completely isolated from your system Python.

---

## 🎯 Full Local Development Setup

Here's the complete workflow:

```bash
# 1. Navigate to project
cd c:\workspace\job-recommendation-service

# 2. Create virtual environment (first time only)
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file
cp .env.example .env
# Edit .env with your database settings if needed

# 7. Start the application
uvicorn app.main:app --reload --port 8000

# 8. Open browser
# Navigate to: http://localhost:8000/docs
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# Check virtual environment is active
echo %VIRTUAL_ENV%  # Windows
# Or: echo $VIRTUAL_ENV  # Mac/Linux
# Should show your venv path

# Verify Python is from venv
where python  # Windows
which python  # Mac/Linux
# Should show venv path

# Test imports
python -c "import fastapi; import sqlalchemy; import pytest; print('All packages OK!')"

# Run application
uvicorn app.main:app --reload --port 8000

# In another terminal, test health endpoint
curl http://localhost:8000/health

# Run tests
pytest tests/ -v
```

All should work without errors!

---

## 🚀 Next Steps

Once you've completed the setup:

1. **See [docs/QUICKSTART.md](../docs/QUICKSTART.md)** - Quick start guide
2. **Read [docs/README.md](../docs/README.md)** - Full documentation
3. **Run tests** - `pytest -v`
4. **Start developing** - API auto-reloads with --reload flag

---

## 📝 Important Notes

⚠️ **Do NOT commit `venv/` folder to Git**
- The `.gitignore` file already excludes it
- Just commit `requirements.txt`
- Others can regenerate `venv` with `pip install -r requirements.txt`

✅ **Always use virtual environment**
- Never run without activating venv
- Always activate before running code
- Always deactivate when done

---

**You're ready to start development!** 🎉

For more details on running the app, see [docs/QUICKSTART.md](../docs/QUICKSTART.md)
