import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
from collections import OrderedDict, Counter
from konlpy.tag import Twitter

class make_book_info:
    def __init__(self, keyword):
        self.__keyword = keyword
    
    def _make_url(self, pg):
        url_keyword = urllib.parse.quote(self.__keyword)
        netloc = 'https://book.naver.com/search/search_in.nhn'
        query = '?query={}&&pattern=0&orderType=rel.desc&viewType=list&searchType=bookSearch&serviceSm=service.basic&title=&author=&publisher=&isbn=&toc=&subject=&publishStartDay=&publishEndDay=&categoryId=&qdt=1&filterType=0&filterValue=&serviceIc=service.author&buyAllow=0&ebook=0'.format(url_keyword)
        page = '&page={}'.format(pg)
        return netloc + query + page
    
    def response_parser(self, parser= 'bs', pg= 1):
        
        response = urllib.request.urlopen(self._make_url(pg))
        
        if parser == 'bs':
            bs_soup = bs(response.read(),'lxml')
            return bs_soup
        elif parser =='etree':
            tree = etree.parse(response, etree.HTMLParser(encoding='utf-8'))
            return tree            

    
    def make_book_link(self, parser, check_page):    
        #link = OrderedDict()
        
        c_parser = self.response_parser(parser , pg = 1)

        tot_page = int(re.match('\d+', c_parser.select_one('body > div.tit_area > span.num.num2 > strong').text).group())
        get_link = c_parser.select('#searchBiblioList > li > div > div > a')
                                 
        link = {get_link[i].find('img')['alt'] : get_link[i]['href'] for i in range(len(get_link))}               
        
        if isinstance(check_page, int):
            page = check_page
        elif check_page.lower() == 'full':
            page = tot_page // 10
        else:
            page = int((tot_page // 10) // 2)
        
        
        for i in range(2, page):
            c_parser = self.response_parser(parser, i)        
            get_link = c_parser.select('#searchBiblioList > li > div > div > a')
                                      
            for j in range(len(get_link)):
                
                try:
                    get_link[j].find('img')['alt']
                except:
                    print('alt not in site')
                    link[get_link[j].text] = get_link[j]['href']
                
                link[get_link[j].find('img')['alt']] = get_link[j]['href']#\
            
           # link[']
        return link

    def cleantext(self, text):           #필요한 문자만 추출하는 함수.
    	#ctext = text
    #	cText = str(text)[:str(text).find('<a href')]
        cText = re.sub(r'\r.*?\s','',text)
        cText = re.sub('(부록\s[a-zA-Z] | CHAPTER\s[0-9])/g','',cText)    				
        cText = re.sub('<.*?>','',cText)
        cText = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\\n\\t\\r\-_+<>@\#$%&\\\=\(\'\"\u3000\u8000\xa0■《》●『』▣▶★]','', cText)
        cText = re.sub('flash.*?back','',cText)
        return(cText)

    def make_sentence(self, url):
        intro_req = requests.get(url)
        intro_soup = bs(intro_req.text.encode(), 'lxml')
        
        try:
            intro_soup.select_one('#bookIntroContent > p').text
        except AttributeError:
            return ''                          
        
        intro_text = intro_soup.select_one('#bookIntroContent > p').text
                                           
        try:
            gg = intro_soup.select_one('#tableOfContentsContent').text
        except:
            gg = ''                          
        intro_text = intro_text + gg#intro_soup.select_one('#tableOfContentsContent').text                                    
        return intro_text

    def tokenizer_morhs(self, cnText, wCn = 2, cCn = 5):
    
        tw = Twitter()                                  
        nouns = tw.nouns(cnText)	                   
        count = Counter(nouns)                                  
    
        if wCn or cCn !=1:
            count = Counter({w:c for w,c in count.items() if len(w) >= wCn and c >= cCn})
        
        return list(count.keys())








