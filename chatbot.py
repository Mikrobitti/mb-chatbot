#!/usr/bin/env python
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer

bot_name = 'Mikrobitti'
trainer = 'corpus'

bot = ChatBot(
    bot_name,
    # Käytetään tiedon varastointiin JSON-tiedostoa. Jos dataa on paljon, on
    # parempi käyttää tietokantaa.
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    # Esiprosessoreilla botin saaman syötteen voi siistiä sopivaan muotoon.
    # Tässä tapauksessa poistetaan turhat välimerkit käsiteltävästä syötteestä.
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    # Input- ja output-adaptereilla voidaan liittää botti erilaisiin sisään-
    # ja ulostuloihin. Tässä esimerkissä niitä ei tarvita, sillä interaktioon
    # riittävät Pythonin standardikirjaston IO-funktiot.
    #
    #   input_adapter='chatterbot.input.TerminalAdapter',
    #   output_adapter='chatterbot.output.TerminalAdapter',
    #
    # Logiikka-adaptereilla voidaan määritellä botin käyttäytyminen tietyissä
    # tilanteissa. Tässä esimerkissä opetetaan botti laskemaan sekä kertomaan, 
    # jos se ei osaa muodostaa vastausta. annetaan yksi avainsanaan perustuva 
    # vastaus.
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Help',
            'output_text': 'I am a friendly chatbot! How may I help you?'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.20,
            'default_response': 'Sorry, I didn\'t get that.'
        }
    ],
    # Filtereillä voidaan tehdä kyselyjä Chatterbotin dataan botin toiminnan
    # hienosäätämiseksi. RepetitiveResponseFilter rajoittaa saman vastauksen
    # toistumista, jotta keskustelu ei jäisi kiertämään kehää.
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    # Määritetään tiedosto, johon data tallennetaan.
    database='./database.json'
)

if trainer == 'list':
    # Koulutetaan botti yksinkertaisesti listalla keskustelun kulusta. Botti
    # oppii käydyistä keskusteluista ja alkaa käyttää myös käyttäjän antamia
    # lauseita.
    conversation = [
        'Hi!',
        'Hello!',
        'How are you?',
        'I\'m fine, thank you',
        'Nice to meet you.',
        'Thank you.',
        'See you soon!'
    ]
    bot.set_trainer(ListTrainer)
    bot.train(conversation)

elif trainer == 'corpus':
    # Koulutetaan botti valmiilla korpusmateriaalilla. Suuri aineistomäärä voi
    # hidastaa botin käyttöä jos käytetään tallennukseen tiedostoa. Tällöin
    # vaihto tietokantaan voi olla aiheellinen. Chatterbotin dokumentaatio
    # kertoo, miten MongoDB-tietokantaa voi käyttää Chatterbotin kanssa. 
    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train(
        # Käytössä oleva aineisto on kohtalaisen suppea, jotta vastauksen haku
        # ei kestä liian kauan.
        'chatterbot.corpus.english.greetings',
        'chatterbot.corpus.english.conversations'
    )

name = input(bot_name + ': Hello! What is your name? ')
print(bot_name + ': Nice to meet you!')

while True:
    try:
        sentence = input(name + ': ')
        response = bot.get_response(sentence)
        print(bot_name + ': ' + response.text)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
