
class Response():
    def only_status(self, result):
        if result:
            return {"status": result}