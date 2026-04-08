% Thesis Phase 2: MATLAB Digital Twin Initialization
clear; clc;

% 1. Define the ROS 2 Domain 
% (By default, ROS 2 Humble uses Domain ID 0. This ensures MATLAB and Ubuntu speak on the same frequency).
setenv('ROS_DOMAIN_ID', '0');

% 2. Create the MATLAB ROS 2 Node
disp('Initializing MATLAB Digital Twin Supervisor Node...');
supervisor_node = ros2node("/matlab_supervisor");

% 3. Scan the network for active ROS 2 topics
disp('Scanning for Orbital Printer telemetry...');
pause(3); % Give the DDS middleware a moment to discover nodes

% Fetch and display the topics
topics = ros2("topic", "list");
disp('--- Active ROS 2 Topics Found ---');
disp(topics);

disp('If the bridge is successful, you should see your ROS 2 topics above.');