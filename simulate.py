#!/usr/bin/env python3

import subprocess
import time
import argparse

parser = argparse.ArgumentParser(description='Multiple px4 trajectory simulations')

# Required positional argument

parser.add_argument('file_name', type=str,
                    help='Trajectory file name.csv')

parser.add_argument('traj_length', type=int,
                    help='Trajectory duration in seconds')

takeoff_time = 15
gazebo_startup_time = 10

args = parser.parse_args()

client = gazebo = subprocess.Popen("gnome-terminal -- ./../Micro-XRCE-DDS-Agent/build/MicroXRCEAgent udp4 -p 8888",
                              stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8', shell=True)

for i in range(1,10):
    
    start = subprocess.Popen("docker start px4_ros2",stdout=subprocess.PIPE,universal_newlines=True, shell=True)

    if(i == 1):
        gazebo = subprocess.Popen("gnome-terminal -- docker exec -u 0 -it px4_ros2 bash -c 'cd PX4-Autopilot; HEADLESS=1 make px4_sitl gazebo-classic'",
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8', shell=True)
    else:
        j = i - 1
        gazebo = subprocess.Popen("gnome-terminal -- docker exec -u 0 -it px4_ros2 bash -c 'cd PX4-Autopilot; HEADLESS=1 make px4_sitl gazebo-classic_iris_delta_p"+str(j)+"'",
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8', shell=True)

    time.sleep(gazebo_startup_time)
    traj = subprocess.Popen("gnome-terminal -- docker exec -u 0 -it px4_ros2 bash -c 'cd sensitivity_experiment; source install/setup.bash; ros2 run trajectory_publisher trajectory_publisher --ros-args -p file_name:=\""+args.file_name+".csv\"'",
                            stdout=subprocess.PIPE, stdin=subprocess.PIPE, encoding='utf8', shell=True)

    time.sleep(args.traj_length + takeoff_time + 12)
    stop = subprocess.Popen("docker stop px4_ros2",stdout=subprocess.PIPE,universal_newlines=True, shell=True)
    time.sleep(2)
        

