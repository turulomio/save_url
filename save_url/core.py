from argparse import ArgumentParser, RawTextHelpFormatter
from subprocess import run, PIPE
from datetime import datetime
from colorama import Fore, Style, init
from gettext import translation
from importlib.resources import files
from math import floor, pow, log
from mechanize import Browser
from save_url import __version__, __versiondate__
from shutil import which
from sys import exit

try:    
    t=translation('save_url', files("save_url") / 'locale')
    _=t.gettext
except:
    _=str
def red(s):
        return Fore.RED + Style.BRIGHT + s + Style.RESET_ALL
    

def search_monolith():
    """
        Returns absolute path to monolith if exists in path. if monolith is not found exit this app
    """
    r=which("monolith")
    if r is None:
        print(red(_("Monolith executable wasn't found in your system path")))
        print(red(_("Monolith is a CLI tool for saving complete web pages as a single HTML file that you can find in https://github.com/Y2Z/monolith")))
        exit(2) 
    print(r)
    

def dtnaive2string(dt, type=1):
    if dt==None:
        resultado="None"
    elif type==1:
            resultado="{}{}{} {}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    return resultado


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

def getTitle(url):
    try:
        br = Browser()
        br.open(url)
        title=br.title()
        title=title.replace("\n","")
        title=title.replace("/","")
        title=title.strip()
    except Exception as e:
        print(red(_("Error getting page title: {0}").format(e)))
        title=None
    return title

def console_save_url():
    parser=ArgumentParser(
            prog='save_url', 
            description="Script to save and url in a single file with an automatic and structured name. It uses monolith as its backend.",
            epilog="If you like this app, please give me a star in https://github.com/turulomio/save_url."+ "\n" + "Developed by Mariano Muñoz 2019-{} \xa9".format( __versiondate__.year),
            formatter_class=RawTextHelpFormatter
            )
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('url', help="Url to save")
    parser.add_argument('--notime', help="Removes date and time from the beginning of the file name", action="store_true", default=False)
    args=parser.parse_args()
    save_url(args.url, args.notime)


def save_url(url, notime):
    init()
    search_monolith()
    
    title=getTitle(url)
    result=run(["monolith", url], shell=False, stdout=PIPE)
    if title is None:
        title=input_string("I couldn't extract web page title. Please write it")
    content=result.stdout.decode("UTF-8")
    if notime:
        filename="{}.html".format(title[:114])
    else:
        filename="{} {}.html".format(dtnaive2string(datetime.now()), title[:100])

    with open(filename,"w") as f:
        f.write(content)

    if len(content)==0 or result.returncode!=0:
        print(red(_("Something is wrong with saved file. Please Checkit")))
    else:
        print (Style.BRIGHT + _("File '{}' ({}) saved correctly.").format(Fore.GREEN + filename + Fore.RESET, Fore.YELLOW + humanizeFileSize(len(content)) + Fore.RESET ) + Style.RESET_ALL)
