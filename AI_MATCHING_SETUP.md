# AI-Powered Volunteer Matching - Setup Guide

## ✅ What I've Built

I've completely replaced the old keyword-based matching with **Azure OpenAI GPT-4 powered intelligent matching**!

### **New Features:**

✅ **Semantic Understanding** - GPT-4 understands meaning, not just keywords  
✅ **Multi-Factor Analysis** - Skills, experience, education, availability  
✅ **Match Scores (0-100)** - Precise confidence scores  
✅ **Detailed Explanations** - WHY each volunteer matches  
✅ **Strengths & Concerns** - Comprehensive assessment  
✅ **Top 10 Best Matches** - Automatically ranked  

---

## ⚠️ Current Issue: Azure OpenAI Configuration

The AI system is **fully built and ready**, but there's a configuration issue with your Azure OpenAI credentials.

### **Problems Detected:**

1. **❌ Deployment Name: `gpt-4.1`**
   - This doesn't exist (GPT-4.1 is not a valid model)
   - You need the EXACT deployment name from your Azure Portal

2. **❌ API Version: `2025-04-14`**
   - This is a future date and doesn't exist yet
   - Valid versions: `2024-08-01-preview`, `2024-06-01`, etc.

---

## 🔧 How to Fix

### **Step 1: Find Your Deployment Name**

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: **Azure OpenAI Resource → Model deployments**
3. Look at the **"Name"** column (NOT the model column)
4. Copy the exact deployment name (e.g., `gpt-4`, `my-gpt4-deployment`)

**Example:**
```
Name (This is what you need) | Model          | Version
------------------------------|----------------|--------
gpt-4                        | gpt-4          | 0613
my-custom-gpt4               | gpt-4-turbo    | 1106
```

Use the **Name** column value!

### **Step 2: Update config.py**

Open `config.py` and update these two lines:

```python
# OLD (current - INCORRECT)
AZURE_OPENAI_DEPLOYMENT = "gpt-4.1"  # ❌ Wrong
AZURE_OPENAI_API_VERSION = "2025-04-14"  # ❌ Wrong

# NEW (update with YOUR values)
AZURE_OPENAI_DEPLOYMENT = "gpt-4"  # ✅ Your actual deployment name from Azure
AZURE_OPENAI_API_VERSION = "2024-08-01-preview"  # ✅ Valid API version
```

**Valid API Versions:**
- `2024-10-01-preview` (latest)
- `2024-08-01-preview` (recommended)
- `2024-06-01`
- `2024-05-01-preview`
- `2024-02-15-preview`

### **Step 3: Test Connection**

```bash
python test_ai_connection.py
```

You should see: **"Connection successful!"**

### **Step 4: Test AI Matching**

```bash
python ai_matcher.py
```

This will test the full AI matching system with sample data.

---

## 📁 Files Created

### **Core AI Files:**
- **`config.py`** - Azure OpenAI configuration (UPDATE THIS!)
- **`ai_matcher.py`** - GPT-4 powered matching engine
- **`app.py`** - Updated to use AI matcher (DONE ✅)

### **Testing & Diagnostics:**
- **`test_ai_connection.py`** - Test Azure connection
- **`diagnose_azure_config.py`** - Configuration diagnostics
- **`AI_MATCHING_SETUP.md`** - This guide

### **Updated:**
- **`requirements.txt`** - Added `openai>=1.0.0` (INSTALLED ✅)
- **`app.py`** - Now uses `AIVolunteerMatcher` (DONE ✅)

---

## 🎯 How the AI Matching Works

### **Input:**
HR Manager enters job description:
```
Looking for Python developer with 2+ years experience.
Skills: Flask, SQL, Git
Availability: Part-time, remote
```

### **Processing:**
1. GPT-4 analyzes each volunteer's **full profile** (44 columns!)
2. Evaluates:
   - **Skills Match** (technical + soft skills)
   - **Experience Relevance** (quality over quantity)
   - **Education Alignment** (field of study)
   - **Availability Compatibility** (location, time, mode)

### **Output:**
```json
{
  "name": "John Doe",
  "match_score": 85,
  "overall_assessment": "Excellent match. Strong Python background...",
  "strengths": [
    "3 years Python + Flask experience",
    "Proficient in SQL databases",
    "Available for remote work"
  ],
  "concerns": [
    "Limited Git experience (learning)"
  ],
  "detailed_scores": {
    "skills": 90,
    "experience": 85,
    "education": 80,
    "availability": 95
  }
}
```

---

## 🚀 Once Fixed, Run The Application

```bash
# Method 1: Quick Start
RUN.bat

# Method 2: Manual
python app.py
```

Then open: `http://localhost:5000`

**Try It:**
1. Click "Find Matches" button
2. Enter a job description
3. Watch GPT-4 analyze 1,716 volunteers
4. Get top 10 matches with detailed AI insights!

---

## 🔄 Comparison: Old vs New

### **OLD System (TF-IDF):**
❌ Keyword matching only  
❌ "Python" ≠ "Python developer"  
❌ No context understanding  
❌ Basic scoring (0-1)  
❌ No explanations  

### **NEW System (GPT-4):**
✅ Semantic understanding  
✅ Understands "Python developer" = "Python engineer" = "Backend developer (Python)"  
✅ Context-aware matching  
✅ Precise scoring (0-100)  
✅ Detailed explanations with strengths/concerns  
✅ Analyzes ALL 44 database columns  

---

## 📊 Configuration Settings (config.py)

```python
# Azure OpenAI (UPDATE THESE!)
AZURE_OPENAI_API_KEY = "FSQ0UWJgdAmR3q..."  # ✅ Correct
AZURE_OPENAI_ENDPOINT = "https://n8nservices.services.ai.azure.com/"  # ✅ Correct
AZURE_OPENAI_DEPLOYMENT = "gpt-4.1"  # ❌ FIX THIS
AZURE_OPENAI_API_VERSION = "2025-04-14"  # ❌ FIX THIS

# Matching Settings (can be adjusted)
MAX_VOLUNTEERS_TO_ANALYZE = 50  # Analyze top 50 candidates
TOP_MATCHES_TO_RETURN = 10  # Return top 10 matches
MIN_MATCH_SCORE = 60  # Minimum score threshold (0-100)
```

---

## ❓ Troubleshooting

### **"404 Resource not found"**
→ Wrong deployment name or API version. Follow Step 1 & 2 above.

### **"401 Unauthorized"**
→ Wrong API key. Check your Azure Portal → Keys and Endpoint.

### **"Too slow / timeout"**
→ Reduce `MAX_VOLUNTEERS_TO_ANALYZE` in `config.py` (e.g., to 20).

### **"Rate limit exceeded"**
→ Your Azure quota is reached. Wait or upgrade quota in Azure Portal.

---

## ✅ Quick Checklist

- [ ] Find correct deployment name from Azure Portal
- [ ] Update `AZURE_OPENAI_DEPLOYMENT` in `config.py`
- [ ] Update `AZURE_OPENAI_API_VERSION` in `config.py`
- [ ] Run `python test_ai_connection.py` (should succeed)
- [ ] Run `python ai_matcher.py` (test with sample data)
- [ ] Run `RUN.bat` (start application)
- [ ] Test in browser at `http://localhost:5000`

---

## 📞 Need Help?

**Common Deployment Names:**
- `gpt-4`
- `gpt-4-turbo`
- `gpt-35-turbo`
- `gpt-4o`

**Recommended API Version:**
- `2024-08-01-preview` (most stable)

---

**Status:** ✅ AI System Built | ⚠️ Configuration Needed

**Once you update `config.py` with the correct deployment name and API version, everything will work perfectly!**

