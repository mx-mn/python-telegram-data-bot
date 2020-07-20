import pprint

from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup
from General import actual_db, init


class Question:
    def __init__(self, text=None,
                 question_id=None,
                 is_blocked=False,
                 is_custom=False,
                 keyboard=None):
        """Constructor with default values."""
        self.question_id = question_id
        self.text = text
        self.is_blocked = is_blocked
        self.is_custom = is_custom

        if keyboard is None:
            self.keyboard = [[]]
        else:
            self.keyboard = keyboard

    def set_key(self, text, x, y):
        if (y > len(self.keyboard)) or (x > len(self.Keyboard[y])):
            print("out of bounds")
        else:
            self.keyboard[x][y] = text

    def get_markup(self):
        if self.is_custom:
            return ReplyKeyboardMarkup(self.keyboard,
                                       one_time_keyboard=True)
        else:
            return None

    def sprint_keyboard(self):
        """Returns multi-line string of current keyboard."""
        ret = ''
        for row in self.keyboard:
            for key in row:
                ret += '[' + key + '] '
            ret += '\n'
        return ret


def question_dict_to_obj(question_dict):
    """Create a Question obj from database representation."""
    q = Question(text=question_dict["text"],
                 question_id=question_dict["question_id"],
                 is_blocked=question_dict["is_blocked"],
                 is_custom=question_dict["is_custom"],
                 keyboard=question_dict["keyboard"])
    return q


def question_obj_to_dict(question):
    """Create a database representation from Question obj ."""
    q = {
        "question_id": question.question_id,
        "text": question.text,
        "is_blocked": question.is_blocked,
        "is_custom": question.is_custom,
        "keyboard": question.keyboard,
    }
    return q


class Database:
    def __init__(self, connection_string, database_name,
                 collection_name):
        self.client = MongoClient(connection_string)
        self.database = self.client.get_database(database_name)
        self.collection = self.database[collection_name]

    def add_user(self, user):
        """Add a user obj to the Database."""
        u = \
            {
                "user_info": {
                    "chat_id": user.chat_id,
                    "notify_time": user.notify_time,
                    "questions": user.questions
                },
                "user_data": {}
            }
        self.collection.insert_one(u)

        print("DEBUG::add_user() user added to database with "
              "chat_id : " + str(user.chat_id))

    def add_question(self, question, chat_id):
        q = question_obj_to_dict(question)
        my_query = {"user_info.chat_id": chat_id}
        new_values = {"$push": {"user_info.questions": q}}

        self.collection.update_one(my_query, new_values)

        print("DEBUG::add_question() question added to database with "
              "chat_id : " +
              str(chat_id) + "and text " + question.text)

    def add_data_to_question(self, chat_id, question_id, data):
        """Append a data point to specified question in Database."""
        my_query = {"user_info.chat_id": chat_id}
        new_values = {
            "$push": {
                "user_data.questions." + str(question_id): data
            }
        }
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

    def user_exists(self, chat_id):
        """Returns True if the chat_id is already in the DB."""
        user = self.collection.find_one(
            {"user_info.chat_id": chat_id})
        return user is not None

    def get_all_users(self):
        """Returns a Dict of all user objects in the database."""
        users = {}
        for user_dict in self.collection.find():
            # create a user obj
            cid = user_dict["user_info"]["chat_id"]
            user_obj = User(cid, self.database)

            pprint.pprint(user_dict)

            for q_dict in user_dict["user_info"]["questions"]:
                q_obj = question_dict_to_obj(q_dict)

                # append in the questions array and insert in db
                user_obj.questions.append(q_obj)

            users[cid] = user_obj

        return users


class User:
    """Class user represents a unique chat."""

    def __init__(self, chat_id):
        """Initialise the unique chat_id and database."""
        self.chat_id = 0  # unique chat_id
        self.question_id = 0  # counter for max question id
        self.next_question = 0  # index of next question to ask
        self.prev_question = 0  # index of last asked question
        self.notify_time = None  # time of notification
        self.questions = []  # contains question objects
        self.temp_question = None  # container for question generation
        self.chat_id = chat_id  # unique chat_id
        print("user instance " + str(self.chat_id) + " created")

    def add_question(self, question):
        """Append question at end of question_list and database."""
        # add the running question id
        question.question_id = self.question_id

        # append in the questions array and insert in db
        self.questions.append(question)
        actual_db.add_question(question, self.chat_id)

        # inc question_id
        self.question_id += 1

    def get_next_question(self):
        """Return the question object from question_list."""
        while self.next_question < len(self.questions):

            # skip blocked questions
            if self.questions[self.next_question].is_blocked:
                self.next_question += 1

            # the first question that is not blocked is returned
            # indexes of prev and next question get updated
            else:
                ret = self.questions[self.next_question]
                self.prev_question = self.next_question
                self.next_question += 1
                return ret

        # exception on reaching EOF
        raise Exception("last question reached")

    def store_prev_question_response(self, response):
        """Store the user response in database."""
        prev_q = self.questions[self.prev_question]
        actual_db.add_data_to_question(self.chat_id,
                                           prev_q.question_id,
                                           response)


def test_add_questions_and_question_data():
    init()
    actual_db.collection.delete_many({})
    cid = 1234
    u1 = User(cid)
    actual_db.add_user(u1)
    q1 = Question("Q1", 0, False, False, None)
    q2 = Question("Q2", 1, False, False, None)
    q3 = Question("Q3", 2, False, False, None)
    actual_db.add_question(q1, cid)
    actual_db.add_question(q2, cid)
    actual_db.add_question(q3, cid)

    actual_db.add_data_to_question(cid, 0, "geeht so")
    actual_db.add_data_to_question(cid, 0, "verhaltensunauffällig")
    actual_db.add_data_to_question(cid, 0, "supi")
    actual_db.add_data_to_question(cid, 0, "schlecht so")

    actual_db.add_data_to_question(cid, 2, "Jugu")
    actual_db.add_data_to_question(cid, 2, "heruig")
    actual_db.add_data_to_question(cid, 2, "poirt")
    actual_db.add_data_to_question(cid, 2, "dafaso")

# test1()
# test_add_questions_and_question_data()
