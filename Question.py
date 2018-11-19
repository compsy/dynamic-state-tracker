


class Question():

    def __init__(self):
        self.question = "not set"
        self.type = "continuous"
        self.data = list()
        self.max = "Very much"
        self.min = "Not at all"

    def set_question(self, question_param):
        self.question = self.convert_to_safe(question_param)

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
        
    def reset_data(self):
        self.data = list()

    def get_question(self):
        return self.question

    def get_data(self):
        return self.data

    def get_type(self):
        return self.type
        
    def set_min_max(self, min_param, max_param):
        self.min = self.convert_to_safe(min_param)
        self.max = self.convert_to_safe(max_param)
    
    def get_min(self):
        return self.min

    def get_max(self):
        return self.max
    
        
    def convert_to_safe(self, text):
        modified = text.replace("-", " ")
        modified = modified.replace("//", " ")
        modified = modified.replace("|", "")
        return modified   