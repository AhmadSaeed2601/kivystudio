from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from kivy.lang import Builder

from .logger_space import ErrorLogger

class TerminalSpace(BoxLayout):

    manager = ObjectProperty(None)
    ''' Instance of screen manager used '''

    tab_container = ObjectProperty(None)
    ''' instance of a gridlayout where tha tab lays'''

    def __init__(self, **k):
        super(TerminalSpace, self).__init__(**k)
        self.logger = ErrorLogger()
        self.add_widget(self.logger, title='Logs')

    def add_widget(self, widget, title=''):
        if len(self.children) > 1:
            tab = TerminalTab()
            tab.text=title
            tab.name=title
            tab.bind(state=self.tab_state)
            self.tab_container.add_widget(tab)
            screen = Screen(name=title)
            screen.add_widget(widget)
            self.manager.add_widget(screen)
        else:
            super(TerminalSpace, self).add_widget(widget)

    def tab_state(self, tab, state):
        if state=='down':
            self.manager.current = tab.name

class TerminalTab(ToggleButtonBehavior, Label):

    def on_state(self, *a):
        if self.state=='down':
            self.text = "[u]" + self.text + "[/u]"
            self.color = (.9,.9,.9,1)
        else:
            self.text = self.text.replace('[u]','').replace('[/u]','')
            self.color = (.5,.5,.5,1)

Builder.load_string('''
<TerminalSpace>:
    tab_container: tab_container
    manager: manager
    orientation: 'vertical'
    pos_hint: {'y': 0, 'center_x': .5}
    size_hint_y: .4
    canvas.before:
        Color:
            rgba: .12,.12,.12,1
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 1,1,1,1
        Line:
            points: [self.x,self.top,self.right,self.top]
            width: dp(1.4)
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        GridLayout:
            id: tab_container
            rows: 1
        BoxLayout:
            size_hint_x: None
            width: self.minimum_width
            IconLabelButton:
                icon: 'fa-close'
                size_hint_x: None
                width: '12dp'

    ScreenManager:
        id: manager

<TerminalTab>:
    allow_no_selection: False
    size_hint_x: None
    width: '94dp'
    markup: True

''')