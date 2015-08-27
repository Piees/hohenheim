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
        self.xval = 1150
        self.yval = 70
        try:
            self.xval = sizehelphelp['axe']['x']
        except:
            pass ###### MAKE FOR DEPO!!!!!! >>><<<<<
        try:
            self.yval = sizehelphelp['axe']['y']
        except:
            pass

#        self.invaxe = Image(source='images/axe.png', x=metrics.dp(1200),
#            y=metrics.dp(70), width=metrics.dp(30))
#        print(sizehelphelp['axe'])
        self.invaxe = Image(source='images/axe.png',
            x=metrics.dp(self.xval),
            y=metrics.dp(self.yval),
            width=metrics.dp(30))
        self.invdepo = Image(source='images/depo.png',
            x=metrics.dp(self.xval),
            y=metrics.dp(self.yval),
            width=metrics.dp(30))
        self.takehelp = {'axe': self.axe, 'depo': self.depo}
        self.gmhelp = {'giant': self.giant}
        self.invhelp = {'invaxe': self.invaxe}
        self.background = Sprite(source='images/background.jpg')
        self.add_widget(self.background)
        print(self.gm['giant'])
        self.add_widget(self.invaxe)
        self.add_widget(self.textinput)
        self.addobjects()


    def invx(self, xhelp):


    def addobjects(self):
        for key in self.gm:
            if self.gm['%s'%key] == True:
                self.add_widget(self.gmhelp['%s'%key])
        for key in self.gm['takeables']:
            if self.gm['takeables']['%s'%key] == True:
                self.add_widget(self.takehelp['%s'%key])
        self.remove_widget(self.invaxe)
        self.add_widget(self.invaxe)
        self.remove_widget(self.invdepo)
        self.add_widget(self.invdepo)
#        for key in self.inv:
#            if self.inv['%s'%key] == True:
#                self.add_widget(self.takehelp['%s'%key])



    #def on_enter(instance, value):
    def on_enter(self, value):
        if re.search('^take',value.text) != None:
            if value.text[5:] == '':
                pass
            else:
                take(value.text[5:])
        #self.remove_widget(self.textinput)
        #HohenGame.refgame(HohenGame())
        #HohenGame.remove_widget(HohenGame.giant)
        #print(value.text)
        self.refgame()
        value.text = ''
        #take('axe')

    def refgame(self):
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
        #print(sizehelphelp['axe'])
        print 'test'
#        try:
#            print(sizehelphelp['axe']['x'])
#        except:
#            pass
#        self.fish = {}
#        for key in self.inv:
#            self.fish['%s'%key] = 20
        self.remove_widget(self.background)
        self.remove_widget(self.giant)
        self.remove_widget(self.axe)
        self.remove_widget(self.depo)
        print('fishy')
        self.add_widget(self.background)
        print(self.gm['giant'])
        self.addobjects()
        self.remove_widget(self.textinput)
        self.add_widget(self.textinput)


    #def changemap(self, num):
    #    print self.currstg
    #    if max_maps > HohenGame.gm['currstg']:
    #        HohenGame.gm['currstg'] += num
    #    parent = self.parent
    #    parent.remove_widget(self)
    #    parent.add_widget(HohenGame())

    #def on_touch_down(self, *ignore):
    #    self.changemap(1)
    #    print(self.textinput.text)



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
