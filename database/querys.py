query = {
    "create table": {"param": False, "res": False, "sql": 'CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, actual_result INTEGER, last_result FLOAT)'},
    "get quiz":{"param": True, "res": True, "sql": 'SELECT question_index, actual_result FROM quiz_state WHERE user_id = (?)'},
    "update quiz":{"param": True, "res": False, "sql": 'INSERT OR REPLACE INTO quiz_state (user_id, question_index, actual_result) VALUES (?, ?, ?)'},
    "set result":{"param": True, "res": False, "sql": 'UPDATE quiz_state SET last_result = (?) WHERE user_id = (?)'},
    "get result":{"param": True, "res": True, "sql": 'SELECT last_result FROM quiz_state WHERE user_id == (?)'}
}