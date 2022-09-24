import json


def getTitles(qnt):
    f = open('jabref/issues.json')
    data = json.load(f)

    titles = []

    i=0
    for issue in data['issues']:
        titles.append(issue['issue_data']['title'])
        if i == qnt:
            break
        i = i+1
    
    return titles 
