


class Question():

    def __init__(self):
        self.question = "not set"
        self.type = "slider"
        self.data = list()

    def set_question(self, question_param):
        self.question = question_param

    def set_type(self, type_param):
        self.type = type_param

    def set_data(self, data_param):
        self.data = data_param

    def add_data(self, data_param):
        self.data.append(data_param)

    def last_value(self):
        if len(self.data) > 0:
            return self.data[len(self.data)-1]
        return None


    def get_question(self):
        return self.question

    def get_data(self):
        return self.data

    def get_type(self):
        return self.type