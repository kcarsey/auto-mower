import PySimpleGUI as sg

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [[sg.Text('This is layout 1 - It is all Checkboxes')],
           *[[sg.CB(f'Checkbox {i}')] for i in range(5)]]

layout2 = [[sg.Text('This is layout 2')],
           [sg.Input(key='-IN-')],
           [sg.Input(key='-IN2-')]]

layout3 = [[sg.Text('This is layout 3 - It is all Radio Buttons')],
           *[[sg.R(f'Radio {i}', 1)] for i in range(8)]]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [[sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
          [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Button('Exit')]]

window = sg.Window('Swapping the contents of a window', layout, no_titlebar=True, location=(0,0), size=(1024,600), finalize=True) #keep_on_top=True to keep on top
window.maximize()


layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Cycle Layout':
        window[f'-COL{layout}-'].update(visible=False)
        layout = layout + 1 if layout < 3 else 1
        window[f'-COL{layout}-'].update(visible=True)
    elif event in '123':
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(event)
        window[f'-COL{layout}-'].update(visible=True)
window.close()
