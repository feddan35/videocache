import numpy as np

class tryhard2solve(object):

    def __init__(self):
        self.nrvideos       = 5
        self.endpoints      = 2
        self.nrofrequests   = 4
        self.nrcache        = 3
        self.achesize       = 100
        self.eplatency      = [1000, 500]
        self.videosizes     = [50, 50, 80, 30, 110]
        self.epcachelatency = [[[0, 100], [2, 200], [1, 300]]]
        self.requests       = [[[3, 1500], [1, 1000], [4, 500]], [[0, 1000]]

        self.nrofusedCS     = 3
        self.cachedvideos   = [[2], [3, 1], [0, 1]]

    def set(self, nrvideos, endpoints, nrofrequests, nrcache, cachesize, eplatency, videosizes, epcachelatency, requests):
        self.nrvideos       = nrvideos
        self.endpoints      = endpoints
        self.nrofrequests   = nrofrequests
        self.nrcache        = nrcache
        self.achesize       = cachesize
        self.eplatency      = eplatency
        self.videosizes     = videosizes
        self.epcachelatency = epcachelatency
        self.requests       = requests

    def solver(self):
        #TODO something
        file = open("result.txt","w")
        file.write(str(self.nrofusedCS) + '\n')
        for cacheid,videos in enumerate(self.cachedvideos):
            file.write(str(cacheid) + ' ')
            for video in videos:
                file.write(str(video) + ' ')
            file.write('\n')
        file.close()

sample = tryhard2solve()
sample.solver()


    #Datacentre object
#    which has a list of video objects

#list of endpoints
#    each enpoint will have a dictionary of latencies
#        key id of the cache
#        dclat latency to the dc

#list of requests