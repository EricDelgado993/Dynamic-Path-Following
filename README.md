# Dynamic Path Following

## Overview
This project implements a dynamic path-following behavior for a character using a "chase the rabbit" algorithm, as discussed in the academic context. The program focuses on creating a responsive and smooth path-following experience by leveraging various supporting geometry functions and integrating them with previously implemented movement behaviors. The character follows a predefined path, and its trajectory is simulated and logged over time for analysis and visualization.

The character's simulated trajectories are recorded in a `.txt` file in CSV format, which can be used to visualize and analyze the movement over a duration of 125 simulated seconds.

## Project Files
  - [Dynamic Path Following Program](https://github.com/EricDelgado993/Dynamic-Path-Following/blob/main/Dynamic%20Path%20Following/Path%20Following.py)
  - [Character Movement Plot Data](https://github.com/EricDelgado993/Dynamic-Path-Following/blob/main/Dynamic%20Path%20Following/results.txt)

## Features

### 1. Dynamic Path Following
- Implements the "chase the rabbit" algorithm that allows the character to follow a predefined path smoothly and accurately.

### 2. Geometry Support Functions
- Includes various geometry functions essential for path-following behavior, enabling accurate simulation of character movement.

### 3. Integration with Dynamic Character Movement
- Builds on previous dynamic movement behaviors (Seek, Movement Update, and Newton-Euler-1 integration techniques) to create a cohesive simulation experience.

### 4. Trajectory Tracking
- Generates a trajectory text file for character movement over 125 seconds, with time steps of 0.5 seconds. Each time step logs the position, velocity, and orientation of the character.

### 5. Output Format
- The trajectory data is saved in a CSV format, which includes a record for each character per time step, starting from time = 0. The file format is consistent with Program 1, with field 10 of the output file specifying the steering behavior code as "Follow path" (code 11).

### 6. Plotting Character Movement
- The program outputs a plot of the character's movement after the full 125-second simulation.

## Program Details

### Requirements:
- Implement the dynamic Follow Path behavior using the "chase the rabbit" algorithm.
- The Follow Path behavior relies on and reuses the Seek behavior, movement update, and other relevant functionality from the [Dynamic Character Movement Program](https://github.com/EricDelgado993/Dynamic-Movement).
- The simulation should run for 125 seconds with a time step of 0.5 seconds.
- Initial conditions for the character:
  - Character ID: 1
  - Steering behavior: Follow Path
  - Initial position: (20, 95)
  - Initial velocity: (0, 0)
  - Initial orientation: 0
  - Max velocity: 4
  - Max acceleration: 2
  - Path to follow: 1
  - Path offset: 0.04
  - Path vertices: (0, 90), (-20, 65), (20, 40), (-40, 15), (40, -10), (-60, -35), (60, -60), (0, -85)

### Expected Output:
- The program generates a text file containing the character’s trajectory over the 125-second duration, capturing position, velocity, and orientation for each time step.

### Plot of Character Movement After 125 Seconds
![Character Movement Plot](https://github.com/user-attachments/assets/e5228114-3cd4-4352-b199-48cd50673724)
