###############################################################################
# Name: namesilo.py
# Author: fullmetalcache
# Date: 2018-02-28
# Overview: This module is a front-end for the NameSilo api
################################################################################

import urllib2

class NameSilo( object ):
    def __init__(self, apiKey, paymentId):
        self.apiKey = apiKey
        self.paymentId = paymentId
        self.baseUrl = "https://www.namesilo.com/apibatch";
        self.hdr = hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive' }

        #Registers a domain, deletes the default DNS records
        #and then creates/sets an A record to point to
        #the given IP address
    def RegisterAndSetARecord( self, domain, ipAddress ):
        self.registerDomain( domain )

        #Remove default DNS records
        dnsRecords = self.getDnsRecordIds( domain )
        for record in dnsRecords:
            self.deleteDnsRecord( domain, record )

        rrhost = domain.split(".")[0]

        self.addDnsRecord( domain, "A", rrhost, ipAddress )

    #Adds a new DNS record given the following:
    #   domain - target domain
    #   rrtype - record type (A, AAAA, CNAME, MX, TXT)
    #   rrhost - host value for the record (without .domain on the end)
    #   rrvalue -
    #               A -     IPv4 Address
    #               AAAA -  IPv6 Address
    #               CNAME - Target hostname
    #               MX -    Target HostName
    #               TXT -   The Text
    def addDnsRecord( self, domain, rrtype, rrhost, rrvalue, rrttl = 3600):
        addDnsRecordUrl = "{0}/dnsAddRecord?version=1&type=xml&key={1}&domain={2}&rrtype={3}&rrhost={4}&rrvalue={5}&rrttl={6}"

        req = urllib2.Request(  addDnsRecordUrl.format( self.baseUrl, self.apiKey, domain, rrtype, rrhost, rrvalue, rrttl ),
                                headers = self.hdr )

        resp = ""

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
            return

        content = resp.read()

        return content


    #Deletes a DNS record given a domain name and rrid. The rrid's can be obtained via the
    #getDnsRecordIds method in this class
    def deleteDnsRecord( self, domain, rrid ):
        deleteDnsRecordUrl = "{0}/dnsDeleteRecord?version=1&type=xml&key={1}&domain={2}&rrid={3}"

        req = urllib2.Request(  deleteDnsRecordUrl.format( self.baseUrl, self.apiKey, domain, rrid ),
                                headers = self.hdr )

        resp = ""

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
            return

        content = resp.read()

        return content

    #Gets the dns records for a given domain and returns the record_id field
    #The record_id can be used to delete or update DNS records
    def getDnsRecordIds( self, domain ):
        getDnsRecordsUrl = "{0}/dnsListRecords?version=1&type=xml&key={1}&domain={2}"

        req = urllib2.Request(  getDnsRecordsUrl.format( self.baseUrl, self.apiKey, domain ),
                                headers = self.hdr )

        resp = ""

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
            return

        content = resp.read()
        records = content.split("<record_id>")
        results = []
        for rec in records[1:]:
            rec = rec.split("</record_id>", 1)[0]
            results.append( rec )

        return results

    #Checks if one or more domains are available.
    #A single domain can be passed in as a string
    #Multiple domains should be passed in as a list
    #Returns Null if no domains were available
    def registerAvailability(self, domains):
        domainsString = ""
        checkRegAvailabilityUrl ="{0}/checkRegisterAvailability?version=1&type=xml&key={1}&domains={2}"
        if not isinstance( domains, str):
            for dom in domains:

                domainsString += dom + ","

            domainsString = domainsString[:-1]

        else:
            domainsString = domains

        req = urllib2.Request(  checkRegAvailabilityUrl.format( self.baseUrl, self.apiKey, domainsString ),
                                headers = self.hdr )

        resp = ""

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
            return

        content = resp.read()
        try:
            content = content.split("<available>", 1)[1]
            content = content.split("</available>",1)[0]
        except:
            return

        results = []
        for dom in content.split("<domain>"):
            results.append( dom.split("</domain>", 1)[0] )

        return results[1:]

    #Registers a domain using the API Key and PaymentId that are given
    #The PaymentId is obtained by adding a verified payment method
    #via the NameSilo website. For instance, inputting Credit Card Info
    #and then uploading a redacted picture of the card to the site.
    def registerDomain( self, domain ):
        regDomainUrl ="{0}/registerDomain?version=1&type=xml&key={1}&domain={2}&payment_id={3}&years=1&auto_renew=0&private=1"

        req = urllib2.Request(  regDomainUrl.format( self.baseUrl, self.apiKey, domain, self.paymentId ),
                                headers = self.hdr )

        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.fp.read()
            return

        return True
