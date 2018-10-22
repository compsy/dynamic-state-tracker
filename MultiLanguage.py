


class MultiLanguage():

    def __init__(self, lang):
        
        self.word_array = list()
        self.cur_language = lang
        
        ## For Main window 
        first_word = ["Play Video", "Video afspelen"]
        second_word = ["Set Questions", "vragen stellen"]
        third_word = ["Set Form", "Vorm instellen"]
        fourth_word = ["Review","Beoordeling"]
        
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        
        
        ## For Review Window
        first_word = ["Export", "Exporteren"]
        second_word = ["Statistics", "Statistieken"]
        third_word = ["Hide best fit", "Geen beste pasvorm"]
        fourth_word = ["Best fit", "Beste pasvorm"]
        fifth_word = ["No best fit", "Geen beste pasvorm"]
    
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        self.word_array.append(fifth_word)
        
        
        # For add/submit/remove/time
        first_word = ["Add", "Toevoegen"]
        second_word = ["Remove", "Verwijderen"]
        third_word = ["Submit", "Voorleggen"]
        fourth_word = ["Time", "Tijd"]
        
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        
        # For save/answer
        first_word = ["Save", "Opslaan"]
        second_word = ["answer", "antwoord"]

        self.word_array.append(first_word)
        self.word_array.append(second_word)
    def set_language(self, lang):
        self.cur_language = lang
        
    
    def find_dutch(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[1]
        return "None"
        
    def find_correct_word(self, eng_word):
        if(self.cur_language == "English"):
            return eng_word
        elif(self.cur_language == "Dutch"):
            return self.find_dutch(eng_word)

            
    