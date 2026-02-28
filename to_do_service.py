# רשימה גלובלית לאחסון המשימות
tasks = []
# משתנה עזר ליצירת מזהה ייחודי (ID) רץ
_next_id = 1


def add_task(task_data: dict) -> dict:
    """
    מוסיפה משימה חדשה לרשימה ומייצרת לה ID אוטומטי.
    מצפה למילון עם השדות: title, description, type, start_date, end_date, status.
    """
    global _next_id

    new_task = {
        "id": _next_id,
        "title": task_data.get("title"),
        "description": task_data.get("description"),
        "type": task_data.get("type"),
        "start_date": task_data.get("start_date"),
        "end_date": task_data.get("end_date"),
        "status": task_data.get("status")
    }

    tasks.append(new_task)
    _next_id += 1
    return new_task


def get_tasks(filters: dict = None) -> list:
    """
    מחזירה את רשימת המשימות. ניתן לסנן לפי שדות ספציפיים.
    לדוגמה: filters={'status': 'completed'}
    """
    if not filters:
        return tasks

    filtered_tasks = []
    for task in tasks:
        match = True
        for key, value in filters.items():
            if task.get(key) != value:
                match = False
                break
        if match:
            filtered_tasks.append(task)

    return filtered_tasks


def update_task(task_id: int, updates: dict) -> bool:
    """
    מעדכנת משימה קיימת לפי ה-ID שלה.
    מחזירה True אם העדכון הצליח, אחרת False.
    """
    for task in tasks:
        if task["id"] == task_id:
            task.update(updates)
            return True
    return False


def delete_task(task_id: int) -> bool:
    """
    מוחקת משימה מהרשימה לפי ה-ID שלה.
    מחזירה True אם המחיקה הצליחה.
    """
    global tasks
    initial_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    return len(tasks) < initial_length


# --- דוגמת שימוש קצרה ---
"""
if __name__ == "__main__":
    # הוספה
    add_task({"title": "ללמוד פייתון", "status": "בביצוע", "type": "לימודים"})
    add_task({"title": "לקנות חלב", "status": "פתוח", "type": "בית"})

    # סינון
    print("משימות פתוחות:", get_tasks({"status": "פתוח"}))

    # עדכון
    update_task(1, {"status": "הושלם"})

    # מחיקה
    delete_task(2)

    print("רשימה סופית:", tasks)
"""