from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_service import run_agent

# 1. אתחול האפליקציה
app = FastAPI(title="Todo AI Agent API")

# 2. הגדרת CORS - מאפשר לאפליקציית React (או כל מקור אחר) לגשת לשרת
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # בסביבת ייצור כדאי להגביל לדומיין הספציפי של ה-React
    allow_credentials=True,
    allow_methods=["*"],  # מאפשר את כל סוגי הבקשות (GET, POST, וכו')
    allow_headers=["*"],
)


# 3. הגדרת המודל עבור גוף הבקשה (Request Body)
class ChatRequest(BaseModel):
    message: str


# 4. ה-Endpoint הראשי לתקשורת עם ה-Agent
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # שליחת הודעת המשתמש ל-Agent שמימשנו ב-agent_service
        user_message = request.message
        agent_response = run_agent(user_message)

        return {
            "status": "success",
            "response": agent_response
        }
    except Exception as e:
        # במקרה של שגיאה (למשל בעיית תקשורת עם ה-LLM)
        raise HTTPException(status_code=500, detail=str(e))


# 5. נקודת קצה לבדיקת תקינות השרת
@app.get("/health")
def health_check():
    return {"status": "up and running"}


if __name__ == "__main__":
    import uvicorn

    # הרצת השרת בפורט 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)