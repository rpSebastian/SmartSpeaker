import requests 
import time
from .music_api import Music_api
import random

class Music():
    def __init__(self, speaker = None, music_player = None):
        self.speaker = speaker
        self.music_player = music_player
        self.music_list = []
        self.music_api = Music_api()

    def process(self, response):
        intent = response['schema']['intent']
        print(intent)
        if intent == "MUSICRANK" or intent == "MUSICINFO" or intent == "":
            self.musicrank(response)
        if intent == "PAUSE":
            self.music_player.stop()
        if intent == "CONTINUE":
            self.music_player.play_music()
        if intent == "CHANGE_TO_NEXT" or intent == "CHANGE_MUSIC":
            self.music_player.next_music()
        if intent == "CHANGE_MODE":
            self.music_player.change_mode(response['schema']['slots'][0]['normalized_word'])
        if intent == "ALBUMRANK":
            if len(response['qu_res']['lexical_analysis']) >= 3:
                self.play_album(response['qu_res']['lexical_analysis'][2]['term'])

    def play_album(self, pid):
        uid = {'一': 497814004, '二': 576744858}
        if pid not in uid.keys():
            return 
        url = "http://music.163.com/api/playlist/detail?id=" + str(uid[pid])
        result = requests.get(url).json()
        result = result['result']['tracks']
        for element in result:
            element['ar'] = element['artists']
        music_list = result
        self.music_player.set_musci_list(music_list)
        self.music_player.play_music()
        
    def get_hot_music_list(self):
        # uid = 497814004
        uid = 2779453332
        url = "http://music.163.com/api/playlist/detail?id=" + str(uid)
        result = requests.get(url).json()
        result = result['result']['tracks']
        for element in result:
            element['ar'] = element['artists']
        return result
        

    def musicrank(self, response):
        slots = response['schema']['slots']
        singer_name = None
        music_name = None
        for slot in slots:
            if slot['name'] == 'user_music_name':
                music_name = slot['normalized_word']
            elif slot['name'] == 'user_singer_name':
                singer_name = slot['normalized_word']
        music_list = self.get_music(singer_name, music_name)
        self.music_player.set_musci_list(music_list)
        self.music_player.play_music()

    def get_music(self, singer_name = None, music_name = None):
        keywards = None
        if music_name is not None:
            keywards = music_name
        elif singer_name is not None:
            keywards = singer_name
        if keywards is not None:        
            music_list = self.music_api.get_music_list(keywards)
        else:
            music_list = self.get_hot_music_list()
        return music_list


    
