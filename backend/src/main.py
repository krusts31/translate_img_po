from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {'msg': 'Hello World'}


@app.get("/api/{s}")
def homepage(s: int):
    return {"message": s * s}

if __name__ == "__main__":
    uvicorn.run(app)
