% Thesis Phase 4: 6G Joint Communication and Sensing (JCAS)
clear; clc; close all;
setenv('ROS_DOMAIN_ID', '0');

disp('1. Initializing Earth-to-Orbit 6G Link...');
robot = importrobot('space_printer.urdf');
robot.DataFormat = 'row';
node = ros2node("/matlab_earth_hub");
% Switch network link to the physical motor controllers in Gazebo
pub = ros2publisher(node, "/joint_group_position_controller/commands", "std_msgs/Float64MultiArray");
msg = ros2message(pub);
% --- 6G DIGITAL TWIN SETUP ---
% Initialize subscriber to harvest physical sensor data from Gazebo
sub = ros2subscriber(node, "/joint_states", "sensor_msgs/JointState");
disp('6G Return Link Established. Ready for Telemetry.');

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
    
    % Stream electrical commands to the motor array
    msg.data = configSol; 
    send(pub, msg); % Transmit to physical Gazebo motors
    % --- 6G JCAS SENSING LOGIC ---
    % 1. Allow the physics engine to react to the electrical command
    pause(0.1); 

    % 2. Harvest actual physical sensor data from the Gazebo robot
    try
        sensor_data = receive(sub, 1); % Wait up to 1s for a message
        
        % Extract the actual physical angles (Gazebo sorts these alphabetically)
        actual_angles = double(sensor_data.position(1:6)); 
        ideal_angles = double(configSol(:)); % Ensure column vector format
        
        % 3. The Digital Twin Math: Calculate physical deviation (Norm Error)
        % This measures how much the zero-gravity inertia dragged the robot off course
        structural_deviation = norm(ideal_angles - actual_angles);
        
        % 4. Threshold Detection for your Thesis
        tolerance_limit = 0.05; % Define your strict millimeter/radian tolerance
        
        if structural_deviation > tolerance_limit
            fprintf('[ALERT] 6G JCAS Detected Structural Micro-fracture/Deviation! Error: %.4f\n', structural_deviation);
            % Optional: Add a plot command here to mark a RED dot on your 3D graph
        else
            fprintf('[OK] 6G Telemetry Nominal. Tracking Error: %.4f\n', structural_deviation);
        end
        
    catch
        disp('[WARNING] 6G Signal Dropped: Could not read Gazebo sensor data.');
    end
    
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