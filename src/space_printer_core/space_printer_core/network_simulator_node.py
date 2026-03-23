import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time
import random
import csv
import os

class NetworkSimulatorNode(Node):
    def __init__(self):
        super().__init__('network_simulator_node')
        
        # Subscribe to the telemetry stream
        self.subscription = self.create_subscription(
            String,
            '/telemetry_stream_6g',
            self.telemetry_callback,
            10)
            
        # Set up a CSV file to save your thesis data!
        self.csv_file_path = os.path.expanduser('~/space_twin_ws/6g_network_metrics.csv')
        self.init_csv()
        
        self.get_logger().info("6G Network Simulator initialized. Waiting for packets...")

    def init_csv(self):
        # Create the CSV file and write the header row
        with open(self.csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['tx_timestamp_ms', 'rx_timestamp_ms', 'simulated_latency_ms', 'packet_size_bytes', 'status'])

    def telemetry_callback(self, msg):
        # 1. Catch the packet
        rx_time = time.time()
        payload = json.loads(msg.data)
        tx_time_ms = payload['timestamp_ms']
        
        # 2. Simulate 6G Physics (Sub-millisecond latency + slight jitter)
        # 6G target latency is roughly 0.1ms to 1ms
        base_latency_ms = 0.5 
        jitter_ms = random.uniform(-0.1, 0.2)
        total_simulated_latency_ms = base_latency_ms + jitter_ms
        
        # Simulate network transit time by making the script pause for a microsecond fraction
        time.sleep(total_simulated_latency_ms / 1000.0)
        
        # 3. Calculate End-to-End Metrics
        # Simulate a 99.999% reliability (1 in 100,000 packets might drop)
        status = "DROPPED" if random.random() > 0.99999 else "RECEIVED"
        
        if status == "RECEIVED":
            self.get_logger().info(f"Rx Packet | Latency: {total_simulated_latency_ms:.3f} ms | Size: {payload['data_size_bytes']}B")
        else:
            self.get_logger().warn("URLLC Packet Dropped! (Simulated)")

        # 4. Save to CSV for your thesis graphs
        with open(self.csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([tx_time_ms, int(rx_time * 1000), round(total_simulated_latency_ms, 4), payload['data_size_bytes'], status])

def main(args=None):
    rclpy.init(args=args)
    node = NetworkSimulatorNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
