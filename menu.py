from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

class MenuWidget(Widget):

    def on_parent(self, widget, parent):
        print("ON Parent W :" + str(self.width) + " " + str(self.height))

    def on_size(self, *args):
        print("ON SIZE W :" + str(self.width) + " " + str(self.height))
