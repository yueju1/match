from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    mode =input('Please select the operating mode: \n1: Calibration of the realistic equipment\n2: Calibration in simulation\n')

    Para_real = ('/pm_robot_xyz_axis_controller/state',
                 '/pm_robot_xyz_axis_controller/follow_joint_trajectory',
                 '/Camera_Bottom_View/pylon_ros2_camera_node/image_raw',
                 [-0.359, -0.0458, 0.03, -1200000.0],
                 [-0.359, -0.0458, 0.03, 600000.0],
                 [600000.0])
    
    Para_sim = ('/joint_trajectory_controller/state',
                '/joint_trajectory_controller/follow_joint_trajectory',
                '/Cam2/image_raw',
                [-0.359, -0.0458, -0.051544, 0.0],
                [-0.359, -0.0458, -0.051544, 6.2],
                [6.2])
  
    if mode == '1':
        Parameter = Para_real
        
    if mode == '2':
        Parameter = Para_sim
    
    ld = LaunchDescription()
    
    auto_centering_node = Node(
        package="open_cv", 
        executable="text",
        parameters=[{'1':Parameter[0]},
                    {'2':Parameter[1]},
                    {'4':Parameter[3]},
                    {'6':Parameter[5]}
                    ]
    )
    
    image_processing_node = Node(
        package="open_cv",
        executable="image_processing"
    )
    
    ld.add_action(auto_centering_node)
    ld.add_action(image_processing_node)
    
    
    return ld