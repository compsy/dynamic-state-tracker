class Form():
    def __init__(self):
        self.question = "not set"
        self.data = " "
        
    def set_question(self, question_param):
        self.question = self.convert_to_safe(question_param)

    def get_question(self):
        return self.question

    
    def set_data(self, text):
        self.data = text
        
    def get_data(self):
        return self.data
        
    
        
    def convert_to_safe(self, text):
        modified = text.replace("-", " ")
        modified = modified.replace("//", " ")
        modified = modified.replace("|", "")
        return modified   