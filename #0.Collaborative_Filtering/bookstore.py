import requests
import urllib.parse
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
from collections import OrderedDict, Counter
from konlpy.tag import Twitter

class MakeBookInfo:
    
    def __init__(self, keyword):
        self.__keyword = keyword
        self.__dic = None
        
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

    def json_style(self, style = '2'):
        j_link = {}
        if style != '2':
            j_link['data'] = {self.__keyword : []}
        else:         
            j_link['data'] = {self.__keyword : {'title' : [0],
                                                'link' : [0],
                                                'star' : [0],
                                                'review' : [0],
                                                'price' : [0]
                                                }}
        return j_link
    
    def except_title(self, f):
        flag = True
        try:
            f.find('img')['alt']
        except:
            flag = False
        return flag
    
    def set_dict(self, get_link, detail_li):
        
        self.__dic['data'][self.__keyword]['title'].extend([i.find('img')['alt']  if self.except_title(i) else i.text for i in get_link])
        self.__dic['data'][self.__keyword]['link'].extend([i['href'] for i in get_link])
        self.__dic['data'][self.__keyword]['star'].extend([i[0] if i else 'Null' for i in detail_li])
        self.__dic['data'][self.__keyword]['review'].extend([i[1] if i else 'Null' for i in detail_li])
        self.__dic['data'][self.__keyword]['price'].extend([i[2] if i and len(i) > 2 else 'Null' for i in detail_li])
    
    def make_book_link(self, parser, check_page):    

        c_parser = self.response_parser(parser , pg = 1)
        tot_page = int(re.match('\d+', c_parser.select_one('body > div.tit_area > span.num.num2 > strong').text).group())
        
        get_link = c_parser.select('#searchBiblioList > li > div > div > a')
        detail_info = c_parser.select('#searchBiblioList > li > dl > dd.txt_desc')                         
        detail_li = [re.findall('\d+.\d*', i.text) for i in detail_info if re.findall('\d+.\d*', i.text)]
                            
        
        self.__dic = self.json_style('2')
        self.set_dict(get_link, detail_li)
        
        if isinstance(check_page, int):
            page = check_page
            
            if tot_page < (page * len(get_link)):
                page = tot_page // len(get_link)
                
        elif check_page.lower() == 'full':
            page = tot_page // 10
        else:
            page = int((tot_page // 10) // 2)

        for i in range(2, page):
            c_parser = self.response_parser(parser, i)
            get_link = c_parser.select('#searchBiblioList > li > div > div > a')
            detail_info = c_parser.select('#searchBiblioList > li > dl > dd.txt_desc')
            detail_li = [re.findall('\d+.\d*', i.text) for i in detail_info if re.findall('\d+.\d*', i.text)]
            self.set_dict(get_link, detail_li)
        
        return self.__dic

    def make_sentence(self, url):
        intro_req = requests.get(url)
        intro_soup = bs(intro_req.text.encode(), 'lxml')
        
        try:
            intro_book = intro_soup.select_one('#bookIntroContent > p').text
            assert intro_soup.select_one('#tableOfContentsContent').text
            table_contents = intro_soup.select_one('#tableOfContentsContent').text
        except AttributeError:
            intro_book = ''                          
        except AssertionError:
            table_contents = ''
        #intro_text = intro_soup.select_one('#bookIntroContent > p').text
        intro_text = intro_book + table_contents
        return intro_text

    def cleantext(self, text):           
        cText = re.sub(r'\r.*?\s','',text)
        cText = re.sub('(부록\s[a-zA-Z] | CHAPTER\s[0-9])/g','',cText)    				
        cText = re.sub('<.*?>','',cText)
        cText = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\\n\\t\\r\-_+<>@\#$%&\\\=\(\'\"\u3000\u8000\xa0■《》●『』▣▶★]','', cText)
        cText = re.sub('flash.*?back','',cText)
        return(cText)

    def tokenizer_morhs(self, cnText, wCn = 2, cCn = 5):
    
        tw = Twitter()                                  
        nouns = tw.nouns(cnText)	                   
        count = Counter(nouns)                                  
    
        if wCn or cCn !=1:
            count = Counter({w:c for w,c in count.items() if len(w) >= wCn and c >= cCn})
        
        return list(count.keys())




if __name__ == '__main__':
    import pandas as pd

    book_link1 = MakeBookInfo(keyword='철학')
    philosophy_link1, ch = book_link1.make_book_link( parser='bs',
                                                check_page=20)

