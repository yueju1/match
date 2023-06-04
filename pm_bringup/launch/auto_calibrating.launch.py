from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    
    ld = LaunchDescription()
    
    auto_centering_node = Node(
        package="open_cv", 
        executable="auto_centering"
    )
    
    image_processing_node = Node(
        package="open_cv",
        executable="image_processing"
    )
    
    ld.add_action(auto_centering_node)
    ld.add_action(image_processing_node)
    
    
    return ld