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
    videosizes = content[i].rstrip('\n').split(" ")
    epcachelatency = [[] for j in range(0,endpoints)]
    while(ep<endpoints):
        i += 1
        fline = content[i].split()
        eplatency.append(int(fline[0]))
        epnrcache = int(fline[1])
        for k in range(0,epnrcache):
            i += 1
            epcachelatency[ep].append([list(content[i].rstrip('\n').split(" "))])
        ep += 1
    requests = [[] for j in range(0,endpoints)]
    i +=1
    for l in range(0,nrofrequests):
        fline = content[i].split()
        requests[int(fline[1])].append([int(fline[0]),int(fline[2])])
        i += 1
                #test commit
    
    return [nrvideos,endpoints,nrofrequests,nrcache,cachesize,eplatency,videosizes,epcachelatency,requests]
