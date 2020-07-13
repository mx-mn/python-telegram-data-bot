from telegram import ReplyKeyboardMarkup

class Question:
    id = 0
    text = ''
    response = ''
    is_blocked = False
    is_custom = False

    keyboard = [[]]

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


class User:
    id = 0
    question_counter = 0
    questions = []
    notifying = False
    notify_time = 0

    def add_question(self, question):
        self.questions.append(question)

    def get_next_question(self):

        if len(self.questions) > self.question_counter:
            self.question_counter += 1
            return self.questions[self.question_counter]

        else:
            raise Exception("last question reached")

    def store_response(self, response):
        if self.question_counter > 0:
            n = 1

            while self.questions[self.question_counter - n].is_blocked:
                n += 1

            self.questions[self.question_counter-n].response = response

    def delete_question(self, id):

        if len(self.questions) < id:
            del self.questions[id]

        else:
            raise Exception("out of Bounds")

    def block_question(self, id):
        if len(self.questions) < id:
            self.questions[id].blocked = not self.questions[id].blocked
        else:
            raise Exception("out of Bounds")
