import PySimpleGUI as sg
import time

# Define the layout for each tab
tab1_layout = [
    [sg.Text('This is tab 1')],
    [sg.Button('OK')]
]

# Create the layout for the clock tab
tab2_layout = [
    # Add a Text element to display the clock
    [sg.Text('Time: ', key='clock', size=(10, 1))]
]

tab3_layout = [
    [sg.Text('This is tab 3')],
    [sg.Button('OK')]
]

# Create the tab group
tab_group = sg.TabGroup([
    [sg.Tab('Tab 1', tab1_layout)],
    [sg.Tab('Tab 2', tab2_layout)],
    [sg.Tab('Tab 3', tab3_layout)],
], size=(800, 480), tab_location='bottomleft')

# Create the window layout
layout = [
    [tab_group],
]

# Create the window
window = sg.Window('Window Title', layout, no_titlebar=True, location=(0,0), size=(1024, 600), finalize=True)
window.maximize()

# Set the update interval for the clock (in seconds)
update_interval = 1

# Run the event loop to process events
while True:
    # Update the clock every update_interval seconds
    if (time.time() % update_interval) == 0:
        # Get the current time
        current_time = time.strftime('%H:%M:%S')

        # Update the clock Text element
        window['clock'].update(current_time)

    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()


