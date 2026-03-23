import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import json
import time

class TelemetryNode(Node):
    def __init__(self):
        super().__init__('telemetry_node')
        
        # Subscribe to the robot's joint states
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_callback,
            10)
        
        # Publisher for the 6G network simulator to pick up
        self.publisher_ = self.create_publisher(String, '/telemetry_stream_6g', 10)
        self.get_logger().info("6G Telemetry Node initialized. Broadcasting packets...")

    def joint_callback(self, msg):
        # Package the raw ROS data into a standard JSON payload
        payload = {
            "timestamp_ms": int(time.time() * 1000),
            "device_id": "space_printer_01",
            "data_size_bytes": 256, # Simulated payload size
            "joints": dict(zip(msg.name, msg.position))
        }
        
        # Convert to a string message
        telemetry_msg = String()
        telemetry_msg.data = json.dumps(payload)
        
        # Publish to the telemetry stream
        self.publisher_.publish(telemetry_msg)
        self.get_logger().info(f"Tx Payload: {telemetry_msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = TelemetryNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
