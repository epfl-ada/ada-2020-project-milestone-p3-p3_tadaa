
# -*- coding: utf-8 -*-
from datetime import datetime
import math
import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
import folium
import googlemaps
import time
import os
from configuration import *

import pathlib


# DONE: Créer une classe Location pour définir des objets contenant des coordonnées géographiques (latitude, longitude : en dégrés)
class Location:
    # Done: Créer des attributs *privés* permettant de stocker la clé (api_key) pour l'accès à l'API de Google et l'objet Client (module googlemaps) correspondant (api_client)
    # Done: Créer la méthode correspondante : set_api_key (*optionnel* : et __check_api_init pour vérifier que les attributs ci-dessus ont bien été initialisés)

    # Done: Définir un constructeur. (*optionnel* : Faire les vérifications appropriées pour les valeurs passées en paramètre)

    # Done: Redéfinir la méthode __str__ de sorte à retourner une châine de ce type (*optionnel* : limiter le nombre de décimales à 5 pour l'affichage des coordonnées):
    # Location [latitude: 48.85479, longitude: 2.34756]

    # Done: Définir les getters

    # Done: Définir une méthode getHaversineDistance comme vue en TP

    _longitude = None
    _latitude = None

    __api_client = None
    __api_key = ""
    __EARTH_RADIUS = 6371008.8

    @classmethod
    def set_api_key(cls, api_key: str):
        cls.__api_key = str(api_key)
        cls.__api_client = googlemaps.Client(key=cls.__api_key)
    @classmethod
    def __check_api_inits(cls):
        if not cls.__api_key:
            raise Exception('no api key found !', file=sys.stderr)

    def __init__(self, latitude: float, longitude: float):

        if not (-180 < longitude < 180):
            raise Exception('Longitude invalide [-180, 180]', file=sys.stderr)

        if not (-90 < latitude < 90):
            raise Exception('Latitude invalide [-90, 90]', file=sys.stderr)

        try:  # rajouter les try except à chaque autre test de ce genre (dans configuration.py aussi)
            self._longitude = float(longitude)
            self._latitude = float(latitude)

        except Exception as e:
            raise ValueError(e.args[0])

    def __str__(self):
        return 'Location [latitude: {0:.5f}, longitude: {1:0.5f}]'.format(self._latitude, self._longitude)

    def getLatitude(self):
        return self._latitude

    def getLongitude(self):
        return self._longitude

    def getHarvesineDistance(self, location):
        delta = math.radians(self._latitude)
        deltap = math.radians(location.getLatitude())
        lamb = math.radians(self._longitude)
        lambp = math.radians(location.getLongitude())
        return 2 * self.__EARTH_RADIUS * math.asin(math.sqrt(math.sin((delta - deltap) / 2) ** 2 + math.cos(delta) * math.cos(deltap) * math.sin((lamb - lambp) / 2) ** 2))




    # DONE: Définir une méthode get_name(self) -> str qui retourne, en utilisant l'API Google reverse geocoding, le nom correspondant aux coordonées contenues dans l'objet Location
    # "Avenue de la Gare 46, 1003 Lausanne, Suisse" pour 46.517738, 6.632233
    # TODO : Claire, vérifie si c'est juste en le faisant par toi-même
    def get_name(self):
        reverse_geocode_results = Location.__api_client.reverse_geocode((self._latitude, self._longitude),language='fr')
        return reverse_geocode_results[0]['formatted_address']

    # DONE : Définir une méthode get_travel_distance_and_time(self, destination: Location) qui retourne, en utilisant l'API Google distance matrix, le couple (temps en secondes, distance en mètres) pour aller *à pied* de la Location self à la Location destination

    def get_travel_distance_and_time(self, distance):
        distance_result = Location.__api_client.distance_matrix(origins=(self._latitude, self._longitude), destinations=(distance._latitude, distance._longitude), mode='walking', language='fr')
        return distance_result['rows'][0]['elements'][0]['duration']['value'], distance_result['rows'][0]['elements'][0]['distance']['value']
# Done: Définir une classe LocationSample qui contient un temps (timestamp: int) et une Location.
# Done: Redéfinir les opérateur de comparaison (de sorte à pouvoir utiliser, sort, min, <, >, etc.) en se basant sur les timestamps des LocationSample (ordre chronologique).
# Done: Redéfinir la méthode __str__ de sorte à retourner une châine de ce type (*optionnel* : représenter la date sous forme textuelle):
# LocationSample [timestamp: 1488540300, location: Location [latitude: 48.85479, longitude: 2.34756]]
# ou (*optionnel*)
# LocationSample [timestamp: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]

class LocationSample:
    _location = None
    _timestamp = None

    def __eq__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp==other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __ne__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp!=other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __lt__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp<other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __le__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp<=other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __gt__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp==other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __ge__(self, other):
        if isinstance(other, LocationSample) and isinstance(self, LocationSample):
            return self._timestamp==other._timestamp
        else :
            raise Exception("Un terme de la comparaison n'est pas un objet LocationSample")

    def __init__(self, timestamp: int, location: Location):
        self._timestamp = timestamp
        self._location = location

    def getLocation(self):
        return self._location

    def getTimestamp(self):
        return self._timestamp

    def spatialDistance(self, location: Location):
        return self._location.getHarvesineDistance(location)


    def temporalDistance(self, timestamp: int):
        return timestamp - self.getTimestamp()

    #DONE : faire la fonction str. pour prendre la latitude ou la longitude, il faut appeler l'objet Location avec un getter et avec son propre getter pour la latitude (ex : self.getLocation().getLatitude())
    def __str__(self):
        return "LocationSample [timestamp: {}, location: Location [latitude: {}, longitude: {}]".format(str(datetime.fromtimestamp(self._timestamp)), "%.5f" %self.getLocation().getLatitude(), "%.5f" %self.getLocation().getLongitude())


# DONE: définir une classe (abstraite) LocationProvider qui décrit des objets permettant de produire une liste d’objets LocationSample. Elle spécifie l’existence d’une méthode getLocationSamples qui renvoie une liste d’objets LocationSample triés par ordre chronologique (qui n’est pas implémentée, c’est aux classes filles de l’implémenter).
class LocationProvider:
    def __init__(self):
        raise NotImplementedError('Please implement me !')

    def getLocationSamples(self):
        raise NotImplementedError('Please implement me !')

    # Done: implémenter la méthode printLocationSamples en utilisant getLocationSamples. Cette méthode doit retourner une chaîne de caractère décrivant, sous la forme suivante, les objets LocationSamples renvoyés par la méthode getLocationSamples.
    # ['LocationSample [timestamp: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]', 'LocationSample [timestamp: 2017-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]']
    #J'ai modifié ton str de cette fonction car elle affichait rien de cette manière.
    def printLocationSamples(self):
        # return str([str(x)+"\n" for x in self.getLocationSamples()])
        for sample in self.getLocationSamples() :
            print(str(sample))

    # DONE: permet d'afficher d’afficher le résultat de getLocationSamples sur une carte. *Ne pas modifier cette méthode*
    def showLocationSamples(self):
        samples = self.getLocationSamples()
        if len(samples) == 0:
            return

        coordinates = [(sample.getLocation().getLatitude(), sample.getLocation().getLongitude()) for sample in
                       samples]
        timestamps = [sample.getTimestamp() for sample in samples]

        # Creating the HTML map
        map = folium.Map(location=coordinates[0],
                         zoom_start=8)  # Map zoom in location defined as the first coordinate
        folium.PolyLine(locations=coordinates).add_to(map)  # draw a line intersecting all the points

        for i in range(len(coordinates)):
            folium.Marker(coordinates[i],
                          popup=datetime.fromtimestamp(timestamps[i]).strftime('%d/%m/%Y at %H:%M:%S')).add_to(
                map)  # put markers on each and annotate with timestamps

        map.save('map.html')
        url = pathlib.Path(os.path.abspath("map.html")).as_uri()

        # Make GUI with the map embedding
        app = QApplication(sys.argv)
        web = QWebEngineView()
        web.load(QUrl(url))
        web.show()
        sys.exit(app.exec_())

    # @staticmethod
    # def _argmin(l: list, metric, condition):
    #     mini = 0
    #     minie = None
    #     for e in l:
    #         if minie is None or (condition(e) and metric(e) < mini):
    #             mini = metric(e)
    #             minie = e
    #     return minie

    # DONE: Implémenter les méthodes getClosestSpatialLocationSample et getClosestTemporalLocationSample, en utilisant getLocationSamples, qui renvoie respectivement l’objet LocationSample le plus proche (en termes de distance géographique) ou en temps, de la valeur passée en argument. (Optionnel : définir une méthode argmin qui prend en argument une liste l, une fonction f et une fonction c et qui renvoie l’élément de l qui maximise la fonction f parmi les éléments de l pour lesquels c renvoie vrai. Utiliser cette méthode pour implémenter les deux méthodes susmentionnées).
    def getClosestSpatialLocationSample(self, location: Location) -> LocationSample:

        closest = None

        for otherloc in self.getLocationSamples():
            if closest is None or otherloc.spatialDistance(location) < mindist:
                mindist = otherloc.spatialDistance(location)
                closest = otherloc

        return closest

    def getClosestTemporalLocationSample(self, timestamp: int) -> LocationSample:

        closest = None

        for location in self.getLocationSamples():
            if closest is None or abs(location.temporalDistance(timestamp)) < mintemp:
                mintemp = abs(location.temporalDistance(timestamp))
                closest = location

        return closest

    # DONE: Implémenter la méthode getSurroundingTemporalLocationSamples qui renvoie les objets LocationSample de la trace (obtenue via getLocationSamples) juste avant et juste après le timestamp passé en paramètre (la dernière information de localisation antérieure au timestamp et la première postérieure au timestamp).
    #J'ai ajouté le paramètre à temporalDistance()
    def getSurroundingTemporalLocationSamples(self, timestamp: int) -> (LocationSample, LocationSample):

        locationbefore = None
        locationafter = None
        #timestamp - self._timestamp c'est ce que retourne temporalDistance
        for location in self.getLocationSamples():
            # print(str(timestamp)+" vs "+str(location.getTimestamp()))
            # print(str(datetime.fromtimestamp(timestamp))+" vs "+str(datetime.fromtimestamp(location.getTimestamp())))
            # print(str(location.__class__.__name__))
            delta = location.temporalDistance(timestamp)
            if delta > 0 and (locationbefore is None or delta < locationbefore.temporalDistance(timestamp)): # or delta < deltabefore pourquoi ? j'ai remplacé par locationbefore.temporalDistance() pour qu'il trie les traces en fonction de la plus proche du timestamp en paramètre
                deltabefore = delta
                locationbefore = location
            elif delta < 0 and (locationafter is None or delta >locationafter.temporalDistance(timestamp)): # or delta > deltaafter pourquoi ? pas encore défini
                deltaafter = delta
                locationafter = location
        print(locationbefore, locationafter)
        return locationbefore, locationafter

    def __str__(self):
        return '{:s} ({:d} location samples)'.format(self.__class__.__name__, len(self.getLocationSamples()))


if __name__ == '__main__':
    # Tester l'implémentation de cette classe avec les instructions de ce bloc main (le résultat attendu est affiché ci-dessous). Commenter les lignes testant les fonctions non impémentées.
    Location.set_api_key('AIzaSyBsgJp_3ElinD9-T5r2Fbcg0AABR7caito')

    paris = Location(48.854788, 2.347557)
    lausanne = Location(46.517738, 6.632233)
    print('{:.1f} km'.format(Location.getHarvesineDistance(paris, lausanne) / 1000))
    print(lausanne.get_name())

    sample1 = LocationSample(1488540300, paris)

    print(sample1.getLocation())
    print(sample1.getTimestamp())
    print(sample1)

    sample2 = LocationSample(1488549365, lausanne)

    print(sample1 < sample2)

    a = [sample2, sample1]
    a.sort()

    print([str(x) for x in a])

    crime = LocationSample(1490977820, Location(46.520336, 6.572844))
    print(crime.getLocation().get_travel_distance_and_time(Location(46.521045, 6.574664)))

    # 412.7 km
    # Avenue de la Gare 46, 1003 Lausanne, Suisse
    # Location [latitude: 48.85479, longitude: 2.34756]
    # 1488540300
    # LocationSample [timestamp: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]
    # True
    # ['LocationSample [timestamp: 2017-03-03 12:25:00, location: Location [latitude: 48.85479, longitude: 2.34756]]', 'LocationSample [timestamp: 2017-03-03 14:56:05, location: Location [latitude: 46.51774, longitude: 6.63223]]']
    # (131, 179)
