#<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d24790.277856716584!2d-82.13013938115233!3d39.043027350019734!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sus!4v1671314973302!5m2!1sen!2sus" width="640" height="480" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>

import PySimpleGUI as sg
from PySimpleGUI import Webview

sg.theme('DarkAmber')  # Add a touch of color

# All the stuff inside your window.
layout = [[sg.Text('PyWebview inside PySimpleGUI')],
          [sg.Webview(url='https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d24790.277856716584!2d-82.13013938115233!3d39.043027350019734!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sus!4v1671314973302!5m2!1sen!2sus', size=(640, 480))],
          [sg.Button('Close')]]

# Create the Window
window = sg.Window('Window Title', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close'):  # if user closes window or clicks cancel
        window.close()
        break
window.close()
