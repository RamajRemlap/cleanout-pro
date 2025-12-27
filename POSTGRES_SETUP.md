# PostgreSQL Setup Guide - Docker Alternative

## Problem
Docker commands are hanging on this system. We need PostgreSQL to test the CleanoutPro API.

## Solution Options

### Option 1: Install PostgreSQL for Windows (Recommended - 5 minutes)

1. **Download PostgreSQL 15**
   - Go to: https://www.postgresql.org/download/windows/
   - Download and run the installer
   - Or direct link: https://sbp.enterprisedb.com/getfile.jsp?fileid=1258649

2. **Installation Settings**
   - Password: `cleanout_dev_password`
   - Port: `5432`
   - Accept other defaults

3. **Create Database**
   ```powershell
   # Open PowerShell and run:
   cd "C:\Program Files\PostgreSQL\15\bin"
   .\psql.exe -U postgres

   # In psql prompt:
   CREATE DATABASE cleanoutpro;
   CREATE USER cleanout WITH PASSWORD 'cleanout_dev_password';
   GRANT ALL PRIVILEGES ON DATABASE cleanoutpro TO cleanout;
   \q
   ```

4. **Test Connection**
   ```bash
   cd C:\Users\Jeles\OneDrive\Documents\GitHub\cleanout-pro\backend
   python create_test_data.py
   ```

---

### Option 2: Use Free Cloud Database (Fastest - 2 minutes)

**Neon.tech (Free Tier)**

1. Go to https://neon.tech/ and sign up (GitHub login works)
2. Create new project: "cleanoutpro"
3. Copy connection string (looks like: `postgresql://user:pass@host/dbname`)
4. Update backend/.env:
   ```
   DATABASE_URL=postgresql://your-connection-string-here
   ```
5. Run test data script:
   ```bash
   cd C:\Users\Jeles\OneDrive\Documents\GitHub\cleanout-pro\backend
   python create_test_data.py
   ```

---

### Option 3: Fix Docker (If you want to debug)

**Diagnostic Steps:**

1. **Restart Docker Desktop**
   - Close Docker Desktop completely
   - Open Task Manager → End all Docker processes
   - Restart Docker Desktop
   - Wait 2-3 minutes for full startup

2. **Check WSL 2**
   ```powershell
   wsl --status
   wsl --update
   ```

3. **Check Docker Settings**
   - Open Docker Desktop
   - Settings → Resources → WSL Integration
   - Enable for your distros
   - Apply & Restart

4. **Try PostgreSQL again**
   ```bash
   cd C:\Users\Jeles\OneDrive\Documents\GitHub\cleanout-pro
   docker-compose up -d postgres
   ```

---

## Current Status

✅ Backend code complete (all 12 API endpoints)
✅ API running on http://localhost:8001
✅ Test data script ready
❌ PostgreSQL not accessible (Docker issue)

## Next Steps

1. Choose one of the options above
2. Once PostgreSQL is running, test with:
   ```bash
   cd C:\Users\Jeles\OneDrive\Documents\GitHub\cleanout-pro\backend
   python create_test_data.py
   ```
3. API will be fully testable at http://localhost:8001/docs

## Quick Test (Without Database)

To verify API structure without database:
```bash
cd C:\Users\Jeles\OneDrive\Documents\GitHub\cleanout-pro\backend
python test_api_structure.py
```

This confirms all code is valid and imports work correctly.
