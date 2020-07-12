class Question:
    ID = 0
    Text = ''
    blocked = False
    custom = False

    keyboard = [[]]

    def get_text(self):
        return self.Text

    def get_keyboard(self):
        return self.keyboard

    def set_text(self, text):
        self.Text = text

    def set_keyboard(self, keyboard):
        self.keyboard = keyboard

    def set_key(self, text, x, y):
        if (y > len(self.keyboard)) or (x > len(self.Keyboard[y])):
            print("out of bounds")
        else:
            self.keyboard[x][y] = text


class User:
    ID = 0
    currentQuestion = 0
    questions = []
    keyboards = []
    Notification = False
    NotifyTime = 0

    def __init__(self):
        ID = 1

    def add_question(self, question):
        self.questions.append(question)

    def add_keyboard(self, keyboard):
        self.keyboards.append(keyboard)

    def get_next_question(self):

        if len(self.questions) > self.currentQuestion:
            self.currentQuestion += 1
            return self.questions[self.currentQuestion]

        else:
            self.currentQuestion = 0
            return False

    def delete_question(self, id):

        if len(self.questions) < id:
            del self.questions[id]

        else:
            print("out of bounds")

    def edit_reminder(self, hh, mm):
        if hh < 24 and mm < 60:
            print("not implemented Yet")
    
    def block_question(self, id, state):
        if len(self.questions) < id:
            self.questions[id].blocked = state
        else:
            print("out of bounds")
 