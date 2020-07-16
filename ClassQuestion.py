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
