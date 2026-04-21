import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys, select, termios, tty

msg = """
Điều khiển tay máy:
---------------------------
Khớp tịnh tiến (Slider): W (Lên) / S (Xuống)
Khớp quay (Revolute):  A (Trái) / D (Phải)
Space : Reset về 0
CTRL-C để thoát
"""

class ArmTeleop(Node):
    def __init__(self):
        super().__init__('arm_teleop')
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.slider_pos = 0.0
        self.rev_pos = 0.0

    def send_cmd(self):
        traj = JointTrajectory()
        traj.joint_names = ['slider_joint', 'revolute_arm']
        point = JointTrajectoryPoint()
        point.positions = [self.slider_pos, self.rev_pos]
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = 500000000 # 0.5s cho mượt
        traj.points.append(point)
        self.publisher_.publish(traj)

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0.1)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = ArmTeleop()
    print(msg)
    try:
        while True:
            key = getKey(settings)
            if key == 'w': node.slider_pos = min(0.0, node.slider_pos + 0.01)
            elif key == 's': node.slider_pos = max(-0.07, node.slider_pos - 0.01)
            elif key == 'a': node.rev_pos += 0.1
            elif key == 'd': node.rev_pos -= 0.1
            elif key == ' ': node.slider_pos, node.rev_pos = 0.0, 0.0
            elif key == '\x03': break
            node.send_cmd()
    finally:
        rclpy.shutdown()