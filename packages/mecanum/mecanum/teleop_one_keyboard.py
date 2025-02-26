# bierze z konsoli pojedynczy znak 

#!/usr/bin/env python3
import rclpy    #ros z pythonem
from rclpy.node import Node
from std_msgs.msg import String



import tty,sys,select,termios
settings = termios.tcgetattr(sys.stdin)

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

class sterowanie(Node):
    to_publish = ""

    def __init__(self):
        super().__init__("odczyt_z_klawiatury_node")
        self.direction = self.create_publisher(String, "kierunek_ruchu", 5)
        self.timer = self.create_timer(0.0, self.pub)

    def pub(self):
        msg = String()
        msg.data = getKey()
        if msg.data == '`': # zakonczenie teleop
            rclpy.shutdown()
        self.direction.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)

    node1 = sterowanie()
    rclpy.spin(node1)

    rclpy.shutdown()






if __name__ == "__main__":
    main()