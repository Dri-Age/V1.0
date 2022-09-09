# Import all modules.
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from PIL import Image
import requests
import datetime
import io

# Load the kivy string that handles all design.
Builder.load_string('''
<MainScreen>:

    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'background.jpg'

    MDLabel:
        id: logo
        text: 'Dri-Age'
        halign: 'center'
        font_style: 'H2'
        font_name: 'Antonio'
        pos_hint: {'center_x': 0.5, 'center_y': 0.875}

    MDLabel:
        id: chosen
        text: ''
        text_color: 0, 0, 0, 0
        halign: 'center'
        font_style: 'H6'
        font_name: 'Antonio'
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}

    MDLabel:
        id: choose
        text: 'Choose your first age limit:'
        text_color: 0, 0, 0, 0
        halign: 'center'
        font_style: 'H6'
        font_name: 'Antonio'
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}

    MDFillRoundFlatButton:
        size_hint: 0.3, 0.4
        pos_hint: {'center_x': 0.66, 'center_y': 0.275}
        on_press:
            app.openCamera()

    MDIcon:
        id: camera_icon
        halign: 'center'
        icon: 'camera-outline'
        font_size: '100sp'
        pos_hint: {'center_x': 0.66, 'center_y': 0.265}
        opacity: 1 # visibility

    MDFillRoundFlatButton:
        id: age_limit_16
        text: '16+'
        font_size: '35sp'
        font_name: 'Antonio'
        size_hint: 0.1, 0.1
        pos_hint: {'center_x': 0.25, 'center_y': 0.425}
        on_press:
            app.setAge(16)

    MDFillRoundFlatButton:
        id: age_limit_18
        text: '18+'
        font_size: '35sp'
        font_name: 'Antonio'
        size_hint: 0.1, 0.1
        pos_hint: {'center_x': 0.4, 'center_y': 0.425}
        on_press:
            app.setAge(18)

    MDTextField:
        id: age_limit_custom_text
        hint_text: 'custom age limit'
        pos_hint: {'center_x': 0.325, 'center_y': 0.25}
        size_hint_x: None
        font_name: 'Antonio'
        width: 450
        icon_right: 'pencil'

    MDFillRoundFlatButton:
        id: age_limit_custom_btn
        text: 'add custom'
        font_name: 'Antonio'
        pos_hint: {'center_x': 0.27, 'center_y': 0.1}
        on_press:
            app.setAge("c")

    MDFillRoundFlatButton:
        id: age_limit_remove
        text: ''
        size_hint: 0.05, 0.05
        pos_hint: {'center_x': 0.41, 'center_y': 0.1}
        on_press:
            app.setAge("dc")

    MDIcon:
        id: trash-can
        halign: 'center'
        icon: 'trash-can'
        font_size: '30sp'
        pos_hint: {'center_x': 0.41, 'center_y': 0.1}
        opacity: 1 # visibility


<CameraScreen>:

    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: 'background.jpg'

    MDScreen:
        MDBoxLayout:
            orientation: "vertical"
            MDLabel:
                text: ""

    Camera:
        id: camera
        index: 0
        resolution: (1280, 960)
        play: True

    MDFillRoundFlatButton:
        id: camera_click
        size_hint: 0.3, 0.3
        height: '48dp'
        pos_hint: {'center_x': 0.95, 'center_y': 0.5}
        on_press:
            app.capture()

    MDIcon:
        id: camera_icon
        halign: 'center'
        icon: 'camera-outline'
        font_size: '80sp'
        pos_hint: {'center_x': 0.92, 'center_y': 0.5}
        opacity: 1 # visibility

    MDFillRoundFlatButton:
        size_hint: 0.2, 0.2
        pos_hint: {'center_x': 0.95, 'center_y': 0.05}
        on_press:
            app.openMain()

    MDIcon:
        id: back_icon
        halign: 'center'
        icon: 'arrow-left-bold'
        font_size: '60sp'
        pos_hint: {'center_x': 0.95, 'center_y': 0.05}
        opacity: 1 # visibility

    MDRaisedButton:
        text: ''
        id: half_leftside
        font_size:'65sp'
        size_hint: 0.33, 1
        pos_hint: {'center_x': 0.215, 'center_y': 0.5}
        on_press:
            app.openCamera()
        opacity: 0
        disabled: True
        md_bg_color: [0, 0, 0, 0]

    MDRaisedButton:
        text: ''
        id: half_rightside
        font_size:'65sp'
        size_hint: 0.35, 1
        pos_hint: {'center_x': 0.64, 'center_y': 0.5}
        on_press:
            app.openCamera()
        opacity: 0
        disabled: True
        md_bg_color: [0, 0, 0, 0]

    MDRaisedButton:
        text: ''
        id: whole
        font_size:'65sp'
        size_hint: 0.9, 1
        pos_hint: {'center_x': 0.4, 'center_y': 0.5}
        on_press:
            app.openCamera()
        opacity: 0
        disabled: True
        md_bg_color: [0, 0, 0, 0]
''')

# Declare all screens available in the app.
class MainScreen(Screen):
    pass
class CameraScreen(Screen):
    pass

# Define the app.
class Main(MDApp):

    # Define some (root) variables that are accessible from all screens.
    age_limit1 = ""
    age_limit2 = ""
    btns = []

    # This function is called when the app is first started.
    def build(self):

        # Define themes that color the app.
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "LightGreen"

        # Set the title of the app.
        self.title = "Dri-Age"

        # Initialize the screen manager for switching between screens.
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='mainScreen'))
        sm.add_widget(CameraScreen(name='cameraScreen'))
        return sm

    # This function switches to the main screen.
    def openMain(self):
        self.root.current = 'mainScreen'

    # This function switches to the camera screen.
    def openCamera(self):

        # Only open the camera when at least 1 age to check has
        # been entered in the main screen.
        if len(MDApp.get_running_app().btns) != 0:

            # Reset the variables that define whether a person can
            # enter or not. Prevents reading in values from the
            # previous person.
            self.root.get_screen('cameraScreen').ids.whole.text =  ''
            self.root.get_screen('cameraScreen').ids.whole.opacity = 0
            self.root.get_screen('cameraScreen').ids.whole.disabled = True
            self.root.get_screen('cameraScreen').ids.half_leftside.text =  ''
            self.root.get_screen('cameraScreen').ids.half_leftside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_leftside.disabled = True
            self.root.get_screen('cameraScreen').ids.half_rightside.text =  ''
            self.root.get_screen('cameraScreen').ids.half_rightside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_rightside.disabled = True

            # Switch to the screen.
            self.root.current = 'cameraScreen'

    # This function sets the age the app should check.
    def setAge(self, btn):
        # This selects a custom age to check, if only zero
        # or one ages have been added already.
        if btn == "c" and len(MDApp.get_running_app().btns)<2:
            btn = self.root.get_screen('mainScreen').ids.age_limit_custom_text.text
            # This handles cases where the user enters
            # something that is not an integer.
            try:
                btn = int(btn)
            except:
                btn = None
        # This deletes all ages that the app should check.
        elif btn == "dc":
            btn = None
            MDApp.get_running_app().btns = []
            # This shows the default labels for zero ages.
            self.root.get_screen('mainScreen').ids.choose.text = 'Choose your first age limit.'
            self.root.get_screen('mainScreen').ids.chosen.text = ''
        # This empties the custom age filed after selecting
        # a custom age.
        self.root.get_screen('mainScreen').ids.age_limit_custom_text.text = ''

        # If an age should be added (custom or a predefined)
        # this actually adds it.
        if btn != None:
            # If the age has not already been selected and
            # only zero or one ages are already selected
            # the age is added to be checked.
            if btn not in MDApp.get_running_app().btns:
                if len(MDApp.get_running_app().btns)<2:
                    MDApp.get_running_app().btns.append(btn)
            # If the age has already been selected
            # it is removed.
            else:
                MDApp.get_running_app().btns.remove(btn)
            # Depending on the number of ages the abb should check
            # different text is displayed.
            btns_len = len(MDApp.get_running_app().btns)
            if btns_len == 0:
                self.root.get_screen('mainScreen').ids.choose.text = 'Choose your first age limit.'
                self.root.get_screen('mainScreen').ids.chosen.text = ''
            elif btns_len == 1:
                self.root.get_screen('mainScreen').ids.choose.text = 'Choose your second age limit or start scanning'
                self.root.get_screen('mainScreen').ids.chosen.text = 'You chose: ' + str(MDApp.get_running_app().btns[0])
            elif btns_len == 2:
                self.root.get_screen('mainScreen').ids.choose.text = 'You are ready to scan.'
                self.root.get_screen('mainScreen').ids.chosen.text = 'You chose: ' + str(MDApp.get_running_app().btns[0]) + ' & ' + str(MDApp.get_running_app().btns[1])

    # This function takes an image and then uses
    # all functionality to convert the MRZ to a string
    # and display the result on the screen.
    def capture(self):
        # Takes an image with opencv, stores it in the
        # variable 'camera' and converts it through several
        # functions and operations to bytes needed for
        # our server.
        camera = self.root.get_screen('cameraScreen').ids['camera']
        texture = camera.texture
        size = texture.size
        pixels = texture.pixels
        pil_image = Image.frombytes(mode='RGBA', size=size, data=pixels)
        output = io.BytesIO()
        pil_image.save(output, format="png")
        # Defines the variables for our request and makes
        # a POST request to the server.
        files = {'file': output.getvalue()}
        url = "http://35.187.23.141:80"
        values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
        r = requests.post(url, files=files, data=values)
        # If the request was successful the ocr string is
        # extracted from the server's response.
        if r.ok:
            ocr_string = r.text[:-1]
        # Otherwise this resets the variables that define whether a
        # person can enter or not. Prevents reading in values from
        # the previous person.
        else:
            self.root.get_screen('cameraScreen').ids.whole.text = ''
            self.root.get_screen('cameraScreen').ids.whole.opacity = 0
            self.root.get_screen('cameraScreen').ids.whole.disabled = True
            self.root.get_screen('cameraScreen').ids.half_leftside.text = ''
            self.root.get_screen('cameraScreen').ids.half_leftside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_leftside.disabled = True
            self.root.get_screen('cameraScreen').ids.half_rightside.text = ''
            self.root.get_screen('cameraScreen').ids.half_rightside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_rightside.disabled = True
            self.root.current = 'cameraScreen'
            return None

        # This runs if the ocr string is from a driver's license.
        if len(ocr_string) < 78:
            # Uses splitting and other string methods to store
            # the year (with added 1900/2000), month and day.
            try:
                ocr = ocr_string.split("\n")
                birthdate = ocr[1].rstrip("<")
                yob = int(birthdate[-6:-4])
                mob = int(birthdate[-4:-2])
                dob = int(birthdate[-2:])
                if yob > int(str(datetime.date.today().year)[2:]):
                    yob += 1900
                else:
                    yob += 2000
            # If the numbers were mistakenly read as characters
            # this handles that error.
            except:
                yob, mob, dob = None, None, None
        # This runs if the ocr string is from a identity card.
        elif len(ocr_string) < 100:
            # Uses splitting and other string methods to store
            # the year (with added 1900/2000), month and day.
            try:
                ocr = ocr_string.split("\n")
                birthdate = ocr[1][:7]
                yob = int(birthdate[:2])
                mob = int(birthdate[2:4])
                dob = int(birthdate[4:6])
                cs = int(birthdate[6])
                if yob > int(str(datetime.date.today().year)[2:]):
                    yob += 1900
                else:
                    yob += 2000
                print(yob, mob, dob)
            # If the numbers were mistakenly read as characters
            # this handles that error.
            except:
                yob, mob, dob = None, None, None
        # This runs if the ocr string couldn't be read properly
        # and handles that error.
        else:
            yob, mob, dob = None, None, None

        # If we had no error above this shows the results.
        if not (yob == None or mob == None or dob == None):
            # These two lines compute the age given the actual
            # day and a birthdate,
            today = datetime.date.today()
            # Subtracts a boolean (0 or 1) if necessary.
            current_age = today.year - yob - ((today.month, today.day) < (mob, dob))

            # This runs when only one age has been selected to
            # be checked.
            if len(MDApp.get_running_app().btns) == 1:
                # Stores the age that has been selected.
                age1 = MDApp.get_running_app().btns[0]
                # Decides whether the person can enter or not
                # and selects the corresponding color.
                if current_age >= age1:
                    allow1 = "\nAllowed"
                    self.root.get_screen('cameraScreen').ids.whole.md_bg_color = [0, 1, 0, 1]
                else:
                    allow1 = "\nDenied"
                    self.root.get_screen('cameraScreen').ids.whole.md_bg_color = [1, 0, 0, 1]
                # Shows the decision made above.
                self.root.get_screen('cameraScreen').ids.whole.text =  str(age1) + "+" + allow1
                self.root.get_screen('cameraScreen').ids.whole.opacity = 0.5
                self.root.get_screen('cameraScreen').ids.whole.disabled = False

            # This runs when two ages have been selected to
            # be checked.
            elif len(MDApp.get_running_app().btns) == 2:
                # Stores the ages that have been selected.
                age1 = MDApp.get_running_app().btns[0]
                age2 = MDApp.get_running_app().btns[1]
                # Decides whether the person can enter or not
                # and selects the corresponding color.
                if current_age >= age1:
                    allow1 = "\nAllowed"
                    self.root.get_screen('cameraScreen').ids.half_leftside.md_bg_color = [0, 1, 0, 1]
                else:
                    allow1 = "\nDenied"
                    self.root.get_screen('cameraScreen').ids.half_leftside.md_bg_color = [1, 0, 0, 1]
                # Decides whether the person can enter or not
                # and selects the corresponding color.
                if current_age >= age2:
                    allow2 = "\nAllowed"
                    self.root.get_screen('cameraScreen').ids.half_rightside.md_bg_color = [0, 1, 0, 1]
                else:
                    allow2 = "\nDenied"
                    self.root.get_screen('cameraScreen').ids.half_rightside.md_bg_color = [1, 0, 0, 1]
                # Shows the decision made above.
                self.root.get_screen('cameraScreen').ids.half_leftside.text =  str(age1) + "+" + allow1
                self.root.get_screen('cameraScreen').ids.half_leftside.opacity = 0.5
                self.root.get_screen('cameraScreen').ids.half_leftside.disabled = False
                self.root.get_screen('cameraScreen').ids.half_rightside.text = str(age2) + "+" + allow2
                self.root.get_screen('cameraScreen').ids.half_rightside.opacity = 0.5
                self.root.get_screen('cameraScreen').ids.half_rightside.disabled = False

        # If we had an error above this resets the variables that define whether a
        # person can enter or not. Prevents reading in values from
        # the previous person.
        else:
            self.root.get_screen('cameraScreen').ids.whole.text = ''
            self.root.get_screen('cameraScreen').ids.whole.opacity = 0
            self.root.get_screen('cameraScreen').ids.whole.disabled = True
            self.root.get_screen('cameraScreen').ids.half_leftside.text = ''
            self.root.get_screen('cameraScreen').ids.half_leftside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_leftside.disabled = True
            self.root.get_screen('cameraScreen').ids.half_rightside.text = ''
            self.root.get_screen('cameraScreen').ids.half_rightside.opacity = 0
            self.root.get_screen('cameraScreen').ids.half_rightside.disabled = True
            self.root.current = 'cameraScreen'


# Start the app.
Main().run()
