# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Starting the Application
```bash
# Quick start (recommended)
./run.sh

# Manual start
cd backend && uv run uvicorn app:app --reload --port 8000
```

### Development Setup
```bash
# Install dependencies
uv sync

# Create environment file
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

### Dependency Management
**Always use `uv` for all dependency management - never use `pip` directly:**
```bash
# Add dependencies
uv add <package>

# Remove dependencies  
uv remove <package>

# Sync/install dependencies
uv sync
```

### Access Points
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Architecture Overview

This is a **Retrieval-Augmented Generation (RAG) system** that enables querying of course materials using semantic search and AI-powered responses.

### Core Architecture Pattern

The system follows a **tool-enabled RAG architecture** where Claude AI can dynamically search course materials:

```
Frontend (Vanilla JS) → FastAPI → RAG System → AI Generator
                                      ↓
                              Tool Manager → Vector Store (ChromaDB)
```

### Key Components and Interactions

**RAG System (`rag_system.py`)**: Central orchestrator that coordinates all components:
- Manages document ingestion and chunking
- Handles query processing with conversation context
- Coordinates between AI generation and vector search

**AI Generator (`ai_generator.py`)**: Claude API integration with tool support:
- Uses tool-enabled Claude calls with `CourseSearchTool`
- Handles tool execution flow: Claude → tool call → results → final response
- Maintains conversation context across exchanges

**Vector Store (`vector_store.py`)**: ChromaDB-based semantic search:
- Stores both course metadata and content chunks
- Provides semantic similarity search with configurable results
- Supports course name matching and lesson filtering

**Tool System (`search_tools.py`)**: Implements searchable tools for Claude:
- `CourseSearchTool`: Smart semantic search with course/lesson filtering
- Tool definitions follow Anthropic's tool calling specification
- Tracks sources for response attribution

**Document Processor (`document_processor.py`)**: Text processing pipeline:
- Extracts course structure (title, lessons) from transcript files
- Creates semantic chunks with overlap for better retrieval
- Handles course metadata extraction and standardization

### Data Flow Architecture

**Query Processing**: User query → session context → Claude with tools → dynamic vector search (if needed) → synthesized response

**Document Ingestion**: Course files → structured extraction → chunking → vector embeddings → ChromaDB storage

### Configuration System

Centralized config in `config.py` using environment variables:
- `ANTHROPIC_API_KEY`: Required for Claude API
- `ANTHROPIC_MODEL`: Currently "claude-sonnet-4-20250514" 
- Chunking parameters: `CHUNK_SIZE=800`, `CHUNK_OVERLAP=100`
- Vector search: `MAX_RESULTS=5`, embedding model "all-MiniLM-L6-v2"

### Session Management

Conversation state managed in `session_manager.py`:
- Tracks conversation history with `MAX_HISTORY=2` exchanges
- Session IDs generated automatically for new conversations
- Provides context for follow-up questions

### Frontend Integration

Vanilla JavaScript client (`frontend/script.js`):
- RESTful API communication with `/api/query` and `/api/courses` endpoints
- Real-time chat interface with loading states
- Source attribution display with collapsible details

## Important Implementation Details

### Tool-First Search Strategy
The system uses Claude's tool calling rather than pre-retrieval. Claude decides when to search based on query context, enabling more intelligent retrieval patterns.

### Vector Store Collections
ChromaDB maintains separate collections for metadata and content, allowing different search strategies for course discovery vs. content retrieval.

### Course File Processing
Expects course transcript files in `/docs/` folder. Files are processed for structure (lessons) and chunked semantically rather than by fixed boundaries.

### Error Handling
The system includes comprehensive error handling for document processing, API failures, and vector store operations with graceful degradation.