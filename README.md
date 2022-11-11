# Test repo for Ros2 Control and Ignition Gazebo (6/Fortress)

Steps:

In one terminal start the simulation with:
```
ros2 launch ignition_ros2_control_test sim.launch.py model:=src/ignition_ros2_control_test/urdf/simple-robot.urdf.xacro
```
In another terminal run

```
ros2 control load_controller joint_trajectory_controller
ros2 control set_controller_state joint_trajectory_controller inactive
ros2 control set_controller_state joint_trajectory_controller active
```

Error: [ign gazebo-1] [ERROR] [1668181548.332225200] [controller_manager]: Can't activate controller 'joint_trajectory_controller': Command interface with 'the_joint/position' does not exist