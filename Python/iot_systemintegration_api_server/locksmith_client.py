from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
import requests
import json

BASE_API = "http://host.docker.internal:9080"


class LocksmithClient:
    """GUI class for Locksmith Client. """
    def __init__(self, root):
        # currently selected door to open.
        self.current_door = 0
        # Login info
        self.username = ""
        self.password = ""

        # Colors
        bg = "#656565"
        fg = "#ffffff"
        # fonts
        ft_open = tkFont.Font(family='Times', size=16)
        # setting title
        root.title("Insane High-Tech Master Key")
        # setting window size
        width = 700
        height = 400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)

        # Frames
        main_frame = tk.Frame(root, bg=bg)

        # Define Grid
        main_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        main_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')

        # Widgets
        self.label_username = tk.Label(main_frame,
                                       bg=bg,
                                       text='Username',
                                       justify='left'
                                       )
        self.txt_username = tk.Text(main_frame,
                                    bg='#ffffff',
                                    fg='#000000')
        self.label_password = tk.Label(main_frame,
                                       bg=bg,
                                       text='Password',
                                       justify='left'
                                       )
        self.txt_password = tk.Text(main_frame,
                                    bg='#ffffff',
                                    fg='#000000')
        self.listbox_doors = tk.Listbox(main_frame,
                                        width=15,
                                        borderwidth="0px",
                                        bg=bg,
                                        fg=fg,
                                        justify="left"
                                        )

        self.btn_get_doors = tk.Button(main_frame,
                                       text="Hämta dörrar!",
                                       command=self.get_doors,
                                       bg=bg,
                                       border=0,
                                       compound=tk.TOP
                                       )

        self.listbox_loggs = tk.Listbox(main_frame,
                                        width=15,
                                        borderwidth="0px",
                                        bg=bg,
                                        fg=fg,
                                        justify="left"
                                        )

        self.btn_open_door = tk.Button(main_frame,
                                       text="Öppna Dörren!",
                                       command=self.open_door,
                                       bg=bg,
                                       border=0,
                                       compound=tk.TOP
                                       )

        # Layout
        main_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.label_username.grid(row=0,
                                 rowspan=1,
                                 column=0,
                                 columnspan=1,
                                 sticky='sw'
                                 )
        self.txt_username.grid(row=1,
                               rowspan=1,
                               column=0,
                               columnspan=1,
                               sticky='new')
        self.label_password.grid(row=2,
                                 rowspan=1,
                                 column=0,
                                 columnspan=1,
                                 sticky='sw'
                                 )
        self.txt_password.grid(row=3,
                               rowspan=1,
                               column=0,
                               columnspan=1,
                               sticky='new')

        self.btn_get_doors.grid(row=4,
                                rowspan=1,
                                column=0,
                                columnspan=1,
                                sticky='e')

        self.listbox_doors.grid(row=5,
                                rowspan=3,
                                column=0,
                                columnspan=1,
                                sticky='nsew')

        self.listbox_loggs.grid(row=0,
                                rowspan=8,
                                column=1,
                                columnspan=2,
                                sticky='nsew')

        self.btn_open_door.grid(row=1,
                                rowspan=4,
                                column=3,
                                columnspan=1,
                                sticky='nsew'
                                )

        # Widget Events
        self.listbox_doors.bind("<<ListboxSelect>>", self.show_loggs)

    def open_door(self):
        """
        Sends request to API-Gateway to open a door.

        :return: No returning argument.
        """
        username = self.username
        password = self.password
        door_id = self.current_door
        if self.current_door:
            requests.post(url=f"{BASE_API}/locksmith/doors/{door_id}",
                          auth=(username, password),
                          json={'header': {'door_id': door_id, 'username': username, 'type': 'client_open'},
                                'body': {'text': f'open_{door_id}'}})

    def get_doors(self):
        """
        Sends request to API-gateway to get all doors available for user.

        :return: No returning arguments.
        """
        self.listbox_doors.delete(0, END)
        self.current_door = 0

        self.username = self.txt_username.get("1.0", "end-1c").strip(" \n\t")
        self.password = self.txt_password.get("1.0", "end-1c").strip(" \n\t")

        if len(self.username) > 0 and len(self.password) > 0:
            url = f"{BASE_API}/locksmith/doors"
            response = requests.get(url=url,
                                    auth=(self.username, self.password),
                                    json={'header': {'username': self.username, 'type': 'get_user_doors'}})

            for door in json.loads(response.text)['doors']:
                self.listbox_doors.insert(self.listbox_doors.size(), str(door))

    def show_loggs(self, event):
        """
        Handles cursor select event for door listbox.\n
        Requests all logs for the selected door and shows them in another listbox.

        :param event: Cursor Selection event.
        :return: No returning arguments.
        """
        selection = event.widget.curselection()
        if selection:
            self.listbox_loggs.delete(0, END)
            door_id = self.listbox_doors.get(selection[0])
            self.current_door = door_id

            url = f"{BASE_API}/locksmith/doors/{door_id}/loggs"
            print(url)
            response = requests.get(url=url,
                                    auth=(self.username, self.password),
                                    json={'header': {'type': 'get_door_loggs'}})
            print(response.text)
            for logg in json.loads(response.text)['loggs']:
                # Builds a log string to show
                logg_txt = f"- {logg['username']} at {logg['entry_time']}: {logg['event']} "
                if logg['access']:
                    logg_txt += 'Succeeded'
                else:
                    logg_txt += 'Failed'

                self.listbox_loggs.insert(self.listbox_loggs.size(), logg_txt)


    @staticmethod
    def run():
        root = tk.Tk()
        app = LocksmithClient(root)
        root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = LocksmithClient(root)
    root.mainloop()



