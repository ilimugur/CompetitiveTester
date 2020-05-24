from random import randint, uniform, shuffle

def dfs( u, adjList, visited ):
    hasCycle = False
    visited[u] = 1
    for v in adjList[u]:
        if visited[v] == 0:
            hasCycle = hasCycle or dfs(v)
        elif visited[v] == 1:
            hasCycle = True
    visited[u] = 2
    return hasCycle

# Returns a random integer in the inclusive range
def getRandomInteger( lowerBound, upperBound ):
    return randint(lowerBound, upperBound)

def getRandomFloat( lowerBound, upperBound ):
    return uniform(lowerBound, upperBound)

def getString( length, allowedChars ):
    s = ''
    lastIndex = length - 1
    for i in range(length):
        s.append( allowedChars[ randint( 0, lastIndex) ] )
    return s

def addEdgeToGraph(E, edgesSeen, u, v, isDirected, weight = None):
    if weight is None:
        E.append( (u, v) )
    else:
        E.append( (u, v, weight) )
    edgesSeen[u].add(v)
    if not isDirected:
        if w is None:
            E.append( (v, u) )
        else:
            E.append( (v, u, weight) )
        edgesSeen[v].add(u)

# Generates 1-indexed graph based on given parameters
def getGraph( vertexLowerBound, vertexUpperBound,
              edgesLowerBound, edgesUpperBound,
              isWeighted = False, weightsLowerBound = 0, weightsUpperBound = 0,
              isSimpleGraph = True, hasSelfLoops = False, isDirected = False,
              isConnected = False, isDAG = False ):
    n = getRandomInteger(vertexLowerBound, vertexUpperBound)
    if isConnected:
        edgesLowerBound = n - 1

    if isSimpleGraph:
        # In a simple graph there can be no more edges
        # This is to prevent getting stuck in an infinite loop below
        if isDirected:
            vertexUpperBound = min(vertexUpperBound, n * (n - 1))
        else:
            vertexUpperBound = min(vertexUpperBound, n * (n - 1) / 2)

    m = getRandomInteger(edgesLowerBound, edgesUpperBound)

    E = []
    edgesSeen = [ set() for i in range(n+1) ]

    if isConnected:
        # isDirected == False is implied here, as directed graphs
        # have no notion of connectedness apart from being strongly connected.
        vertexList = [i for i in range(1, n + 1)]
        shuffle(vertexList)
        for i in range(1, n+1):
            u = vertexList[i-1]
            v = vertexList[i]

            if isWeighted:
                w = getRandomInteger(weightsLowerBound, weightsUpperBound)
                addEdgeToGraph(E, edgesSeen, u, v, isDirected, weight = w)
            else:
                addEdgeToGraph(E, edgesSeen, u, v, isDirected)

        m -= n - 1

    while m > 0:
        u = getRandomInteger(1, n)
        v = getRandomInteger(1, n)
        if u == v and not hasSelfLoops:
            continue

        if isSimpleGraph and v in edgesSeen[u]:
            continue

        if isWeighted:
            w = getRandomInteger(weightsLowerBound, weightsUpperBound)
            addEdgeToGraph(E, edgesSeen, u, v, isDirected, weight = w)
        else:
            addEdgeToGraph(E, edgesSeen, u, v, isDirected)

        if isDAG:
            visited = [ False for i in range(n+1) ]
            hasBackEdge = dfs( u, edgesSeen, visited )
            if hasBackEdge:
                E.pop()
                continue
        m -= 1
                
    shuffle(E)
    return (n, E)
