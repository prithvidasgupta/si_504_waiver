def read_file():
    file = open('./BaconData/BaconCastFull.txt')
    movies = file.readlines()
    file.close()
    return movies


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


def generateBaconNumbers(listAllActors, actorNetwork):
    bacon = 'Bacon, Kevin'
    queue = []
    queue.append(bacon)
    levelCount = 1
    levelSize = len(queue)
    baconNumbers = [None for i in range(len(listAllActors))]
    baconNumbers[listAllActors.index(bacon)] = 1

    print(len(actorNetwork[bacon]))

    while queue:
        if (levelSize == 0):
            levelCount += 1
            levelSize = len(queue)
        actor = queue[0]
        queue.pop(0)
        print(levelSize)
        print(levelCount)
        for co_actor in actorNetwork[actor]:
            if baconNumbers[listAllActors.index(co_actor)]:
                continue
            baconNumbers[listAllActors.index(co_actor)] = levelCount
            queue.append(co_actor)
        levelSize -= 1
    filter(None, baconNumbers)
    return baconNumbers


def search(actor1, actor2, listAllActors, actorNetwork):
    minmumPath = generateMinimumPath(
        actor1, actor2, listAllActors, actorNetwork)
    return reconstructPath(actor1, actor2, minmumPath, listAllActors)


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


def getContinueInput():
    while True:
        cont = input('Continue finding degree of separation? (yes/no) ')
        if cont.lower().strip() == 'exit':
            quit()
        elif cont.lower() == 'yes':
            return True
        elif cont.lower() == 'no':
            return False
        else:
            print('Invalid input. Please enter "yes" or "no"')
            continue


def formatOutput(actor):
    actor = actor.split(', ')
    actor.reverse()
    return ' '.join(actor)


def run():
    movies = read_file()
    actorNetwork, listAllActors = generateNetwork(movies)
    #median,mean = generateBaconMedianMean(actorNetwork)
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
        cont = getContinueInput()
        if(cont):
            continue
        else:
            # print('Median Bacon Number: '+str(median))
            # print('Mean Bacon Number (3 decimal places): '+str(mean))
            quit()


# run()

movies = read_file()
actorNetwork, listAllActors = generateNetwork(movies)
nums = generateBaconNumbers(listAllActors, actorNetwork)
print(len(nums))
