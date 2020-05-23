from random import randint, shuffle

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

def getString( length, allowedChars ):
    s = ''
    lastIndex = length - 1
    for i in range(length):
        s.append( allowedChars[ randint( 0, lastIndex) ] )
    return s

# Generates 1-indexed graph based on given parameters
def getGraph( vertexLowerBound, vertexUpperBound,
              edgesLowerBound, edgesUpperBound,
              isWeighted = False, weightsLowerBound = 0, weightsUpperBound = 0,
              isSimpleGraph = True, hasSelfLoops = False, isDirected = False,
              isConnected = False, isDAG = False ):
    n = getRandomInteger(vertexLowerBound, vertexUpperBound)
    if isConnected:
        edgesLowerBound = n - 1
    m = getRandomInteger(edgesLowerBound, edgesUpperBound)

    E = []
    edgesSeen = [ set() for i in range(n+1) ]

    if isConnected:
        vertexList = [i for i in range(1, n + 1)]
        shuffle(vertexList)
        for i in range(1, n+1):
            E.append( ( vertexList[i - 1], vertexList[i] ) )
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
            E.append( (u, v, w) )
            edgesSeen[u].add(v)
            if not isDirected:
                E.append( (v, u, w) )
                edgesSeen[v].add(u)
        else:
            E.append( (u, v) )
            edgesSeen[u].add(v)
            if not isDirected:
                E.append( (v, u) )
                edgesSeen[v].add(u)

        if isDAG:
            visited = [ False for i in range(n+1) ]
            hasBackEdge = dfs( u, edgesSeen, visited )
            if hasBackEdge:
                E.pop()
                continue
        m -= 1
                
    shuffle(E)
    return (n, E)
