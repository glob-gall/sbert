import json
import requests

def getTitles(qnt = -1):
    f = open('jabref/issues.json')
    data = json.load(f)

    titles = []

    i=0
    for issue in data:
        titles.append(issue['issue_data']['title'])
        if i == qnt:
            break
        i = i+1
    
    return titles 
# titles = getTitles(5)
# for t in titles:
#     print(t)

def getMergedTitles(qnt = -1):
    f = open('jabref/issues.json')
    data = json.load(f)

    titles = []

    i=0
    for issue in data:
        if "pull_request" in issue['issue_data']:
            if issue['issue_data']['pull_request']['merged_at'] != None:
                titles.append(issue['issue_data']['title'])
                i+=1
        if i == qnt:
            break
    return titles 
# titles = getMergedTitles(5)
# for t in titles:
#     print(t)

def getMergedIssues(qnt = -1):
    f = open('jabref/issues.json')
    data = json.load(f)

    issues = []

    i=0
    for issue in data:
        if "pull_request" in issue['issue_data']:
            if issue['issue_data']['pull_request']['merged_at'] != None:
                issues.append(issue)
                i+=1
        if i == qnt:
            break
    return issues
# issues = getMergedIssues(5)
# for issue in issues:
#     print(issue)

def getIssueById(id):
    f = open('jabref/issues.json')
    data = json.load(f)
    
    findedIssue=None
    for issue in data:
        if issue['issue_data']['id'] == int(id):
            findedIssue = issue
    
    f.close()
    if(findedIssue):
        return findedIssue
    print(f"issue com id {id} nao encontrada");
    return None
# issue1 = getIssueById(29247944)
# print(issue1)
# print("\n\n")


def getIssueByTitle(title):
    f = open('jabref/issues.json')
    data = json.load(f)
    
    findedIssue=None
    for issue in data:
        if issue['issue_data']['title'] == title:
            findedIssue = issue
    
    f.close()
    if(findedIssue):
        return findedIssue
    print(f"issue com titulo {title} nao encontrada");
    return None

def getModifiedFilesByTitle(title):
    issue = getIssueByTitle(title)
    if(issue == None):
        return
    diff_url = None

    try:
        diff_url = issue['issue_data']['pull_request']['diff_url']
    except KeyError as ke:
        print("issue sem pull request")
        return []

    response = requests.get(diff_url)

    files=[]
    lines = response.text.splitlines()
    for line in lines:
        if line.startswith('diff'):
            files.append(line)
    return files


# files = getModifiedFiles('Entry sorting for Export')
# for f in files:
#     print(f)

