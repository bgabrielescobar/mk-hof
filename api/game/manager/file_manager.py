import json

class FileManager:

    DB_PATH = "api/game/db"
    USERS_JSON= DB_PATH + "/users.json"

    # Obtain json data from file    
    def get_json(PATH_FILE):
        with open(PATH_FILE, 'r') as file:
            data = json.loads(file.read())
        return data