import requests
import re

def get_timing(l):
    for x in l:
        if re.match('time.+', x):
            return x
    return False


issues = requests.get("https://api.github.com/repos/geneontology/go-ontology/issues?assignee=dosumis;state=open;per_page=100")
ij = issues.json()
ij.extend(requests.get(issues.links['next']['url']).json())
out = open('issue_tab.tsv', 'w+')
headers = ['title', 'user', 'creation date', 'new term request', 'curator_request', 'est_time_req', 'waiting for feedback', 'labels' 'url']
out.write("\t".join(headers)+"\n")
user = ''
for i in ij:
    labels = [l['name'] for l in i['labels']]
    if 'auto-migrated' in labels:
        m = re.search('Reported by: (.+)', i['body'])
        if m:
            user = m.group(1)
    else:
        user = i['user']['login']
    if 'curator-request' in labels:
        cr = True
    else:
        cr = False

    if 'waiting for feedback' in labels:
        wff = True
    else:
        wff = False
    if 'New term request' in labels:
        ntr = True
    else:
        ntr = False
    timing = get_timing(labels)
    row = [i['title'], user, i['created_at'], str(ntr), str(cr), str(timing), str(wff), str(labels), i['html_url']]
    out.write("\t".join(row)+"\n")
out.close()


