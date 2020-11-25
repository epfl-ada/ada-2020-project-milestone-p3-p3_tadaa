# -*- coding: utf-8 -*-
from location import *
import tweepy
import sys
import time
import datetime
import copy
import json
from configuration import *


class TwitterLocationProvider(LocationProvider):
    __api_key = None
    __api_key_secret = None


    @classmethod
    def set_api_key(cls, api_key: str):
        cls.__api_key = str(api_key) #cela crée une copie

    @classmethod
    def set_api_key_secret(cls, api_key_secret: str):
        cls.__api_key_secret = str(api_key_secret)

    # DONE: créer une méthode __extractLocationSampleFromTweet qui prendra en paramètre un tweet (au format renvoyé par le module tweepy), et qui se chargera d’en extraire la date et l’heure de création (sous forme d’une timestamp), ainsi que la latitude et la longitude.
    @staticmethod
    def __extractLocationSampleFromTweet(tweet : json):
        v = Configuration().get_instance().get_element('verbose') #paramètre verbose de configuration

        (t, lat, lng) = (None, None, None)
#Ce qui est renvoyé par un tweet : voir Onenote
# "created_at" renvoie "Tue May 23 07:56:36 +0000 2017" pour le format
        month={"January":1, "February":2, "March":3, "April":4, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12, "Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
        # print(tweet["coordinates"]["coordinates"],tweet["created_at"])

        if tweet["coordinates"] and tweet["created_at"] : #coordinates renvoie un tuple ? ou ?
            # print(tweet["coordinates"]["coordinates"], tweet["created_at"])  #[6.5681952, 46.5200894] Wed Apr 26 14:15:07 +0000 2017
            lat, lng= tweet["coordinates"]["coordinates"][1], tweet["coordinates"]["coordinates"][0]
            # on enlève le jour de la semaine car ne sert à rien dans le parsing
            mois=str(month[tweet["created_at"][4:7]])
            t=datetime.datetime.strptime(mois+tweet["created_at"][7:], "%m %d %H:%M:%S +0000 %Y").timestamp()

        elif v is True:
            # print("Le tweet : "+str(tweet["text"])+" n'a pas toutes les données attendues.")
            print("Warning: Skipping tweet (Missing time and/or location information (842372886627258369))")


        return t, lat, lng



    # DONE: impémenter le constructeur. Dans le constructeur, on construit une liste de LocationSample, que l’on stocke dans un attribut d’instance __samples, en extrayant, à l’aide de la méthode __extractLocationSampleFromTweet précédemment complétée, les informations de tweet extrait du compte Twitter passé en paramètre.
    def __init__(self, twitterUsername: str, twitterAccessToken: str, twitterAccessTokenSecret: str):
        self.__twitterAccessToken = twitterAccessToken
        self.__twitterAccessTokenSecret = twitterAccessTokenSecret
        self.__username=twitterUsername
        self.__samples=[]

        v = Configuration().get_instance().get_element('verbose') #paramètre verbose de configuration

        auth = tweepy.OAuthHandler(TwitterLocationProvider.__api_key, TwitterLocationProvider.__api_key_secret)
        auth.set_access_token(self.__twitterAccessToken,self.__twitterAccessTokenSecret)
        client=tweepy.API(auth)
        user=client.get_user(self.__username)

        if user.name != None :
            name = user.name
            self.__name = name
        elif v is True :
            print("Warning: Could not extract teaching_isplab's Twitter account information (détails sur l’erreur)")



        # print('Connecté au compte : %s' % self.__name)

        timeline = client.user_timeline()  # count=1 on obtient le dernier message posté #DONE : combien on prend de messages ? disons 10

        tweets=[] #listes d'objet json qui seront au bon format pour __extract
        for tweet in timeline:
            # print(tweet.text)
            # tweets.append(json.dumps(tweet._json, indent=3)) #c'était une erreur pour le montrer voir TP8c
            tweets.append(tweet._json)
        for tweetjson in tweets :
            # print(type(tweetjson))
            données = TwitterLocationProvider.__extractLocationSampleFromTweet(tweetjson)
            try:

                # print(données[0], données[1], données[2])
                if données[0]!=None and données[1]!=None and données[2]!=None :
                    # print(données[0],données[1],données[2])
                    x=LocationSample(données[0], Location(données[1], données[2]))
                    self.__samples.append(x)
                elif v is True :
                    print("Warning: Skipping tweet (Missing time and/or location information (842372886627258369))")
                else :
                    continue
            except Exception:
                if v is True :
                    print("Warning: Skipping tweet (Missing time and/or location information (842372886627258369))")
                else :
                    continue
            # trier _samples avec     def getTimestamp(self): return self._timestamp
            self.__samples=sorted(self.__samples, key=lambda x : x.getTimestamp())


    def get_username(self) :
        return self.__username
    def get_name(self):
        return self.__name

        # DONE: implémenter la méthode getLocationSamples :	Attention	:	faire	en	sorte	que	la	liste	des	samples	(l’attribut	__samples	de	l’objet	WifiLogsLocationProvider)	ne	puisse	pas	être	altérée	via	le	résultat	de	la	méthode	getLocationSamples.
    def getLocationSamples(self):
        return copy.deepcopy(self.__samples)


        # DONE: redéfinir la méthode __str__ de sorte à retourner une chaîne de ce type :
        # TwitterLocationProvider (user 'teaching_isplab' aka 'Teaching ISPLab UNIL', 7 location samples)
    def __str__(self):#DONE : display name
        return "{} (user {:s} aka {}, {} location samples)".format(str(self.__class__.__name__), str(self.get_username()),str(self.get_name()), str(len(self.__samples)))


if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous)



    TwitterLocationProvider.set_api_key('Z4bLkruoqSp0JXJfJGTaMQEZo')
    TwitterLocationProvider.set_api_key_secret('gYyLCa7QiDje76VaTttlylDjGThCBGcp9MIcEGlzVq6FJcXIdc')

    lp = TwitterLocationProvider('rvkint95', '842358721544101888-SZdgC5jX2bYU9Ooe3czsSAfBn7H1y8D','2OaioxOdKsdIJCX2884xtsieHyYNLmNK0vPJjXQQDEaKR')
    print(lp)
    lp.printLocationSamples()


    # TwitterLocationProvider (user 'teaching_isplab' aka 'Teaching ISPLab UNIL', 7 location samples)
    # LocationSample [timestamp: 2017-03-16 13:01:13, location: Location [latitude: 46.52216, longitude: 6.58409]]
    # Warning: Skipping tweet (Missing time and/or location information (842372886627258369))
    # LocationSample [timestamp: 2017-03-16 13:44:33, location: Location [latitude: 46.52217, longitude: 6.58411]]
