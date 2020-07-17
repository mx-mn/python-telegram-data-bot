from ClassQuestion import Question
from ClassDB import Database


class User:
    database = None
    chat_id = 0
    next_question = 0
    prev_question = 0
    notifying = False
    notify_time = 0

    def __init__(self, chat_id, database):
        self.chat_id = chat_id
        self.database = database
        self.next_question = 0
        print("user created")

    def add_question(self, question):
        """Append question at end of question_list and database."""
        self.database.add_question(self.chat_id,
                                   question.text,
                                   question.is_blocked,
                                   question.is_custom,
                                   question.keyboard)

    def get_next_question(self):
        """Return the question object from question_list."""
        user = self.database.get_user(self.chat_id)

        # skip blocked questions
        while user["questions"][self.next_question]["is_blocked"]:
            self.next_question += 1

        # remember index of previous non blocked question
        self.prev_question = self.next_question

        if self.next_question < len(user["questions"]):
            question = Question()
            question.text = user["questions"][
                self.next_question]["text"]
            question.keyboard = user["questions"][
                self.next_question]["keyboard"]
            question.is_custom = user["questions"][
                self.next_question]["is_custom"]
            question.is_blocked = user["questions"][
                self.next_question]["is_blocked"]
            question.id = self.next_question

            self.next_question += 1
            return question

        else:
            raise Exception("last question reached")

    def store_response(self, response):
        """store the user response in corresponding question."""
        self.database.add_data_to_question(self.chat_id,
                                           self.prev_question,
                                           response)

    def block_question(self, question_pos):
        self.database.change_question_attr(self.chat_id,
                                           question_pos,
                                           "is_blocked", True)

    def unblock_question(self, question_pos):
        self.database.change_question_attr(self.chat_id,
                                           question_pos,
                                           "is_blocked", False)

# TESTING
def test():

    db = Database("mongodb+srv://MASTER:9NZc9agZd21YP9nL@cluster0.umetu"
                  ".azure.mongodb.net/mydatabase?retryWrites=true&w"
                  "=majority", "mydatabase", "python_telegram_bot")

    db.collection.delete_many({})
    user1 = User("h39834t0", db)
    user2 = User("13501253", db)


    db.add_user(user1.chat_id)
    db.add_user(user2.chat_id)

    text1 = "Frage 1?"
    text2 = "Frage 2?"
    text3 = "Frage 3?"
    text4 = "Frage 4?"

    db.add_question(user1.chat_id, "blocked Question 1 with custom?",
                    True, True, [["button"],["button"]])
    db.add_question(user1.chat_id, "unblocked Question 2 ?",
                    False, False, [[]])
    db.add_question(user1.chat_id, "not blcoked Question with custom",
                    False, True, [["button", "butti!"],["button"]])
    db.add_question(user1.chat_id, "blocked Question §?",
                    True, False, [[]])

    db.add_question(user2.chat_id, "not blocked Question",
                    False, False, [[]])
    db.add_question(user2.chat_id, "not blocked Question with "
                                   "custom keyboard",
                    False, True, [["button1"]])

    db.add_question(user2.chat_id, "not blocked Question",
                    False, False, [[]])
    db.add_question(user2.chat_id, "not blocked Question with "
                                   "custom keyboard",
                    False, True, [["button1"]])
    while True:
        try:
            q = user1.get_next_question()
            user1.store_response("response")
            print(q.text)
        except:
            break

    while True:
        try:
            q = user2.get_next_question()
            user2.store_response("response")
            print(q.text)
        except:
            break

    user2.block_question(2)

    while True:
        try:
            q = user2.get_next_question()
            user2.store_response("response")
            print(q.text)
        except:
            break

# test()
