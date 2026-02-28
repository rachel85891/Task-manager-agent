import json
import os
from dotenv import load_dotenv
import openai
from to_do_service import add_task, get_tasks, update_task, delete_task

# הגדרת הלקוח (יש להזין מפתח API תקין)
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. הגדרת ה-Tools (הפונקציות שהמודל יכול להפעיל)
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "הוספת משימה חדשה לרשימה",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_data": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "כותרת המשימה"},
                            "description": {"type": "string", "description": "תיאור המשימה"},
                            "type": {"type": "string", "description": "סוג המשימה (עבודה, אישי וכו')"},
                            "start_date": {"type": "string", "description": "תאריך התחלה"},
                            "end_date": {"type": "string", "description": "תאריך סיום"},
                            "status": {"type": "string", "description": "סטטוס המשימה (פתוח, בביצוע, הושלם)"}
                        },
                        "required": ["title"]
                    }
                },
                "required": ["task_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "שליפת משימות לפי סינונים אופציונליים",
            "parameters": {
                "type": "object",
                "properties": {
                    "filters": {
                        "type": "object",
                        "description": "מילון סינונים (למשל לפי status או type)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "עדכון משימה קיימת לפי ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ה-ID של המשימה"},
                    "updates": {"type": "object", "description": "השדות לעדכון"}
                },
                "required": ["task_id", "updates"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "מחיקת משימה מהרשימה לפי ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ה-ID של המשימה"}
                },
                "required": ["task_id"]
            }
        }
    }
]

# מיפוי שמות הפונקציות לפונקציות האמיתיות בקוד
available_functions = {
    "add_task": add_task,
    "get_tasks": get_tasks,
    "update_task": update_task,
    "delete_task": delete_task,
}


def run_agent(user_query: str):
    # שלב 1: שליחת השאילתה ל-LLM עם הגדרת הכלים
    messages = [
        {"role": "system", "content": "אתה עוזר אישי חכם לניהול משימות. ענה בעברית מנומסת וידידותית."},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # או gpt-3.5-turbo
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # שלב 2: בדיקה האם המודל רוצה להפעיל פונקציה
    if tool_calls:
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            # הרצת הפונקציה הלוגית מה-todo_service
            print(f"DEBUG: מפעיל פונקציה {function_name} עם {function_args}")
            function_response = function_to_call(**function_args)

            # הוספת התוצאה להיסטוריית ההודעות
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response, ensure_ascii=False),
            })

        # שלב 3: פנייה חוזרת ל-LLM כדי לנסח תשובה סופית למשתמש
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return second_response.choices[0].message.content

    return response_message.content


# דוגמה להרצה

if __name__ == "__main__":
    print(run_agent("תוסיף לי משימה לקנות פרחים לשבת בסטטוס פתוח"))
    print(run_agent("איזה משימות יש לי?"))
