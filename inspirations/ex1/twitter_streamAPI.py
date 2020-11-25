#!/usr/bin/env python
#coding: utf-8
#authors: T. Pineau
#creation: 20.10.2020

import tweepy #pip install tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from datetime import datetime
import time, json, re, sys

class CustomListener(StreamListener):
    def __init__(self, folder=None, maxTweets=10):
        self.folder = folder # Le dossier dans lequel on va enregistrer notre tweets
        self.maxTweets = maxTweets # Le nombre maximum de tweets à récupérer
        self.tweetsNumber = 0 # Le nombre de tweets déjà récupérés (0 initialement)

    def on_data(self, data):
        self.tweetsNumber += 1 # On incrémente la valeur du nombre de tweets récupérés
        try:
            if "limit" not in data:
                tweetData = json.loads(data) # Les données sous forme de json sont transformée en un dictionnaire
                print("Tweet %s / %s:\n\tDate: %s\n\tUser: %s\n\tContent: %s" % (str(self.tweetsNumber), str(self.maxTweets), tweetData['created_at'], tweetData['user']['name'], re.sub('\s+', ' ', tweetData['text']))) #Affichage du résultat
                with open(self.folder+'/'+str(tweetData['id'])+'.json', 'w', encoding="utf-8") as f: f.write(json.dumps(tweetData, indent=4)) #Ecriture du tweet dans un fichier .json
                if int(self.tweetsNumber) >= int(self.maxTweets): sys.exit() # Si le nombre de tweet maximum est atteint, fin du programme.
        except Exception as e: print("Exception rencontrée dans le traitement des tweets: %s" % (e)) #S'il y a une erreur l'affiche (sans faire planter le script)
        time.sleep(2)


if __name__ == '__main__':
    # Clefs et droits d'authentification pour Twitter => Modifier le fichier account.py !!!
    from account import consumer_key, consumer_secret, access_token, access_secret

    # Authentification aux services de Twitter
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)

    # Création d'une liste avec les termes de recherche
    terms=["#ivi2020"]

    # Exécution du module StreamListener https://tweepy.readthedocs.io/en/v3.5.0/streaming_how_to.html#step-1-creating-a-streamlistener
    twitterStream = Stream(auth, CustomListener(folder='./stream_results', maxTweets=10))
    twitterStream.filter(track=terms)
