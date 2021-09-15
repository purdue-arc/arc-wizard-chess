The node section contains program for all the nodes of the command center. 

There are three nodes: get_command, chess_algorithm, and robot_position_controller.

The get_command node accepts input from the user (read from the voice input) as the tile of the chess board that the robot should move to, as well as which robot should be moved. For the time being example input was created as PA5 (which means move pawn to A5). The node publishes that message to the chess_algorithm node, and subscribes to messages from two other nodes.

The chess_algorithm node subscribes to the get_command node, and reads the inputted robot movement message. It then sends back if the command is good (if the requested move is legal, this function needs to be added with the chess algorithm code), converts the message to the tile that the robot should move to (also has to be added using the chess algorithm code, for the time being example coordinates were used), and sends that tile coordinates to the robot_position_controller node.

The robot_position_controller subscribes to the message of the chess_algorithm, and moves the robot from the current example position (set in the code), to the position specified by the user, and converted to coordinates in previous nodes. For the time being, the robot movement is shown on a virtual chessboard. The node also sends to the get_command node message if a robot has moved to a right place on the chess board. 

The board.py file contains code that shows the virtual chess board, and chess pieces on it.
