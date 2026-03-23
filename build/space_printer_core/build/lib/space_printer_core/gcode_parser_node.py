import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time
import math
import os

class GcodeParserNode(Node):
    def __init__(self):
        super().__init__('gcode_parser_node')
        
        # Publisher to drive the robot joints (replacing the manual GUI)
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)
        self.gcode_file = os.path.expanduser('~/space_twin_ws/test_print.gcode')
        
        self.get_logger().info("G-Code Parser Initialized. Starting Autonomous Print...")
        
        # Start the parsing loop
        self.timer = self.create_timer(1.0, self.parse_and_publish)
        self.gcode_lines = []
        self.current_line = 0
        
        self.load_gcode()

    def load_gcode(self):
        if os.path.exists(self.gcode_file):
            with open(self.gcode_file, 'r') as f:
                self.gcode_lines = [line.strip() for line in f if line.startswith('G1')]
            self.get_logger().info(f"Loaded {len(self.gcode_lines)} print commands.")
        else:
            self.get_logger().error("G-code file not found!")

    def parse_and_publish(self):
        if self.current_line >= len(self.gcode_lines):
            self.get_logger().info("Print Complete! Looping back to start...")
            self.current_line = 0

        # 1. Parse X, Y, Z from the G-Code string
        line = self.gcode_lines[self.current_line]
        parts = line.split()
        x, y, z = 0.0, 0.0, 0.0
        
        for part in parts:
            if part.startswith('X'): x = float(part[1:])
            if part.startswith('Y'): y = float(part[1:])
            if part.startswith('Z'): z = float(part[1:])

        # 2. Simulated Inverse Kinematics (Mapping coordinates to joint angles)
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
        
        # Generate sweeping joint angles based on the G-code coordinates
        j1 = math.atan2(y, x)
        j2 = z * 2.0
        j3 = x * 3.0
        j4 = y * 3.0
        j5 = (x + y) / 2.0
        j6 = math.pi / 4  # Extruder angle
        
        msg.position = [j1, j2, j3, j4, j5, j6]

        # 3. Publish to the robot
        self.publisher_.publish(msg)
        self.get_logger().info(f"Executing: {line} -> Publishing Joint States")
        
        self.current_line += 1

def main(args=None):
    rclpy.init(args=args)
    node = GcodeParserNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
