from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from ingrediints import ing
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from reciep import rec

KV = '''
<Content>
    id:content
    orientation: "horizontal"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"
    MDTextField:
        id: gramms
        hint_text: "City"
    MDLabel:
        id: texts
        text: ""
        theme_text_color: "Custom"
        text_color: [0, 0, 0, 0.5]

MDScreen:
    id: scr
    scr1: scr1
    MDBottomNavigation:
        text_color_normal: "#173B1E"
        panel_color: "#BCBCBC"
        selected_color_background: "#173B1E"
        text_color_active: "black"
        MDBottomNavigationItem:
            id: scr1
            name: 'screen 1'
            text: 'Ингредиенты'
            icon: 'fridge'
            badge_icon: "numeric-10"
            MDScrollView:
                pos_hint:{"center_x":.5,"center_y":.75}
                size_hint: (1,.2)
                MDList:
                    id: container
            MDScrollView:
                pos_hint:{"center_x":.5,"center_y":.25}
                size_hint: (1,.5)
                MDList:
                    id: list_products
            BoxLayout:
                size_hint_y: None
                height: self.minimum_height
                pos_hint: {"center_x": .5, "center_y": 0.9}
                MDTextField:
                    id:pole
                    hint_text: "Helper text on focus"
                    helper_text: "This will disappear when you click off"
                    helper_text_mode: "on_focus"
                    on_text: app.indigrid()
                MDIconButton:
                    icon: "close"
                    line_color: "black"
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_press: app.clear()
                

        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Рецепты'
            icon: 'silverware-variant'


            MDLabel:

                text: 'Рецепты'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Любимое'
            icon: 'heart'
            MDLabel:
                text: 'Избранное'
                halign: 'center'

'''

products = {}
product = ''


class Content(BoxLayout):
    pass


class Test(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Light"
        return self.screen

    def indigrid(self):
        self.root.ids.container.clear_widgets()
        to_print = set()
        for i in ing.keys():
            if len(self.screen.ids.pole.text.lower()) != 0 and self.screen.ids.pole.text.lower() == i[
                                                                                                    :len(
                                                                                                        self.screen.ids.pole.text)].lower():
                to_print.add(i.capitalize())
        if len(to_print) == 0:
            pass
        for i in to_print:
            self.root.ids.container.add_widget(
                OneLineListItem(text=i, on_release=self.dobavka))

    def dobavka(self, arg):
        global product
        product = arg.text
        if not self.dialog:
            self.dialog = MDDialog(
                title="Discard draft?",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.zakritie
                    ),
                    MDFlatButton(
                        text="ADD",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_press=self.final
                    ),
                ],
            )
        self.dialog.content_cls.ids.texts.text = ing[arg.text]
        self.dialog.content_cls.ids.gramms.text = ''
        self.dialog.open()

    def final(self, arg):
        self.dialog.dismiss(force=True)
        products[product] = self.dialog.content_cls.ids.gramms.text
        self.root.ids.list_products.clear_widgets()
        for i in products.keys():
            self.root.ids.list_products.add_widget(
                OneLineListItem(text=f'{i} - {products[i]} {ing[i]}', on_release=self.udalenie))

    def udalenie(self, arg):
        nazv = arg.text.split(' - ')
        del products[nazv[0]]
        self.root.ids.list_products.clear_widgets()
        for i in products.keys():
            self.root.ids.list_products.add_widget(
                OneLineListItem(text=f'{i} - {products[i]}', on_release=self.udalenie))

    def zakritie(self, arg):
        self.dialog.dismiss(force=True)

    def clear(self):
        self.screen.ids.pole.text = ''


Test().run()
