import platform
from tkinter import *

import lobby_client

platform.platform()


class LobbyGUI(object):

    def __init__(self, player, width, height, fontsize, server_ip='localhost', server_port=54000,
                 broadcast=1):
        self.height = height
        self.width = width
        self.fontsize = fontsize
        self.client = lobby_client.LobbyClient(name=player.name, server_ip=server_ip,
                                               server_port=int(server_port))
        self.flag = 1
        if broadcast:
            self.flag = self.client.discover_lobby()

            # self.server_ip = ip
        if self.flag:
            self.client.hello()
        self.player = player
        self.openFrame = None

        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        self.root = Tk()
        if self.flag == 0:
            self.root.destroy()
            startGUI().run()
            return
        self.root.title("Game Lobby")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        self.root.geometry('%dx%d' % (width, height))
        welcomeText = "WELCOME, " + self.player.name + "!"
        self.frame = LabelFrame(self.root, bg="azure", padx=100, pady=100)

        welcomeLabel = Label(self.frame, text=welcomeText, width=self.width * 4,
                             height=self.height * 2, bg="RoyalBlue", fg="White",
                             font=("Times", self.fontsize * 4, "bold"))
        listGamesButton = Button(self.frame, text="List Games", command=self.listGames,
                                 width=self.width * 4, height=self.height * 2, cursor="hand1",
                                 fg="RoyalBlue", font=("courier", self.fontsize * 3))
        listMatchButton = Button(self.frame, text="List Match", command=self.listMatches,
                                 width=self.width * 4, height=self.height * 2, cursor="hand1",
                                 fg="RoyalBlue", font=("courier", self.fontsize * 3))
        # joinMatchButton = Button(self.frame, text = "Join Match",  command = self.joinMatchInput, width=80, height=4, cursor = "hand1", fg = "RoyalBlue", font=("courier", 15))
        createMatchButton = Button(self.frame, text="Create Match", command=self.createMatchInput,
                                   width=self.width * 4, height=self.height * 2, cursor="hand1",
                                   fg="RoyalBlue", font=("courier", self.fontsize * 3))
        # featuresButton = Button(self.frame, text = "Match Features",  command = self.featuresInput, width=80, height=4, cursor = "hand1", fg = "RoyalBlue", font=("courier", 15))
        statsButton = Button(self.frame, text="Show my Statistics", command=self.showStats,
                             width=self.width * 4, height=self.height * 2, cursor="hand1",
                             fg="RoyalBlue", font=("courier", self.fontsize * 3))
        exitButton = Button(self.frame, text="SCARED, POTTER!? (Quit)", command=self.exitButton,
                            width=self.width * 2, height=self.height * 2, cursor="hand1", fg="Red",
                            font=("courier", self.fontsize * 3))

        self.frame.pack(expand=1)
        welcomeLabel.grid(row=0, column=0)
        listGamesButton.grid(row=1, column=0)
        listMatchButton.grid(row=2, column=0)
        # joinMatchButton.grid(row=3, column =0)
        createMatchButton.grid(row=3, column=0)
        # featuresButton.grid(row=5, column =0)
        statsButton.grid(row=4, column=0)
        exitButton.grid(row=5, column=0)

        self.listframe = LabelFrame(self.root, padx=300, pady=100)

        self.root.mainloop()

    def listGames(self):
        self.listframe.destroy()
        glist = self.client.send_list_games()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=5, sticky=N, padx=10)
        if glist[1]:
            avGamesLabel = Label(self.listframe, text="Games:", width=self.width * 2,
                                 height=self.height * 2, bg="RoyalBlue", fg="White",
                                 font=("courier", self.fontsize * 3))
            avGamesLabel.grid(row=0, column=0)
            glist = glist[1].split(",")
            for i in range(0, len(glist)):
                listLabel = Label(self.listframe, text=glist[i], width=self.width * 2,
                                  height=self.height, font=("courier", self.fontsize * 3))
                listLabel.grid(row=i + 1, column=0)
        else:
            avGamesLabel = Label(self.listframe, text="No available Games", width=self.width,
                                 height=self.height, font=("courier", self.fontsize * 3))
            avGamesLabel.grid(row=0, column=0)

    def listMatches(self):
        m = StringVar()
        m.set("No Match selected")
        self.listframe.destroy()
        mlist = self.client.send_list_match()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=8, sticky=N, padx=10)
        if mlist[2]:
            avMatchesLabel = Label(self.listframe, text="Available Matches:", width=self.width * 2,
                                   height=self.height * 2, bg="RoyalBlue", fg="White",
                                   font=("courier", self.fontsize * 3))
            avMatchesLabel.grid(row=0, column=0, columnspan=2)
            twoPlayersLabel = Label(self.listframe, text='2 Players:', width=self.width,
                                    height=self.height, font=("courier", self.fontsize * 3),
                                    bg='azure')
            twoPlayersLabel.grid(row=1, column=0)
            twoPlayersLabel = Label(self.listframe, text='4 Players:', width=self.width,
                                    height=self.height, font=("courier", self.fontsize * 3),
                                    bg='azure')
            twoPlayersLabel.grid(row=1, column=1)
            mlist = mlist[2].split(",")
            lrow = 1
            rrow = 1
            for name in mlist:
                mode = self.client.send_match_features(name)[3]
                if '4_players_mode' in mode:
                    rrow += 1
                    listButton = Radiobutton(self.listframe,
                                             text=name.replace("?_?", " ").replace("?ae?",
                                                                                   "ä").replace(
                                                 "?ue?", "ü").replace("?oe?", "ö").replace("?Ae?",
                                                                                           "Ä").replace(
                                                 "?Ue?", "Ü").replace("?Oe?", "Ö"),
                                             width=self.width, height=self.height, variable=m,
                                             value=name,
                                             font=("courier", self.fontsize * 3, "bold"),
                                             bg="azure")
                    listButton.grid(row=rrow, column=1)
                if 'BASIC' in mode:
                    lrow += 1
                    listButton = Radiobutton(self.listframe,
                                             text=name.replace("?_?", " ").replace("?ae?",
                                                                                   "ä").replace(
                                                 "?ue?", "ü").replace("?oe?", "ö").replace("?Ae?",
                                                                                           "Ä").replace(
                                                 "?Ue?", "Ü").replace("?Oe?", "Ö"),
                                             width=self.width, height=self.height, variable=m,
                                             value=name,
                                             font=("courier", self.fontsize * 3, "bold"),
                                             bg="azure")
                    listButton.grid(row=lrow, column=0)

            self.joinButton = Button(self.listframe, width=self.width, height=self.height * 2,
                                     text="JOIN", fg="Green",
                                     command=lambda: self.noMatchSelected(m.get(), len(mlist) + 2,
                                                                          "JOIN"), cursor="hand1")
            self.joinButton.grid(row=max(lrow, rrow) + 1, column=0)
            self.featuresButton = Button(self.listframe, width=self.width, height=self.height * 2,
                                         text="Show Features",
                                         command=lambda: self.noMatchSelected(m.get(),
                                                                              len(mlist) + 2,
                                                                              "FEATURES"),
                                         cursor="hand1")
            self.featuresButton.grid(row=max(lrow, rrow) + 1, column=1)
        else:
            avMatchesLabel = Label(self.listframe, text="No available Matches", fg="Red",
                                   width=self.width * 2, height=self.height * 2,
                                   font=("courier", self.fontsize * 3))
            avMatchesLabel.grid(row=2, column=0, columnspan=2)

    def noMatchSelected(self, match_name, row, argument):
        if match_name == "No Match selected":
            noMatch = Label(self.listframe, text=match_name, fg="Red", width=self.width * 2,
                            height=self.height, font=("courier", self.fontsize * 3))
            noMatch.grid(row=row + 1, column=0, columnspan=2)
        else:
            if argument == "JOIN":
                self.joinMatchInput(match_name)
            else:
                self.showFeatures(match_name)

    def joinMatchInput(self, match_name):
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=7, sticky=N, padx=10)
        joinNameLabel = Label(self.listframe,
                              text='Join "' + match_name.replace("?_?", " ").replace("?ae?",
                                                                                     "ä").replace(
                                  "?ue?", "ü").replace("?oe?", "ö").replace("?Ae?", "Ä").replace(
                                  "?Ue?", "Ü").replace("?Oe?", "Ö") + '"', width=self.width * 2,
                              height=self.height * 2, bg="RoyalBlue", fg="White",
                              font=("courier", self.fontsize * 3))
        joinNameLabel.grid(row=0, column=0, columnspan=2)
        colourLabel = Label(self.listframe, text="Choose Colour:", width=self.width,
                            height=self.height, font=("courier", self.fontsize * 3), bg="azure")
        colourLabel.grid(row=1, column=0, columnspan=2)
        c = StringVar()
        c.set("White")
        red = Radiobutton(self.listframe, text='Red', variable=c, value='Red', fg="Red", bg="azure",
                          pady=5)
        red.grid(row=2, column=0, sticky=W)
        blue = Radiobutton(self.listframe, text='Blue', variable=c, value='Blue', fg="Blue",
                           bg="azure", pady=5)
        blue.grid(row=3, column=0, sticky=W)
        aqua = Radiobutton(self.listframe, text='Aqua', variable=c, value='Aqua', fg="cyan",
                           bg="azure", pady=5)
        aqua.grid(row=4, column=0, sticky=W)
        yellow = Radiobutton(self.listframe, text='Yellow', variable=c, value='Yellow', fg="Gold",
                             bg="azure", pady=5)
        yellow.grid(row=5, column=0, sticky=W)
        olive = Radiobutton(self.listframe, text='Olive', variable=c, value='Olive',
                            fg="dark olive green", bg="azure", pady=5)
        olive.grid(row=2, column=1, sticky=W)
        magenta = Radiobutton(self.listframe, text='Magenta', variable=c, value='Magenta',
                              fg="magenta2", bg="azure", pady=5)
        magenta.grid(row=3, column=1, sticky=W)
        lime = Radiobutton(self.listframe, text='Lime', variable=c, value='Lime', fg="lime green",
                           bg="azure", pady=5)
        lime.grid(row=4, column=1, sticky=W)
        chocolate = Radiobutton(self.listframe, text="Chocolate", variable=c, value='Chocolate',
                                fg="chocolate1", bg="azure", pady=5)
        chocolate.grid(row=5, column=1, sticky=W)
        joinNameOK = Button(self.listframe, text="PLAY", cursor="hand1", fg='Green',
                            command=lambda: self.joinMatch(match_name, c.get()),
                            width=self.width * 2, height=self.height * 2,
                            font=("courier", self.fontsize * 3))
        joinNameOK.grid(row=6, column=0, columnspan=2)

    def joinMatch(self, match_name, c):
        print(c)
        if c == "Red":
            colour = (255, 0, 0)
        elif c == "Blue":
            colour = (0, 0, 255)
        elif c == "Aqua":
            colour = (0, 128, 128)
        elif c == "Yellow":
            colour = (255, 255, 0)
        elif c == "Olive":
            colour = (128, 128, 0)
        elif c == "Magenta":
            colour = (255, 20, 147)
        elif c == "Lime":
            colour = (99, 250, 0)
        elif c == "Chocolate":
            colour = (139, 69, 19)
        else:
            colour = (255, 255, 255)

        answer = self.client.send_join_match(match_name, colour)
        if answer[0] == "ERR_FAILED_TO_JOIN":
            if answer[3] == "full":
                self.listframe.destroy()
                self.listframe = LabelFrame(self.frame, bg="azure")
                self.listframe.grid(row=1, column=1, rowspan=5, sticky=N, padx=10)
                alreadyFull = Label(self.listframe, text="Houston we have a Problem!", fg="Red",
                                    width=self.width * 2, height=self.height,
                                    font=("courier", self.fontsize * 3))
                alreadyFull.grid(row=1, column=0, columnspan=2)
                alreadyFull = Label(self.listframe, text="Room is already full", fg="Red",
                                    width=self.width * 2, height=self.height,
                                    font=("courier", self.fontsize * 3))
                alreadyFull.grid(row=2, column=0, columnspan=2)
                joinButton = Button(self.listframe, text="Join another Match", cursor="hand1",
                                    command=self.listMatches, width=self.width, height=self.height,
                                    font=("courier", self.fontsize * 3))
                joinButton.grid(row=3, column=0)
                createButton = Button(self.listframe, text="Create a new Match", cursor="hand1",
                                      command=self.createMatchInput, width=self.width,
                                      height=self.height, font=("courier", self.fontsize * 3))
                createButton.grid(row=3, column=1)

        else:
            self.root.destroy()
            try:
                self.client.wait_for_game()
            finally:
                print(self.client.result)
                if self.client.result[0] == 1:
                    e = endGameGUI(self.client.result, self.player, self.width, self.height,
                                   self.fontsize, self.server_ip, self.server_port)

    def createMatchInput(self):
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=6, sticky=N, padx=10)
        matchNameLabel = Label(self.listframe, text="Create new Match:", width=self.width * 2,
                               height=self.height * 2, bg="RoyalBlue", fg="White",
                               font=("courier", self.fontsize * 3))
        matchNameLabel.grid(row=1, column=0, columnspan=2)
        nameLabel = Label(self.listframe, text="Choose Name:", width=self.width, height=self.height,
                          font=("courier", self.fontsize * 3), bg="azure")
        nameLabel.grid(row=2, column=0)
        matchNameEntry = Entry(self.listframe, width=int(self.width / 1.2))
        matchNameEntry.grid(row=2, column=1)
        '''
        Choose Mode by DropDown Menu
        '''
        modeLabel = Label(self.listframe, text="Choose Mode:", width=self.width, height=self.height,
                          font=("courier", self.fontsize * 3), bg="azure")
        modeLabel.grid(row=3, column=0)
        modeList = ['2 Players', '4 Players']
        mode = StringVar()
        mode.set(modeList[0])
        modeDrop = OptionMenu(self.listframe, mode, *modeList)
        modeDrop.grid(row=3, column=1)

        '''
        Choose Features by Checkboxes
        '''
        featuresLabel = Label(self.listframe, text="Select Features:", width=self.width * 2,
                              height=self.height, font=("courier", self.fontsize * 3), bg="azure")
        featuresLabel.grid(row=4, column=0, columnspan=2)
        higher_ballSpeed = StringVar()
        hbS = Checkbutton(self.listframe, text='higher ball speed', variable=higher_ballSpeed,
                          onvalue='higher_ballSpeed', offvalue='', bg='azure')
        hbS.grid(row=5, column=0, sticky=W)
        invisibility = StringVar()
        inv = Checkbutton(self.listframe, text='invisibility', variable=invisibility,
                          onvalue='invisibility', offvalue='', bg='azure')
        inv.grid(row=5, column=1, sticky=W)
        half_racket = StringVar()
        hR = Checkbutton(self.listframe, text='half_racket', variable=half_racket,
                         onvalue='half_racket', offvalue='', bg='azure')
        hR.grid(row=6, column=0, sticky=W)
        gravity = StringVar()
        grav = Checkbutton(self.listframe, text='gravity', variable=gravity, onvalue='gravity',
                           offvalue='', bg='azure')
        grav.grid(row=6, column=1, sticky=W)

        matchNameOK = Button(self.listframe, text="CREATE", cursor="hand1", fg="Green",
                             command=lambda: self.createMatch(matchNameEntry.get(), mode.get(),
                                                              [higher_ballSpeed.get(),
                                                               invisibility.get(),
                                                               half_racket.get(), gravity.get()]),
                             width=self.width * 2, height=self.height * 2,
                             font=("courier", self.fontsize * 3))
        matchNameOK.grid(row=7, column=0, columnspan=2)

        # quoteLabel = Label(self.listframe, text='"PONG is like chess, but without dices"', width =40, height=2, font=("Times", 16), bg="azure")
        # quoteLabel.grid(row=8, column=0, columnspan=2)
        # quoteLabel = Label(self.listframe, text='- Lukas Podolski', width =40, height=2, font=("Times", 16), bg="azure")
        # quoteLabel.grid(row=9, column=0, columnspan=2)

    def createMatch(self, match_name, mode, liste):
        if mode == '4 Players':
            mode = '4_players_mode'
        else:
            mode = 'BASIC'
        features = mode
        for f in liste:
            if f != '':
                features += ',' + f

        match_name = match_name.replace(" ", "?_?").replace("ä", "?ae?").replace("ü",
                                                                                 "?ue?").replace(
            "ö", "?oe?").replace("Ä", "?Ae?").replace("Ü", "?Ue?").replace("Ö", "?Oe?")
        answer = self.client.send_create_match(match_name, features)
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure", padx=10)
        self.listframe.grid(row=3, column=1, rowspan=3, sticky=N, padx=10)
        if answer[0] == 'MATCH_CREATED':
            createdLabel = Label(self.listframe,
                                 text='New Match "' + match_name.replace("?_?", " ").replace("?ae?",
                                                                                             "ä").replace(
                                     "?ue?", "ü").replace("?oe?", "ö").replace("?Ae?", "Ä").replace(
                                     "?Ue?", "Ü").replace("?Oe?", "Ö") + '" created!', fg="Green",
                                 width=self.width * 2, height=self.height,
                                 font=("courier", self.fontsize * 3), bg="azure")
            createdLabel.grid(row=0, column=0)
            quoteLabel = Label(self.listframe, text='"MAY THE FORCE BE WITH YOU!"',
                               width=self.width * 2, height=self.height,
                               font=("Times", self.fontsize * 3), bg="azure")
            quoteLabel.grid(row=1, column=0)
        else:
            errorLabel = Label(self.listframe, text='Creation of match failed', fg="red",
                               width=self.width * 2, height=self.height,
                               font=("courier", self.fontsize * 3), bg="azure")
            errorLabel.grid(row=0, column=0)

    def showFeatures(self, match_name):
        self.listframe.destroy()
        features = self.client.send_match_features(match_name)
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=5, sticky=N, padx=10)
        if features[3]:
            avFeaturesLabel = Label(self.listframe,
                                    text='Match Features for "' + match_name.replace("?_?",
                                                                                     " ").replace(
                                        "?ae?", "ä").replace("?ue?", "ü").replace("?oe?",
                                                                                  "ö").replace(
                                        "?Ae?", "Ä").replace("?Ue?", "Ü").replace("?Oe?",
                                                                                  "Ö") + '":',
                                    width=self.width * 2, font=("courier", self.fontsize * 3),
                                    height=self.height * 2, bg="RoyalBlue", fg="White")
            avFeaturesLabel.grid(row=0, column=0)
            features = features[3].split(",")
            row = 1
            for f in features:
                if (f != 'BASIC') & (f != '4_players_mode'):
                    listLabel = Label(self.listframe, text=f, width=self.width * 2,
                                      height=self.height, font=("courier", self.fontsize * 3),
                                      bg="azure")
                    listLabel.grid(row=row, column=0)
                    row += 1
            if row == 1:
                noExtraLabel = Label(self.listframe, text='No extra feature', width=self.width * 2,
                                     height=self.height, font=("courier", self.fontsize * 3),
                                     bg="azure")
                noExtraLabel.grid(row=row, column=0)
            joinButton = Button(self.listframe, width=self.width * 2, height=self.height * 2,
                                text="JOIN", fg="Green",
                                command=lambda: self.joinMatchInput(match_name), cursor="hand1")
            joinButton.grid(row=row + 1, column=0)
        else:
            avMatchesLabel = Label(self.listframe, text="No Features", width=self.width * 2,
                                   height=self.height, font=("courier", self.fontsize * 3))
            avMatchesLabel.grid(row=0, column=0)

    def showStats(self):
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=7, sticky=N, padx=10)
        Button(self.listframe, text='2-Player Stats', command=self.show_2_player_Stats,
               width=self.width, height=self.height * 2, fg="RoyalBlue",
               font=("courier", self.fontsize * 3)).grid(row=0, column=0)
        Button(self.listframe, text='4-Player Stats', command=self.show_4_player_Stats,
               width=self.width, height=self.height * 2, fg="RoyalBlue",
               font=("courier", self.fontsize * 3)).grid(row=0, column=1)

    def show_2_player_Stats(self):
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=7, sticky=N, padx=10)
        nameLabel = Label(self.listframe, text="2-Player Stats for " + self.player.name + ":",
                          width=self.width * 2, height=self.height * 2, bg="RoyalBlue", fg="White",
                          font=("courier", self.fontsize * 3))
        nameLabel.grid(row=0, column=0)
        gamesLabel = Label(self.listframe, text="Matches played: " + str(self.player.games),
                           width=self.width * 2, height=self.height,
                           font=("courier", self.fontsize * 3))
        gamesLabel.grid(row=1, column=0)
        wonLabel = Label(self.listframe, text="Matches won: " + str(self.player.won),
                         width=self.width * 2, height=self.height,
                         font=("courier", self.fontsize * 3), fg="Green")
        wonLabel.grid(row=2, column=0)
        lostLabel = Label(self.listframe, text="Matches lost: " + str(self.player.lost),
                          width=self.width * 2, height=self.height,
                          font=("courier", self.fontsize * 3), fg="Red")
        lostLabel.grid(row=3, column=0)
        ratioLabel = Label(self.listframe,
                           text="Won-Matches-Ratio: " + str(round(self.player.ratio, 2)),
                           width=self.width * 2, height=self.height,
                           font=("courier", self.fontsize * 3), fg="RoyalBlue")
        ratioLabel.grid(row=4, column=0)
        if self.player.games == 0:
            sLabel = Label(self.listframe, text='"Trying is the first step towards failure"',
                           width=self.width * 2, height=self.height,
                           font=("Times", self.fontsize * 3), bg="azure")
            sLabel.grid(row=5, column=0)
            s2Label = Label(self.listframe, text=' - Homer Simpson', width=self.width * 2,
                            height=self.height, font=("Times", self.fontsize * 3), bg="azure")
            s2Label.grid(row=6, column=0)
        elif (self.player.games > 0) & (self.player.ratio <= 0.25):
            sLabel = Label(self.listframe, text='"It must be humbling to suck on so many levels"',
                           width=self.width * 2, height=self.height,
                           font=("Times", self.fontsize * 3), bg="azure")
            sLabel.grid(row=5, column=0)
            s2Label = Label(self.listframe, text=' - Sheldon Cooper', width=self.width * 2,
                            height=self.height, font=("Times", self.fontsize * 3), bg="azure")
            s2Label.grid(row=6, column=0)
        elif (self.player.games > 0) & (self.player.ratio >= 0.75):
            sLabel = Label(self.listframe, text='“With great power comes great responsibility”',
                           width=self.width * 2, height=self.height,
                           font=("Times", self.fontsize * 3), bg="azure")
            sLabel.grid(row=5, column=0)
            s2Label = Label(self.listframe, text=' - Uncle Ben', width=self.width * 2,
                            height=self.height, font=("Times", self.fontsize * 3), bg="azure")
            s2Label.grid(row=6, column=0)
        else:
            sLabel = Label(self.listframe, text='"Much to learn you still have, my old Padawan"',
                           width=self.width * 2, height=self.height,
                           font=("Times", self.fontsize * 3), bg="azure")
            sLabel.grid(row=5, column=0)
            s2Label = Label(self.listframe, text=' - Yoda', width=self.width * 2,
                            height=self.height, font=("Times", self.fontsize * 3), bg="azure")
            s2Label.grid(row=6, column=0)

    def show_4_player_Stats(self):
        self.listframe.destroy()
        self.listframe = LabelFrame(self.frame, bg="azure")
        self.listframe.grid(row=1, column=1, rowspan=7, sticky=N, padx=10)
        nameLabel = Label(self.listframe, text="4-Player Stats for " + self.player.name + ":",
                          width=self.width * 2, height=self.height * 2, bg="RoyalBlue", fg="White",
                          font=("courier", self.fontsize * 3))
        nameLabel.grid(row=0, column=0)
        gamesLabel = Label(self.listframe,
                           text="Matches played: " + str(len(self.player.four_player_results)),
                           width=self.width * 2, height=self.height,
                           font=("courier", self.fontsize * 3))
        gamesLabel.grid(row=1, column=0)
        firstLabel = Label(self.listframe,
                           text="# 1st: " + str(self.player.four_player_results_counted[0]),
                           width=self.width * 2, height=self.height,
                           font=("courier", self.fontsize * 3), fg='Green')
        firstLabel.grid(row=2, column=0)
        secondLabel = Label(self.listframe,
                            text="# 2nd: " + str(self.player.four_player_results_counted[1]),
                            width=self.width * 2, height=self.height,
                            font=("courier", self.fontsize * 3), fg="Gold")
        secondLabel.grid(row=3, column=0)
        thirdLabel = Label(self.listframe,
                           text="# 3rd: " + str(self.player.four_player_results_counted[2]),
                           width=self.width * 2, height=self.height,
                           font=("courier", self.fontsize * 3), fg="Orange")
        thirdLabel.grid(row=4, column=0)
        fourthLabel = Label(self.listframe,
                            text="# 4th: " + str(self.player.four_player_results_counted[3]),
                            width=self.width * 2, height=self.height,
                            font=("courier", self.fontsize * 3), fg="Red")
        fourthLabel.grid(row=5, column=0)
        averageLabel = Label(self.listframe,
                             text="Average Place: " + str(self.player.average_place),
                             width=self.width * 2, height=self.height,
                             font=("courier", self.fontsize * 3), fg="RoyalBlue")
        averageLabel.grid(row=6, column=0)

    def exitButton(self):
        self.root.destroy()


class startGUI(object):

    def __init__(self):
        self.server_ip = '127.0.0.1'
        self.server_port = 54000

        if platform.system() == 'Darwin':
            self.width = 20
            self.height = 2
            self.fontsize = 5
            print('Darwin')
        elif platform.system() == 'Windows':
            self.width = 15
            self.height = 1
            self.fontsize = 3
        else:
            self.width = 15
            self.height = 1
            self.fontsize = 3

    def run(self):
        self.root = Tk()
        self.root.title("Entry Lobby")
        startFrame = LabelFrame(self.root, padx=50, pady=50, bg="azure")
        startLabel = Label(startFrame, text="Type in your Player name", width=self.width * 2,
                           height=self.height * 2, bg="RoyalBlue", fg="White",
                           font=("system", self.fontsize * 4, "bold"))
        self.nameEntry = Entry(startFrame, width=self.width * 2)

        port_label = Label(startFrame, text="PORT", width=self.width // 2,
                           height=self.height, bg="RoyalBlue", fg="White",
                           font=("system", self.fontsize * 2, "bold"))
        self.port_entry = Entry(startFrame, width=self.width // 2)
        self.port_entry.insert(0, '54000')
        ip_label = Label(startFrame, text="IP", width=self.width // 2,
                         height=self.height, bg="RoyalBlue", fg="White",
                         font=("system", self.fontsize * 2, "bold"))
        self.ip_entry = Entry(startFrame, width=self.width // 2 + 5)
        self.ip_entry.insert(0, 'localhost')

        # ipLabel = Label(startFrame, text = "Server IP:", width = self.width, height = self.height, bg = 'azure')
        # ipEntry = Entry(startFrame, width = self.width)
        startButton = Button(startFrame, text="ENTRY", width=self.width * 2, height=self.height * 2,
                             fg="Green", cursor="hand1", command=self.entryButton,
                             font=("courier", self.fontsize * 3))
        quitButton = Button(startFrame, text="QUIT", width=self.width * 2, height=self.height * 2,
                            fg="Red", cursor="hand1", command=self.pressQuit,
                            font=("courier", self.fontsize * 3))
        quoteLabel = Label(startFrame,
                           text='"First rule of Pong Club: You do not talk about Pong Club"',
                           font=("Euphemia UCAS", self.fontsize * 3), width=self.width * 3,
                           height=self.height, bg="azure")
        server_button = Button(startFrame, text="SERVER", width=self.width // 2, height=self.height,
                               fg="RoyalBlue", cursor="hand1", command=self.server_button,
                               font=("courier", self.fontsize * 3))
        local_button = Button(startFrame, text="LOCAL", width=self.width // 2, height=self.height,
                              fg="RoyalBlue", cursor="hand1", command=self.local_button,
                              font=("courier", self.fontsize * 3))

        self.broadcast = StringVar(value=1)
        broadcast_checkbox = Checkbutton(startFrame, text='broadcast', variable=self.broadcast,
                                         onvalue=1, offvalue=0, bg='azure')

        self.nameEntry.bind('<Return>', self.entryButton)
        startFrame.pack()
        startLabel.grid(row=1, column=0, columnspan=2)
        self.nameEntry.grid(row=2, column=0, columnspan=2)
        # ipLabel.grid(row=3, column=0)
        # ipEntry.grid(row=3, column=1)

        startButton.grid(row=4, column=0, columnspan=2)

        quitButton.grid(row=5, column=0, columnspan=2)
        quoteLabel.grid(row=0, column=0, columnspan=2)

        broadcast_checkbox.grid(row=3, column=2, sticky=W)
        port_label.grid(row=4, column=2, columnspan=1)
        self.port_entry.grid(row=4, column=3, columnspan=1)
        ip_label.grid(row=5, column=2, columnspan=1)
        self.ip_entry.grid(row=5, column=3, columnspan=1)

        server_button.grid(row=6, column=2, columnspan=1)
        local_button.grid(row=6, column=3, columnspan=1)

        self.root.mainloop()

    def server_button(self):
        self.server_ip = '129.187.223.130'
        self.ip_entry.delete(0, END)
        self.ip_entry.insert(0, '129.187.223.130')

    def local_button(self):
        self.server_ip = '127.0.0.1'
        self.ip_entry.delete(0, END)
        self.ip_entry.insert(0, '127.0.0.1')

    def entryButton(self, event=None):
        self.server_port = self.port_entry.get()

        playername = self.nameEntry.get()
        if playername == "":
            playername = "Player1"
        connectLabel = Label(self.root, text="connect with server ...")
        connectLabel.pack()
        self.root.destroy()
        player = Player(playername)
        self.entry(player, broadcast=int(self.broadcast.get()))

    def entry(self, player, broadcast):
        lg = LobbyGUI(player, self.width, self.height, self.fontsize, self.server_ip,
                      self.server_port, broadcast=broadcast)
        lg.run()

    def pressQuit(self):
        self.root.destroy()


class endGameGUI(object):

    def __init__(self, result, player, width, height, fontsize, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.player = player
        self.width = width
        self.height = height
        self.fontsize = fontsize
        self.root = Tk()
        self.root.title("Game ended")
        self.endFrame = LabelFrame(self.root, padx=50, pady=50, bg="azure")
        self.endFrame.pack()
        if len(result) == 4:
            self.two_player(result)
        elif len(result) == 6:
            self.four_player(result)
        backLabel = Label(self.endFrame, text="Back to Lobby?", width=self.width * 2,
                          height=self.height, font=("system", self.fontsize * 4), bg="azure")
        backLabel.grid(row=4, column=0, columnspan=2)
        yesButton = Button(self.endFrame, text="YES", width=self.width, height=self.height,
                           font=("system", self.fontsize * 4), fg="Green",
                           command=lambda: self.yesButton(self.player), cursor="hand1")
        yesButton.grid(row=5, column=0)
        noButton = Button(self.endFrame, text="NO", width=self.width, height=self.height,
                          font=("system", self.fontsize * 4), fg="Red", command=self.noButton,
                          cursor="hand1")
        noButton.grid(row=5, column=1)
        self.root.mainloop()

    def two_player(self, result):

        if (result[1] > result[2]) & (result[3] == 1):
            endLabel = Label(self.endFrame,
                             text="Congratulation, " + self.player.name + "! You won the match " + str(
                                 result[1]) + "-" + str(result[2]), width=self.width * 3, height=4,
                             bg="Green", fg="White", font=("system", self.fontsize * 4, "bold"))
            endLabel.grid(row=2, column=0, columnspan=2)
            endLabel2 = Label(self.endFrame,
                              text='“One small step for %s, one giant leap for mankind."' % self.player.name,
                              width=self.width * 3, height=self.height,
                              font=("system", self.fontsize * 3), bg="azure")
            endLabel2.grid(row=0, column=0, columnspan=2)
            self.player.update(won=True)
        elif (result[2] > result[1]) & (result[3] == 2):
            endLabel = Label(self.endFrame,
                             text="Congratulation, " + self.player.name + "! You won the match " + str(
                                 result[2]) + "-" + str(result[1]), width=self.width * 3,
                             height=self.height * 2, bg="Green", fg="White",
                             font=("system", self.fontsize * 4, "bold"))
            endLabel.grid(row=2, column=0, columnspan=2)
            endLabel2 = Label(self.endFrame,
                              text='“One small step for %s, one giant leap for mankind."' % self.player.name,
                              width=self.width * 3, height=self.height,
                              font=("system", self.fontsize * 3), bg="azure")
            endLabel2.grid(row=0, column=0, columnspan=2)
            self.player.update(won=True)
        elif (result[1] < result[2]) & (result[3] == 1):
            endLabel = Label(self.endFrame,
                             text="You lost the match " + str(result[1]) + "-" + str(result[2]),
                             width=self.width * 3, height=self.height * 2, bg="Red", fg="White",
                             font=("system", self.fontsize * 4, "bold"))
            endLabel.grid(row=2, column=0, columnspan=2)
            endLabel2 = Label(self.endFrame,
                              text='“You tried your best and you failed miserably. The lesson is, never try.”',
                              width=self.width * 3, height=self.height,
                              font=("system", self.fontsize * 3), bg="azure")
            endLabel2.grid(row=0, column=0, columnspan=2)
            endLabel3 = Label(self.endFrame, text=' - Homer Simpson', width=self.width * 3,
                              height=self.height, font=("system", self.fontsize * 3), bg="azure")
            endLabel3.grid(row=1, column=0, columnspan=2)
            self.player.update(won=False)
        elif (result[2] < result[1]) & (result[3] == 2):
            endLabel = Label(self.endFrame,
                             text="You lost the match " + str(result[2]) + "-" + str(result[1]),
                             width=self.width * 3, height=self.height * 2, bg="Red", fg="White",
                             font=("system", self.fontsize * 4, "bold"))
            endLabel.grid(row=2, column=0, columnspan=2)
            endLabel2 = Label(self.endFrame,
                              text='“You tried your best and you failed miserably. The lesson is, never try.”',
                              width=self.width * 3, height=self.height,
                              font=("system", self.fontsize * 3), bg="azure")
            endLabel2.grid(row=0, column=0, columnspan=2)
            endLabel3 = Label(self.endFrame, text=' - Homer Simpson', width=self.width * 3,
                              height=self.height, font=("system", self.fontsize * 3), bg="azure")
            endLabel3.grid(row=1, column=0, columnspan=2)
            self.player.update(won=False)
        else:
            endLabel = Label(self.endFrame,
                             text="Draw: Match ended " + str(result[1]) + "-" + str(result[2]),
                             width=self.width * 3, height=self.height * 2, bg="RoyalBlue",
                             fg="White", font=("system", self.fontsize * 4, "bold"))
            endLabel.grid(row=0, column=0, columnspan=2)
            endLabel2 = Label(self.endFrame, text="Good Luck next time!", width=self.width * 2,
                              height=self.height, font=("system", self.fontsize * 4))
            endLabel2.grid(row=2, column=0, columnspan=2)

    def four_player(self, result):
        place = 0
        text = ""
        colour = 'RoyalBlue'
        myID = result[5]
        myScore = result[myID]
        del result[myID]
        opponent_scores = result[1:-1]
        if myScore >= max(opponent_scores):
            place = 1
            final_text = "Congratulations! You won the Match with %d points" % myScore
            colour = 'Green'
        else:
            opponent_scores.remove(max(opponent_scores))
            if myScore >= max(opponent_scores):
                place = 2
                final_text = "Congratulations! You scored %d points and reached the Second Place" % myScore
            else:
                opponent_scores.remove(max(opponent_scores))
                if myScore >= max(opponent_scores):
                    place = 3
                    final_text = "%d points - At least not the worst" % myScore
                else:
                    place = 4
                    final_text = "Last Place with %s points - At least it's over now" % myScore
                    colour = 'Red'

        self.player.update_four_player(place)
        endLabel = Label(self.endFrame, text=final_text, width=self.width * 3,
                         height=self.height * 2, bg=colour, fg="White",
                         font=("system", self.fontsize * 4, "bold"))
        endLabel.grid(row=2, column=0, columnspan=2)

    def yesButton(self, player):
        self.root.destroy()
        s = startGUI()
        s.server_ip = self.server_ip
        s.server_port = self.server_port
        s.entry(player, broadcast=1)

    def noButton(self):
        self.root.destroy()


class Player(object):

    def __init__(self, name, won=0, lost=0):
        self.name = name
        self.won, self.lost = won, lost
        self.games = self.lost + self.won
        if self.games > 0:
            self.ratio = self.won / self.games
        else:
            self.ratio = 0.0

        self.four_player_results = []
        self.four_player_results_counted = [0, 0, 0, 0]
        self.average_place = 0.0

    def update(self, won):
        if won == True:
            self.won += 1
        else:
            self.lost += 1
        self.games = self.won + self.lost
        self.ratio = self.won / self.games

    def update_four_player(self, place):
        self.four_player_results.append(place)
        self.four_player_results_counted[place - 1] += 1
        self.average_place = round(sum(self.four_player_results) / len(self.four_player_results), 2)


if __name__ == '__main__':
    s = startGUI()
    s.run()
