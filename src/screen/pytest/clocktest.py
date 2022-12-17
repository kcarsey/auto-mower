import PySimpleGUI as sg
import datetime

# create the layout for the first tab
tab1_layout = [[sg.Text('Hello World!')],
               [sg.Text('Current time:')],
               [sg.Text(size=(12,1), key='-CLOCK-')]]

# create the layout for the second tab
tab2_layout = [[sg.Text('This is tab 2')]]

# create the layout for the third tab
tab3_layout = [[sg.Text('This is tab 3')]]

# create the layout for the window
layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout), sg.Tab('Tab 3', tab3_layout)]])],
           [sg.Button('Close')]]

# create the window and show it
window = sg.Window('Window with tabs', layout)

# update the clock every second
while True:
    event, values = window.read(timeout=1000)
    if event == sg.WIN_CLOSED:
        break
    # update the clock
    window['-CLOCK-'].update(datetime.datetime.now().strftime('%H:%M:%S'))

window.close()
