cmake_minimum_required(VERSION 3.5)
project(ignition_ros2_control_test)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch urdf rviz config
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
