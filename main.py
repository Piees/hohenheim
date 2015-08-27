from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy import metrics
from kivy.uix.textinput import TextInput
import re
###TO DO : inventory
import os
path, dirs, files = os.walk("/home/piees/hohenheim/images").next()
max_maps = len(files)
sizehelp = []
sizehelphelp = []


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

def take(item):
    switch = False
    for key in HohenGame.gm['takeables']:
        if key == item:
            switch = True
    if switch == True:
        HohenGame.gm['takeables'][item] = False
        HohenGame.inv[item] = True
    print HohenGame.gm
    print HohenGame.inv


class HohenGame(Widget):
    def __init__(self):
        super(HohenGame, self).__init__()
        self.textinput = TextInput(text='fish',
            x=metrics.dp(10), y=metrics.dp(48), multiline=False,
            width=metrics.dp(470), height=metrics.dp(38))
        self.textinput.bind(on_text_validate=self.on_enter)
        self.giant = Sprite(source='images/giant.png', x=metrics.dp(620),
            y=metrics.dp(330))
        self.depo = Sprite(source='images/deposit.png', x=metrics.dp(220),
            y=metrics.dp(470))
        self.axe = Sprite(source='images/axe.png', x=metrics.dp(1220),
            y=metrics.dp(470))
        self.invaxe = Image(source='images/axe.png',
            x=metrics.dp(self.invx('axe')),
            y=metrics.dp(self.invy('axe')),
            width=metrics.dp(30))
        self.invdepo = Image(source='images/deposit.png',
            x=metrics.dp(self.invx('depo')),
            y=metrics.dp(self.invy('depo')),
            width=metrics.dp(30))
        self.takehelp = {'axe': self.axe, 'depo': self.depo}
        self.gmhelp = {'giant': self.giant}
        self.invhelp = {'axe': self.invaxe, 'depo': self.invdepo}
        self.background = Sprite(source='images/background.jpg')
        self.add_widget(self.background)
        self.add_widget(self.textinput)
        self.addobjects()


    def invx(self, xhelp):
        self.xval = 1150
        try:
            self.xval = sizehelphelp['%s'%xhelp]['x']
        except:
            pass
        try:
            pass
            print(sizehelphelp['%s'%xhelp]['x'])
        except:
            pass
        return self.xval

    def invy(self, yhelp):
        self.yval = 70
        try:
            self.yval = sizehelphelp['%s'%yhelp]['y']
        except:
            pass
        return self.yval

    def refinv(self):
        self.invaxe.pos = (self.invx('axe'),self.invy('axe'))
        self.invdepo.pos = (self.invx('depo'),self.invy('depo'))
        print self.invx('depo')
        print self.invx('axe')

    def addobjects(self):
        for key in self.gm:
            if self.gm['%s'%key] == True:
                self.add_widget(self.gmhelp['%s'%key])
        for key in self.gm['takeables']:
            if self.gm['takeables']['%s'%key] == True:
                self.add_widget(self.takehelp['%s'%key])
        for key in self.inv:
            if self.inv['%s'%key] == True:
                self.add_widget(self.invhelp['%s'%key])

    def on_enter(self, value):
        if re.search('^take',value.text) != None:
            if value.text[5:] == '':
                pass
            else:
                take(value.text[5:])
        self.refgame()
        value.text = ''

    def refgame(self):
        self.refinv()
        sizehelp = [] ##what's taken (axe)
        sizehelphelp = {}
        xval = 1150
        yval = 70
        for key in self.inv:
            sizehelp.append(key)
        for x in range(len(self.inv)):
            sizehelphelp['%s'%sizehelp[x]] = {'x': xval,'y': yval}
            xval = xval + 50
            if xval == 1300:
                xval = 1150
            if x > 4:
                yval = 20
        try:
            pass
            print sizehelphelp['axe']['x']
            print sizehelphelp['depo']['x']
        except:
            pass
        self.remove_widget(self.background)
        self.remove_widget(self.giant)
        self.remove_widget(self.axe)
        self.remove_widget(self.depo)
        self.remove_widget(self.invaxe)
        self.remove_widget(self.invdepo)
        self.add_widget(self.background)
        self.addobjects()
        self.remove_widget(self.textinput)
        self.add_widget(self.textinput)

class HohenApp(App):
    def build(self):
        Game = Widget()
        Game.add_widget(HohenGame())
        Window.size = int(metrics.dp(1366)),int(metrics.dp(768))
        return Game


if __name__ == '__main__':
    HohenGame.gm = {'takeables': {
                    'axe': True,
                    'depo': True},
                    'giant': True}
    HohenGame.inv = {}
    HohenApp().run()
