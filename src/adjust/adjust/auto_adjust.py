import rclpy
from rclpy.node import Node
import xml.etree.ElementTree as ET
# import lxml.etree as ET
from decimal import *
# getcontext().rounding=ROUND_DOWN


class Change(Node):
    def __init__(self):
        super().__init__("Change")

        a = Decimal(input("Translation increment on x: "))  # name ok?
        b = Decimal(input("Translation increment on y: "))
        c = Decimal(input("Translation increment on z: "))
        # rotation in x and y axis must not be considered
        d = Decimal(input("Rotation increment around x: "))
        e = Decimal(input("Rotation increment around y: "))   # radians？
        # clockwise or counterclockwise
        f = Decimal(input("Rotation increment around z: "))
        print(getcontext())
        parameter = [a, b, c, d, e, f]

        # considering modifying the input
        tree = ET.parse(
            '/home/pmlab/pm_ros2_ws/src/match_pm_robot/pm_robot_description/urdf/pm_robot.xacro')
        root = tree.getroot()
        
        # ist die Bauteile 1k,2k？
        # for i in root.iter('joint'):
        #     if i.attrib['name'] == "Gripper_Rot_Plate_Joint":
        #         print(i.find('origin').attrib.get('xyz').split(' '))

        for x in root.findall('joint'):

            if x.attrib['name'] == 'Camera_Top_View_Joint':

                n = x.find('origin').attrib.get('xyz').split(' ')

                f = x.find('origin').attrib.get('rpy').split(' ')

        for i in root.iter('joint'):

            if m == 'Gripper' and i.attrib['name'] == "Gripper_Rot_Plate_Joint":

                # is the received measurement data also 6 decimal places
                i.find('origin').set('xyz', '%s %s %s'  # aus urdf  aufrae 运行asd.py
                                     % (parameter[0] +
                                        Decimal(n[0]),
                                        parameter[1] +
                                        Decimal(n[1]),
                                        parameter[2] +
                                        Decimal('0.096')+Decimal(n[2])
                                        ))
                # is the received 'rpy' in radien or degree
                # clockwise or counterclockwise
                i.find('origin').set('rpy', '%s %s %s' % (parameter[3] +
                                                          Decimal(f[0]),
                                                          parameter[4] +
                                                          Decimal(f[1]),
                                                          parameter[5] +
                                                          Decimal(f[2])
                                                          ))
            # elif m in Name[1:]:
            if m in Name[1:] and i.attrib['name'] == m+"_Joint":
                i.find('origin').set('xyz', '%s %s %s'
                                     % (parameter[0] +
                                        Decimal(n[0]),
                                        parameter[1] +
                                        Decimal(n[1]),
                                        parameter[2] +
                                        Decimal(n[2])
                                        ))

             # 2pi situation?
                i.find('origin').set('rpy', '%s %s %s' % (parameter[3]+Decimal(f[0]),
                                                          parameter[4] +
                                                          Decimal(f[1]),
                                                          parameter[5] +
                                                          Decimal(f[2])
                                                          ))
        tree.write('asd1')

        with open('asd1',
                  # (path)
                  'r+', encoding='utf-8') as file:
            co = file.read()

            file.seek(0, 0)
            file.write('<?xml version="1.0" encoding="utf-8"?>\n'+co)
            # print(co.find('<ro'))

        with open('asd1', 'r+', encoding='utf-8') as file1:
            # (path)
            new = file1.read()
            # print(new.find('<ro'))
            file1.seek(new.find('<ro'))

            file1.write('\n<robot name="pm_robot">')


def main():

    rclpy.init()
    rclpy.spin(Change())
    rclpy.shutdown()


if __name__ == '__main__':
    Name = ['Gripper', '1K_Dispenser', '2K_Dispenser']
    # capital letter or both
    m = input('Please enter the name of the component to be calibrated: ')
    if m in Name:
        main()
    else:
        rclpy.node.get_logger('Error').info('Invalid name. Please enter one of the following names:\n'
                                            'Gripper'+','+'1K_Dispenser'+','+'2K_Dispenser')