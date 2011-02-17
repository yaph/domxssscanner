from lib.BeautifulSoup import BeautifulSoup, SoupStrainer
import urlparse
import re

class DOMXSS():
    re_test = re.compile('<a href="([^"]+)"', re.S)
    # regular expressions from https://code.google.com/p/domxsswiki/wiki/FindingDOMXSS
    re_domxss_sources = re.compile('(location\s*[\[.])|([.\[]\s*["\']?\s*(arguments|dialogArguments|innerHTML|write(ln)?|open(Dialog)?|showModalDialog|cookie|URL|documentURI|baseURI|referrer|name|opener|parent|top|content|self|frames)\W)|(localStorage|sessionStorage|Database)')
    re_domxss_sinks = re.compile('((src|href|data|location|code|value|action)\s*["\'\]]*\s*\+?\s*=)|((replace|assign|navigate|getResponseHeader|open(Dialog)?|showModalDialog|eval|evaluate|execCommand|execScript|setTimeout|setInterval)\s*["\'\]]*\s*\()')

    def get_script_urls(self, url, html):
        script_urls = []
        scripts = BeautifulSoup(html, parseOnlyThese=SoupStrainer('script'))
        for tag in scripts:
            if tag.has_key('src'):
                script_urls.append(self.get_absolute_url(url, tag['src']))
        return script_urls

    def get_absolute_url(self, base, url):
        parsed = urlparse.urlparse(url)
        if '' == parsed.scheme == parsed.netloc:
            url = urlparse.urljoin(base, url)
        return url

    def domxss_scan(self, text):
        sources = self.get_domxss_sources(text)
        self.set_template_value('sources', sources)
        sinks = self.get_domxss_sinks(text)
        self.set_template_value('sinks', sinks)

    def get_domxss_list(self, text, regex):
        return [{'pos_start':m.start(),'pos_end':m.end(), 'match':m.group(0)}
            for m in regex.finditer(text)]

    def get_domxss_sources(self, text):
        return self.get_domxss_list(text, self.re_domxss_sources)

    def get_domxss_sinks(self, text):
        return self.get_domxss_list(text, self.re_domxss_sinks)