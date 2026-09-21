from argparse import ArgumentParser, RawTextHelpFormatter
from subprocess import run, PIPE
from datetime import datetime
from colorama import init, Style
from gettext import translation
from importlib.resources import files
from math import floor, pow, log
from mechanize import Browser
from pydicts import colors, casts
from re import compile
from save_url import __version__, __versiondate__
from shutil import which
from sys import exit

try:    
    t=translation('save_url', files("save_url") / 'locale')
    _=t.gettext
except:
    _=str

def search_monolith():
    """
        Returns absolute path to monolith if exists in path. if monolith is not found exit this app
    """
    r=which("monolith")
    if r is None:
        print(colors.red(_("Monolith executable wasn't found in your system path")))
        print(colors.red(_("Monolith is a CLI tool for saving complete web pages as a single HTML file that you can find in https://github.com/Y2Z/monolith")))
        exit(2) 
    return r

def humanizeFileSize(filesize):
    p = int(floor(log(filesize, 2)/10))
    return "%.2f %s" % (filesize/pow(1024,p), ['B','KB','MB','GB','TB','PB','EB','ZB','YB'][p])

def input_string(text):
    while True:
        res=input(Style.BRIGHT+text+": ")
        try:
            if res==None or res=="":
                continue
            res=str(res)
            return res
        except:
            pass

def getTitle(url, content):
    #Tries to get it using mechanize
    try:
        br = Browser()
        br.open(url)
        title=br.title()
        title=title.replace("\n","")
        title=title.replace("/","")
        title=title.strip()
        print(colors.yellow(_("Title was found with mechanize")))
    except Exception as e:
        print(colors.red(_("Error getting page title with mechanize: {0}").format(e)))
        title=None
        
    #Tries to get it using re
    if title is None:
        pattern=compile("(?<=<title>)(.*?)(?=</title>)")
        res=pattern.findall(content)
        if len(res)>0:
            title=res[0]
            print(colors.yellow(_("Title was found searching in <title> tag")))
        else:
            title=None
            print(colors.red(_("Error getting page title searching in <title> tag")))
    return title

def console_save_url():
    parser=ArgumentParser(
            prog='save_url', 
            description=_("Script to save and url in a single file with an automatic and structured name. It uses monolith as its backend."),
            epilog=_("If you like this app, please give me a star in https://github.com/turulomio/save_url.")+ "\n" + _("Developed by Mariano Muñoz 2019-{} ©").format( __versiondate__.year),
            formatter_class=RawTextHelpFormatter
            )
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('url', help=_("Url to save"))
    parser.add_argument('--notime', help=_("Removes date and time from the beginning of the file name"), action="store_true", default=False)
    args=parser.parse_args()
    save_url(args.url, args.notime)


def save_url(url, notime):
    init()
    monolith_path=search_monolith()
    
    result=run([monolith_path, url], shell=False, stdout=PIPE)
    content=result.stdout.decode("UTF-8")
    
    
    title=getTitle(url, content)
    
    if title is None:
        title=input_string(_("I couldn't extract web page title. Please write it"))
    if notime:
        filename="{}.html".format(title[:114])
    else:
        filename="{} {}.html".format(casts.dtnaive2str(datetime.now(), "%Y%m%d %H%M"), title[:100])

    with open(filename,"w") as f:
        f.write(content)

    if len(content)==0 or result.returncode!=0:
        print(colors.red(_("Something is wrong with saved file. Please Checkit")))
    else:
        print(Style.BRIGHT + _("File '{}' ({}) saved correctly.").format(colors.green(filename), colors.yellow(humanizeFileSize(len(content)))) + Style.RESET_ALL)
