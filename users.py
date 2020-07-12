class Question:
    id = 0
    text = ''
    is_blocked = False
    is_custom = False

    keyboard = [[]]

    def set_key(self, text, x, y):
        if (y > len(self.keyboard)) or (x > len(self.Keyboard[y])):
            print("out of bounds")
        else:
            self.keyboard[x][y] = text


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
            self.question_counter = 0
            return False

    def delete_question(self, id):

        if len(self.questions) < id:
            del self.questions[id]

        else:
            print("out of bounds")
    
    def block_question(self, id):
        if len(self.questions) < id:
            self.questions[id].blocked = not self.questions[id].blocked
        else:
            print("out of bounds")
 