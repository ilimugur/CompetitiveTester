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

def getRandomString( minLength, maxLength, allowedChars ):
    length = getRandomInteger(minLength, maxLength)
    s = ''
    lastAllowedCharIndex = len(allowedChars) - 1
    for i in range(length):
        s += (allowedChars[ getRandomInteger(0, lastAllowedCharIndex) ])
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

# queriesInfo is a nested list.
# queriesInfo[i] is a list containing information needed to generate parameters
# required for a query of type i.
# queriesInfo[i][0] must be 1 or 2, indicating whether the query is relevant to
# a single index or a range of indices, respectively. For all j > 0,
# queriesInfo[i][j] is a list. Its first element must be one of the types
# int, str or float.
# The rest of queriesInfo[i][j] includes ordered information needed by the
# module to generate a random value of that type.
#
# For int/float:
#     queriesInfo[i][j] = [int/float, minVal, maxVal]
# For str:
#     queriesInfo[i][j] = [str, minLen, maxLen, allowedChars]
#
# Returns a list of lists Q. Q[i] is a list containing the ith query.
# Q[i][0], Q[i][1] and Q[i][2] are the type, the left endpoint and
# the right endpoint for the range query, respectively. Q[i][3:] contains the
# randomly generated extra parameters for the query, in the order they were
# given in queries list.

def getRangeQueries(numQueries, queriesInfo,
                    minRangeEndpointVal, maxRangeEndpointVal):
    numQueryTypes = len(queriesInfo)
    Q = []

    for k in range(numQueries):
        queryType = getRandomInteger(1, numQueryTypes)
        queryTypeIndex = queryType - 1
        numIdentifyingParams = queriesInfo[queryTypeIndex][0]

        if numIdentifyingParams == 1:
            elementID = getRandomInteger(minRangeEndpointVal, maxRangeEndpointVal)
            query = [queryType, elementID]
        elif numIdentifyingParams == 2:
            minEndpoint = getRandomInteger(minRangeEndpointVal, maxRangeEndpointVal)
            maxEndpoint = getRandomInteger(minEndpoint, maxRangeEndpointVal)
            query = [queryType, minEndpoint, maxEndpoint]
        else:
            print("ERROR: Unsupported amount of identifying params requested.")

        for extraParamInfo in queriesInfo[queryTypeIndex][1: ]:
            # TODO: Check if extraParamInfo conforms to the expected format
            paramType = extraParamInfo[0]
            if paramType == str:
                param = getRandomString(extraParamInfo[1], extraParamInfo[2],
                                        extraParamInfo[3])
            elif paramType == int:
                param = getRandomInteger(extraParamInfo[1], extraParamInfo[2])
            elif paramType == float:
                param = getRandomFloat(extraParamInfo[1], extraParamInfo[2])
            else:
                print("ERROR: Unsupported query parameter type!")
                exit(1)
            query.append(param)
        Q.append(query)

    return Q
