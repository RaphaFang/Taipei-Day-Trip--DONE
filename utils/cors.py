from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://raphaelfang.com",
    "http://raphaelfang.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000", 
    "http://127.0.0.1:5501",
    "https://52.4.229.207",
    "http://52.4.229.207",
    ]

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )