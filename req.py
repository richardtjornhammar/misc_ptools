import requests

def query_hmdb(metabolite):
    query_what = ["http://www.hmdb.ca/unearth/q?query=\'","\';searcher=metabolites"]
    r = requests.get( metabolite.join(query_what) )
    return([s for s in str(r.content).split('/') if 'HMDB' in s ])

if __name__ == '__main__':
    metabolite = 'Phenylalanine (13C9) [M-H]-'
    print ( query_hmdb(metabolite) )
    #
    metabolite = 'Phenylalanine (13C9) [M+H]+'
    print ( query_hmdb(metabolite) )
