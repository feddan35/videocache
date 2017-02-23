def parse(filename):
  with open(filename, 'r') as f:
    content = f.readlines()
    fline = content[0].split()
    nrvideos = int(fline[0])
    endpoints = int(fline[1])
    nrofrequests = int(fline[2])
    nrcache = int(fline[3])
    cachesize = int(fline[4])
    i=1
    ep=0
    eplatency = []
    videosizes = list(content[i].rstrip('\n'))
    epcachelatency = [[] for j in range(0,endpoints)]
    while(ep<endpoints):
        i += 1
        fline = content[i].split()
        eplatency.append(int(fline[0]))
        epnrcache = int(fline[1])
        for k in range(0,epnrcache):
            i += 1
            epcachelatency[ep].append([list(content[i].rstrip('\n'))])
        ep += 1
    requests = []
    for l in range(0,nrofrequests):
        fline = content[i].split()
        requests.append(fline)
        i += 1
                #test commit
    
    return [nrvideos,endpoints,nrofrequests,nrcache,cachesize,eplatency,videosizes,epcachelatency,requests]
