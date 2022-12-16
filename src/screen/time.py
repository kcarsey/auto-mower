import PySimpleGUI as sg
import datetime

# Define the layout for the first tab
tab1_layout = [[sg.Text('This is tab 1')],
               [sg.Button('Button 1')],
               [sg.Text(size=(20,1), key='-CLOCK-', font='Helvetica 20')]]

# Define the layout for the second tab
tab2_layout = [[sg.Text('This is tab 2')],
               [sg.Button('Button 2')]]

# Define the layout for the third tab
tab3_layout = [[sg.Text('This is tab 3')],
               [sg.Button('Button 3')]]

# Create the tab group
tab_group = sg.TabGroup([
    [sg.Tab('Tab 1', tab1_layout)],
    [sg.Tab('Tab 2', tab2_layout)],
    [sg.Tab('Tab 3', tab3_layout)],
], size=(800, 480), tab_location='bottomleft')

# Create the window layout
tab_layout = [
    [tab_group],
]

# Create the main window using sg.Window
window = sg.Window('Window Title', layout=tab_layout, size=(800,480))

# Loop to process events and draw the window
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    elif event == '__TIMEOUT__':
        now = datetime.datetime.now()
        window['-CLOCK-'].update(now.strftime('%H:%M:%S'))

window.close()
