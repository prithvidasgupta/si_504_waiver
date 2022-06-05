"""
"""
def read_file():
    file = open('./BaconData/BaconCastFull.txt')
    movies = file.readlines()
    file.close()
    return movies

"""
"""
def generateNetwork(movies):
    actorNetwork = {}
    allActors = set()

    for movie in movies:
        split = movie.strip().split('/')
        movieCast = split[1:len(split)]
        for actor in movieCast:
            if actor not in allActors:
                allActors.add(actor)
                actorNetwork[actor] = set()
            actorNetwork[actor].update(movieCast)
            actorNetwork[actor].remove(actor)
    listAllActors = list(allActors)

    return actorNetwork, listAllActors


"""

"""
def generateMinimumPath(actr1, actr2, listAllActors, actorNetwork):
    queue = []
    queue.append(actr1)
    visited = [False for i in range(len(listAllActors))]
    minmumPath = [None for i in range(len(listAllActors))]
    visited[listAllActors.index(actr1)] = True

    while queue:
        actor = queue[0]
        queue.pop(0)
        for co_actor in actorNetwork[actor]:
            # converting to array indexes as the index itself will be used in the output to store the path information
            co_actor_idx = listAllActors.index(co_actor)
            actor_idx = listAllActors.index(actor)
            if not visited[co_actor_idx]:
                queue.append(co_actor)
                # marks the node visited
                visited[co_actor_idx] = True
                # if we have not encountered this node before it indicates that
                # this is the shortest hop between the starting node and the current node
                # so we store in the minimumPath array
                # the index of the co_actor will contain the parent node aka the actor index
                minmumPath[co_actor_idx] = actor_idx
            # exit the graph traversal when the second node is found
            if co_actor == actr2:
                return minmumPath
    return minmumPath

"""
"""
def reconstructPath(actor1, actor2, minmumPath, listAllActors):
    path = []
    temp = listAllActors.index(actor2)
    path.append(listAllActors[temp])
    while (minmumPath[temp] is not None):
        path.append(listAllActors[minmumPath[temp]])
        temp = minmumPath[temp]
    path.reverse()
    if(path[0] == actor1):
        return path
    return []

"""
"""
def generateBaconNumbers(actorNetwork):
    bacon = 'Bacon, Kevin'
    currentSet = set()
    currentSet.add(bacon)
    nextSet = set()
    actorCounts = list()
    processedSet = set()
    run = True
    while run:
        actorCount = 0
        for actor in currentSet:
            if actor in processedSet:
                continue 
            nextSet.update(actorNetwork[actor])
            actorCount+=1
            processedSet.add(actor)
        if len(nextSet)==0:
            run = False
        else:
            actorCounts.append(actorCount)
            currentSet=nextSet
            nextSet = set()
    return actorCounts

"""
"""
def search(actor1, actor2, listAllActors, actorNetwork):
    minmumPath = generateMinimumPath(
        actor1, actor2, listAllActors, actorNetwork)
    return reconstructPath(actor1, actor2, minmumPath, listAllActors)
"""
[1, 2249, 218085, 561132, 111180, 7906, 903, 100, 14]
Haaland, Daniel
Maciel, Henri
Adams, Joanna
Neder, Hermelino
Shafer, Joseph Otero
Bozoyan, Mariam
"""
def generateBaconMedianMean(actorNetwork):
    numbers = generateBaconNumbers(actorNetwork)
    totalActorsInBaconTree = 0
    mean = 0;
    median = 0;
    temp = 0;
    mid =0;
    totalActorsInBaconTree = sum(numbers)
    if(totalActorsInBaconTree%2==0):
        mid=int((totalActorsInBaconTree/2)-1)
    else:
        mid = int(totalActorsInBaconTree/2)
    for number in numbers:
        temp+=number
        if median==0 and mid<temp:
            median = numbers.index(number)
        mean+=number*numbers.index(number)
    mean = mean/totalActorsInBaconTree
    return median,mean


"""
"""
def getActorInput(actorNumber, actorNetwork):
    while True:
        actor = input('Enter name of actor '+str(actorNumber) +
                      '(Example- Tom Holland): ')
        if actor.lower().strip() == 'exit':
            quit()
        actor = actor.split(' ')
        actor.reverse()
        formattedActor = ', '.join(actor)
        if formattedActor in actorNetwork:
            return formattedActor
        else:
            print('Actor not found. Please enter again')
            continue

"""
"""
def getContinueInput(str):
    while True:
        cont = input(str+' (yes/no): ')
        if cont.lower().strip() == 'exit':
            quit()
        elif cont.lower() == 'yes':
            return True
        elif cont.lower() == 'no':
            return False
        else:
            print('Invalid input. Please enter "yes" or "no"')
            continue

"""
"""
def formatOutput(actor):
    actor = actor.split(', ')
    actor.reverse()
    return ' '.join(actor)

"""
"""
def run():
    movies = read_file()
    actorNetwork, listAllActors = generateNetwork(movies)
    print('Find the degree of separation between two actors!')
    while True:
        actor1 = getActorInput(1, actorNetwork)
        actor2 = getActorInput(2, actorNetwork)
        path = search(actor1, actor2, listAllActors, actorNetwork)
        if len(path) == 0:
            print('Path: No path between the two actors found!')
        else:
            print('Path: '+' -> '.join(map(formatOutput, path)))
            print('Degree of separation: '+str(len(path)-1))
        cont = getContinueInput('Continue finding degree of separation?')
        if(cont):
            continue
        else:
            seeBaconNums = getContinueInput('See the median and mean of Kevin Bacon\'s degree of separation?')
            if(seeBaconNums):
                 median,mean = generateBaconMedianMean(actorNetwork)
                 print('Median: '+str(median))
                 print('Mean: '+str(round(mean,3)))
            quit()


run()
