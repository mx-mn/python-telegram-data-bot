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
#        self.collection.delete_many({})

    def add_user(self, chat_id):
        temp_user = \
            {
                "chat_id": chat_id,
                "questions": []
            }
        self.collection.insert_one(temp_user)
        print("DEBUG user added to database with chat_id : " + str(
            chat_id))

    def add_question(self, chat_id, text, is_blocked, is_custom,
                     keyboard):
        new_question = {
            "text": text,
            "is_blocked": is_blocked,
            "is_custom": is_custom,
            "keyboard": keyboard,
            "data": []
        }

        my_query = {"chat_id": chat_id}
        new_values = {"$push": {"questions": new_question}}
        self.collection.update_one(my_query, new_values)
        print("DEBUG question added to database with chat_id : " +
              str(chat_id) + "and text " + text)

    def add_data_to_question(self, chat_id, question_id, response):
        my_query = {"chat_id": chat_id}
        new_values = {"$push": {"questions." + str(question_id) +
                                ".data": response}}

        self.collection.update_one(my_query, new_values)

    def change_question_attr(self, chat_id, question_id, attr,
                             new_val):
        my_query = {"chat_id": chat_id}
        new_values = {
            "$set":
                {"questions." + str(question_id) +
                 "." + str(attr): new_val
                 }
        }

        self.collection.update_one(my_query, new_values)

    # def get_user(self, chat_id):
    #   return self.collection.find_one({"chat_id": chat_id})

    def user_exists(self, chat_id):
        user = self.collection.find_one(
            {"chat_id": chat_id})
        return user is not None


def test():
    db = Database("mongodb+srv://MASTER:9NZc9agZd21YP9nL@cluster0"
                  ".umetu.azure.mongodb.net/mydatabase?retryWrites"
                  "=true&w=majority", "mydatabase",
                  "python_telegram_bot")

    db.collection.delete_many({})
    cid = 1234
    db.add_user(cid)
    db.add_question(cid, "wie gets?", False, False, None)
    db.add_question(cid, "wetter?", False, True, [["gut",
                                                   "schlecht"],
                                                  ["grandioso"]])

    print("user exists with chat_id" + str(cid))
    print(db.user_exists(cid))
    print("user exists with chat_id" + str(2345))
    print(db.user_exists(2345))

    db.add_data_to_question(cid, 0, "geeht so")
    db.add_data_to_question(cid, 0, "verhaltensunauffällig")
    db.add_data_to_question(cid, 0, "supi")
    db.add_data_to_question(cid, 0, "schlecht so")

test()
