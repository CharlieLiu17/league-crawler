import json
from collections import deque

class Indexer:
    def __init__(self):
        filename = "crawled_data.jsonl"
        # self.crawled_urls = set()
        # with open(filename, 'r') as j:
        #     content = j.read()
        #     if (len(content) == 0):
        #         self.index = {}
        #     else:
        #         self.index = json.loads(content)
        # print("INDEX " + str(self.index))

        with open(filename, 'r') as json_file:
            self.json_list = list(json_file)

        # for json_str in json_list:
        #     result = json.loads(json_str)
        #     print(f"result: {result}")
        #     print(isinstance(result, dict))
    
    def create_index(self):
        self.index = {}
        for json_str in self.json_list:
            result = json.loads(json_str)
            response_url = list(result.keys())[0]
            # print(response_url)
            word_list = result[response_url]
            for pair in word_list:
                word = pair[0]
                count = pair[1]
                pair_to_insert = (response_url, count)
                if word in self.index:
                    for idx, page in enumerate(self.index[word]):
                        curr_count = page[1]
                        if count > curr_count:
                            self.index[word].insert(idx, pair_to_insert)
                            break
                else:
                    self.index[word] = deque([pair_to_insert])
        for word in self.index:
            self.index[word] = list(self.index[word])

        with open('index.json', 'w') as outfile:
            json.dump(self.index, outfile, indent=4)

indexer = Indexer()
indexer.create_index()