# ~~~ IMPORTATIONS UTILE DES PACKAGE POUR LE FONCTIONNEMENT DU CODE ~~ #
import openai
import asyncio
import pyttsx3
import speech_recognition as sr
# ~~~ IMPORTATIONS UTILE DES PACKAGE POUR LE FONCTIONNEMENT DU CODE ~~ #

                                        ### -------------------------------------------------- ###

openai.api_key = "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" # Initialise the OpenAI API

recognizer = sr.Recognizer() # Création d'un objet de reconnaissance et de variables de réveil de mots
GPT_WAKE_WORD = "ok assistant" # Mot clé à utiliser pour activer le bot

                                        ### -------------------------------------------------- ###

### ⬇️ Cette fonction permet de vérifier si le mot clé a été utilisé ⬇️ ###
def get_wake_word(phrase):
    if GPT_WAKE_WORD == phrase.lower(): return GPT_WAKE_WORD
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

    ## °°° ⬇️ Tant que c'est vrai (boucle principale), on effectue le code pour interagir avec l'assistant ⬇️ ## °°°
    while True:

        #~~# ⬇️Dans le cas si on récupère la source du micro, on continue le code ⬇️ #~~#
        with sr.Microphone() as source:


            recognizer.adjust_for_ambient_noise(source) # On ajuste l'audio du micro pour enlever les parasites ainsi que les bruit de fonds
            print(f"Pour parler avec l'assistant veuillez dire : 'ok assistant'") # Affiche un message pour demander d'activer l'assistant

            ## °°° ⬇️ Tant que c'est vrai, (boucle) on effectue le code pour vérifier si l'utilisateur utiliser le mot clé pour l'activation du bot ⬇️ °°° ##
            while True:

                audio = recognizer.listen(source) # On récupère l'audio du microphone

                #""" ⬇️ On essaie de transformer l'audio du micro en texte avec 'Google' ⬇️ """#
                try:

                    start_sentence = recognizer.recognize_google(audio, language="fr-FR") # On transforme l'audio en texte
                    print(f"Vous avez dit: {start_sentence}") # On indique à l'utilisateur ce qu'il a dit

                    wake_word = get_wake_word(start_sentence) # On vérifie s'il utilise le mot clé pour activer l'assistant
                    if wake_word is not None: break # Si l'utilisateur utilise bien le mot clé, on sort donc de la boucle (tant que c'est vrai)
                    else: # Sinon, on lui dit qu'il faut prononcer le mot clé en question
                        print("Pour m'activer, vous devez dire : 'ok assistant'")
                        continue # On continue d'effectuer une execution du code de la boucle (tant que c'est vrai)

                #""" ⬇️ Si on récupère une exception, on demande à l'utilisateur de réessayer ⬇️ """#
                except:

                    print("Réessayez, pour parler avec l'assistant veuillez dire : 'ok assistant'")
                    continue # On continue d'effectuer une execution du code de la boucle (tant que c'est vrai)

                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            ### **** ### Si on arrive ici, c'est que tous est bon est que le mot clé a bien été récupéré ### **** ###

            print("Posez votre question...") # On informe à l'utilisateur qu'il peut poser sa question
            synthesize_speech('Que puis-je faire pour vous ?') # L'Assistant va prononcer le message 'Que puis-je faire pour vous ?'

            audio = recognizer.listen(source) # On récupère l'audio du microphone

            #""" ⬇️ On essaie de transformer l'audio du micro en texte avec 'Google' ⬇️ """#
            try:

                question = recognizer.recognize_google(audio, language="fr-FR") # On transforme l'audio en texte
                print(f"Vous avez dit: {question}") # On indique à l'utilisateur ce qu'il a dit

            #""" ⬇️ Si on récupère une exception, on informe à l'utilisateur que l'assistant ne l'entend pas ⬇️ """#
            except:

                print("l'Assistant a du mal à vous entendre, vous allez devoir prononcer de nouveau 'ok assistant' pour l'activer une nouvelle fois...") # On informe de réessayer de poser ça question
                synthesize_speech("Désolé, mais je ne vous entend pas, au revoir...") # L'Assistant va prononcer le message 'Désolé, mais je ne vous entend pas...'
                continue # On continue d'effectuer une execution du code de la boucle principale (tant que c'est vrai)

                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
                                # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            ### **** ### Si on arrive ici, c'est que tous est bon est que l'assistant à récupérer la question de l'utilisateur ### **** ###

            print(f"En attente d'une réponse....") # On informe à l'utilisateur qu'une réponse est en préparation

            ## ⬇️ Envoie une invite à l'API GPT-3.5-turbo pour effectuer la réponse, en précisant des paramètres pour l'API GPT-3.5-turbo ⬇️ ##
            answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[ {"role": "system", "content": "Vous êtes un assistant utile."}, {"role": "user", "content": question} ],
                        temperature=0.5, top_p=1, frequency_penalty=0, presence_penalty=0, n=1, stop=["\nUser:"])
            ## ⬆️ Envoie une invite à l'API GPT-3.5-turbo pour effectuer la réponse, en précisant des paramètres pour l'API GPT-3.5-turbo ⬆️ ##

            bot_answer = answer["choices"][0]["message"]["content"] # On récupère la réponse récupérée par cette API

        print("Réponse de l'assistant :", bot_answer) # On informe à l'utilisateur la réponse générée par l'assistant
        synthesize_speech(bot_answer) # L'Assistant va prononcer la réponse qu'il a générée
        continue # On continue d'effectuer une execution du code de la boucle principale (tant que c'est vrai)

                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###
                                        ### -------------------------------------------------- ###

if __name__ == "__main__": asyncio.run(main()) # On appelle la fonction principale
