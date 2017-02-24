def solve(dc,eps,cache):
    pevc = [[[eps[i].reqs[j]*(eps[i].dclat - eps[i].lats[k]) for k in cache] for j in eps[i].reqs.keys()] for i in eps]
    rvc = [[sum(pevc[i,j]) for j in cache] for i in dc.vids]
    pv = [] 
    for i in dc.vids:
        maxv = rvc[i,0]
        maxi = 0
        maxvid = i
        for j in cache:
            if(rvc[i,j]>maxv):
                maxval = rvc[i,j]
                maxi = j
                maxvid = i
        pv.append([maxval,maxvid,maxi])
    sortedpv = sorted([pv[i]/dc.vids[i].size for i in dc.vids], reverse = True)
    for i in sortedpv:
        if cache[i[2]].size > dc.vids[i[1]].size
            cache[i[2]].add_video(i[1])
    
    return cache
