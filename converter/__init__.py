import json
import copy
from pprint import pprint

with open('converter/base.json') as base_file:
    article_base = json.load(base_file)

def convert(json_string):
    data = json.load(json_string)
    article = copy.deepcopy(article_base)
    article['identifier'] = data['id']
    article['title'] = data['display_headline']
    article['subtitle'] = data['deck']
    article['components'] = createComponents(data)
    return json.dumps(article);

def createComponents(data):
    cs = [];
    cs.append(titleComponent(data));
    cs.append(introComponent(data));

    header = headerComponent(data);
    if header:
        cs.append(header)

    cs.append(bodyComponent(data));
    cs.append(authorComponent(data));

    return cs 

# COMPONENTS

def titleComponent(data):
    return {
      'role': 'title',
      'layout': 'titleLayout',
      'text': data['id'],
      'textStyle': 'titleStyle',
    }

def introComponent(data):
    return {
      'role': 'intro',
      'layout': 'introLayout',
      'text': data['deck'], 
      'textStyle': 'introStyle'
    }

def headerComponent(data):
    if 'image' in data:
        return {
            'role': 'header',
            'layout': 'headerImageLayout',
            'style': {
                'fill': {
                    'type': 'image',
                    'URL': data['image']['article_superhero_large'],
                    'fillMode': 'cover',
                    'verticalAlignment': 'center',
                }
            }
        }

def bodyComponent(data):
    content = ''.join([i for i in data['body'] if type(i) == str])
    return {
        'role': 'body',
        'text': content,
        'format': 'html',
        'layout': 'bodyLayout',
        'textStyle': 'bodyStyle',
    }

def authorComponent(data):
    author = data['authors'][0];
    return {
        'role': 'author',
        'layout': 'authorLayout',
        'text': '{}, {} | {}'.format(author['name'], author['role'], data['hero']['pubdate']),
        'textStyle': 'authorStyle'
    }