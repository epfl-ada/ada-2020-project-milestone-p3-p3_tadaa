#!/usr/bin/env python
#coding: utf-8
#authors: T. Pineau
#creation: 20.10.2020

import tweepy #pip install tweepy
import csv, re, json
from datetime import datetime

def getUser(api, username, filename):
    """Recherche d'un utilisateur retourne le résultat sous format JSON"""
    user = api.get_user(username) #http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.get_user
    with open(filename, 'wb') as f: f.write(json.dumps(user._json, indent=4, ensure_ascii=False).encode('utf-8'))

def searchTweets(api, query, filename):
    """Recherche de tweets en fonction d'un terme spécifique et sauvegarde dans un CSV"""
    csvFile = open(filename, 'w', newline='',  encoding="UTF-8") #ouverture d'un fichier CSV
    writer = csv.writer(csvFile, delimiter=';', quoting=csv.QUOTE_ALL, dialect='excel')
    writer.writerow(["Date", "Auteur", "Contenu"]) #écriture des en-têtes des colonnes

    for tweet in tweepy.Cursor(api.search, q = query,).items(): #voir la doc pour les params de recherche: http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.search
        tweet.text = re.sub('\s+', ' ', tweet.text) # Le contenu des tweets contient parfois des retours à la ligne.
        writer.writerow([tweet.created_at, tweet.author.name, tweet.text]) # Ecriture du résultat dans le csv

    csvFile.close() #fermeture du fichier CSV


if __name__ == '__main__':
    # Clefs et droits d'authentification pour Twitter => Modifier le fichier account.py !!!
    from account import consumer_key, consumer_secret, access_token, access_secret

    # Authentification aux services de Twitter
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Les 2 fonctions définies précédement
    getUser(api, "unil", "./rest_results/get_user.json")
    searchTweets(api, "unil", "./rest_results/search_tweets.csv")
