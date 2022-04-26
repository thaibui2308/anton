from hentai import Tag

class GlobalStat:
    def __init__(self,request_sent=0, hentai_list=[], error_count=0):
        self.request_sent = request_sent
        self.hentai_list = hentai_list
        self.error_count = error_count
        
    @property
    def request_sent(self):
        return self.request_sent
    
    @property
    def hentai_list(self):
        return self.hentai_list
    
    @property
    def error_count(self):
        return self.error_count
    
    def new_request(self):
        self.request += 1
        
    def new_hentai(self, new_hentai):
        for hentai in self.hentai_list:
            h_name = Tag.get(hentai.artist, 'name')
            if h_name == Tag.get(new_hentai.artist, 'name'):
                return
            
        self.hentai_list.append(new_hentai)
        
    def new_error(self):
        self.error_count += 1