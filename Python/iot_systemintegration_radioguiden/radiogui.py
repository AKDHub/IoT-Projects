from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import webbrowser
import os

from radioapi import *
from PIL import Image, ImageTk

# Images
DEFAULT_IMG = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img/srlogo.jpg")
CHANNEL_IMG = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img/channelimg.jpg")
PROGRAM_IMG = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img/prgimg.jpg")
PLAY_LOGO_IMG = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img/playlogo.png")
CHANNELS_API_URL = "http://api.sr.se/api/v2/channels?format=json&size=49"


def load_img_from_path(img_path: str = DEFAULT_IMG, resize: tuple = False) -> ImageTk.PhotoImage:
    """
    Loads an image as ImageTk.PhotoImage object from img_path.
    Resizes the image if resize parameter is entered.
    :param img_path:
    :param resize:
    :return ImageTk.PhotoImage:
    """
    if resize:
        return ImageTk.PhotoImage(Image.open(img_path).resize(resize))
    else:
        return ImageTk.PhotoImage(Image.open(img_path))


def get_program(prg_id: int):
    """
    Returns a RadioProgram object from program id.
    :param prg_id:
    :return:
    """
    if prg_id > 0:
        return RadioProgram(prg_id)
    return None


def get_episode(episode_id: int):
    """
    Returns a ProgramEpisode object from episode id.
    :param episode_id:
    :return:
    """
    if episode_id > 0:
        return ProgramEpisode(episode_id)
    return None


class SwedishRadioApp:
    """
    Creates a GUI for a user-friendly interface with SR (Swedish Radio) API.
    """
    def __init__(self, root):
        # App attributes and variables
        self.sr_station = SwedishRadioStation(CHANNELS_API_URL)
        self.current_chan = self.sr_station.channels[0]
        # fonts
        ft_chanls = tkFont.Font(family='Times', size=16)
        ft_chanl_info = tkFont.Font(family='Times', size=14)
        ft_prg_schedule = tkFont.Font(family='Times', size=14)
        ft_prg_info = tkFont.Font(family='Times', size=16)
        ft_nowp_title = tkFont.Font(family='Times', size=16)
        # Colors
        bg = "#656565"
        fg = "#ffffff"
        # image paths
        self.default_img_path = DEFAULT_IMG
        self.chanl_img_path = CHANNEL_IMG
        self.prg_img_path = PROGRAM_IMG

        # setting title
        root.title("Radio SR-widget")
        # setting window size
        width = 1050
        height = 450
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        # Frames
        main_frame = tk.Frame(root, bg=bg)
        prg_info_frame = tk.Frame(main_frame, bg=bg)
        now_playing_frame = tk.Frame(main_frame, bg=bg)

        # Define Grid
        main_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        main_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        prg_info_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        prg_info_frame.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')

        now_playing_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        now_playing_frame.rowconfigure((0, 1, 2), weight=1, uniform='a')

        # App Widgets
        start_img = load_img_from_path(self.default_img_path, (150, 150))
        self.label_chanl_img = tk.Label(main_frame,
                                        bg=bg,
                                        image=start_img
                                        )
        self.label_chanl_img.image = start_img

        self.scrollbar_channels = Scrollbar(main_frame,
                                            bg=bg)
        self.listbox_channels = tk.Listbox(main_frame,
                                           width=15,
                                           borderwidth="0px",
                                           font=ft_chanls,
                                           bg=bg,
                                           fg=fg,
                                           justify="left",
                                           yscrollcommand=self.scrollbar_channels.set
                                           )
        self.scrollbar_channels.config(command=self.listbox_channels.yview)

        # Fill listbox with channels
        for channel in self.sr_station.channels:
            self.listbox_channels.insert(self.listbox_channels.size(), channel.name)

        self.scrollbar_schedule = Scrollbar(main_frame,
                                            bg=bg)
        self.listbox_schedule = tk.Listbox(main_frame,
                                           width=15,
                                           borderwidth="0px",
                                           font=ft_prg_schedule,
                                           bg=bg,
                                           fg=fg,
                                           justify="left",
                                           yscrollcommand=self.scrollbar_schedule.set
                                           )
        self.scrollbar_schedule.config(command=self.listbox_schedule.yview)

        self.info_str = StringVar()
        self.info_str.set("Välkommen till vår widget för att lyssna på Sveriges radio.")
        self.label_chanl_info = tk.Label(main_frame,
                                         bg=bg,
                                         fg=fg,
                                         font=ft_chanl_info,
                                         justify="left",
                                         textvariable=self.info_str,
                                         wraplength=250,
                                         )

        # Widgets Now Playing
        self.nowp_title_str = StringVar()
        self.nowp_title_str.set("Spelas nu på kanalen - ")
        self.label_now_playing_title = tk.Label(now_playing_frame,
                                                bg=bg,
                                                fg=fg,
                                                font=ft_nowp_title,
                                                justify="left",
                                                textvariable=self.nowp_title_str,
                                                wraplength=400,
                                                )

        play_logo = load_img_from_path(PLAY_LOGO_IMG, (40, 40))
        self.play_button = tk.Button(now_playing_frame,
                                     text="Spela i\nWebbläsaren",
                                     image=play_logo,
                                     command=self.play_radio_station,
                                     bg=bg,
                                     fg=fg,
                                     border=0,
                                     compound=tk.TOP
                                     )
        self.play_button.image = play_logo

        # Widgets Program info
        self.prg_info_str = StringVar()
        self.prg_info_str.set("")
        self.label_program_info = tk.Label(prg_info_frame,
                                           bg=bg,
                                           fg=fg,
                                           font=ft_prg_info,
                                           justify="left",
                                           textvariable=self.prg_info_str,
                                           wraplength=400,
                                           )
        self.label_prg_img = tk.Label(prg_info_frame,
                                      bg=bg,
                                      )

        # Layout
        main_frame.pack(side=TOP, fill=BOTH, expand=True)
        # widget placement in main_frame grid.
        self.label_chanl_img.grid(row=0,
                                  column=0,
                                  sticky='nsew')
        self.listbox_channels.grid(row=1,
                                   column=0,
                                   rowspan=2,
                                   sticky='nsew',
                                   padx=12)
        self.scrollbar_channels.grid(row=1,
                                     column=0,
                                     rowspan=2,
                                     sticky='nse')
        self.label_chanl_info.grid(row=0,
                                   column=1,
                                   columnspan=2,
                                   sticky='nsw',
                                   padx=5)
        self.listbox_schedule.grid(row=1,
                                   column=1,
                                   rowspan=2,
                                   columnspan=2,
                                   sticky='nsew',
                                   padx=12)
        self.scrollbar_schedule.grid(row=1,
                                     column=2,
                                     rowspan=2,
                                     sticky='nse')
        prg_info_frame.grid(row=1,
                            column=3,
                            rowspan=2,
                            columnspan=3,
                            sticky='nsew'
                            )
        now_playing_frame.grid(row=0,
                               column=3,
                               columnspan=3,
                               sticky='nsew')
        # Widget placement in program info frame
        self.label_program_info.grid(row=2,
                                     column=0,
                                     rowspan=3,
                                     columnspan=6,
                                     sticky='nw'
                                     )
        self.label_prg_img.grid(row=0,
                                column=0,
                                rowspan=2,
                                columnspan=2
                                )
        # Widget placement in now playing frame
        self.label_now_playing_title.grid(row=0,
                                          column=2,
                                          columnspan=4,
                                          sticky='wnse'
                                          )
        self.play_button.grid(row=0,
                              column=0,
                              rowspan=2,
                              columnspan=2,
                              sticky='w'
                              )

        # Widget Events
        self.listbox_channels.bind("<<ListboxSelect>>", self.show_channel_info)
        self.listbox_schedule.bind("<<ListboxSelect>>", self.show_program_info)

    def show_channel_info(self, event):
        """
        Event function.
        Updates channel info widgets with information about
        the currently selected channel.
        :param event:
        :return:
        """
        selection = event.widget.curselection()
        if selection:
            chanl = self.sr_station.channels[selection[0]]
            self.current_chan = chanl

            # Update channel image
            img_path = self.chanl_img_path
            img_data = chanl.get_image_data()
            if not img_data:
                img_path = self.default_img_path
            else:
                with open(img_path, 'wb') as handler:
                    handler.write(img_data)

            chanl_img = load_img_from_path(img_path, (150, 150))
            self.label_chanl_img.configure(image=chanl_img)
            self.label_chanl_img.image = chanl_img

            # Update Channel information label
            self.info_str.set(chanl.get_tagline())

            # Update Schedule Listbox for Channel
            self.listbox_schedule.delete(0, END)
            schedule_from_now = chanl.get_schedule_from_now()
            for entry in schedule_from_now:
                self.listbox_schedule.insert(self.listbox_schedule.size(),
                                             "%s - %s" % (entry.get_start_time().strftime('%H:%M'),
                                                          entry.get_title()
                                                          )
                                             )

            # Update Now Playing image and info
            if len(schedule_from_now) > 0:
                self.nowp_title_str.set(f"Spelas nu på kanalen - {schedule_from_now[0].get_title()}")
            else:
                self.nowp_title_str.set("Spelas nu på kanalen -")

    def show_program_info(self, event):
        """
        Event function.
        Updates program info widgets with information about
        the currently selected program.
        :param event:
        :return:
        """
        selection = event.widget.curselection()
        if selection:
            select_index = selection[0]
            schedule_entry = self.current_chan.get_schedule_from_now()[select_index]

            prg = get_program(schedule_entry.get_prg_id())
            episode = get_episode(schedule_entry.get_episode_id())

            # Update Program information label
            self.prg_info_str.set(schedule_entry.get_description())

            # Update program image
            img_path = self.prg_img_path
            # Search for program image
            img_data = schedule_entry.get_image_data()
            if not img_data and (prg is not None):
                img_data = get_img_data_from_url(prg.get_img_url())
            if not img_data and (episode is not None):
                img_data = get_img_data_from_url(episode.get_img_url())
            if not img_data:
                img_path = self.default_img_path
            else:
                # save image
                with open(img_path, 'wb') as handler:
                    handler.write(img_data)

            prg_img = load_img_from_path(img_path, resize=(120, 120))
            # Avoid Image being garbage collected.
            self.label_prg_img.configure(image=prg_img)
            self.label_prg_img.image = prg_img

    def play_radio_station(self):
        """
        Action function.
        Opens browser with current channel liveaudio file.
        :return:
        """
        webbrowser.open_new_tab(self.current_chan.get_liveaudio_url())


if __name__ == "__main__":
    root = tk.Tk()
    app = SwedishRadioApp(root)
    root.mainloop()
