<b>Dynamic Path Following</b>
<br>This project involves implementing and testing a dynamic path-following behavior for a character, leveraging a "chase the rabbit" algorithm as presented in an academic context. The implementation focuses on creating a responsive path-following experience by integrating support functions and reusing previous movement behaviors. The character follows a specified path and outputs its trajectory over a simulated duration. The character's simulated trajectories are logged over time in a .txt file in CSV format for easy analysis and visualization.

<br><b>Project Files</b></br>
  - [Dynamic Path Following Program](https://github.com/EricDelgado993/Dynamic-Path-Following/blob/main/Dynamic%20Path%20Following/Path%20Following.py)
  - [Character Movement Plot Data](https://github.com/EricDelgado993/Dynamic-Path-Following/blob/main/Dynamic%20Path%20Following/results.txt)

<br><b>Features</b></br>
  - <b>Dynamic Path Following:</b> Implements a "chase the rabbit" algorithm, which enables a character to follow a predefined path smoothly and accurately.
  - <b>Geometry Support Functions:</b> Includes various geometry functions essential for the Follow Path behavior.
  - <b>Integration with Dynamic Character Movement:</b>  Builds on prior Seek behavior, movement update, and Newton-Euler-1 integration techniques for a cohesive simulation experience.
  - <b>Trajectory Tracking:</b> enerates a trajectory text file for character movement over 125 seconds, with time steps of 0.5 seconds. Each time step records position, velocity, and orientation.

<br><b>Plot of Character Movement After 125 Seconds</b></br>
![Character Movement Plot](https://github.com/user-attachments/assets/e5228114-3cd4-4352-b199-48cd50673724)
