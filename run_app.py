# pyrefly: ignore [missing-import]
import uvicorn
import os
import sys

if __name__ == '__main__':
    print("Starting IPL Win Probability Predictor Application...")
    print("Server URL: http://127.0.0.1:8000")
    print("Interactive API Docs: http://127.0.0.1:8000/docs")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
