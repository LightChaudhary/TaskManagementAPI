from fastapi import FastAPI

app = FastAPI(title="SWE project")

@app.get("/")
def root() -> dict:
    return {"message" : "Hello!, Prakash"}
