% Thesis Phase 4: 6G Joint Communication and Sensing (JCAS)
clear; clc; close all;
setenv('ROS_DOMAIN_ID', '0');

disp('1. Initializing Earth-to-Orbit 6G Link...');
robot = importrobot('space_printer.urdf');
robot.DataFormat = 'row';
node = ros2node("/matlab_earth_hub");
pub = ros2publisher(node, "/joint_states", "sensor_msgs/JointState");
msg = ros2message(pub);
msg.name = {'joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6'};

ik = inverseKinematics('RigidBodyTree', robot);
weights = [1 1 1 1 1 1]; 
initialGuess = robot.homeConfiguration;

% Prepare the Thesis-Ready 3D Live Graph
figure('Name', '6G JCAS Live Structural Sensing', 'NumberTitle', 'off');
hold on; grid on; view(3);
xlabel('X (m)'); ylabel('Y (m)'); zlabel('Z (m)');
title('Live 6G Terahertz Structural Sensing (Digital Twin)');
xlim([0.2 0.6]); ylim([-0.2 0.2]); zlim([0.3 0.6]);

disp('2. Commencing Orbital Print & 6G Sensing...');
t = linspace(0, 10, 100);

for i = 1:length(t)
    % 1. COMMUNICATION: Calculate Target & Stream Control Packets
    x_target = 0.4 + 0.1 * cos(t(i));
    y_target = 0.0 + 0.1 * sin(t(i));
    z_target = 0.4 + (0.01 * t(i));
    
    targetPose = trvec2tform([x_target y_target z_target]);
    [configSol, ~] = ik('extruder_nozzle', targetPose, weights, initialGuess);
    initialGuess = configSol; 
    
    msg.position = configSol;
    msg.header.stamp = ros2time(node, 'now');
    send(pub, msg); % Transmit to ROS 2 (Orbit)
    
    % 2. SENSING (JCAS): Simulate THz Radar Return
    % We simulate the 6G signal bouncing off the print with slight quantum noise
    sense_x = x_target + (randn * 0.002);
    sense_y = y_target + (randn * 0.002);
    sense_z = z_target + (randn * 0.002);
    
    % Inject a simulated "Micro-fracture" anomaly at step 60 and 61
    if i == 60 || i == 61
        sense_x = sense_x + 0.02; % Sensing beam detects a structural shift
        plot3(sense_x, sense_y, sense_z, 'r*', 'MarkerSize', 8, 'LineWidth', 2);
        disp(['[ALERT] 6G JCAS Detected Structural Micro-fracture at step ', num2str(i)]);
    else
        % Normal structural integrity
        plot3(sense_x, sense_y, sense_z, 'b.', 'MarkerSize', 10);
    end
    
    drawnow; % Update the live graph
    pause(0.1); 
end

disp('Print Complete. Sensing Data Logged.');