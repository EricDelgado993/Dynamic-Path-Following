#==========================================================
# CS 330-01 Programming Assignment 2
# Dynamic Movement Path Following Movement Update Algorithm
# Eric Delgado
# 10/24/2024 
#==========================================================

import numpy as np
import math
import copy

class Character:

    def __init__(self, time, id, position_X, position_Z, velocity_X, velocity_Z, 
                 linearAcc_X, linearAcc_Z, orientation, steeringCode, 
                 collisionStatus, maxVelocity, maxAcceleration,
                 arrivalRadius, slowingRadius, timeToTarget, pathToFollow,
                 pathOffset):
        
        self.time = time                          # Simulation time
        self.id = id                              # Character ID (numeric)
        self.position_X = position_X              # X position of character on map (meters)
        self.position_Z = position_Z              # Z position of character on map (meters)
        self.velocity_X = velocity_X              # X direction of character's velocity (meters)
        self.velocity_Z = velocity_Z              # Z direction of character's velocity (meters)
        self.linearAcc_X = linearAcc_X            # X direction of character's linear acceleration (meters per second per second)
        self.linearAcc_Z = linearAcc_Z            # Z direction of character's linear acceleration (meters per second per second)
        self.orientation = orientation            # Character orientation (radians)
        self.steeringCode = steeringCode          # Steering hevaior code (1=continueCharacter, 6=seek, 7=flee, 8=arrive, 11=followPath)
        self.collisionStatus = collisionStatus    # Always "False" in this implementation
        self.maxVelocity = maxVelocity            # Velocity cap used for regulating character's speed
        self.maxAcceleration = maxAcceleration    # Acceleration cap used for regulating character's acceleration
        self.arrivalRadius = arrivalRadius        # Distance to target where character stops
        self.slowingRadius = slowingRadius        # Distance to target where character slow down occurs
        self.timeToTarget = timeToTarget          # Time needed to approach the target
        self.pathToFollow = pathToFollow          # Identifier of path character will follow  
        self.pathOffset = pathOffset              # Path position offset  

    def seek(self, source, target):

        # Get the direction to the target.
        directionVector = np.array([(target[0] - source[0]), 
                                   (target[1] - source[1])])
    
        # Acccelerate at the maximum rate.
        posVector = self.__normalize(directionVector[0], directionVector[1], self.maxAcceleration)

        self.__update(posVector) 

    def followPath(self, path):

        # Capture the current position of the character.
        characterPosition = np.array([self.position_X, self.position_Z])
    
        # Find current position on path.
        currentParam = path.getParam(characterPosition)

        # Calculate target parameter by offsetting the current parameter.
        targetParam = currentParam + self.pathOffset

        # Calculate the target position using the target parameter.
        targetPosition = path.getPosition(targetParam)

        # Pass target position into the seek function.
        self.seek(characterPosition, targetPosition)

    def __update(self, vector):

        self.time += 0.5    # increase total time by 0.5 sec
        deltaTime = 0.5     # timestep used in calculations

        # Compute the length of linear acceleration vector.
        length = self.__lengthOf(self.linearAcc_X, self.linearAcc_Z)

        # Prevents character's acceleration from exceeding maxAcceleration.
        # Acceleration vector is normalized and acceleration values are updated.
        if length > self.maxAcceleration:
            self.linearAcc_X = (self.linearAcc_X / length) * self.maxAcceleration
            self.linearAcc_Z = (self.linearAcc_Z / length) * self.maxAcceleration
        
        else:
            self.linearAcc_X = vector[0]
            self.linearAcc_Z = vector[1]

        # Update the position of the character.
        self.position_X += (self.velocity_X * deltaTime)
        self.position_Z += (self.velocity_Z * deltaTime)

        # Update the velocity of the chracter.
        self.velocity_X += (vector[0] * deltaTime)
        self.velocity_Z += (vector[1] * deltaTime)

        # Compute the length of velocity vector.
        length = self.__lengthOf(self.velocity_X, self.velocity_Z)

        # Prevents character's speed from exceeding maxVelocity.
        # Speed vector is normalized and velocity values are updated.
        if length > self.maxVelocity:
            self.velocity_X = (self.velocity_X / length) * self.maxVelocity
            self.velocity_Z = (self.velocity_Z / length) * self.maxVelocity
    
    def __lengthOf(self, x, z):

        return math.sqrt(math.pow(x, 2) + math.pow(z, 2))

    def __normalize(self, x, z, vectorQuantity):

        vector = []

        length = self.__lengthOf(x, z)

        vector.append((x / length) * vectorQuantity)
        vector.append((z / length) * vectorQuantity)

        return vector
    
class Path(object):

    def __init__(self):

        self.ID = 0                    # Unique path ID
        self.x = np.array([])          # Array of X coordinates of path verticies
        self.z = np.array([])          # Array of Z coordinates of path verticies
        self.params = np.array([])     # Array of path parameters at each vertex
        self.distance = ([])           # Array of cumulative path distances at each vertex
        self.numSegments = 0           # Number of line segments in the path
    
    def pathAssemble(self, ID, x_coordinates, z_coordinates):

        self.ID = ID
        self.x = x_coordinates
        self.z = z_coordinates
        self.numSegments = self.x.size - 1
        self.params = np.zeros(self.x.size)
        self.distance = np.zeros(self.x.size)

        # Iterate through all line segements in the path.
        for i in range(self.numSegments):

            # Add up cumulative distance of path at a given vertex.
            # Insert each entry into the array.
            self.distance[i + 1] = (
                self.distance[i] 
                + self.__magnitudeOf(self.x[i], self.z[i], self.x[i + 1], self.z[i + 1])
            )

        # Iterate through all line segments in the path.
        for i in range(self.numSegments):

            # Record the percentage of distance covered in the total path at
            # the given point.
            self.params[i + 1] = self.distance[i + 1] / np.max(self.distance)

    def getPosition(self, param):
        
        endpointVector_A = np.array([0, 0])     # Coordinates of the first vertex within the line segment
        endpointVector_B = np.array([0, 0])     # Coordinates of the second vertex within the line segment
        endpointParam_A = 0                     # Parameter value of the first vertex
        endpointParam_B = 0                     # Parameter value of the second vertex
        paramIndex = 0                          # Index for path's parameter array

        # Iterate through all line segments in the path to find which
        # verticies param falls in between.
        for i in range(self.numSegments):

            # Captures the indexes at which the current parameter value
            # falls in between the parameter values of the two verticies.
            if self.params[i] <= param <= self.params[i + 1]:

                paramIndex = i
        
        # Capture the x and z coordinates of the two verticies.
        endpointVector_A[0] = self.x[paramIndex]
        endpointVector_A[1] = self.z[paramIndex]
        endpointVector_B[0] = self.x[paramIndex + 1]
        endpointVector_B[1] = self.z[paramIndex + 1]
        
        # Capture the param value of the two verticies.
        endpointParam_A = self.params[paramIndex]
        endpointParam_B = self.params[paramIndex + 1]

        # Use the endpoint parameter values in conjunction with the current
        # parameter value to create a value to scale the resulting vector.
        scalar = ((param - endpointParam_A) / (endpointParam_B - endpointParam_A))

        # Find closest point on map with respect to the nearest line segment.
        position = endpointVector_A + (scalar * (endpointVector_B - endpointVector_A))
  
        return position
            
    def getParam(self, position):

        endpointVector_A = np.array([0, 0])     # Coordinates of the first vertex within the line segment
        endpointVector_B = np.array([0, 0])     # Coordinates of the second vertex within the line segment
        endpointParam_A = 0                     # Parameter value of the first vertex
        endpointParam_B = 0                     # Parameter value of the second vertex
        closestPoint = np.array([0, 0])         # Coordinates of the closest point to the line segment
        closestDistance = math.inf              # Magnitude between character's position and closestPoint
        closestSegment = 0                      # Index referencing the verticies of the closest line segment
        
        # Iterate through each line segment in the path to find the
        # closest line segment in the path.
        for i in range(self.numSegments):

            endpointVector_A[0] = self.x[i]
            endpointVector_A[1] = self.z[i]
            endpointVector_B[0] = self.x[i + 1]
            endpointVector_B[1] = self.z[i + 1]

            # Retrieve the closest point to the line segment in the path.
            checkPoint = self.closestPointSegment(position, endpointVector_A, endpointVector_B)
            
            # Get the magnitude between the character's current position and
            # the closest point in the path.
            checkDistance = self.__magnitudeOf(position[0], position[1], checkPoint[0], checkPoint[1])

            # Get the index of the closest line segment.
            if (checkDistance < closestDistance):
                
                closestPoint = checkPoint
                closestDistance = checkDistance
                closestSegment = i

        # Capture the x and z coordinates of the two verticies
        # composing the closest line segment.
        endpointVector_A[0] = self.x[closestSegment]
        endpointVector_A[1] = self.z[closestSegment]
        endpointVector_B[0] = self.x[closestSegment + 1]
        endpointVector_B[1] = self.z[closestSegment + 1]

        # Capture the param value of the two verticies.
        endpointParam_A = self.params[closestSegment]
        endpointParam_B = self.params[closestSegment + 1]

        # Capture the point closest to the line segment.
        endpointVector_C = closestPoint

        # Compute |C-A| / |B-A| to create a value to scale the parameter
        # of the closest point.
        scalar = (
            self.__magnitudeOf(endpointVector_C[0], endpointVector_C[1], endpointVector_A[0], endpointVector_A[1])
            / self.__magnitudeOf(endpointVector_B[0], endpointVector_B[1], endpointVector_A[0], endpointVector_A[1])
        )

        # Calculte the parameter of the closest point.
        endpointParam_C = endpointParam_A + (scalar * (endpointParam_B - endpointParam_A))

        return(endpointParam_C)

    def closestPointLine(self, vector_Q, vector_A, vector_B):

        # Find point on line closest to the query point in 2D.
        scalar = (
            self.__vectorDot((vector_Q - vector_A), (vector_B - vector_A))
            / self.__vectorDot((vector_B - vector_A), (vector_B - vector_A))
        )

        closestPoint = (vector_A + (scalar * (vector_B - vector_A)))

        return closestPoint

    def closestPointSegment(self, vector_Q, vector_A, vector_B):

        # Find point on segment closest to the query point in 2D.
        scalar = (
            self.__vectorDot((vector_Q - vector_A), (vector_B - vector_A)) 
            / self.__vectorDot((vector_B - vector_A), (vector_B - vector_A))
        )

        if (scalar <= 0):

            return vector_A
        
        elif (scalar >= 1):

            return vector_B
        
        else:
            
            return (vector_A + (scalar * (vector_B - vector_A)))
 
    def __magnitudeOf(self, x1, z1, x2, z2):

        return math.sqrt(
                        math.pow((x2 - x1), 2)
                         + math.pow((z2 - z1), 2)
        )
        
    def __vectorDot(self, vector_A, vector_B):

        return (
                (vector_A[0] * vector_B[0])
                + (vector_A[1] * vector_B[1])
        )

# Intantiate x and z coordinates of path.
vertexList_X = np.array([0, -20, 20, -40, 40, -60, 60, 0])
vertexList_Z = np.array([90, 65, 40, 15, -10, -35, -60, -85])

# Create and assemble path object.
characterPath = Path()
characterPath.pathAssemble(2071, vertexList_X, vertexList_Z)

trajectoryList = []
time = 0 

# Instantiate character with base values.
character1 = Character(0, 2701, 20, 95, 0, 0, 0, 0, 0.0, 11, 
                       False, 4, 2, 0, 0, 0, 1, 0.04)

# Populate trajectoryList and invoke movement behavior at each timestep.
while time <= 125:

    trajectoryList.append(copy.copy(character1))
    character1.followPath(characterPath)
      
    time += 0.5

file = open('results2.txt', 'w')

# Iterate through each element in trajectoryList and write each line to file.
for Character in trajectoryList:

    file.write(str(Character.time)
               + ", " + str(Character.id)
               + ", " + str(Character.position_X)
               + ", " + str(Character.position_Z)
               + ", " + str(Character.velocity_X)
               + ", " + str(Character.velocity_Z)
               + ", " + str(Character.linearAcc_X)
               + ", " + str(Character.linearAcc_Z)
               + ", " + str(Character.orientation)
               + ", " + str(Character.steeringCode)
               + ", " + str(Character.collisionStatus)
               + "\n")

file.close