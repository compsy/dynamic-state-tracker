
import json

class MultiLanguage():

    def __init__(self, lang):
        self.cur_language = lang
        
        # Load all words, otherwise just load nothing and the program will use the english words!
        try:
            f = open("saves/Languages/Languages.txt", "r")
            data = f.read()
            self.word_array = json.loads(data)
            f.close()
        except:
            self.word_array = list()
       
    def set_language(self, lang):
        self.cur_language = lang
        
    
    def find_dutch(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[1]
        return eng_word
        
    def find_spanish(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[3]
        return eng_word
        
    def find_french(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[2]
        return eng_word     

        
    def find_correct_word(self, eng_word):
        if(self.cur_language == "English"):
            return eng_word
        elif(self.cur_language == "Dutch"):
            return self.find_dutch(eng_word)
        elif(self.cur_language == "French"):
            return self.find_french(eng_word)
        elif(self.cur_language == "Spanish"):
            return self.find_spanish(eng_word)    
    