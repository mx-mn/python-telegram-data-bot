from ClassQuestion import Question
from ClassDB import Database


class User:
    database = None
    chat_id = 0
    question_counter = 0
    question_list = []
    notifying = False
    notify_time = 0

    def __init__(self, chat_id, database):
        self.chat_id = chat_id
        self.database = database

    def add_question(self, question):
        """Append question at end of question_list and database."""
        self.question_list.append(question)
        self.database.add_question(self.chat_id,
                                   question.text,
                                   question.is_blocked,
                                   question.is_custom,
                                   question.keyboard)

    def get_next_question(self):
        """Return the question object from question_list."""
        if self.question_counter < len(self.question_list):
            question = self.question_list[self.question_counter]
            self.question_counter += 1
            return question

        else:
            raise Exception("last question reached")

    def store_response(self, response):
        """store the user response in corresponding question."""
        n = 1

        while self.question_list[self.question_counter -
                                 n].is_blocked:
            n += 1

        self.question_list[
            self.question_counter - n].response = response

    def block_question(self, id):
        """Toggles the is_blocked flag."""
        if len(self.question_list) < id:
            self.question_list[id].blocked = not self.question_list[
                id].blocked
        else:
            raise Exception("out of Bounds")

    def upload_responses_to_database(self):
        """Loads the mined data stored in question_list into the
        database."""
        for q in self.question_list:
            self.database.add_data_to_question(self.chat_id,
                                               q.text, q.response)


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

    text1 = "wie ist das wetter heut so?"
    text2 = "wie ist die Luft heut so?"

    db.add_question(user1.chat_id, text1,
                    True, False, [[]])
    db.add_question(user2.chat_id, text1,
                    True, False, [[]])
    db.add_question(user1.chat_id, text2,
                    True, False, [[]])
    db.add_question(user2.chat_id, text2,
                    True, True, [[]])

    for i in range(5):
        db.add_data_to_question(user1.chat_id, text1,
                                "entry " + str(i))

    for i in range(3):
        db.add_data_to_question(user1.chat_id, text2,
                                "entry " + str(i))

    for i in range(40):
        db.add_data_to_question(user2.chat_id, text1,
                                "entry " + str(i))


test()
