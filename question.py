


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

    def add_ata(self, data_param):
        self.data.append(data_param)


