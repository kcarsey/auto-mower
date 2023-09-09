import sys
import tkinter
import tkinter.messagebox
from tkinter import font as tkfont
from tkintermapview import TkinterMapView
import tkintermapview 


class SampleApp(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("1024x600")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, MapView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        label = tkinter.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tkinter.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tkinter.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tkinter.Button(self, text="Go to Map",
                            command=lambda: controller.show_frame("MapView"))
        button1.pack()
        button2.pack()
        button3.pack()


class PageOne(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        label = tkinter.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tkinter.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tkinter.Frame):
 
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        label = tkinter.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tkinter.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

class MapView(tkinter.Frame):
 
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        self.controller = controller
        
        button = tkinter.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        map_widget = tkintermapview.TkinterMapView(self)
        map_widget.pack(fill="both", expand=True)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

        # set current position and zoom
        # map_widget.set_position(52.516268, 13.377695, marker=False)  # Berlin, Germany
        # map_widget.set_zoom(17)

        # set current position with address
        # map_widget.set_address("Berlin Germany", marker=False)

        def marker_click(marker):
            print(f"marker clicked - text: {marker.text}  position: {marker.position}")

        # set a position marker (also with a custom color and command on click)
        marker_2 = map_widget.set_marker(52.516268, 13.377695, text="Brandenburger Tor", command=marker_click)
        marker_3 = map_widget.set_marker(52.55, 13.4, text="52.55, 13.4")
        # marker_3.set_position(...)
        # marker_3.set_text(...)
        # marker_3.delete()

        # set a path
        path_1 = map_widget.set_path([marker_2.position, marker_3.position, (52.568, 13.4), (52.569, 13.35)])
        # path_1.add_position(...)
        # path_1.remove_position(...)
        # path_1.delete()






       

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()