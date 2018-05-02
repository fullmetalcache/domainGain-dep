###############################################################################
# Name: expireddomains.py
# Author: fullmetalcache
# Date: 2018-02-28
# Overview: Queries expireddomains.net for recently expired domains.
#
#           Requires a username and password that can be obtained by visiting
#           expiresdomains.net and signing up for a free account
###############################################################################
from fmcprint import *
import cookielib, urllib, urllib2

class ExpiredDomains( object ):
    def __init__( self ):
        self.baseUrl = "https://member.expireddomains.net/"
        self.loginUrl = self.baseUrl + "login/"
        self.baseSearchUrl = self.baseUrl + "domains/expiredinfo/?r=a&flimit=100&fadult=1&fsimweb=1&fwhois=22"
        self.searchRecentUrl = self.baseSearchUrl + "&o=changes"
        self.searchSimWebUrl = self.baseSearchUrl + "&o=similarweb"
        self.unauthSearchUrl = "https://www.expireddomains.net/deleted-domains/?r=a&ftlds[]={0}&start={1}"
        self.unauthSearchSimWebUrl = "https://www.expireddomains.net/deleted-domains/?o=similarweb&r=a&ftlds[]={0}&start={1}"
        self.unauthSearchAcrUrl = "https://www.expireddomains.net/deleted-domains/?o=aentries&r=d&ftlds[]={0}&start={1}"
        self.domainTypes=[2, 3, 4, 12, 249]
        self.startNums = [0, 50, 100, 150, 200, 250, 300, 350]
        self.cookies = cookielib.CookieJar()

    #Logs into expireddomains.net with the provided username and password
    #Cookies are saved for later use
    def login( self, uname, passw):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor( self.cookies ))
        values = {  'login' : uname,
                    'password' : passw,
                    'redirect_2_url': '%2F' }

        data = urllib.urlencode( values )
        resp = opener.open( self.loginUrl, data )
        content = resp.read()

        return content

    #Pulls the most recently-expired .info domains from expireddomains.net
    def searchRecent( self ):
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookies ) )
        resp = opener.open( self.searchRecentUrl )
        content = resp.read()
        results = self.parseResp( content )

        return results

    #Pulls expired domains with the best SimilarWeb rating from expireddomains.net
    def searchSimWeb( self ):
        opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookies ) )
        resp = opener.open( self.searchSimWebUrl )
        content = resp.read()
        results = self.parseResp( content )

        return results

    #Parses response from expireddomain.net to pull out the domain names returned
    def parseResp( self, resp ):
        resp = resp.split("data-clipboard-text=\"", 1)[1]
        resp = resp.split("\">", 1) [0]
        results = resp.split('\n')
        results = results[:-1]

        return results

    def parseUnauthResp( self, resp ):
        results = []
        doms = resp.split("field_domain\">")

        for dom in doms:
            try:
                dom = dom.split("title=\"", 1)[1]
                dom = dom.split("\"", 1)[0]
                results.append( dom )
            except:
                pass

        return results[1:]

    #Performs an unauthenticated search on expired domains for .info domains
    def unauthSearch( self, url):
        results = []
        for domType in self.domainTypes:
            for num in self.startNums:
                opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( self.cookies ) )
                resp = opener.open( url.format( domType, num ) )
                content = resp.read()
                results += self.parseUnauthResp( content )

        return results
