# trzeba dodać kalkulacje ruchu Meccanum, polaczenie przez USB (ros_serial, pyserial lub asyncio)

#!/usr/bin/env python3
import rclpy    #ros z pythonem
from rclpy.node import Node
from std_msgs.msg import String
import time

workTime = int(1e9) #ns po jakim czsie bez nowych danych robot zatrzyma sie
updateFreqZatrz = 1.0   #s czestotliwosc odswiezania sprawdzania zatrzymania

class sterowanie(Node):

    curTime = 0
    isStopped = False

    def __init__(self):
        super().__init__("sterownik_node")
        self.create_timer(updateFreqZatrz, self.stop)
        self.subskrypcja = self.create_subscription(String, "kierunek_ruchu", self.ster_fun, 5)

    def ster_fun(self, recived_msg):
        self.isStopped = False
        self.curTime = time.time_ns()

        data = recived_msg.data
        self.get_logger().info(data)

        
    
    def stop(self):
        if self.isStopped == False:
            if self.curTime + workTime < time.time_ns():
                self.get_logger().info("stop")
                self.isStopped = True

    def mecanum(self,x,y,ang)->list:
        return [x,y,ang,0]
    
def main(args=None):
    rclpy.init(args=args)

    node1 = sterowanie()
    rclpy.spin(node1)

    rclpy.shutdown()

if __name__ == "__main__":
    main()