import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped # Used for Cartesian spatial trajectories

class GcodeParserNode(Node):
    def __init__(self):
        super().__init__('gcode_parser_node')
        
        # Publisher to send the parsed Cartesian trajectories to MoveIt 2 or a controller
        self.trajectory_pub = self.create_publisher(PoseStamped, '/target_pose', 10)
        
        self.get_logger().info("G-code Parser Node initialized. Ready to ingest toolpaths.")

    def parse_gcode_file(self, filepath):
        """
        Reads a standard 3D printing G-code file and processes it line by line.
        """
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    self.process_gcode_line(line.strip())
        except FileNotFoundError:
            self.get_logger().error(f"G-code file not found at: {filepath}")

    def process_gcode_line(self, line):
        """
        Translates G-code commands (like G0, G1) into Cartesian spatial trajectories.
        """
        # Ignore comments and empty lines
        if not line or line.startswith(';'):
            return

        # TODO: Add regex or string splitting here to extract X, Y, Z coordinates
        # and extruder commands (E). Then, format them into a PoseStamped message
        # and publish it using self.trajectory_pub.publish(pose_msg)
        
        self.get_logger().debug(f"Processed line: {line}")

def main(args=None):
    rclpy.init(args=args)
    node = GcodeParserNode()
    
    # Example usage (you would eventually pass this via a ROS parameter or service)
    # node.parse_gcode_file('/path/to/your/test_print.gcode')
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

