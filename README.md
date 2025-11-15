# News Generator

A web application that searches for news using Perplexity AI, allows you to curate and group sources, and generates professional news articles using OpenRouter (with various LLM providers).

## Features

- **Smart Search**: Use Perplexity AI to search for news with advanced filters
- **Source Curation**: Select and organize search results
- **Link Grouping**: Combine multiple sources for comprehensive articles
- **AI Generation**: Generate professional news articles using OpenRouter
- **Job Queue**: Background processing with Celery and Redis
- **Configurable**: Custom prompts, token limits, and model selection

## Tech Stack

### Backend
- FastAPI (Python)
- Celery (job queue)
- Redis (message broker)
- Perplexity API (search)
- OpenRouter API (LLM generation)

### Frontend
- React + TypeScript
- Vite (build tool)
- Tailwind CSS
- Axios (HTTP client)

## Prerequisites

- Python 3.11+
- Node.js 20+
- Redis Cloud account (free tier)
- Perplexity API key
- OpenRouter API key

## Installation

### 1. Clone or navigate to the project

```bash
cd news-generator
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env

# Edit .env and add your API keys:
# - PERPLEXITY_API_KEY=your_key_here
# - OPENROUTER_API_KEY=your_key_here
# - REDIS_URL=your_redis_cloud_url
```

### 3. Redis Cloud Setup

1. Go to https://redis.com/try-free/
2. Create a free account
3. Create a new database
4. Copy the connection string (format: `redis://default:password@host:port`)
5. Add it to your `.env` file as `REDIS_URL`

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
```

## Running the Application

You need to run 3 services:

### Terminal 1: Backend API

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

python -m uvicorn app.main:app --reload --port 8000
```

Backend will run at: http://localhost:8000

### Terminal 2: Celery Worker

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

celery -A app.core.celery_app worker --loglevel=info --pool=solo
```

Note: `--pool=solo` is required for Windows. On Mac/Linux you can remove it.

### Terminal 3: Frontend

```bash
cd frontend
npm run dev
```

Frontend will run at: http://localhost:5173

## Usage

1. **Search for News**
   - Enter your search query
   - Optionally configure advanced filters (time range, country, language, etc.)
   - Click "Search"

2. **Review Results**
   - Browse the search results
   - Select individual URLs by checking their boxes
   - OR create groups of related URLs:
     - Click "Create Group"
     - Select 2+ URLs
     - Give the group a name (optional)
     - Click "Save Group"

3. **Configure Generation (Optional)**
   - Click "Configure" in the Settings panel
   - Add custom prompt instructions
   - Adjust max tokens per note
   - Select preferred LLM model

4. **Generate Notes**
   - Click "Generate Notes"
   - Wait for processing (you'll see progress)
   - Review generated articles
   - Copy to clipboard as needed

## Limits

- Maximum 5 notes per generation (individual URLs + groups)
- Default 8000 tokens per note (configurable up to 16000)
- Maximum 50 search results per query

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
news-generator/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── services/      # External service integrations
│   │   ├── models/        # Pydantic schemas
│   │   ├── core/          # Config, Celery, tasks
│   │   └── main.py        # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── types/         # TypeScript types
│   │   └── App.tsx        # Main app
│   ├── package.json
│   └── .env
└── README.md
```

## Troubleshooting

### Backend won't start
- Check that your virtual environment is activated
- Verify all API keys in `.env` are correct
- Ensure Redis URL is properly formatted

### Celery worker fails
- On Windows, make sure to use `--pool=solo`
- Check Redis connection
- Verify Redis Cloud database is running

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify `VITE_API_URL` in frontend `.env`

### Generation fails
- Check OpenRouter API key is valid
- Verify you have credits in your OpenRouter account
- Check Celery worker logs for errors

## Cost Considerations

- **Perplexity**: Charged per API request
- **OpenRouter**: Charged per token (varies by model)
- **Redis Cloud**: Free tier includes 30MB (sufficient for this app)

Monitor your usage in each service's dashboard.

## Future Enhancements

- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Save and export generated notes
- [ ] Streaming generation (real-time output)
- [ ] Jina AI integration (full content extraction)
- [ ] Better error handling and retry logic
- [ ] Cost tracking dashboard
- [ ] Export to various formats (PDF, Word, Markdown)

## License

MIT

## Support

For issues or questions, please open an issue in the GitHub repository.
