from asyncio.windows_events import NULL
from logging import error
import sys
import random
from PyQt5 import uic, QtCore
import gd
import time
from urllib.request import urlopen
import json
from gd.utils.decorators import source
from PyQt5.QtWidgets import QMainWindow, QApplication
from PySide2.QtWidgets import QApplication
from gd.typing import Song
from pypresence import Presence
import webbrowser

class MainCode():
    try:
        def GDIn():
            class Interfaz(QMainWindow):
                def __init__(self):
                    super().__init__()
                    self.AbrirUI()
                    self.Debug.setText("Starting...")
                    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                    self.setGeometry(0, 0, 495, 140)
                    self.setWindowFlags(
                        QtCore.Qt.WindowStaysOnTopHint |
                        QtCore.Qt.FramelessWindowHint |
                        QtCore.Qt.X11BypassWindowManagerHint
                    )
                    #Inicio y Variables
                    self.StatusService()
                    global SongUrl
                    SongUrl = "https://www.newgrounds.com/"
                    self.Playing.setChecked(True)
                    self.Editor.setChecked(True)
                    self.OffsetTimer()
                    try:
                        self.IniciarRich()
                    except:
                        self.error()
                    self.TimerC()
                    #Objetos Clickeados
                    self.Offset.valueChanged.connect(self.OffsetTimer)
                    self.More.clicked.connect(self.MoreInfo)
                    self.MainW.stateChanged.connect(self.Window)
                    self.Expand.clicked.connect(self.ExpandWindow)
                    self.MiniW.clicked.connect(self.MinimizedWindow)
                    self.CheckServers.clicked.connect(self.OpenLinkServers)
                    self.ReinicieStatus.clicked.connect(self.StatusService)

                def OpenLinkServers(self):
                    webbrowser.open_new_tab("https://matos7u7.zyrosite.com/status")

                def MoreInfo(self):
                    if self.More.isChecked()==True:
                        self.More.setText(f"▲")
                        self.setGeometry(0, 0, 500, 300)
                    else:
                        self.More.setText(f"▼")
                        self.setGeometry(0, 0, 500, 140)
                
                def Window(self):
                    if self.MainW.isChecked()==False:
                        self.Expand.setGeometry(0, 0, 45, 20)
                        self.iconrich.setGeometry(0, 320, 35, 30)
                        self.setGeometry(0, 0, 45, 40)
                        self.More.setChecked(False)
                        self.More.setText(f"▼")
                    else:
                        self.Expand.setGeometry(0, 320, 45, 20)
                        self.iconrich.setGeometry(5, 5, 35, 30)
                        self.MoreInfo()
                
                def ExpandWindow(self):
                    self.Expand.setGeometry(0, 320, 45, 20)
                    self.iconrich.setGeometry(5, 5, 35, 30)
                    self.MainW.setChecked(True)
                    self.MoreInfo()
                
                def MinimizedWindow(self):
                    self.MainW.setChecked(False)
                    self.iconrich.setGeometry(0, 320, 30, 30)
                    self.Window()

                def StatusService(self):
                    global StatusServer
                    print("Getting server status, please wait a moment ...")
                    try:
                        url = f"https://gdbrowser.com/api/profile/Robtop"
                        datos = urlopen(url)
                        sourcePID = json.loads(datos.read())
                        try:
                            if "username" in sourcePID:
                                print("Status Server ON")
                                StatusServer = True
                            else:
                                print("Status Server OFF")
                                StatusServer = False
                        except:
                            print("Status Server OFF, CODE: ERROR GD SERVERS")
                            StatusServer = False
                    except:
                        print("Status Server OFF, CODE: ERROR NO SERVERS")
                        StatusServer = False


                def IniciarRich(self):
                    global rpc
                    global timeelapsed
                    rpc = Presence(856034450482528256)
                    rpc.connect()
                    timeelapsed = time.time()
                    try:
                        self.GetSong()
                        self.GetInfoPlayer()
                    except:
                        self.error()
                
                def GetNamePlayer(self):
                    global Player
                    try:
                        testgd = gd.memory.get_memory()
                        Player = testgd.get_user_name()
                    except:
                        Player = "."

                def OffsetTimer(self):
                    global TimerSet
                    TimerSet = self.Offset.value()
                    self.OffC.display(TimerSet)
                    self.TimerC()
                    print("Current update time: ",TimerSet)

                def TimerC(self):
                    self.timer = QtCore.QTimer()
                    self.timer.timeout.connect(self.Update)
                    self.timer.start(TimerSet)
                    self.Debug.setText(f"Actualizando pantalla en {TimerSet}")
                    self.repaint()

                def Update(self):
                    self.Debug.setText("Enviando peticiones")
                    self.repaint()
                    if self.Rich.isChecked()==True:
                        self.TimerC()
                        try:
                            rpc.update(state=" ... ",
                            details="AFK",
                            large_image="gd")
                        except:
                            self.error()
                    else:
                        self.Clase()
            
                def AbrirUI(self):
                    print("Running interface")
                    Dir = r'C:/ProyectosPYO/richgd' 
                    File = r'/UIGDT.ui'
                    DirFile = Dir + File
                    print("Optimizing program")
                    uic.loadUi(r'UIGDT.ui',self)

                def Clase(self):
                    self.Debug.setText("Obteniendo peticiones")
                    self.Rich.setEnabled(True)
                    try:
                        memory = gd.memory.get_memory()
                        self.GDOpen.setChecked(True)
                    except:
                        self.error()
                    #Si GD esta abierto entonces abrir (2 opciones)
                    if self.GDOpen.isChecked()==True:
                        if memory.is_in_level() and self.Playing.isChecked()==True:
                            try:
                                self.RichGame()
                            except:
                                self.DiscError()
                        else:
                            if memory.is_in_level() or memory.is_level_demon()==True:
                                self.Playing.setChecked(True)
                                if memory.is_level_demon()==True and self.Playing.isChecked()==True:
                                    try:
                                        self.RichGame()
                                    except:
                                        self.DiscError()
                            else:
                                self.MenuGD()

                def RichGame(self):
                    self.progressBar.setHidden(False)
                    self.idlevel.setHidden(False)
                    try:
                        memory = gd.memory.get_memory()
                    except:
                        self.TimerC()
                    LvlName = memory.get_level_name()
                    Att = memory.get_attempt()
                    SongID = memory.get_song_id()
                    BestNor = memory.get_normal_percent()
                    BestPra = memory.get_practice_percent()
                    Porcen = int(memory.get_percent())
                    IDL = memory.get_level_id()
                    Creator = memory.get_level_creator()
                    PracticeMode = memory.is_practice_mode()
                    Difficult = memory.get_level_difficulty()
                    TypeLevel = Difficult.name.lower()
                    Song = SongU
                    SongUrl = f"https://www.newgrounds.com/audio/listen/{SongID}"
                    if self.SoUp.isChecked()==False:
                        self.GetSong()
                        if Song == "ErrorLocal☑" or Song == "Practice: Stay Inside Me ☑":
                            Song = "[NONG]"
                            SongUrl = "https://www.newgrounds.com/audio/0"
                        else:
                            if Song == "ErrorOnline☑":
                                Song = "Not Available"
                                SongUrl = f"https://www.newgrounds.com/audio/{SongID}"
                            else:
                                if Song == "ErrorNoInfo☑" and IDL <= 25:
                                    self.SoUp.setChecked(True)
                                    Song = ".."
                                else:
                                    if Song == "ErrorNoInfo☑":
                                        self.SoUp.setChecked(False)
                                        Song = ".."
                                    else:
                                        print("Updated song name")
                    else:
                        if Song == "ErrorLocal☑" or Song == "Practice: Stay Inside Me ☑":
                            if Song == "Practice: Stay Inside Me ☑":
                                Song = "[NONG]"
                                SongUrl = "https://www.newgrounds.com/audio/0"
                                self.SoUp.setChecked(True)
                            else:
                                if Song == "ErrorLocal☑" and IDL <= 25:
                                    Song == "Official Robtop"
                                    self.SoUp.setChecked(True)
                                else:
                                    if Song == "ErrorLocal☑":
                                        Song == "..."
                                        self.SoUp.setChecked(False)
                        else:
                            if Song == "ErrorOnline☑":
                                Song = "Not Available"
                                SongUrl = f"https://www.newgrounds.com/audio/{SongID}"
                            else:
                                if Song == "ErrorNoInfo☑" and IDL <= 25:
                                    Song = "..."
                                else:
                                    if Song == "ErrorNoInfo☑":
                                        self.SoUp.setChecked(False)
                                        Song = "..."

                    if IDL >= 25 or IDL == 0:
                        if IDL == 0:
                            self.idlevel.setText("ID: Not available")
                            btns = [{ "label": f"ID Not available",
                            "url": f"https://gdbrowser.com/{IDL}"}]
                        else:
                            self.idlevel.setText(f"ID: {IDL}")
                            btns = [{ "label": f"ID: {IDL}",
                            "url": f"https://gdbrowser.com/{IDL}"},
                            { "label": f"Song: {Song}", "url": f"{SongUrl}"}]
                    else:
                        self.idlevel.setText("Official robtop level")
                        btns = [{ "label": f"Official robtop level",
                        "url": f"https://www.youtube.com/user/RobTopGames"}]
                        Creator = "Robtop"
                        TypeLevel = "oficial"
                    if PracticeMode:
                        Mode = "Practice"
                    else:
                        Mode = "Normal"

                    if memory.is_level_epic():
                        ModeRate = "-epic"
                    else:
                        ModeRate = ""
                        if memory.is_level_featured():
                            ModeRate = "-featured"
                        else:
                            ModeRate = ""

                    self.GetTimeLvl()
                    GetMode = memory.get_gamemode()
                    Gamemode = GetMode.name.lower()

                    self.levelinfo.setText(f"{LvlName}")
                    self.progressBar.setValue(int(Porcen))
                    self.textp.setText(f"{Porcen}%")
                    self.bestPinfo.setText(f"Best: {BestNor}%")
                    try:
                        rpc.update(state=f"by {Creator} | {Porcen}% | Record Normal: {BestNor} % & Record Practice: {BestPra} %",
                        details=f"Playing {LvlName} [{Mode}] <{Gamemode}> | Attempts: {Att}", 
                        buttons=btns,
                        large_image="gd",
                        large_text=f"{Player}",
                        small_image=f"{TypeLevel}{ModeRate}",
                        end=timeleft)
                    except:
                        btns = [{ "label": f"ID: {IDL}",
                        "url": f"https://gdbrowser.com/{IDL}"},
                        { "label": f"ID Song: {SongID}", "url": f"{SongUrl}"}]
                        rpc.update(state=f"by {Creator} | {Porcen}% | Record Normal: {BestNor} % & Record Practice: {BestPra} %",
                        details=f"Playing {LvlName} [{Mode}] <{Gamemode}> | Attempts: {Att}", 
                        large_image="gd",
                        buttons=btns,
                        large_text=f"{Player}",
                        small_image=f"{TypeLevel}{ModeRate}",
                        end=timeleft)
                    
                def MenuGD(self):
                    if Player == "" or Player == ".":
                        self.Playing.setChecked(True)
                        self.GetNamePlayer()
                    if self.InfoGet.isChecked()==False:
                        self.GetInfoPlayer()
                        self.MenuGD()
                    try:
                        if self.YTUp.isChecked()==False:
                            self.GetInfoPlayer()
                            self.YTUp.setChecked(True)
                        else:
                            pass
                    except:
                        pass
                    messages = [f"{Player} is exploring things", f"{Player} is waiting for the update", f"{Player} in discord",
                    f"{Player} is playing the cube that jumps xD", f"{Player} looking for a level to play",
                    f"{Player} is ¡Super Pro!", f"{Player} think he loves you, shh it's a secret...", f"{Player} is eager to complete back on track >:D"]
                    if self.Playing.isChecked()==True and self.Editor.isChecked()==False and channelyt==False:
                        self.GetInfoPlayer()
                        rpc.update(state=f"In Menu | {random.choice(messages)}", 
                        details=f"Rank: {globalrank} | Stars: {stars} | Demons: {demons}", 
                        large_image="gd",
                        start=timeelapsed)
                        self.Playing.setChecked(False)
                        self.levelinfo.setText(f"In Menu")
                        self.progressBar.setValue(0)
                        self.textp.setText(f" ")
                        self.bestPinfo.setText(f" ")
                        self.GetSong()
                        print("Sending menu information")
                    else:
                        try:
                            if self.Playing.isChecked()==True and self.Editor.isChecked()==False:
                                self.GetInfoPlayer()
                                rpc.update(state=f"In Menu | {random.choice(messages)}", 
                                details=f"Rank: {globalrank} | Stars: {stars} | Demons: {demons}", 
                                large_image="gd",
                                buttons= [{ "label": f"Visit the Youtube of {Player}","url": f"https://www.youtube.com/channel/{channelyt}"}],
                                start=timeelapsed)
                                self.Playing.setChecked(False)
                                self.levelinfo.setText(f"In Menu")
                                self.progressBar.setValue(0)
                                self.textp.setText(f" ")
                                self.bestPinfo.setText(f" ")
                                self.repaint()
                                self.GetSong()
                                print("Sending menu information")
                        except:
                            try:
                                if self.Playing.isChecked()==True and self.Editor.isChecked()==False:
                                    self.GetInfoPlayer()
                                    rpc.update(state=f"In Menu | {random.choice(messages)}",
                                    details=f"Rank: {globalrank} | Stars: {stars} | Demons: {demons}",
                                    large_image="gd",
                                    buttons= [{ "label": f"Visit my Youtube","url": f"https://www.youtube.com/channel/{channelyt}"}],
                                    start=timeelapsed)
                                    self.Playing.setChecked(False)
                                    self.levelinfo.setText(f"In Menu")
                                    self.progressBar.setValue(0)
                                    self.textp.setText(f" ")
                                    self.bestPinfo.setText(f" ")
                                    self.GetSong()
                                    self.repaint()
                                    print("Sending menu information")
                            except:
                                self.DiscError()

                    try:
                        memory = gd.memory.get_memory()
                        self.TimerC()
                        self.idlevel.setHidden(True)
                        self.progressBar.setHidden(True)
                        if memory.is_in_editor():
                            self.EditorMode()
                        else:
                            self.Editor.setChecked(False)
                    except:
                        pass
                
                def EditorMode(self):
                    self.repaint()
                    self.SoUp.setChecked(False)
                    self.Rich.setHidden(True)
                    self.Editor.setChecked(True)
                    self.Playing.setChecked(True)
                    memory = gd.memory.get_memory()
                    LvlName = memory.get_editor_level_name()
                    Objets = memory.get_object_count()
                    rpc.update(state=f"Objets: {Objets}",
                    details=f"Creating: {LvlName} | Mode Editor",
                    large_image="gd",
                    large_text=f"{Player}",
                    small_image="edit",
                    start=timeelapsed)
                    self.levelinfo.setText(f"In Editor - {LvlName}")
                    self.progressBar.setValue(0)
                    self.textp.setText(" ")
                    self.idlevel.setText(f"Objets: {Objets}")
                    self.bestPinfo.setText(f" ")
                    self.repaint()

                def GetTimeLvl(self):
                    global timeleft
                    testgd = gd.memory.get_memory()
                    Long = testgd.get_level_length()
                    Timed = (Long * 3.1)/1000
                    Porcentaje = testgd.get_percent()
                    try:
                        Pased = Timed/100
                        TimeElapsed = Pased * Porcentaje
                        Restante = Timed - TimeElapsed
                    except:
                        pass
                    gettime = time.time()
                    timeleft = gettime + Restante

                def GetInfoPlayer(self):
                    print("Trying to get player information")
                    global channelyt
                    global demons
                    global globalrank
                    global stars
                    if StatusServer == True:
                        try:
                            url = f"https://gdbrowser.com/api/profile/{Player}"
                            datos = urlopen(url)
                            sourcePID = json.loads(datos.read())
                            if "username" in sourcePID:
                                print("Obtaining information ...")
                                self.InfoGet.setChecked(True)
                                getyt = sourcePID["youtube"]
                                getrank = sourcePID["rank"]
                                getstars = sourcePID["stars"]
                                getdemons = sourcePID["demons"]
                                if getyt:
                                    channelyt = getyt
                                    print("Info *Youtube* obtained")
                                else:
                                    channelyt = False
                                    print("Error getting *Youtube*")
                                if getdemons:
                                    demons = getdemons
                                    print("Info *Demons* obtained")
                                else:
                                    demons = "0"
                                    print("Error getting *Demons*")
                                if getrank:
                                    globalrank = getrank
                                    print("Info *Global rank* obtained")
                                else:
                                    globalrank = "(Unranked)"
                                    print("Error getting *Global Rank*")
                                if getstars:
                                    stars = getstars
                                    print("Info *Stars* obtained")
                                else:
                                    stars = "0"
                                    print("Error getting *Stars*")
                        except:
                            print("Error getting information from servers")
                            channelyt = False
                            demons = "No info"
                            globalrank = "No info"
                            stars = "No info"
                            self.InfoGet.setChecked(True)
                            print(f"Player name to get: {Player}")
                            self.StatusService()
                            self.GetNamePlayer()
                    else:
                        print("Server Status OFF")
                        channelyt = False
                        demons = "No info"
                        globalrank = "No info"
                        stars = "No info"
                        self.InfoGet.setChecked(True)
                        self.GetNamePlayer()


                def GetSong(self):
                    global SongU
                    try:
                        memory = gd.memory.get_memory()
                        client = gd.Client()
                        async def getsong(Song):
                            IDsong = memory.get_song_id()
                            Song = await client.get_song(IDsong)
                            return Song
                        SongU = client.run(getsong(Song))
                    except:
                        SongU = "ErrorLocal☑"
                        try:
                            if StatusServer == True:
                                memory = gd.memory.get_memory()
                                IDLvl = memory.get_level_id()
                                url = f"https://gdbrowser.com/api/level/{IDLvl}"
                                datos = urlopen(url)
                                sourcePID = json.loads(datos.read())
                                if "officialSong" in sourcePID:
                                    if SongU == "ErrorLocal☑":
                                        id = int(sourcePID["officialSong"])
                                        SongIDOF = id - 1
                                        NameSong = gd.Song.official(SongIDOF, client=client)
                                        SongU = f"{NameSong}" + " ☑"
                                else:
                                    SongU = "ErrorOnline☑"
                            else:
                                SongU = "ErrorOnline☑"
                                print("Server Musics OFF")
                        except:
                            self.StatusService()
                    self.SoUp.setChecked(True)

                def DiscError(self):
                    print("Discord Open?")
                    self.progressBar.setHidden(True)
                    self.idlevel.setText(" ")
                    self.textp.setText(f" ")
                    self.levelinfo.setText(f"Discord is not open")
                    self.bestPinfo.setText("Closing...")
                    self.repaint()
                    time.sleep(3)
                    sys.exit()
                
                def error(self):
                    self.Rich.setEnabled(False)
                    self.Rich.setChecked(False)
                    self.progressBar.setHidden(True)
                    self.levelinfo.setText(f"Error, Open Discord")
                    self.idlevel.setText("or Geometry Dash")
                    self.textp.setText(f" ")
                    self.bestPinfo.setText(f" ")
                    self.repaint
                    if self.GDOpen.isChecked()==True:
                        rpc.close()
                        print("GD exited")
                        sys.exit()
                    else:
                        self.GetNamePlayer()
                        self.GetSong()
                        self.GetInfoPlayer()

            def main():
                app = QApplication(sys.argv)
                GUI = Interfaz()
                GUI.show()
                sys.exit(app.exec_())

            if __name__ == '__main__':
                main()
        GDIn()

    except:
        class InterfazError(QMainWindow):
            def __init__(self):
                super().__init__()
                uic.loadUi("thxu.ui", self)
                print("thx for using GDRICH!")

        if __name__ == '__main__':          
            app = QApplication.instance()
            if app == None:
                app = QApplication([])
            GUI = InterfazError()
            GUI.show()
            sys.exit(app.exec_())
