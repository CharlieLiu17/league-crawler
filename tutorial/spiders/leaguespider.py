import scrapy
from bs4 import BeautifulSoup
import re
import string
from nltk.stem.wordnet import WordNetLemmatizer
import inflect
import json
from collections import deque


class LeagueSpider(scrapy.Spider):
    name = "league"
    

    def start_requests(self):
        self.crawled_urls = set()
        # print("INDEX " + self.index)

        urls = [
            'https://www.leagueoflegends.com/en-us/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.crawled_urls.add(response)
        s = set(["the", "your", "for", "all", "you", "this", "thi", "with", "and"])
        link_set = set(["leagueoflegends.com/en", "riotgames.com"])
        soup = BeautifulSoup(response.text, features="lxml")
        text = soup.get_text().strip().translate(str.maketrans('', '', string.punctuation))
        phrases = re.findall('[A-Z][^A-Z]*', text)
        words = []
        for phrase in phrases:
            if len(phrase) <= 2:
                continue
            new_words = phrase.split()
            for word in new_words:
                if len(word) > 2:
                    words.append(word)
        p = inflect.engine()
        for idx, word in enumerate(words):
            # Cleaning verbs and nouns
            words[idx] = self.get_singular(WordNetLemmatizer().lemmatize(word,'v').lower(), p)
        words = filter(lambda w: w not in s, words)
            
        word_map = {}
        for word in words:
            if word in word_map:
                word_map[word] = word_map[word] + 1
            else:
                word_map[word] = 1
        #listified dictionary, composed of tuples, tuple legend: 0 = word string, 1 = count in page
        word_list = word_map.items()
        word_list = sorted(word_list, key = lambda x: x[1],reverse=True)
        word_list = word_list[0:50] 
        
                    

        print("WORDS " + str(words))
        print("WORD LIST " + str(word_list))
        
        web_links = soup.select('a')
        

        yield {response.url: word_list}


        next_pages = [web_link['href'] for web_link in web_links] 
        print("LINKS " + str(next_pages))
        for next_page in next_pages:
            if (next_page is not None):
                next_page = response.urljoin(next_page)
                if next_page not in self.crawled_urls and (self.contains_any(next_page, link_set)):
                    yield scrapy.Request(next_page, callback=self.parse)
    
    def get_singular(self, plural_noun, p):
        plural = p.singular_noun(plural_noun)
        if (plural):
            return plural
        else:
            return plural_noun

    def contains_any(self, str, set):
        return 1 in [c in str for c in set]