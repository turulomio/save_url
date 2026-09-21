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
    t = translation('save_url', files("save_url") / 'locale')
    _ = t.gettext
except:
    _ = str

CHROMIUM_BROWSERS = [
    "chromium",
    "chromium-browser",
    "google-chrome-stable",
    "google-chrome",
    "chrome",
    "brave-browser",
    "brave",
    "microsoft-edge",
    "microsoft-edge-stable",
    "vivaldi",
]

def find_binary(names):
    """
    Searches for the first available binary name or list of names in the system PATH.
    Returns the absolute path if found, or None.
    """
    if isinstance(names, str):
        names = [names]
    for name in names:
        path = which(name)
        if path:
            return path
    return None

def normalize_url(url):
    """
    Ensures URL has a schema (defaults to https://).
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        return f"https://{url}"
    return url

def get_singlefile_cmd(bin_path, url):
    cmd = [bin_path]
    browser = find_binary(CHROMIUM_BROWSERS)
    if browser:
        cmd.append(f"--browser-executable-path={browser}")
    script_path = str(files("save_url") / "anti_cookie.js")
    css_path = str(files("save_url") / "anti_cookie.css")
    cmd.append(f"--browser-script={script_path}")
    cmd.append(f"--browser-stylesheet={css_path}")
    cmd.extend(["--dump-content", url])
    return cmd

BACKENDS = {
    "singlefile": {
        "binaries": ["single-file", "single-file-cli"],
        "cmd": get_singlefile_cmd,
        "name": "single-file-cli",
        "url": "https://github.com/gildas-lormeau/single-file-cli",
    },
    "monolith": {
        "binaries": ["monolith"],
        "cmd": lambda bin_path, url: [bin_path, url],
        "name": "monolith",
        "url": "https://github.com/Y2Z/monolith",
    },
}

def search_backend(backend_name="singlefile"):
    """
        Returns absolute path to backend executable if exists in path. If backend is not found exit this app
    """
    if backend_name not in BACKENDS:
        print(colors.red(_("Unsupported backend '{}'").format(backend_name)))
        exit(2)
        
    cfg = BACKENDS[backend_name]
    r = find_binary(cfg["binaries"])
    if r is None:
        print(colors.red(_("Executable '{}' wasn't found in your system path").format(cfg["binaries"][0])))
        print(colors.red(_("Please install {} from {}").format(cfg["name"], cfg["url"])))
        exit(2) 
    return r

def run_backend(url, backend_name="singlefile"):
    if backend_name == "singlefile" and find_binary(CHROMIUM_BROWSERS) is None:
        if find_binary("monolith"):
            print(colors.yellow(_("No Chromium-based browser found for single-file. Using 'monolith' backend instead.")))
            backend_name = "monolith"
        else:
            print(colors.red(_("No Chromium-based browser (chromium, google-chrome, brave) was found in your system path.")))
            print(colors.red(_("single-file-cli requires Chromium. Please install a Chromium browser or install monolith.")))
            exit(2)

    bin_path = search_backend(backend_name)
    cmd = BACKENDS[backend_name]["cmd"](bin_path, url)
    result = run(cmd, shell=False, stdout=PIPE)
    return result.stdout.decode("UTF-8", errors="replace"), result.returncode

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
    # Try searching in downloaded HTML content first (fast & offline)
    if content:
        pattern = compile(r"(?i)<title[^>]*>(.*?)</title>")
        res = pattern.findall(content)
        if len(res) > 0 and res[0].strip():
            title = res[0].replace("\n", "").replace("/", "").strip()
            print(colors.yellow(_("Title was found searching in <title> tag")))
            return title

    # Fallback to mechanize
    try:
        br = Browser()
        br.open(url)
        title = br.title()
        if title:
            title = title.replace("\n", "").replace("/", "").strip()
            print(colors.yellow(_("Title was found with mechanize")))
            return title
    except Exception as e:
        print(colors.red(_("Error getting page title with mechanize: {0}").format(e)))

    return None

def console_save_url():
    parser=ArgumentParser(
            prog='save_url', 
            description=_("Script to save an url in a single file with an automatic and structured name."),
            epilog=_("If you like this app, please give me a star in https://github.com/turulomio/save_url.")+ "\n" + _("Developed by Mariano Muñoz 2019-{} ©").format( __versiondate__.year),
            formatter_class=RawTextHelpFormatter
            )
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('url', help=_("Url to save"))
    parser.add_argument('-b', '--backend', choices=['singlefile', 'monolith'], default='singlefile', help=_("Backend to use: 'singlefile' (default) or 'monolith'"))
    parser.add_argument('--notime', help=_("Removes date and time from the beginning of the file name"), action="store_true", default=False)
    args=parser.parse_args()
    save_url(args.url, args.notime, args.backend)


def save_url(url, notime=False, backend="singlefile"):
    init()
    url = normalize_url(url)
    content, returncode = run_backend(url, backend)
    
    title=getTitle(url, content)
    
    if title is None:
        title=input_string(_("I couldn't extract web page title. Please write it"))
    if notime:
        filename="{}.html".format(title[:114])
    else:
        filename="{} {}.html".format(casts.dtnaive2str(datetime.now(), "%Y%m%d %H%M"), title[:100])

    with open(filename,"w") as f:
        f.write(content)

    if len(content)==0 or returncode!=0:
        print(colors.red(_("Something is wrong with saved file. Please Checkit")))
    else:
        print(Style.BRIGHT + _("File '{}' ({}) saved correctly.").format(colors.green(filename), colors.yellow(humanizeFileSize(len(content)))) + Style.RESET_ALL)
