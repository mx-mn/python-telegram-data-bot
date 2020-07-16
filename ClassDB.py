from pymongo import MongoClient

# mongodb+srv://MASTER:9NZc9agZd21YP9nL@cluster0.umetu.azure.mongodb.net/mydatabase?retryWrites=true&w=majority


class Database:
    client = None
    database = None
    collection = None

    def __init__(self, connection_string, database_name,
                 collection_name):
        self.client = MongoClient(connection_string)
        self.database = self.client.get_database(database_name)
        self.collection = self.database[collection_name]

    def add_user(self, chat_id):
        u = \
            {
                "chat_id": chat_id,
                "questions": {}
            }
        self.collection.insert_one(u)

    def add_question(self, chat_id, text, is_blocked, is_custom,
                     keyboard):
        new_question = \
            {
                text:
                {
                    "text": text,
                    "is_blocked": is_blocked,
                    "is_custom": is_custom,
                    "keyboard": keyboard,
                    "data": []
                }
            }
        my_query = {"chat_id": chat_id}
        new_values = {"$set": {"questions." + text: new_question}}
        self.collection.update_one(my_query, new_values)

    def add_data_to_question(self, chat_id, question_text, response):
        my_query = {"chat_id": chat_id}
        new_values = {"$push": {"questions." + question_text +
                                ".data": response}}

        self.collection.update_one(my_query, new_values)
