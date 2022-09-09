# Import all modules.
from kivy.config import Config
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import datetime
import cv2
import os
import pytesseract
from helper import convert


# Define the path to the underlying tesseract engine.
# Use different paths for windows (nt) and mac (posix).
# THIS APP RUNS ON WINDOWS AND MAC, HOWEVER
# THE DESIGN IS OPTIMIZED FOR A MACBOOK AIR M1.
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
elif os.name == 'posix':
    pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
else:
    raise RuntimeError

# Fix the size of the window in order to ensure a
# consistent user experience.
Config.set('graphics', 'resizable', False)

# Load the kivy file that handles all design.
Builder.load_file("app.kv")

# Declare all screens available in the app.
class MainScreen(Screen):
    pass
class CameraScreen(Screen):
    pass
class UploadScreen(Screen):
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
        sm.add_widget(UploadScreen(name='uploadScreen'))
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

    # This function switches to the upload screen.
    def openUpload(self):
        self.root.current = 'uploadScreen'

    # This function uploads an image and then uses
    # all functionality to convert the MRZ to a string
    # and display the result on the screen.
    def confirmUpload(self):

        # Takes an image with opencv and stores it in the
        # variable 'image'.
        image = cv2.imread(self.root.get_screen('uploadScreen').ids.my_image.source)
        # Resets the image that was taken to prevent reading
        # in values from the previous person.
        self.root.get_screen('uploadScreen').ids.my_image.source = ''
        # Uses the helper script to cut out the MRZ zone from
        # the whole picture.
        roi = convert(image)
        # Tries to read the image of the MRZ zone with tesseract
        # and convert it to a string.
        try:
            ocr_string = pytesseract.image_to_string(roi, lang="ocrb")
        # On failing this resets the variables that define whether a
        # person can enter or not. Prevents reading in values from
        # the previous person.
        except:
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

            # Shows the camera screen.
            self.root.current = 'cameraScreen'

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

    # This function selects the image from the device.
    # Printing for debug purposes.
    def selected(self, filename):
        try:
            self.root.get_screen('uploadScreen').ids.my_image.source = filename[0]
            print(filename[0])
        except:
            pass

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
        # variable 'camera' and exports it as png.
        camera = self.root.get_screen('cameraScreen').ids['camera']
        camera.export_to_png("xyz.png")
        # Reads in the png from before and removes it
        # from the storage location.
        image = cv2.imread("xyz.png")
        os.remove("xyz.png")
        # Uses the helper script to cut out the MRZ zone from
        # the whole picture.
        roi = convert(image)
        # Tries to read the image of the MRZ zone with tesseract
        # and convert it to a string.
        try:
            ocr_string = pytesseract.image_to_string(roi, lang="ocrb")
        # On failing this resets the variables that define whether a
        # person can enter or not. Prevents reading in values from
        # the previous person.
        except:
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
