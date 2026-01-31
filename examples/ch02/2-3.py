from fastapi import FastAPI, Depends

app = FastAPI()

def paginate(skip: int = 0, limit: int = 10):
    return {"skip" : skip, "limit": limit }

@app.get("/messages")
def list_messages_controller(pagination: dict = Depends(paginate)):
    return pagination

@app.get("/conversations")
def list_conversations_controller(pagination: dict = Depends(paginate)):
    return pagination