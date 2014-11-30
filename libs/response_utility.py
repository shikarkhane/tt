import json

class Response():
    def only_status(self, result):
        if result:
            return json.dumps({"status": result})