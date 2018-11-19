class Form():
    def __init__(self):
        self.question = "not set"
        self.data = " "
        
    def set_question(self, question_param):
        modified = question_param.replace("//", " ")
        self.question = modified

    def get_question(self):
        return self.question

    
    def set_data(self, text):
        self.data = text
        
    def get_data(self):
        return self.data