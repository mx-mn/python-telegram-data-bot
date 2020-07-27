from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup

import iso8601

# actual_users: Dict[int, User]  # Dict[ chat_id : User_obj]
global actual_users
# actual_db: Database
global actual_db


def init(connection_string, database_name,
         collection_name):
    global actual_users
    global actual_db

    actual_db = Database(connection_string, database_name,
                         collection_name)

    # TODO: comment the reset
    # actual_db.collection.delete_many({})

    actual_users = actual_db.get_all_users()


def get_user(chat_id):
    """Returns the user object of the current update."""
    try:
        global actual_users
        u = actual_users[chat_id]
        return u

    except Exception as E:
        print(E)


def sprint_cmd_list(cmd_list):
    """Returns column of click-able commands from list."""
    try:
        ret = ''
        for cmd in cmd_list:
            ret += '/' + cmd + '\n'
        return ret
    except Exception as E:
        print(E)


def set_user(user):
    """Inserts user if not existing, otherwise overrides existing."""
    try:
        global actual_users
        actual_users[user.chat_id] = user
    except Exception as E:
        print(E)


class Question:
    def __init__(self, text=None,
                 question_id=None,
                 is_blocked=False,
                 is_custom=False,
                 keyboard=None):
        try:
            self.question_id = question_id
            self.text = text
            self.is_blocked = is_blocked
            self.is_custom = is_custom

            if keyboard is None:
                self.keyboard = [[]]
            else:
                self.keyboard = keyboard
        except Exception as E:
            print(E)

    def set_key(self, text, x, y):
        try:
            if (y > len(self.keyboard)) or (
                    x > len(self.keyboard[y])):
                print("out of bounds")
            else:
                self.keyboard[x][y] = text
        except Exception as E:
            print(E)

    def get_markup(self):
        try:
            if self.is_custom:
                return ReplyKeyboardMarkup(self.keyboard,
                                           one_time_keyboard=True)
            else:
                return None

        except Exception as E:
            print(E)

    def sprint_keyboard(self):
        """Returns multi-line string of current keyboard."""
        try:
            ret = ''
            for row in self.keyboard:
                for key in row:
                    ret += '[' + key + '] '
                ret += '\n'
            return ret

        except Exception as E:
            print(E)


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
        try:
            self.client = MongoClient(connection_string)
            self.database = self.client.get_database(database_name)
            self.collection = self.database[collection_name]

        except Exception as E:
            print(E)

    def set_notify_time(self, cid, notify_time):
        """Adds the notify_time to specified user"""
        try:
            my_query = {"user_info.chat_id": cid}
            print(notify_time.isoformat())
            new_values = \
                {
                    "$set": {"user_info.notify_time":
                                 notify_time.isoformat()}
                }
            self.collection.update_one(my_query, new_values)

        except Exception as E:
            print(E)

    def add_user(self, user):
        """Add a user obj to the Database."""
        try:
            u = \
                {
                    "user_info": {
                        "chat_id": user.chat_id,
                        "notify_time": None,
                        "questions": user.questions
                    },
                    "user_data": {}
                }
            self.collection.insert_one(u)

        except Exception as E:
            print(E)

    def add_question(self, question, chat_id):
        try:
            q = question_obj_to_dict(question)
            # add the new question
            my_query = {"user_info.chat_id": chat_id}
            new_values = {"$push": {"user_info.questions": q}}
            self.collection.update_one(my_query, new_values)

            # add the question id
            my_query = {"user_info.chat_id": chat_id}
            new_values = {"$set": {"user_info.question_id":
                                       question.question_id}}
            self.collection.update_one(my_query, new_values)

        except Exception as E:
            print(E)

    def add_data_to_question(self, chat_id, question_id, data):
        """Append a data point to specified question in Database."""
        try:
            my_query = {"user_info.chat_id": chat_id}
            new_values = \
                {
                    "$push":
                        {
                            "user_data." + str(question_id): data
                        }
                }
            self.collection.update_one(my_query, new_values)

        except Exception as E:
            print(E)

    def get_all_users(self):
        """Returns a Dict of all user objects in the database."""
        try:
            users = {}
            for user_dict in self.collection.find():
                # create a user obj
                cid = user_dict["user_info"]["chat_id"]
                user_obj = User(cid)

                #  TODO: also get notify_time from Database

                for q_dict in user_dict["user_info"]["questions"]:
                    q_obj = question_dict_to_obj(q_dict)

                    # append in the questions array and insert in db
                    user_obj.questions.append(q_obj)

                users[cid] = user_obj

            return users

        except Exception as E:
            print(E)


class User:
    """Class user represents a unique chat."""

    def __init__(self, chat_id):
        """Initialise the unique chat_id and database."""
        self.question_id = 0  # counter for max question id
        self.next_question = 0  # index of next question to ask
        self.prev_question = 0  # index of last asked question
        self.notify_time = None  # the utc time of notification
        self.timer_job = None  # timer_job for notification
        self.questions = []  # contains question objects
        self.temp_question = None  # container for question generation
        self.chat_id = chat_id  # unique chat_id
        print("user instance " + str(self.chat_id) + " created")

    def set_notify_time(self, notify_time):
        try:
            global actual_db
            self.timer_job = notify_time
            actual_db.set_notify_time(self.chat_id, notify_time)
        except Exception as E:
            print(E)

    def add_question(self, question):
        """Append question at end of question_list and database."""
        global actual_db
        try:
            # add the running question id
            question.question_id = self.question_id

            # append in the questions array and insert in db
            self.questions.append(question)
            actual_db.add_question(question, self.chat_id)
            self.question_id += 1

        except Exception as E:
            print(E)

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
        global actual_db

        try:
            prev_q = self.questions[self.prev_question]
            actual_db.add_data_to_question(self.chat_id,
                                           prev_q.question_id,
                                           response)
        except Exception as E:
            print(E)


def test_add_questions_and_question_data():
    init()
    global actual_db
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
"""Global Variables."""
