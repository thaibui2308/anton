import json
import os
import xmltodict
import requests
import urllib.parse

QUERY_URL = "http://api.wolframalpha.com/v2/query?appid={}".format(os.environ['APPID'])

# Free form questions
def free_form_question(question):
    response = requests.get(QUERY_URL+"&input={}&includepodid=Result".format(question))
    answer = xmltodict.parse(response.content)
    
    # The return object is a OrderedDict, this method changes an OrderedDict to a normal dict
    answer = json.loads(json.dumps(answer))
    
    if answer['queryresult']['@success'] == 'false':
        return False
    
    else:
        return answer['queryresult']['pod']['subpod']['plaintext']


def urlEncoder(URL):
    encoded_URL = urllib.parse.quote(URL)
    return encoded_URL

# Questions concerning solving a mathematical problem
def scientific_question(question):
    # TODO: encode the query parameter because when the equation has a '+' sign the script broke
    response = requests.get(QUERY_URL+'&input={}&podstate=Result__Step-by-step+solution&format=plaintext'.format(urlEncoder(question)))
    answer = xmltodict.parse(response.content)
    
    answer = json.loads(json.dumps(answer))
    
    if answer['queryresult']['@success'] == 'false':
        return False
    else: 
        pods = answer['queryresult']['pod']
        for pod in pods:
            if pod['@id'] == 'Result':
                if type(pod['subpod']) == dict:
                    return pod['subpod']['plaintext']
                return pod['subpod'][-1]['plaintext']
        
        

print(scientific_question("Solve x'+x=0"))


