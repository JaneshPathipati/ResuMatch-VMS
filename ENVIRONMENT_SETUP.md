# 🔐 Environment Setup Guide

## Overview

ResuMatch VMS uses **environment variables** to manage sensitive configuration like API keys and database passwords. This keeps your credentials safe and out of version control.

---

## 📁 Configuration Files

### `.env` (Local Only - NOT in Git)
- Contains your actual credentials and configuration
- **NEVER commit this file to Git** (already in `.gitignore`)
- Each developer/deployment has their own `.env` file

### `.env.example` (Template - IN Git)
- Template showing required environment variables
- Has placeholder values instead of real credentials
- Committed to Git for documentation

### `config.py` (Code - NOT in Git)
- Python code that loads variables from `.env`
- Uses `python-dotenv` library
- **NEVER commit this file to Git** (already in `.gitignore`)

---

## 🚀 Setup Instructions

### 1. Copy the Template

```bash
# On Windows PowerShell
Copy-Item .env.example .env

# On Mac/Linux
cp .env.example .env
```

### 2. Edit `.env` File

Open `.env` and replace placeholder values with your actual credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_actual_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-01-01-preview

# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=resumatch_db
MYSQL_USERNAME=root
MYSQL_PASSWORD=your_actual_mysql_password
MYSQL_USE_SSL=False
```

### 3. Verify Configuration

Test that your configuration loads correctly:

```bash
python -c "import config; print('✅ Config loaded successfully')"
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep `.env` file local and secure
- Add `.env` to `.gitignore` (already done)
- Use `.env.example` for documentation
- Use different credentials for development/production
- Rotate API keys regularly

### ❌ DON'T:
- Never commit `.env` to Git
- Never share `.env` file via email/chat
- Never hardcode credentials in code
- Never log or print sensitive values
- Never commit `config.py` with real credentials

---

## 🌍 Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | `FSQ0UWJgdAmR...` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | `https://xxx.cognitiveservices.azure.com/` |
| `MYSQL_PASSWORD` | MySQL database password | `SecurePass123` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_TYPE` | `mysql` | Database type: `mysql` or `sqlite` |
| `MYSQL_HOST` | `localhost` | MySQL server host |
| `MYSQL_PORT` | `3306` | MySQL server port |
| `MYSQL_DATABASE` | `resumatch_db` | MySQL database name |
| `MYSQL_USERNAME` | `root` | MySQL username |
| `MAX_VOLUNTEERS_TO_ANALYZE` | `50` | Number of volunteers to analyze |
| `TOP_MATCHES_TO_RETURN` | `10` | Number of top matches to return |
| `MIN_MATCH_SCORE` | `60` | Minimum match score threshold |

---

## 🔧 Troubleshooting

### Error: "AZURE_OPENAI_API_KEY is not set in .env file!"

**Solution:** Make sure:
1. `.env` file exists in project root
2. `AZURE_OPENAI_API_KEY=your_key` is in `.env` (no spaces around `=`)
3. Your key is not empty

### Error: "No such file or directory: '.env'"

**Solution:** Create `.env` by copying `.env.example`:
```bash
cp .env.example .env
```

### Error: "MYSQL_PASSWORD is not set in .env file!"

**Solution:** Add your MySQL password to `.env`:
```env
MYSQL_PASSWORD=your_actual_password
```

---

## 📦 Deployment

### Local Development
- Use `.env` file (already configured)

### Production Server
- Set environment variables via server configuration
- Don't upload `.env` file to server
- Use server's environment variable system

### Docker
- Use `.env` file with `docker-compose`
- Or pass via `docker run -e VAR=value`

### Cloud Platforms
- **Heroku**: Use `heroku config:set VAR=value`
- **AWS**: Use Systems Manager Parameter Store or Secrets Manager
- **Azure**: Use App Settings or Key Vault
- **Google Cloud**: Use Secret Manager

---

## ✅ Verification Checklist

- [ ] `.env` file created from `.env.example`
- [ ] All required variables filled in `.env`
- [ ] `.env` is in `.gitignore`
- [ ] `config.py` is in `.gitignore`
- [ ] Configuration test passes
- [ ] Application runs successfully

---

## 🆘 Need Help?

If you're having trouble with environment setup:

1. Check that `.env` file exists in project root
2. Verify all required variables are set
3. Make sure there are no typos in variable names
4. Run the verification command above
5. Check the application logs for specific error messages

---

**Remember: Your `.env` file is like your house key - keep it safe and never share it! 🔐**

