# Project Altair Phase 3

## Task 3: Three Stops Before Cha

### Requirements
- ROS 2 Jazzy
- Turtlesim
- Python 3

### Build
```bash
cd ~/altair-phase3/altair_phase3_ws
colcon build --packages-select altair_phase3
source install/setup.bash
```

### Launch the mission
```bash
ros2 launch altair_phase3 field.launch.py
```

The launch file starts Turtlesim and the mission node. The turtle visits these waypoints in order:
1. Bottle: (8.0, 5.5)
2. Mallet: (8.0, 8.0)
3. Base: (5.5, 5.5)

After reaching Base, the mission stops and reports `DONE`.

### Obstacle pause and resume test

Open a second terminal and source the workspace:
```bash
source ~/altair-phase3/altair_phase3_ws/install/setup.bash
```

Simulate an obstacle:
```bash
ros2 topic pub --once /field_blocked std_msgs/msg/Bool "{data: true}"
```

Try to resume while blocked. The request should be rejected:
```bash
ros2 service call /resume_mission std_srvs/srv/Trigger "{}"
```

Clear the obstacle:
```bash
ros2 topic pub --once /field_blocked std_msgs/msg/Bool "{data: false}"
```

The turtle remains paused until the resume service is called again:
```bash
ros2 service call /resume_mission std_srvs/srv/Trigger "{}"
```

A successful response confirms that the mission resumed toward the next unfinished waypoint.

### Interfaces
- Pose input: `/turtle1/pose` (`turtlesim/msg/Pose`)
- Velocity output: `/turtle1/cmd_vel` (`geometry_msgs/msg/Twist`)
- Obstacle input: `/field_blocked` (`std_msgs/msg/Bool`)
- Resume service: `/resume_mission` (`std_srvs/srv/Trigger`)

Close keyboard teleoperation and other velocity publishers before running this mission so the mission node is the sole publisher to `/turtle1/cmd_vel`.
