from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from UDP_PC import broadcast_PC
from functools import partial
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
import webbrowser
import math
import threading


class searchPage(FloatLayout):
    Robot_num = []  # 每个机器人IP地址
    Robot_state = []  # 机器人连接状态
    Robot_len = 0  # 机器人IP数量
    Robot_index = 0  # 机器人序号
    Robot_Page = 0  # 总页数
    Robot_currentPage = 0  # 当前页数
    Robot_pageNum = 7  # 一页显示的数量

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #fullscreen = True
        with self.canvas:
            searchPage.size = 1920, 1200
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self.redraw, size=self.redraw)

        with self.canvas:
            searchPage.size = 1920, 300
            Color(98/255, 102/255, 107/255, 1)
            self.bg_rect = Rectangle(pos=(0, 1057), size=self.size)
            self.bind(pos=self.redraw, size=self.redraw)

        with self.canvas:
            Color(.2, .2, .2, 1)
            Line(points=[20, 985, 1900, 985], width=1)
            self.add_widget(Label(text='Elfin机器人连接助手',
                                  font_name='packages/font/SourceHanSansCN-Bold.ttf', font_size='40',
                                  size_hint=(None, None),
                                  pos_hint={"x": 260 / 1920,
                                            "center_y": 1150 / 1200},
                                  color=[1, 1, 1, 1]))
            self.add_widget(AsyncImage(source="packages/hans.png",
                                       pos_hint={"center_x": 70 / 1920,
                                                 "center_y": 1150 / 1200}))  # 216.5   84
            self.add_widget(Label(text='机器人名称',
                                  font_name='packages/font/SourceHanSansCN-Heavy.ttf',
                                  font_size='32',
                                  size_hint=(None, None),
                                  pos_hint={"x": .075,
                                            "center_y": .89},
                                  color=[51 / 255, 51 / 255, 51 / 255, 1]))
            self.add_widget(AsyncImage(source="packages/hans.png",
                                       pos_hint={"center_x": 70 / 1920,
                                                 "center_y": 1150 / 1200}))
            self.add_widget(Label(text='IP',
                                  font_name='packages/font/SourceHanSansCN-Heavy.ttf',
                                  font_size='32',
                                  size_hint=(None, None),
                                  pos_hint={"x": .4,
                                            "center_y": .89},
                                  color=[51 / 255, 51 / 255, 51 / 255, 1]))
        self.add_Button('search')
        self.loading = AsyncImage(source="packages/loading.gif",
                                  pos_hint={"center_x": .5,
                                            "center_y": .5},
                                  anim_delay=.025)

        self.LastPage = Button(text='上一页',
                               font_name='packages/font/SourceHanSansCN-Normal.ttf',
                               font_size='28', size=(150, 60),
                               size_hint=(None, None),
                               pos_hint={"center_x": .3,
                                         "center_y": 140/1200},
                               color=[55/255, 144/255, 252/255, 1],
                               background_normal="",
                               background_color=[1, 1, 1, 1])
        self.LastPage.bind(on_press=partial(self.lastPage))
        self.NextPage = Button(text='下一页',
                               font_name='packages/font/SourceHanSansCN-Regular.ttf',
                               font_size='28', size=(150, 60),
                               size_hint=(None, None),
                               pos_hint={"center_x": .7,
                                         "center_y": 140/1200},
                               # 边框颜色187.187.187.1
                               color=[55/255, 144/255, 252/255, 1],
                               background_normal="",
                               background_color=[1, 1, 1, 1])
        self.NextPage.bind(on_press=partial(self.nextPage))
        # print('数量是：',threading.activeCount())

    def redraw(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def searchButton(self, *args):
        searchPage.Robot_num = []
        Robot_len = 0
        Robot_Page = 0
        searchPage.Robot_index = 0
        searchPage.Robot_currentPage = 1
        self.clear_widgets()
        self.add_widget(self.loading)
        search = threading.Thread(target=self.run_search)
        search.start()

    def run_search(self):
        searchPage.Robot_num, searchPage.Robot_state = broadcast_PC()
        self.clear_widgets()
        searchPage.Robot_len = len(searchPage.Robot_num)
        self.robot_list()

    def connectButton(self, index, *args):
        ip = searchPage.Robot_num[index]
        if searchPage.Robot_state[index] == '连接':
            searchPage.Robot_state[index] = '已连接'
        self.clear_widgets()
        self.add_Button('search')
        connect = threading.Thread(target=self.run_connect)
        connect.start()
        webbrowser.open(ip)

    def run_connect(self):
        y_coordinate = 860
        searchPage.Robot_index = (
            searchPage.Robot_currentPage - 1) * searchPage.Robot_pageNum
        self.add_Button('page')
        for i in range(searchPage.Robot_pageNum):
            searchPage.Robot_index += 1
            self.add_robot(y_coordinate)
            y_coordinate -= 110
        if searchPage.Robot_currentPage < searchPage.Robot_Page:
            self.add_Button('next')
        elif searchPage.Robot_currentPage == searchPage.Robot_Page:
            searchPage.add_Button('last')

    def nextPage(self, *args):
        y_coordinate = 860
        searchPage.Robot_currentPage += 1
        self.clear_widgets()
        #self.__init__()  # 初始化界面
        self.add_Button('search')
        self.add_Button('page')
        self.add_Button('last')  # 添加 （机器人总数 - 当前机器人编号） 数量的机器人
        for i in range(searchPage.Robot_len - searchPage.Robot_index):
            searchPage.Robot_index += 1
            self.add_robot(y_coordinate)
            y_coordinate -= 110
            if i == searchPage.Robot_pageNum - 1:
                break
        if searchPage.Robot_currentPage != searchPage.Robot_Page:  # 如果不是最后一页，增加下一页按钮
            self.add_Button('next')

    def lastPage(self, *args):
        y_coordinate = 860
        searchPage.Robot_currentPage -= 1
        searchPage.Robot_index = (
            searchPage.Robot_currentPage - 1) * searchPage.Robot_pageNum
        self.clear_widgets()
        self.add_Button('page')
        self.add_Button('currentPage')
        self.add_Button('next')
        if searchPage.Robot_currentPage != 1:  # 如果不是第一个，添加上一页按键
            self.add_Button('last')
        if searchPage.Robot_currentPage == 1:  # 如果是第一页，从0开始
            searchPage.Robot_index = 0
        for i in range(searchPage.Robot_pageNum):
            searchPage.Robot_index += 1
            self.add_robot(y_coordinate)
            y_coordinate -= 110

    def robot_list(self):
        y_coordinate = 860
        if searchPage.Robot_num[0] != 'Error':
            searchPage.Robot_Page = math.ceil(
                searchPage.Robot_len / searchPage.Robot_pageNum)  # 向上取整得页数
            for i in range(searchPage.Robot_len):
                searchPage.Robot_index += 1
                self.add_robot(y_coordinate)
                y_coordinate -= 110
                if i == (searchPage.Robot_pageNum - 1) and searchPage.Robot_Page > 1:
                    self.add_Button('next')
                    break
            self.add_Button('page')
        else:
            self.error()
        self.add_Button('search')

    def add_Button(self, button):
        if button == 'search':
            self.search = Button(text='搜索',
                                 font_name='packages/font/SourceHanSansCN-Normal.ttf',
                                 font_size='36', size=(480, 100),
                                 size_hint=(None, None),
                                 # pos_hint={"center_x": .5,
                                 # "center_y": 140/1200},
                                 pos=(720, 90),
                                 # pos=(720, 90),1920/2=96-240=720
                                 color=[1, 1, 1, 1],
                                 background_normal="",
                                 background_down='packages/search.png',
                                 background_color=[
                                     55 / 255, 144 / 255, 252 / 255, 1])
                                 #disabled=self.Flag)
            self.search.bind(on_release=self.searchButton)
            self.add_widget(self.search)
        if button == 'next':
            self.add_widget(self.NextPage)
        if button == 'last':
            self.add_widget(self.LastPage)
        if button == 'page':
            self.Label_Page = Label(text=str(searchPage.Robot_currentPage) + '     总页数' + str(searchPage.Robot_Page),
                                    font_name='packages/font/SourceHanSansCN-Normal.ttf',
                                    font_size='24',
                                    size_hint=(None, None),
                                    pos_hint={"center_x": .5,
                                              "center_y": 45/1200},
                                    color=[153 / 255, 153 / 255, 153 / 255, 1])
            self.add_widget(self.Label_Page)

    def add_robot(self, y_coordinate):
        self.list_Robot_ID = Label(text='Robot_' + str(searchPage.Robot_index),
                                   font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                   font_size='30', size_hint=(None, None),
                                   pos=(90, y_coordinate),
                                   color=[51/255, 51/255, 51/255, 1])
        self.list_Robot_IP = Label(text=searchPage.Robot_num[searchPage.Robot_index - 1],
                                   font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                   font_size='30',
                                   size_hint=(None, None),
                                   pos=(800, y_coordinate),
                                   color=[51/255, 51/255, 51/255, 1])
        self.list_Robot_Button = Button(text=searchPage.Robot_state[searchPage.Robot_index - 1],
                                        font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                        font_size='30',
                                        size_hint=(None, None),
                                        size=(160, 60),
                                        pos=(1650, y_coordinate),
                                        color=[1, 1, 1, 1],
                                        background_normal="",
                                        background_color=[55/255, 144/255, 252/255, 1])
        self.list_Robot_Button.bind(
            on_press=partial(self.connectButton, searchPage.Robot_index-1))
        self.add_widget(self.list_Robot_ID)
        self.add_widget(self.list_Robot_IP)
        self.add_widget(self.list_Robot_Button)

    def error(self):
        if searchPage.Robot_num[1] == 10000:
            self.add_widget(Label(text='连接网络失败，请检查网络是否异常',
                                  font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                  font_size='30',
                                  size_hint=(None, None),
                                  pos_hint={"center_x": .5,
                                            "center_y": 0.75},
                                  color=[153 / 255, 153 / 255, 153 / 255, 1]))
        elif searchPage.Robot_num[1] == 10001:
            self.add_widget(Label(text='没有搜索到附近的机器人！',
                                  font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                  font_size='30',
                                  size_hint=(None, None),
                                  pos_hint={"center_x": .5,
                                            "center_y": 0.75},
                                  color=[153 / 255, 153 / 255, 153 / 255, 1]))
        else:
            self.add_widget(Label(text='unknow error',
                                  font_name='packages/font/SourceHanSansCN-Regular.ttf',
                                  font_size='30',
                                  size_hint=(None, None),
                                  pos_hint={"center_x": .5,
                                            "center_y": 0.75},
                                  color=[153 / 255, 153 / 255, 153 / 255, 1]))


class HansApp(App):
    def build(self):
        return searchPage()


if __name__ == '__main__':
    HansApp().run()
