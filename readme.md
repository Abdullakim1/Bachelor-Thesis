# 1. Source the main ROS 2 installation
source /opt/ros/humble/setup.bash

# 2. Tell Gazebo where to find the TurtleBot 3D mesh (.stl) files so it isn't invisible
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/opt/ros/humble/share

# 3. Launch the empty Gazebo world
ros2 launch gazebo_ros gazebo.launch.py

Robot State Publisher

# 1. Source your local workspace
source install/setup.bash

# 2. Start the publisher node using your generated URDF
ros2 run robot_state_publisher robot_state_publisher src/space_printer_description/urdf/turtlebot_miner.urdf

Spawn the Robot into Gazebo

# 1. Source your local workspace
source install/setup.bash

# 2. Set the expected TurtleBot model environment variable
export TURTLEBOT3_MODEL=waffle

# 3. Spawn the combined robot model into the Gazebo world slightly above the ground (z=0.2)
ros2 run gazebo_ros spawn_entity.py -entity turtlebot_miner -file src/space_printer_description/urdf/turtlebot_miner.urdf -z 0.2

Teleoperation (Drive the Robot)

# 1. Source the main ROS 2 installation
source /opt/ros/humble/setup.bash

# 2. Run the teleop keyboard node
ros2 run teleop_twist_keyboard teleop_twist_keyboard

I need to add u squared-net model for saliency for vision
Autonomous navigation
6G somehow must be part of this project first as implementation like sensing and then I need to work on theoretical part
