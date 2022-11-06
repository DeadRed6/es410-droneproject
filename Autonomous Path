import numpy as np
import GPS
import Path_planning_file_management
class AstarShortestPath:
    def __init__(self,parent=None,position=None):
        ''' Attributes of a node in A* Search algorithm '''
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position
    
    def Astar(self,Map,StartCoordinate,EndCoordinate):
        ''' Find path as a set of coordinates between a given start and end coordindate '''
        StartNode = AstarShortestPath(None, StartCoordinate) # Initialise start node
        StartNode.g = StartNode.h = StartNode.f = 0 # Node attributes set to 0
        EndNode = AstarShortestPath(None, EndCoordinate) # Initialise end node
        EndNode.g = EndNode.h = EndNode.f = 0 # Node attributes set to 0
        OpenList = [] # Initialise open list
        ClosedList = [] # Initialise closed list
        
        OpenList.append(StartNode) # Add start node to open list
        while len(OpenList) > 0: # While end node is not found
            # Find current node and the respective index within open list
            CurrentNode = OpenList[0]
            CurrentNodeIndex = 0
            for index, item in enumerate(OpenList):
                if item.f < CurrentNode.f:
                    CurrentNode = item
                    CurrentNodeIndex = index
            # Remove current node from open list and add to closed list
            OpenList.pop(CurrentNodeIndex)
            ClosedList.append(CurrentNode)
            # Check if end node is found and return path from start node to end node
            if CurrentNode == EndNode:
                Path = []
                Current = CurrentNode
                while Current is not None:
                    Path.append(Current.position)
                    Current = Current.parent
                return Path[::-1] # Return reversed path
            # Generate neighbours
            Neighbours = []
            for NeighbourNodeDirectionIndex in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent nodes
                NeighbourNodeCoordinate = (CurrentNode.position[0] + NeighbourNodeDirectionIndex[0], CurrentNode.position[1] + NeighbourNodeDirectionIndex[1]) # Neighbour node's coordinate
                if NeighbourNodeCoordinate[0] > (len(Map) - 1) or NeighbourNodeCoordinate[0] < 0 or NeighbourNodeCoordinate[1] > (len(Map[len(Map)-1]) -1) or NeighbourNodeCoordinate[1] < 0:
                    # Ensure neighbour node is within range (reachable)
                    continue
                if Map[NeighbourNodeCoordinate[0]][NeighbourNodeCoordinate[1]] != 0:
                    # Ensure neighbour node is not an obstacle
                    continue
                # Add neighbour node to list
                NeighbourNode = AstarShortestPath(CurrentNode, NeighbourNodeCoordinate)
                Neighbours.append(NeighbourNode)
            for Neighbour in Neighbours: # For each neighbour in neighbours
                for NodeInClosedList in ClosedList:
                    if Neighbour == NodeInClosedList: # If meighbour is in the closed list
                        break
                else: # Calculate the f, g and h values
                    Neighbour.g = CurrentNode.g + 1
                    Neighbour.h = ((Neighbour.position[0] - EndNode.position[0]) ** 2) + ((Neighbour.position[1] - EndNode.position[1]) ** 2)
                    Neighbour.f = Neighbour.g + Neighbour.h
                    # Neighbour is already in the open list:
                    for NodeInOpenList in OpenList: # Check if new path to neighbours is <= to existing path (checkiing g) - admissible path
                        if Neighbour == NodeInOpenList and Neighbour.g >= NodeInOpenList.g:
                            break
                    else: # Add the neighbour to the open list
                        OpenList.append(Neighbour)
def GenerateLocalMap(self,ListOfCoordinatesCartesian):
        ''' Generate local map based on given coordinates to perform algorithm '''
        # Find max dimension of map from list of coordinates to visit
        MaxDimension = 0
        for Coordinate in ListOfCoordinatesCartesian:
            if max(Coordinate) > MaxDimension:
                MaxDimension = max(Coordinate)
        # Generate map of size (MaxDimension+1 by MaxDimension+1) represented by array of zeros
        Map = np.zeros((MaxDimension+1,MaxDimension+1))
        return Map
    
    def AddObstacle(self,Map,ListOfObstaclesCartesian):
        ''' Add obstacle to local map based on given coordinates '''
        MapWithObstacle = np.copy(Map)
        MapWithObstacle[ListOfObstaclesCartesian[0][0]:ListOfObstaclesCartesian[1][0]+1,ListOfObstaclesCartesian[0][1]:ListOfObstaclesCartesian[1][1]+1] = 1
        return MapWithObstacle
    def FindRoutes(self,Map,ListOfCoordinatesCartesian):
        ''' Find route between each coordinate to visit while avoiding obstacles '''
        Routes = []
        for CoordinateIndex in range(len(ListOfCoordinatesCartesian)-1): # Find shortest non-optimised route between consecutive coordinates
            StartCoordinate = ListOfCoordinatesCartesian[CoordinateIndex]
            EndCoordinate = ListOfCoordinatesCartesian[CoordinateIndex+1]
            Route = self.Astar(Map, StartCoordinate, EndCoordinate) # A* Search algorithm
            # Find shortest optimised route between consecutive coordinates
            # Re-run A* Search algorithm and generate map with no obstacles: if no obstacle in route then remove coordinate to visit
            EmptyMap = self.GenerateLocalMap(ListOfCoordinatesCartesian) # prints map within function
            i = 0
            j = 1
            StartCoordinate = Route[i]
            EndCoordinate = Route[j]
            while EndCoordinate != Route[-1]:
                RouteEmptyMap = self.Astar(EmptyMap, StartCoordinate, EndCoordinate)
                ObstaclePresentOrNot = []
                for CoordinateIndex in range(len(RouteEmptyMap)):
                    if Map[RouteEmptyMap[CoordinateIndex]] == 0:
                        ObstaclePresentOrNot.append(0)
                    else:
                        i += 1
                        j += 1
                        ObstaclePresentOrNot.append(1)
                        break
                if any(ObstaclePresentOrNot) == False:
                    Route.remove(RouteEmptyMap[-1])
                StartCoordinate = Route[i]
                EndCoordinate = Route[j]
            Routes.append(Route)
        return Routes
    def GPStoCart(self,Origin,ListOfCoordinatesGPS):
        ''' Convert GPS coordinates into Cartesian coordinates '''
        VectorFormCartesian = [] # GPS coordinates in vector form with each index representing (x,y,z,1)
        RoundedCoordinatesCartesian =[] # List of rounded Cartesian coordinates with each index representing (x,y)
        # Convert each index (containing GPS) into Cartesian coordinates, stored in vector form
        for i in range(len(ListOfCoordinatesGPS)):
            IndexVectorForm = GPS.get_vector(Origin,ListOfCoordinatesGPS[i][0],ListOfCoordinatesGPS[i][1])
            VectorFormCartesian.append(IndexVectorForm)
        # Round each Cartesian coordinate to the nearest integer (note: small error produced here)
        for i in range(len(VectorFormCartesian)):
            RoundedCoordinate = (round(VectorFormCartesian[i][0]),round(VectorFormCartesian[i][1]))
            RoundedCoordinatesCartesian.append(RoundedCoordinate)
        return RoundedCoordinatesCartesian
    def CarttoGPS(self,Origin,Routes):
        ''' Convert Cartesian coordinates into GPS coordinates '''
        ConvertedCoordinatesGPS = [] # List of converted GPS coordinates with each index representing (lat,long)
        # Convert each index (containing Cartesian) into GPS coordinates
        for i in range(len(Routes)):
            for j in range(len(Routes[i])):
                IndexGPS = GPS.get_gps(Origin, [Routes[i][j][0], Routes[i][j][1], -0.05457, 1]) # [Route][Route Coordinate][Lat,Long],z,1
                ConvertedCoordinatesGPS.append([IndexGPS[0],IndexGPS[1]])
        # Remove back to back repeated coordinates (if coordinate i is equal to coordinate i+1) - formatting procedure
        i = 0
        while ConvertedCoordinatesGPS[i] != ConvertedCoordinatesGPS[-1]:
            if ConvertedCoordinatesGPS[i] == ConvertedCoordinatesGPS[i+1]:
                ConvertedCoordinatesGPS.remove(ConvertedCoordinatesGPS[i])
            else:
                i += 1
        return ConvertedCoordinatesGPS
   
