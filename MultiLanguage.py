
import json
import jsonify
#from py_translator import Translator

class MultiLanguage():

    def __init__(self, lang):
        self.cur_language = lang
        
        # Load all words, otherwise just load nothing and the program will use the english words!
        try:
            f = open("saves/Languages/Languages.txt", "r")
            data = f.read()
            data = data.replace('\n', '')
            self.word_array = json.loads(data)
            f.close()
        except:
            print("error loading words")
            self.word_array = list()
            
        # For seeing the words
        #for word in self.word_array:
        #    print(word[0] + " : " + json.dumps(word[4]) + "\n")
            
        #self.re_save_words()
        
    def re_save_words(self):
        try:
            f = open("saves/Languages/Languages.txt", "w+")
            f.write(json.dumps(self.word_array))
        except:
            print("failed to save to json")
       
    def set_language(self, lang):
        self.cur_language = lang
        
    
    def find_dutch(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[1]
        return self.auto_translate(eng_word, 'nl')
        
    def find_spanish(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[3]
        return self.auto_translate(eng_word, "es")
        
    def find_french(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[2]
        return self.auto_translate(eng_word, "fr")  
        
    def find_german(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[4]
        return self.auto_translate(eng_word, "de")  

        
    def find_correct_word(self, eng_word):
        if(self.cur_language == "English"):
            return eng_word
        elif(self.cur_language == "Nederlands"):
            return self.find_dutch(eng_word)
        elif(self.cur_language == "Français"):
            return self.find_french(eng_word)
        elif(self.cur_language == "Español"):
            return self.find_spanish(eng_word)    
        elif(self.cur_language == "Deutsche"):
            return self.find_german(eng_word)    
       
       
    def auto_translate(self, eng_word, dest):
       # try:
        #    translated_word = Translator().translate(text=eng_word, dest=dest, src = "en").text
       #     return translated_word
       # except:
       #     print("Translation of '" + eng_word + "' failed.")
       return eng_word
        