


class MultiLanguage():

    def __init__(self, lang):
        
        self.word_array = list()
        self.cur_language = lang
        
        ## For Main window 
        first_word = ["Start Video", "Start Video", "Commencer la video", "empezar video"]
        second_word = ["Set items", "Items instellen", "Definir objets", "definir objetos"]
        third_word = ["Basic questions", "Basisvragen", "Questions de base", "Preguntas de base"]
        fourth_word = ["Show result","Bekijk resultaten", "afficher resultats", "ver resultados"]
        
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        
        
        ## For Review Window
        # Use trend instead of best fit!
        first_word = ["Export", "Exporteren", "Exporter", "Exportar"]
        second_word = ["Statistics", "Statistieken", "Statistiques", "Estadisticas"]
        third_word = ["Hide trend", "Geen trend", "Son tendance", "Sin tendance"]
        fourth_word = ["Trend", "Trend", "Tendance", "Tendencia"]
        fifth_word = ["No trend", "Geen trend", "Sans tendance", "Sin tendencia" ]
    
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        self.word_array.append(fifth_word)
        
        
        # For add/submit/remove/time
        first_word = ["Add", "Toevoegen", "Ajouter", "Añadir"]
        second_word = ["Remove", "Verwijderen","supprimer", "Quitar"]
        third_word = ["Submit", "Klaar", "Envoyer", "Enviar"]
        fourth_word = ["Time", "Tijd", "Temps", "Tiempo"]
        
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        
        # For save/answer
        first_word = ["Save", "Opslaan", "Sauvgarder", "Guardar"]
        second_word = ["answer", "antwoord", "Reponse", "Respuesta"]
        third_word = ["continuous", "continue", "continu", "Continuo"]

        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        
        # Statistics 
        first_word = ["Mean", "Gemiddelde", "Moyenne", "Media"]
        second_word = ["Mode", "Modus", "Mode", "Modo"]
        third_word = ["Median", "Mediaan","mediane", "mediana"]
        fourth_word = ["Range", "Bandbreedte", "Intervalle", "Intervalo"]
        
        self.word_array.append(first_word)
        self.word_array.append(second_word)
        self.word_array.append(third_word)
        self.word_array.append(fourth_word)
        
        
        # Extra
        first_word = ["Thank you and goodbye!", "Bedankt en tot ziens!", "Merci et aurevoir!", "Gracias y adios!"]
        self.word_array.append(first_word)
        
    def set_language(self, lang):
        self.cur_language = lang
        
    
    def find_dutch(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[1]
        return "None"
        
    def find_spanish(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[3]
        return "None"
        
    def find_french(self, eng_word):
        for word in self.word_array:
            if(word[0] == eng_word):
                return word[2]
        return "None"     

        
    def find_correct_word(self, eng_word):
        if(self.cur_language == "English"):
            return eng_word
        elif(self.cur_language == "Dutch"):
            return self.find_dutch(eng_word)
        elif(self.cur_language == "French"):
            return self.find_french(eng_word)
        elif(self.cur_language == "Spanish"):
            return self.find_spanish(eng_word)    
    