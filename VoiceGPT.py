# ~~~ IMPORTATIONS UTILE DES PACKAGE POUR LE FONCTIONNEMENT DU CODE ~~ #
import time
import sys
import os
import openai
import asyncio
import pyttsx3
import speech_recognition as sr
# ~~~ IMPORTATIONS UTILE DES PACKAGE POUR LE FONCTIONNEMENT DU CODE ~~ #

                                        ### -------------------------------------------------- ###

openai.api_key = "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" # Initialise the OpenAI API

recognizer = sr.Recognizer() # Création d'un objet de reconnaissance et de variables de réveil de mots
GPT_WAKE_WORD = "ok assistant" # Mot clé à utiliser pour activer le bot
GPT_SLEEP_WORD = ["au revoir assistant", "à la prochaine assistant"] # Mot clé à utiliser pour désactiver le bot

audio = None # Permettra de récupérer l'audio du microphone
bot_answer = None # Permettra de récupérer la réponse du bot

error = False # Permettra de savoir s'il y a une erreur ou non

                                        ### -------------------------------------------------- ###

### ⬇️ Cette fonction permet de vérifier si le mot clé d'activation a bien été utiliser ⬇️ ###
def get_wake_word(phrase):

    if GPT_WAKE_WORD == phrase.lower(): return GPT_WAKE_WORD
    else: return None


### ⬇️ Cette fonction permet de vérifier si le mot clé de désactivation a bien été utiliser ⬇️ ###
def get_sleep_word(phrase):

    if phrase.lower() in GPT_SLEEP_WORD: return phrase.lower()
    else: return None

                                        ### -------------------------------------------------- ###

### ⬇️ Cette fonction permet de faire parler le bot ⬇️ ###
def synthesize_speech(text):

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###

### ⬇️ Ici, c'est la fonction principale, dedans, on effectue toute la logique ⬇️ ###
async def main():

    global error # Récupère la variable de vérification en cas d'erreur (True ou False)

    ## °°° ⬇️ Tant que c'est vrai (boucle principale), on effectue le code pour interagir avec l'assistant ⬇️ ## °°°
    while True:

        #~~# ⬇️Dans le cas si on récupère la source du micro, on continue le code ⬇️ #~~#
        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(source) # On ajuste l'audio du micro pour enlever les parasites ainsi que les bruit de fonds
            print(f"Pour parler avec l'assistant veuillez dire : 'ok assistant'") # Affiche un message pour demander d'activer l'assistant

            global audio # Récupère la variable de l'audio initialisé en début de fichier
            audio = None # Redéfinit l'audio du microphone sur 'none' (rien)

            global bot_answer # Récupère la variable de la réponse du bot

            ## °°° ⬇️ Tant que c'est vrai, (boucle) on effectue le code pour vérifier si l'utilisateur utiliser le mot clé pour l'activation du bot ⬇️ °°° ##
            while True:

                if audio is None: audio = recognizer.listen(source) # On récupère l'audio du microphone s'il n'a pas encore été récupéré
                time.sleep(2) # On attend 2 secondes

                #""" ⬇️ On essaie de transformer l'audio du micro en texte avec 'Google' ⬇️ """#
                try:

                    start_sentence = recognizer.recognize_google(audio, language="fr-FR") # On transforme l'audio en texte
                    print(f"Vous avez dit: {start_sentence}") # On indique à l'utilisateur ce qu'il a dit

                    wake_word = get_wake_word(start_sentence) # On vérifie s'il utilise le mot clé pour activer l'assistant
                    if wake_word is not None: break # Si l'utilisateur utilise bien le mot clé, on sort donc de la boucle (tant que c'est vrai)
                    else: # Sinon, on lui dit qu'il faut prononcer le mot clé en question pour l'activation du bot
                        print("Pour activer l'assistant, vous devez dire : 'ok assistant'") # Informe à l'utilisateur qu'il faut prononcer 'ok assistant'
                        audio = None # Redéfinit l'audio du microphone sur 'none' (rien)

                #""" ⬇️ Si on récupère une exception, on demande à l'utilisateur de réessayer ⬇️ """#
                except:

                    print("Réessayez, pour parler avec l'assistant veuillez dire : 'ok assistant'")
                    audio = recognizer.listen(source) # On récupère l'audio du microphone


                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            ### **** ### Si on arrive ici, c'est que tous est bon est que le mot clé a bien été récupéré ### **** ###

            print("Posez votre question ou dite 'au revoir assistant' ou 'à la prochaine assistant' pour partir...") # On informe à l'utilisateur qu'il peut poser sa question
            synthesize_speech('Que puis-je faire pour vous ?') # L'Assistant va prononcer le message 'Que puis-je faire pour vous ?'

            audio = None # Redéfinit l'audio du microphone sur 'none' (rien)

            ## °°° ⬇️ Tant que c'est vrai, (boucle) on effectue le code pour vérifier la question de l'utilisateur ⬇️ °°° ##
            while True:

                if audio is None: audio = recognizer.listen(source) # On récupère l'audio du microphone
                time.sleep(3) # On attend 3 secondes

                #""" ⬇️ On essaie de transformer l'audio du micro en texte avec 'Google' ⬇️ """#
                try:

                    question = recognizer.recognize_google(audio, language="fr-FR") # On transforme l'audio en texte

                    print(f"Vous avez dit: {question}") # On indique à l'utilisateur ce qu'il a dit
                    print(f"En attente d'une réponse....") # On informe à l'utilisateur qu'une réponse est en préparation


                    #""" ⬇️ On essaie de générer une réponse claire avec l'API d'openAI ⬇️ """#
                    try:

                        ## ⬇️ Envoie une invite à l'API GPT-3.5-turbo pour effectuer la réponse, en précisant des paramètres pour l'API GPT-3.5-turbo ⬇️ ##
                        answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "Vous êtes un assistant utile."}, {"role": "user", "content": question} ],
                                                              temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, n=1, stop=["\nUser:"])
                        ## ⬆️ Envoie une invite à l'API GPT-3.5-turbo pour effectuer la réponse, en précisant des paramètres pour l'API GPT-3.5-turbo ⬆️ ##

                        bot_answer = answer["choices"][0]["message"]["content"] # On récupère la réponse récupérée par cette API

                                                ## ***** ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ***** ##

                        print("Réponse de l'assistant :", bot_answer) # On informe à l'utilisateur la réponse générée par l'assistant
                        synthesize_speech(bot_answer) # L'Assistant va prononcer la réponse qu'il a générée

                                                        ## *** ~~~~~~~~~~~~~~~~~~ *** ##

                        sleep_word = get_sleep_word(question) # On vérifie s'il utilise le mot clé pour désactiver l'assistant

                        audio = None # Redéfinit l'audio du microphone sur 'none' (rien)
                        bot_answer = None # Redéfinit la réponse du bot sur 'none' (rien)
                        if sleep_word is not None: break # Si l'utilisateur utilise bien le mot clé, on sort donc de la boucle actuelle (tant que c'est vrai)


                    #""" ⬇️ Si on récupère une exception, c'est qu'il y a eu une erreur avec la clé d'API OpenAI, dans ce cas, on retourne l'erreur, et on sort ⬇️ """#
                    except:
                        print("Une erreur s'est produite, la clé d'API OpenAI ne fonctionne pas, fermeture du script...")
                        error = True # Une erreur s'est produite, donc on définit la variable de vérification d'erreur sur 'Vrai'
                        break # On sort donc de la boucle actuelle (tant que c'est vrai)

                #""" ⬇️ Si on récupère une exception, on informe à l'utilisateur que l'assistant ne l'entend pas ⬇️ """#
                except:

                    if not audio or not bot_answer:
                        print("L'Assistant a du mal à vous entendre, réessayer ou dite 'au revoir assistant' ou 'à la prochaine assistant' pour partir...") # On informe de réessayer de poser ça question
                        synthesize_speech("Désolé, mais je ne vous entend pas...") # L'Assistant va prononcer le message 'Désolé, mais je ne vous entend pas...'
                        audio = recognizer.listen(source) # On récupère l'audio du microphone

            if error is True: break # On sort de la condition en cas d'erreur

        if error is True: break # On sort de la boucle principale en cas d'erreur


                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###

if __name__ == "__main__": asyncio.run(main()) # On appelle la fonction principale
