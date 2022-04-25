from hentai import Hentai, Utils, Sort
def getHentaiById(id):
    if Hentai.exists(id):
        return Hentai(id)
    return False
        

# This function returns a list of hentai objects
def getPopularHentaisByTag(tag):
    result = Utils.search_by_query('tag:'.format(tag), sort = Sort.PopularWeek)
    return result

def getRandomHentai():
    return Utils.get_random_hentai()

