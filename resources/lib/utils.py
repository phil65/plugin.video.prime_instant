import re
import urllib2
from HTMLParser import HTMLParser
import json
import xbmc
import xbmcaddon
import cookielib

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
cj = cookielib.MozillaCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', userAgent)]


def cleanInput(text):
    if type(text) is not unicode:
        text = unicode(text, "iso-8859-15")
        xmlc = re.compile('&#(.+?);', re.DOTALL).findall(text)
        for c in xmlc:
            text = text.replace("&#" + c + ";", unichr(int(c)))

    p = HTMLParser()
    return p.unescape(text)


def cleanTitle(title):
    title = title.rsplit('[HD]', 1)[0]
    return cleanInput(title)


def cleanSeasonTitle(title):
    blacklist = [": The Complete", ": Season", "Season", "Staffel", "Volume", "Series"]
    for item in blacklist:
        if item in title:
            title = title[:title.rfind(item)]
    return title.strip(" -,")


def cleanTitleTMDB(title):
    title = title.rsplit('[', 1)[0]
    title = title.rsplit(' OmU', 1)[0]
    return title


def log(msg, level=xbmc.LOGNOTICE):
    # xbmc.log('%s: %s' % (addonID, msg), level)
    log_message = u'{0}: {1}'.format(addonID, msg)
    xbmc.log(log_message.encode("utf-8"), level)
    """
    xbmc.LOGDEBUG = 0
    xbmc.LOGERROR = 4
    xbmc.LOGFATAL = 6
    xbmc.LOGINFO = 1
    xbmc.LOGNONE = 7
    xbmc.LOGNOTICE = 2
    xbmc.LOGSEVERE = 5
    xbmc.LOGWARNING = 3
    """


def prettyprint(string):
    log(json.dumps(string,
                   sort_keys=True,
                   indent=4,
                   separators=(',', ': ')))


def getUnicodePage(url):
    print url
    req = opener.open(url)
    if "content-type" in req.headers and "charset=" in req.headers['content-type']:
        encoding = req.headers['content-type'].split('charset=')[-1]
        return unicode(req.read(), encoding)
    else:
        return unicode(req.read(), "utf-8")


def translation(string_id):
    return addon.getLocalizedString(string_id)  # .encode('utf-8')
