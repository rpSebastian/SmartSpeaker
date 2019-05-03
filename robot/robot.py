from robot.recognition import Recognition
from robot.nlu import Nlu
from robot.speaker import Speaker
from robot.skills import Weather, Chat, Ticket, Noun, Music
from robot.music_player import Music_Player

class Robot():
    def __init__(self):
        self.recognizer = Recognition()
        self.music_player = Music_Player()
        self.nlu = Nlu()       
        self.speaker = Speaker()
        self.weather = Weather(self.speaker)
        self.chat = Chat(self.speaker)
        self.ticket = Ticket(self.speaker)
        self.noun = Noun(self.speaker)
        self.music = Music(self.speaker, self.music_player)

    def get_music_player(self):
        return self.music_player
        
    def process(self, fname):
        speech = self.recognizer.recognize(fname)
        if speech is not None:
            skill, response = self.nlu.query(speech)
            if skill == 'weather':
                print("命中技能天气")
                self.weather.process(response)
            elif skill == 'chat':
                print("命中技能闲聊")
                self.chat.process(response)
            elif skill == 'noun_interpretaion':
                print("命中技能名词解释")
                self.noun.process(response)
            elif skill == 'ticket':
                print("命中技能订购车票")
                self.ticket.process(response)
            elif skill == 'music':
                print("命中技能播放音乐")
                self.music.process(response)