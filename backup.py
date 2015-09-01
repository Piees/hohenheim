from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy import metrics
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from collections import OrderedDict
import re


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size


class HohenGame(Widget):
    def __init__(self):
        super(HohenGame, self).__init__()
        self.textinput = TextInput(hint_text='Your commands here..',
            x=metrics.dp(10), y=metrics.dp(48), multiline=False,
            width=metrics.dp(470), height=metrics.dp(38))
        self.cmd = Label(text="Welcome to Hohenheim!", x=metrics.dp(196),
            y=metrics.dp(130), text_size=(metrics.dp(460), metrics.dp(160)),
            markup=True)
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
        self.add_widget(self.cmd)
        self.addobjects()

    def cmdb(self, statement, switch):
        if switch == 'bold':
            self.cmd.text += "[b][i]\n" + statement + '[/i][/b]'
        else: self.cmd.text += statement

    def take(self, item):
        self.switch = False
        for key in self.gm['takeables']:
            if key == item:
                if self.gm['takeables'][item]['state'] == 'game':
                    self.switch = True
                elif self.gm['takeables'][item]['state'] == True:
                    self.cmdb("You already have " + item, 'bold')
        if self.switch == True:
            self.gm['takeables'][item]['state'] = 'inv'
            #self.cmd.text += "[b][i]\nYou took " + item + '[/i][/b]'
            self.cmdb("You took " + item, 'bold')


    def invx(self, xhelp):
        self.xval = 1150
        try:
            self.xval = self.sizehelphelp['%s'%xhelp]['x']
        except:
            pass
        return self.xval

    def invy(self, yhelp):
        self.yval = 70
        try:
            self.yval = self.sizehelphelp['%s'%yhelp]['y']
        except:
            pass
        return self.yval

    def refinv(self):
        self.invaxe.pos = (self.invx('axe'),self.invy('axe'))
        self.invdepo.pos = (self.invx('depo'),self.invy('depo'))
        #self.invdepo.pos = (1300,70)

    def addobjects(self):
        for key in self.gm:
            if self.gm['%s'%key] == True:
                self.add_widget(self.gmhelp['%s'%key])
        for key in self.gm['takeables']:
            if self.gm['takeables']['%s'%key]['state'] == 'game':
                self.add_widget(self.takehelp['%s'%key])
            if self.gm['takeables']['%s'%key]['state'] == 'inv':
                self.add_widget(self.invhelp['%s'%key])

    def on_enter(self, value):
        print self.gm
        print self.inv
        self.cmd.text += '\n'+self.textinput.text
        if re.search('^take',value.text) != None:
            if value.text[5:] == '':
                pass
            else:
                self.take(value.text[5:])
        self.refgame()
        value.text = ''


#    def _refocus_txtinp(self,*args):
#        self.cmd.focus = True
#        print "hi"

    def refgame(self):
        self.sizehelp = [] ##what's taken (axe)
        self.sizehelphelp = {} ##FIX THIS FOR NEW SYNTAX OF INV
        xval = 1150
        yval = 70
        for key in self.gm['takeables']:
            if self.gm['takeables'] == 'inv':
                self.sizehelp.append(key)
        self.sizehelp.reverse()
        for x in range(len(self.gm['takeables'])):
            self.sizehelphelp['%s'%self.sizehelp[x]] = {'x': xval,'y': yval}
            xval += 50
            if xval == 1300:
                xval = 1150
            if x > 4:
                yval = 20
        self.refinv()
        try:
            pass
        except:
            pass
        self.remove_widget(self.background)
        self.remove_widget(self.giant)
        self.remove_widget(self.axe)
        self.remove_widget(self.depo)
        self.remove_widget(self.invaxe)
        self.remove_widget(self.invdepo)
        self.remove_widget(self.cmd)
        self.add_widget(self.background)
        self.addobjects()
        self.remove_widget(self.textinput)
        self.add_widget(self.textinput)
        self.add_widget(self.cmd)
#        Clock.schedule_once(self._refocus_txtinp, 2)


class HohenApp(App):
    def build(self):
        Game = Widget()
        Game.add_widget(HohenGame())
        Window.size = int(metrics.dp(1366)),int(metrics.dp(768))
        return Game


if __name__ == '__main__':
    HohenGame.gm = {'takeables': {
                    'axe': {'state': 'game'},
                    'depo': {'state': 'game'}},
                    'giant': True}
    HohenGame.inv = {}
    HohenApp().run()
