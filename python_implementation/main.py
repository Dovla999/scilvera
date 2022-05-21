import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "users.app:users", host="0.0.0.0", log_level="info", reload=True, port=8000
    )