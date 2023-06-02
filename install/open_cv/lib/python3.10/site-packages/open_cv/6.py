import cv2
import sys
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge



class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        self.subscription = self.create_subscription(
            Image,
            '/Cam2/image_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.br = CvBridge()

opencv特定点的追踪
        https://github.com/makelove/OpenCV-Python-Tutorial/blob/master/my02-%E8%A7%86%E9%A2%91-%E5%AF%B9%E8%B1%A1%E8%B7%9F%E8%B8%AA/tracker.py
        https://www.cnblogs.com/annie22wang/p/9366610.html
        https://www.cvmart.net/community/detail/5856
        https://zhuanlan.zhihu.com/p/479341525
        https://www.google.com/search?channel=fs&client=ubuntu-sn&q=ros+opencv+%E7%89%B9%E5%AE%9A%E7%82%B9%E8%BF%BD%E8%B8%AA
        https://www.guyuehome.com/23381/notice.html
        https://www.guyuehome.com/34967
        opencv point tracking
        https://stackoverflow.com/questions/62079484/opencv-tracking-points-in-an-image
        https://stackoverflow.com/questions/14689090/tracking-user-defined-points-with-opencv



    def listener_callback(self,msg):
        im = self.br.imgmsg_to_cv2(msg)
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼
        tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
        tracker_type = tracker_types[2]
    
        if int(minor_ver) < 3:
            tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
            if tracker_type == 'MOSSE':
                tracker = cv2.TrackerMOSSE_create()
    
        # Read video
        video = cv2.VideoCapture(im)
    
        # Exit if video not opened.
        if not video.isOpened():
            print ("Could not open video")
            sys.exit()
    
        # Read first frame.
        ok, frame = video.read()
        if not ok:
            print ('Cannot read video file')
            sys.exit()
        
        # Define an initial bounding box
        bbox = (287, 23, 86, 320)
    
        # Uncomment the line below to select a different bounding box
        bbox = cv2.selectROI(frame, False)
    
        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)
    
        while True:
            # Read a new frame
            ok, frame = video.read()
            if not ok:
                break
            
            # Start timer
            timer = cv2.getTickCount()
    
            # Update tracker
            ok, bbox = tracker.update(frame)
    
            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    
            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            else :
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    
            # Display tracker type on frame
            cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        
            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
    
            # Display result
            cv2.imshow("Tracking", frame)
    
            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27 : break


def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    #image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
