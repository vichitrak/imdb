#-------------------------------------------------------------------------------
# Name:        imdb-lookup-folder
# Purpose:
#
# Author:      manoj mj
#
# Created:
# Copyright:   (c) www.manojmj.com
# Licence:
#-------------------------------------------------------------------------------
#importing libraries
import json
import webbrowser
import os
import collections
import sys
#Check Python Version on the system, as per version import the urllib libray
PY_VERSION = sys.version_info[0]
if PY_VERSION == 2:
    import urllib as ur
if PY_VERSION == 3:
    import urllib.request as ur

#define an empty data dictionary
data_dictionary = {}
#List of words(Ripper Names) to remove from movie names, which are usually found in the ripped movie names.
replace = ["E SuB xRG",".avi","1.4","5.1","-","DVDRip","BRRip","XviD","1CDRip","aXXo","[","]","(",")","{","}","{{","}}",
        "x264","720p","DvDScr","MP3","HDRip","WebRip","ETRG","YIFY","StyLishSaLH","StyLish Release","TrippleAudio",
        "EngHindiIndonesian","385MB","CooL GuY","a2zRG","x264","Hindi","AAC","AC3","MP3"," R6","HDRip","H264","ESub","AQOS",
        "ALLiANCE","UNRATED","ExtraTorrentRG","BrRip","mkv","mpg","DiAMOND","UsaBitcom","AMIABLE","BRRIP","XVID","AbSurdiTy","DvD","mp3","MPEG4","CRYS",
        "DVDRiP","TASTE","BluRay","HR","COCAIN","_",".","BestDivX","MAXSPEED","mediafiremoviez","Eng","500MB","FXG","Ac3","Feel","Subs","S4A","BDRip","FTW","Xvid","Noir","1337x","ReVoTT",
        "GlowGaze","mp4","Unrated","hdrip","ARCHiViST","TheWretched","www","torrentfive","1080p","201 080p","1080","WEB DL","JYK","SecretMyth","Kingdom","Release","RISES","DvDrip","eXceSs","ViP3R","RISES","BiDA","READNFO","lish","NimitMak","SilverRG","sujaidr",
        "HELLRAZ0R","tots","BeStDivX","UsaBit","FASM","NeroZ","576p","LiMiTED","Series","ExtraTorrent","DVDRIP","~",
        "BRRiP","699MB","700MB","greenbud","B89","480p","AMX","007","DVDrip","h264","phrax","ENG","TODE","LiNE",
        "XVid","sC0rp","PTpower","OSCARS","DXVA","MXMG","3LT0N","TiTAN","4PlayHD","HQ","HDRiP","MoH","MP4","BadMeetsEvil",
        "XViD","3Li","PTpOWeR","3D","HSBS","CC","RiPS","WEBRip","R5","PSiG","'GokU61","GB","GokU61","NL","EE","NL",
        "PSEUDO","DVD","Rip","NeRoZ","EXTENDED","DVDScr","DVDSCR","xvid","WarrLord","SCREAM","MERRY","XMAS","iMB","7o9",
        "Exclusive","171","DiDee","v2","Scr","SaM","MOV","BRrip","CharmeLeon","Silver RG","1xCD","DDR","1CD","X264","ExtraTorrenRG",
		"Srkfan","UNiQUE","Dvd","Dual Audio","crazy torrent","Blackjesus","RIP","NEO","Mr  KickASS","Mr KickASS","MicroStar RG","Spidy","PRiSTiNE","HD","Ganool","TS","BiTo","ARiGOLD","rip","Rets","teh","ChivveZ","song4",
        "playXD","LIMITED","600MB","700MB","900MB","350MB","375MB","380MB","395MB","2015","2014","Manudil","P2PDL","juggs","RLSM","WiLDFYRE","prisak",
        "HKRG","FANTASTiC","MZON3","BlackStaticRG","Subtitles","+","PDvD","MyDownloadCity","GooN","Ali Baloch","dvd","- ","DUB","BDRIP","6CH","KIKS","HC",
        "EVO","Maxillion","BHATTI87","2 0","lish","Lokioddin","PimpRG","AG","BUZZccd","WBRG","GECKOS","H 264","TheFalcon","PLAYNOW","DUBBED",
        "OCW","mSD","AliBaloch","Mediafiremoviez","BlueRay","EVO","IceBane","RyD3R","Zwartboek","CODY","MiCRO","Dual","R@J@T","cam","Demonuk", "NIKONRG","AbhinavRocks","HKRG","FLAWL3SS","Jalucian","DTS","DVDRip","XviD","MAXSPEED","www.torentz.3xforum.ro","iTALiAN","MD","Dual","TrTd",
        "TeaM","KiNGDOM","KumaR","UNCUT","BHATTI87","P2PDL","Antitrust","26K","Dias","Rus  Junoon","RARBG","PA","GreatMagician","4 G","ChattChitto","RG",
        "BD  D","6ch","Tornster","Atlas47","480P","DUAL AUDIO","HINDI","PRINCEOFDHEMP","DD","EN","SCR","IMAX EDITION","COD","cam","1080P","AraGon","BD",
        "6Chn Cody's","YTS.AG","KickASS","DUBBED","Mediafiremoviez.com","mediafiremoviez.com"
        ]

#Take all the directories from the directory
def createDictionaryFromData(subdir):
    print("Fetching all the movies...\n"),
    all_subdirs = [d for d in os.listdir(subdir)]
    if 'moviefile.xls' in all_subdirs:  #remove 'moviefile.xls' if file is already there
        all_subdirs.remove("moviefile.xls")
    print(all_subdirs)
    for name in all_subdirs:
        year=0
        for y in range(1900,2014):
            if str(y) in name:
                name = name.replace(str(y)," ")
                year = y
                break
        for value in replace:
            name = name.replace(value," ")
        name=name.lstrip()
        name=name.rstrip()
        datalist = []
        urlName = name
        if " " in name:
            urlName = name.replace(" ", "%20")
        if "'" in urlName:
            urlName = name.replace("'", "%27")
        if year!=0:
            url = "http://www.omdbapi.com/?t=" + urlName + "&y=" + str(year) + "&apikey=9b925aaa"
        else:
            url = "http://www.omdbapi.com/?t=" + urlName + "&apikey=9b925aaa"
        response = ur.urlopen(url).read()
        jsonvalues = json.loads(response)
        #print(jsonvalues)
        if jsonvalues["Response"]=="True":
            imdbrating = jsonvalues['imdbRating']
            imdburl = "http://www.imdb.com/title/"+jsonvalues['imdbID']
            imdbgenre = jsonvalues['Genre']
            imdbyear = jsonvalues['Year']
            imdbruntime = jsonvalues['Runtime']
            imdbactors = jsonvalues['Actors']
            imdbplot = jsonvalues['Plot']
            imdbawards = jsonvalues['Awards']
        else:
            imdbrating = "Could not find"
            imdburl = "NA"
            imdbgenre = "NA"
            imdbyear = "NA"
            imdbruntime ="NA"
            imdbactors = "NA"
            imdbplot = "NA"
            imdbawards = "NA"

        moviename=name
        datalist.append(imdbrating.encode('utf-8'))
        datalist.append(imdbgenre.encode('utf-8'))
        datalist.append(imdburl.encode('utf-8'))
        datalist.append(imdbyear.encode('utf-8'))
        datalist.append(imdbruntime.encode('utf-8'))
        datalist.append(imdbactors.encode('utf-8'))
        datalist.append(imdbplot.encode('utf-8'))
        datalist.append(imdbawards.encode('utf-8'))
        #print(datalist)
        if moviename not in  data_dictionary:
            data_dictionary[moviename]=datalist
    return data_dictionary

def createExcelFileWithHeaders():
    filePath = folder+"\\moviefile.xls"
    print(type(filePath))
    file_exist =os.path.isfile(filePath)
    if file_exist:
        os.remove(filePath)
    with open(filePath,"w+") as data:
        data.write("Movie Name\tRating\tGenre\tUrl\tYear\tRuntime\tActors\tPlot\tAwards\n")

def insertDataFromDictToFile():
    createExcelFileWithHeaders()
    subdir = folder
    data_dictionary = createDictionaryFromData(subdir)
    for values in data_dictionary:
        sorted_dict = collections.OrderedDict(reversed(sorted(data_dictionary.items(), key=lambda t: t[1][0])))
    for movie, [rating,genre,url,year,runtime,actors,plot,awards] in sorted_dict.items():
        with open (filePath,"a") as data:
            data.write(str(movie)+"\t"+str(rating.decode('utf-8'))+"\t"+str(genre.decode('utf-8'))+"\t"+str(url.decode('utf-8'))+"\t"+str(year.decode('utf-8'))+"\t"+str(runtime.decode('utf-8'))+"\t"+str(actors.decode('utf-8'))+"\t"+str(plot.decode('utf-8'))+"\t"+str(awards.decode('utf-8'))+"\n")
    print(""+"\nfile is created..\n"+"Done!!")
    input()
folder = sys.argv[1]
filePath = folder+"\\moviefile.xls"
insertDataFromDictToFile()


