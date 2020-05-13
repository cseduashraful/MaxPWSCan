from __future__ import print_function
import os, sys
import numpy as np
import time
from algorithms import g_span as gSpan
from algorithms import load_graphs
from algorithms import read_data
filepath = os.path.dirname(os.path.abspath(__file__))


def main(filename='data/smpl.txt', min_sup=3):
    start_time = time.time()
    filename = os.path.join(filepath, filename)
    weightfilename = os.path.join(filepath, 'data/smplw.txt')
    graphs, edgeClass, minEdge, maxEdge = load_graphs(filename, 10)
    #print(edgeClass)
    #print(minEdge)
    #print(maxEdge)
    
    n = len(graphs)
    extensions = []

    #Read weight from file
    lbl, w, h = 10, 100, 100;
    Matrix = [[[float(0.0) for x in range(lbl)] for y in range(w)] for z in range(h)]
    maxW = 0.0
    data, _ = read_data(weightfilename, has_header=False)
    for line in data:
        u = int(line[0])
        v = int(line[1])
        uvlabel = int(line[2])
        weight = float(line[4])
        Matrix[u][v][uvlabel] = weight
        Matrix[v][u][uvlabel] = weight
        #print(weight)
        if(maxW < weight):
            maxW = weight
    #print(maxW)
    #Call gSpan with empty code
    #print('Hello')
    canCount = 0
    gCount = 0
    fwsCount = 0
    fwsCount, canCount, gCount = gSpan([], graphs, min_sup=min_sup, extensions=extensions,
                                       wMatrix=Matrix, maxW=maxW, fwsCount = fwsCount, canCount = canCount, gCount = gCount,
                                       minEdge=minEdge, maxEdge = maxEdge, occList = edgeClass)
    end_time = time.time()
    for i, ext in enumerate(extensions):
        print('Pattern %d' % (i+1))
        for _c in ext:
            print(_c)
        print('')

    print("--- %s seconds ---" % (end_time - start_time))
    print(fwsCount)
    print(canCount)
    print(gCount)
    
if __name__ == '__main__':
    if ('--help' in sys.argv) or ('-h' in sys.argv):
        print("")
        print("Finds possible frequent and canonical extensions of C in D, using")
        print("min_sup as lowest allowed support value.")
        print("Usage: %s FILENAME minsup" % (sys.argv[0]))
        print("")
        print("FILENAME: Relative path of graph data file.")
        print("minsup:   Minimum support value.")
    else:
        kwargs = {}
        if len(sys.argv) > 1:
            kwargs['filename'] = sys.argv[1]
        if len(sys.argv) > 2:
            kwargs['min_sup'] = sys.argv[2]
        if len(sys.argv) > 3:
            sys.exit("Not correct arguments provided. Use %s -h for more information" % (sys.argv[0]))
        main(**kwargs)


