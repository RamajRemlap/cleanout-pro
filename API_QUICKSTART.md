# CleanoutPro API Quick Start Guide

## Step 1: Start the Backend Server

### Option A: Using VSCode FastAPI Extension (Recommended)
Since you have the VSCode FastAPI extension installed:

1. Open VSCode in the `backend` folder
2. Open `api/main.py`
3. Look for the FastAPI extension icon in the sidebar
4. Click "Start Server" or use the command palette

### Option B: Using Command Line

```bash
cd backend

# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Server will start at:** http://localhost:8000

## Step 2: Verify Server is Running

Open your browser and visit:

- **API Root:** http://localhost:8000
- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

You should see the API documentation interface.

## Step 3: Create a Test Customer

Before you can create jobs, you need a customer:

```bash
cd backend
python create_test_customer.py
```

This will output a **Customer ID** - copy it! You'll need it for creating jobs.

Example output:
```
============================================================
Customer ID: 550e8400-e29b-41d4-a716-446655440000
============================================================
```

## Step 4: Test the API

### Method 1: Using the Interactive Docs (Easiest)

1. Go to http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute"
6. See the response!

**Recommended first tests:**
1. `GET /` - Health check
2. `GET /api/jobs` - List jobs (should be empty initially)
3. `POST /api/jobs` - Create a job (use customer ID from Step 3)
4. `GET /api/jobs/{job_id}` - Get job details

### Method 2: Using the Test Script

```bash
cd backend
python test_api_endpoints.py
```

This runs automated tests on all endpoints.

### Method 3: Using curl or Postman

**Example: Create a Job**
```bash
curl -X POST "http://localhost:8000/api/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "YOUR-CUSTOMER-ID-HERE",
    "property_address": "456 Oak Avenue, Somewhere, USA",
    "notes": "Full house cleanout"
  }'
```

**Example: List All Jobs**
```bash
curl http://localhost:8000/api/jobs
```

**Example: Get Job by ID**
```bash
curl http://localhost:8000/api/jobs/{job_id}
```

## Step 5: Test Complete Workflow

### 5.1 Create a Job
```bash
POST /api/jobs
{
  "customer_id": "YOUR-CUSTOMER-ID",
  "property_address": "123 Main St",
  "notes": "Estate cleanout"
}
```

Response will include `job_id` - copy it!

### 5.2 Get Job Estimate
```bash
GET /api/jobs/{job_id}/estimate
```

Initially shows $0 (no rooms added yet).

### 5.3 Add a Room (Upload Image)
```bash
POST /api/rooms
Form Data:
  - job_id: YOUR-JOB-ID
  - room_name: Master Bedroom
  - room_number: 1
  - image: [select image file]
```

This will:
- Upload the image
- Run AI classification (if Ollama is running)
- Calculate pricing
- Return room details

### 5.4 Check Updated Estimate
```bash
GET /api/jobs/{job_id}/estimate
```

Now shows the calculated cost!

### 5.5 Human Override (Optional)
```bash
PATCH /api/rooms/{room_id}
{
  "human_size_class": "large",
  "human_workload_class": "heavy",
  "human_override_reason": "Photo didn't show full extent of clutter"
}
```

This recalculates the price based on human judgment.

### 5.6 Update Job Status
```bash
PATCH /api/jobs/{job_id}
{
  "status": "approved",
  "human_adjusted_estimate": 1250.00
}
```

## Available Endpoints

### Jobs Endpoints
- `GET /api/jobs` - List all jobs (with filtering)
- `POST /api/jobs` - Create new job
- `GET /api/jobs/{job_id}` - Get job details
- `PATCH /api/jobs/{job_id}` - Update job
- `DELETE /api/jobs/{job_id}` - Delete job
- `GET /api/jobs/{job_id}/estimate` - Get pricing estimate

### Rooms Endpoints
- `GET /api/rooms` - List rooms (filterable by job_id)
- `POST /api/rooms` - Upload room image
- `GET /api/rooms/{room_id}` - Get room details
- `PATCH /api/rooms/{room_id}` - Override AI classification
- `DELETE /api/rooms/{room_id}` - Delete room
- `POST /api/rooms/{room_id}/reprocess` - Re-run AI classification

### System Endpoints
- `GET /` - API info
- `GET /health` - Health check

## Testing AI Vision (Optional)

To test AI room classification, you need Ollama + LLaVA:

### Install Ollama
1. Download from https://ollama.ai
2. Install and start Ollama
3. Pull LLaVA model:
   ```bash
   ollama pull llava:7b
   ```

### Test AI Classification
Once Ollama is running, upload a room image via:
```bash
POST /api/rooms
```

The AI will automatically classify:
- Room size (small/medium/large/extra_large)
- Workload difficulty (light/moderate/heavy/extreme)
- Calculate pricing
- Provide confidence score and reasoning

## Troubleshooting

### Server won't start
```bash
# Check if port 8000 is already in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Mac/Linux

# Try a different port
python -m uvicorn api.main:app --port 8001
```

### Database connection errors
```bash
# Check .env file has correct DATABASE_URL
cat backend/.env  # Mac/Linux
type backend\.env  # Windows

# Test database connection
python test_db_connection.py
```

### ModuleNotFoundError
```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies if needed
pip install -r requirements.txt
```

### AI classification not working
```bash
# Check Ollama is running
ollama list

# Pull LLaVA if not installed
ollama pull llava:7b

# Check Ollama URL in .env
# Should be: OLLAMA_URL=http://localhost:11434
```

## Example API Workflow

Here's a complete example workflow using curl:

```bash
# 1. Create customer (do this once)
python create_test_customer.py
# Copy the customer ID

# 2. Create a job
curl -X POST http://localhost:8000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUSTOMER-ID-HERE",
    "property_address": "789 Pine St, Anytown, USA"
  }'
# Copy the job_id from response

# 3. Check initial estimate
curl http://localhost:8000/api/jobs/JOB-ID-HERE/estimate

# 4. Add rooms with images (use Swagger UI or Postman for file uploads)

# 5. Check updated estimate
curl http://localhost:8000/api/jobs/JOB-ID-HERE/estimate

# 6. Update job status
curl -X PATCH http://localhost:8000/api/jobs/JOB-ID-HERE \
  -H "Content-Type: application/json" \
  -d '{"status": "approved"}'

# 7. List all jobs
curl http://localhost:8000/api/jobs
```

## Next Steps

1. ✅ Start the server
2. ✅ Create a test customer
3. ✅ Test endpoints via Swagger UI
4. ⬜ Install Ollama for AI features
5. ⬜ Build the mobile app (React Native)
6. ⬜ Build the desktop app (Electron + React)
7. ⬜ Set up PayPal integration

## API Documentation

- **Live API Docs:** http://localhost:8000/docs (when server running)
- **OpenAPI Schema:** http://localhost:8000/openapi.json
- **Project README:** ../README.md
- **Database Setup:** ../DATABASE_SETUP.md

---

**Happy Testing! 🚀**
