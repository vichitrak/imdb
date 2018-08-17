#-------------------------------------------------------------------------------
# Name:        imdb-lookup-folder
# Purpose:
#
# Author:      vichitrak
#
# Created:
# Copyright:   (c) www.manojmj.com
# Licence:
#-------------------------------------------------------------------------------
import json
import webbrowser
import os
import collections
import sys
PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    import urllib as ur
if PY_VERSION == 3:
    import urllib.request as ur

replace = ["E SuB xRG",".avi","1.4","5.1","-","DVDRip","BRRip","XviD","1CDRip","aXXo","[","]","(",")","{","}","{{","}}",
        "x264","720p","DvDScr","MP3","HDRip","WebRip","ETRG","YIFY","StyLishSaLH","StyLish Release","TrippleAudio",
        "EngHindiIndonesian","385MB","CooL GuY","a2zRG","x264","Hindi","AAC","AC3","MP3"," R6","HDRip","H264","ESub","AQOS",
        "ALLiANCE","UNRATED","ExtraTorrentRG","BrRip","mkv","mpg","DiAMOND","UsaBitcom","AMIABLE","BRRIP","XVID","AbSurdiTy","DvD","mp3","MPEG4","CRYS",
        "DVDRiP","TASTE","BluRay","HR","COCAIN","_",".","BestDivX","MAXSPEED","mediafiremoviez","Eng","500MB","FXG","Ac3","Feel","Subs","S4A","BDRip",
		"FTW","Xvid","Noir","1337x","ReVoTT",
        "GlowGaze","mp4","Unrated","hdrip","ARCHiViST","TheWretched","www","torrentfive","1080p","201 080p","1080","WEB DL","JYK","SecretMyth","Kingdom",
		"Release","RISES","DvDrip","eXceSs","ViP3R","RISES","BiDA","READNFO","lish","NimitMak","SilverRG","sujaidr",
        "HELLRAZ0R","tots","BeStDivX","UsaBit","FASM","NeroZ","576p","LiMiTED","Series","ExtraTorrent","DVDRIP","~",
        "BRRiP","699MB","700MB","greenbud","B89","480p","AMX","007","DVDrip","h264","phrax","ENG","TODE","LiNE",
        "XVid","sC0rp","PTpower","OSCARS","DXVA","MXMG","3LT0N","TiTAN","4PlayHD","HQ","HDRiP","MoH","MP4","BadMeetsEvil",
        "XViD","3Li","PTpOWeR","3D","HSBS","CC","RiPS","WEBRip","R5","PSiG","'GokU61","GB","GokU61","NL","EE","NL",
        "PSEUDO","DVD","Rip","NeRoZ","EXTENDED","DVDScr","DVDSCR","xvid","WarrLord","SCREAM","MERRY","XMAS","iMB","7o9",
        "Exclusive","171","DiDee","v2","Scr","SaM","MOV","BRrip","CharmeLeon","Silver RG","1xCD","DDR","1CD","X264","ExtraTorrenRG",
		"Srkfan","UNiQUE","Dvd","Dual Audio","crazy torrent","Blackjesus","RIP","NEO","Mr  KickASS","Mr KickASS","MicroStar RG","Spidy","PRiSTiNE","HD",
		"Ganool","TS","BiTo","ARiGOLD","rip","Rets","teh","ChivveZ","song4",
		"playXD","LIMITED","600MB","700MB","900MB","350MB","375MB","380MB","395MB","2015","2014","Manudil","P2PDL","juggs","RLSM","WiLDFYRE","prisak",
		"HKRG","FANTASTiC","MZON3","BlackStaticRG","Subtitles","+","PDvD","MyDownloadCity","GooN","Ali Baloch","dvd","- ","DUB","BED","BDRIP","6CH","KIKS","HC",
		"EVO","Maxillion","BHATTI87","2 0","lish","Lokioddin","PimpRG","AG","BUZZccd","WBRG","GECKOS","H 264","TheFalcon","PLAYNOW",
		"OCW","mSD","AliBaloch","Mediafiremoviez","BlueRay","EVO","IceBane","RyD3R","Zwartboek","CODY","MiCRO","Dual","R@J@T","cam","Demonuk", "NIKONRG",
		"AbhinavRocks","HKRG","FLAWL3SS","Jalucian","DTS","DVDRip","XviD","MAXSPEED","www.torentz.3xforum.ro","iTALiAN","MD","Dual","TrTd",
		"TeaM","KiNGDOM","KumaR","UNCUT","BHATTI87","P2PDL","Antitrust","26K","Dias","Rus  Junoon","RARBG","PA","GreatMagician","4 G","ChattChitto","RG",
		"BD  D","6ch","Tornster","Atlas47","480P","DUAL","HINDI","AUDIO","PRINCEOFDHEMP","DD","EN","SCR","IMAX EDITION","COD","cam","1080P","AraGon","BD",
		"6Chn Cody's","YTS.AG","KickASS","DUBBED","Mediafiremoviez.com","mediafiremoviez.com"
        ]

movieList = list()
imdbRatingsList = list()
skippedMovieList = list()
filePath = os.getcwd()
#filePath = "D:\PP\ML Git\imdb"

def getMovieFromDir():
    movieList = os.listdir(filePath)
    movieList.remove("imdb-rating-folder.cmd")
    #movieList.remove("imdb-rating-folder.py")
    return  movieList

def cleanMovieNames():
    cleanMovieList = list()
    OriginalMovieList = getMovieFromDir()
    for movieName in OriginalMovieList:
        for y in range(1900, 2014):
            if str(y) in movieName:
                movieName = movieName.replace(str(y), " ")
                year = y
                break
        for value in replace:
            movieName = movieName.replace(value, " ")
            movieName = movieName.strip()
        cleanMovieList.append(movieName)
    return cleanMovieList

def fetchRatingsFromAPI():
    j=0
    print("Fetching ratings..")
    cleanedMovieList = cleanMovieNames()
    for movieName in cleanedMovieList:
        j += 1
        if " " in movieName:
            movieName = movieName.replace(" ", "%20")
        if "'" in movieName:
            movieName = movieName.replace("'", "%27")
        url = "http://www.omdbapi.com/?t=" + movieName + "&apikey=9b925aaa"
        response = ur.urlopen(url).read()
        jsonvalues = json.loads(response)
        try:
            imdbRate = jsonvalues['imdbRating']
        except Exception as e:
            error = jsonvalues['Error']
            if(error == "Movie not found!"):
                imdbRate = " - Skipped"
                movieName = movieName.replace("%27", "'")
                movieName = movieName.replace("%20", " ")
                skippedMovieList.append(movieName)
            else:
                imdbRate = " "
                movieName = movieName.replace("%27", "'")
                movieName = movieName.replace("%20", " ")
                skippedMovieList.append(movieName)
        print(j),
        imdbRatingsList.append(imdbRate)
    return imdbRatingsList

#print(fetchRatingsFromAPI())

skippedMovieList = list(set(skippedMovieList))
def printSkippedList():
    print("Skipped Movie List:")
    for skippedMovie in skippedMovieList:
        print(skippedMovie)

def renameFilesOnDisk():

    i = -1
    originalMovieList = getMovieFromDir()
    cleanedMovieNameList = cleanMovieNames()
    print(originalMovieList)
    print(cleanedMovieNameList)
    imdbRatings = fetchRatingsFromAPI()
    for loop in range(0,len(originalMovieList)):
        src = str(filePath) + "\\" + str(originalMovieList[i])
        dst = str(filePath) + "\\" + str(cleanedMovieNameList[i]) + " - IMDB " + str(imdbRatings[i])
        os.rename(src, dst)
        i = i + 1
    print(" "+"Done!!\n")
    printSkippedList()
    print ("\nIf any of your movie folder name is appended with '- IMDB - Skipped'..\n"+\
            "It means, script couldn't handle the ripper names in the folder name\n"+\
            "Please report the movie name so we can improve the user experience""")
    input(" "+"\nPress any key to continue...")
renameFilesOnDisk()

