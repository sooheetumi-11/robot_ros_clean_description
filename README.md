# ROS 2 Mecanum Robot & 2-DOF Arm Simulation

Dự án mô phỏng hệ thống robot di động (Mecanum) tích hợp cánh tay máy 2 bậc tự do (Tịnh tiến - Quay) trong môi trường ROS 2 Humble và Gazebo. 

## 1. Giới thiệu
Package `robot_ros_clean_description` cung cấp toàn bộ thiết kế hệ thống (URDF/Xacro), bản vẽ 3D (Mesh), bộ điều khiển động cơ (ROS 2 Control) và giao diện hiển thị cảm biến (RViz2) cho robot.

* **Khung gầm:** Hệ truyền động 4 bánh Mecanum (nhận lệnh Twist).
* **Tay máy:** 1 khớp tịnh tiến (Slider) và 1 khớp quay (Revolute).
* **Cảm biến tích hợp:** LiDAR (LaserScan) và Camera (Image).

---

##  2. Yêu cầu hệ thống (Requirements)

Để hệ thống chạy mượt mà, máy tính cần cài đặt các môi trường và thư viện sau:

* **OS:** Ubuntu 22.04
* **ROS Version:** ROS 2 Humble
* **Simulator:** Gazebo 11

**Các thư viện ROS 2 cần cài đặt thêm:**
Vui lòng mở Terminal và chạy lệnh sau để cài đặt các thư viện phụ thuộc:
```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros2-control \
                 ros-humble-ros2-controllers \
                 ros-humble-joint-trajectory-controller \
                 ros-humble-teleop-twist-keyboard
```

---

## 3. Hướng dẫn Build & Khởi chạy (Launch)

**Bước 1: Clone package về workspace**
```bash
cd ~/robot_ws/src
git clone [https://github.com/sooheetumi-11/robot_ros_clean_description.git](https://github.com/sooheetumi-11/robot_ros_clean_description.git)
```

**Bước 2: Build hệ thống**
```bash
cd ~/robot_ws
colcon build --packages-select robot_ros_clean_description
source install/setup.bash
```

**Bước 3: Khởi chạy File Launch Tổng Hợp**
Lệnh dưới đây sẽ khởi động cùng lúc: Trạng thái robot, môi trường Gazebo, giao diện RViz (đã load sẵn config cảm biến) và kích hoạt các bộ điều khiển Controller.
```bash
ros2 launch robot_ros_clean_description full_simulation.launch.py
```

---

## 4. Hướng dẫn Điều khiển (Teleop)

Sau khi hệ thống mô phỏng đã load xong, hãy mở các Terminal MỚI (nhớ chạy `source ~/robot_ws/install/setup.bash`) để điều khiển robot:

### A. Điều khiển khung gầm xe di chuyển
Sử dụng package mặc định của ROS 2 để điều khiển đa hướng (tiến, lùi, dịch ngang, xoay tròn):
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```
*(Sử dụng các phím `I`, `J`, `K`, `L`, `,`, `U`, `O`, `M` để lái xe).*

### B. Điều khiển tay máy 2 bậc tự do
Chạy Node Python tự viết để publish lệnh tới `/arm_controller`:
```bash
ros2 run robot_ros_clean_description arm_teleop.py
```
**Phím điều khiển tay máy:**
* `W` / `S` : Nâng / Hạ khớp tịnh tiến (Slider)
* `A` / `D` : Xoay trái / Xoay phải khớp quay (Revolute)
* `Space` : Đưa tay máy về vị trí gốc (Reset)
* `Ctrl + C` : Thoát

---

## 5. Cấu trúc thư mục (Project Structure)
* `urdf/`: Chứa file `robot_ros_clean.xacro` (khung xương robot) và `robot_ros_clean.gazebo` (thiết lập sensor, plugin vật lý).
* `meshes/`: Chứa các bản vẽ 3D (.STL, .DAE) của robot.
* `launch/`: Chứa file `full_simulation.launch.py`.
* `config/`: Chứa file `controllers.yaml` thiết lập phần cứng cho ros2_control.
* `rviz/`: Chứa file `urdf.rviz` lưu cấu hình hiển thị cảm biến (Model, LiDAR, Camera).
* `scripts/`: Chứa file `arm_teleop.py` (Node điều khiển tay máy).
