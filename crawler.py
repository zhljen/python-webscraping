import re
import urlparse
import urllib2


class Crawler(object):
    def download(self, url, num_retries=2):
        html = None
        for i in xrange(num_retries):
            print 'Downloading:', url
            try:
                html = urllib2.urlopen(url).read()
            except urllib2.URLError as e:
                print 'Download error:', e.reason
                if hasattr(e, 'code') and e.code < 500:
                    break
        return html

    def link_crawler(self, seed_url, link_regex):
        crawl_queue = [seed_url]
        seen = set(crawl_queue)
        while crawl_queue:
            for link in self.get_links(self.download(crawl_queue.pop())):
                if (re.match(link_regex, link)):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)

    def crawl_sitemap(self,url):
        for link in re.findall('<loc>(.*?)</loc>', self.download(url)):
            html = self.download(link)
            #print html

    def get_links(self,html):
        return re.compile('<a[^>>+href=["\'](.*?)["\']', re.IGNORECASE).findall(html)

# Crawler().link_crawler('http://example.webscraping.com', 'example.webscraping.com/(index|view)/')
# Crawler().crawl_sitemap('http://example.webscraping.com/sitemap.xml')
