def solve(dc,eps,caches):
    pevc = [[[eps[i].reqs[j]*(eps[i].dclat - eps[i].lats[k]) for k in cache] for j in eps[i].reqs.keys()] for i in eps]
    rvc = [[sum(pevc[i,j]) for j in cache] for i in dc.vids]
    pv = []
    [max(rvc[i]) for i in dc.vidlen]
    for i in dc.vids:
        maxv = rvc[i,0]
        maxi = 0
        for j in cache:
            if(rvc[i,j]>maxv):
                maxv = rvc[i,j]
        pv.append([maxv,maxi])
    sortedpv = sorted([pv[]/dc.vids[i].size for i in dc.vids])
    for i in sortedpv:
        #if A[i] can be cached, cache
    
    return caches
