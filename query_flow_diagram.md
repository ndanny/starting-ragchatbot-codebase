# RAG System Query Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                FRONTEND                                     │
│                              (script.js)                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                              1. User Input
                            (sendMessage())
                                    │
                                    ▼
                          ┌─────────────────┐
                          │  POST Request   │
                          │  /api/query     │
                          │                 │
                          │ {               │
                          │   query: "...", │
                          │   session_id    │
                          │ }               │
                          └─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               BACKEND                                       │
│                              (app.py)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                            2. FastAPI Endpoint
                           @app.post("/api/query")
                                    │
                                    ▼
                          ┌─────────────────┐
                          │  Create session │
                          │  if needed      │
                          └─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            RAG SYSTEM                                       │
│                          (rag_system.py)                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                            3. query() method
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Get conversation│
                          │ history from    │
                          │ SessionManager  │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Build prompt:   │
                          │ "Answer this    │
                          │ question about  │
                          │ course materials│
                          │ {query}"        │
                          └─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI GENERATOR                                      │
│                         (ai_generator.py)                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                         4. generate_response()
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Call Claude API │
                          │ with tools      │
                          │ enabled         │
                          └─────────────────┘
                                    │
                              Tool needed?
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
                   ┌─────────────┐         ┌─────────────┐
                   │    YES      │         │     NO      │
                   └─────────────┘         └─────────────┘
                        │                       │
                        ▼                       ▼
            ┌─────────────────────┐     ┌─────────────────┐
            │ Tool Execution      │     │ Direct Response │
            │                     │     │ from Claude     │
            │ CourseSearchTool    │     └─────────────────┘
            │ searches Vector     │             │
            │ Store (ChromaDB)    │             │
            │                     │             │
            │ Results fed back    │             │
            │ to Claude for       │             │
            │ final synthesis     │             │
            └─────────────────────┘             │
                        │                       │
                        └───────────┬───────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Final Response  │
                          │ + Sources       │
                          └─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                          5. Update conversation
                             history in session
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Return to       │
                          │ FastAPI:        │
                          │ (answer,        │
                          │  sources)       │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ JSON Response:  │
                          │ {               │
                          │   answer: "...", │
                          │   sources: [...],│
                          │   session_id    │
                          │ }               │
                          └─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                       │
│                            (script.js)                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                          6. Display response
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Remove loading  │
                          │ animation       │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Add AI message  │
                          │ to chat with    │
                          │ collapsible     │
                          │ sources         │
                          └─────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │ Re-enable input │
                          │ for next query  │
                          └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEY COMPONENTS                                    │
│                                                                             │
│ • Vector Store (ChromaDB): Semantic search of course materials             │
│ • Session Manager: Maintains conversation context                          │
│ • Document Processor: Chunks course content for retrieval                 │
│ • Tool System: Claude can search when needed                              │
│ • Sources Tracking: Shows which documents were referenced                  │
└─────────────────────────────────────────────────────────────────────────────┘
```