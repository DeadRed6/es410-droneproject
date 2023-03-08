# ES410 Autonomous Drone Design and Control software repo

This repo contains scripts and code that was written for the [ES410 Group Project](https://warwick.ac.uk/services/aro/dar/quality/modules/undergraduate/es/es410/) at the [University of Warwick's School of Engineering](https://warwick.ac.uk/fac/sci/eng/).

## Modified projects

Some code contained within this repo has been downloaded and adapted from other external code repositories, contained within subfolders in this repo. Please see the README and LICENSE files, where applicable, within these subfolders for more details.

## General pre-requisites

Python version `3.9`, along with the `pip` package manager is required. The code in the top level can be run in order to simulate a drone, operate it on a test flight, and view telemetry in the Mission Planner Ground Control Station. Recommended install is in Windows Subsystem for Linux.

`sudo pip install mavproxy==1.7.1 dronekit-sitl pymavlink==2.4.8`

### Usage

In three separate windows:

- `dronekit-sitl copter --home=52.3741770,-1.5648406,0,0` (The co-ordinates are set to a Cryfield Sports Pitch)

- `mavproxy.py --master tcp:127.0.0.1:5760 --sitl 127.0.0.1:5501 --out 127.0.0.1:14550 --out 127.0.0.1:14551` (This redirects SITL output to multiple listeners)

- `python3 simple_goto.py --connect 127.0.0.1:14550`

With Mission Planner open, connect to the vehicle with:

| Parameter | Value |
| --- | --- |
| Protocol | TCP |
| Baud rate | 115200 |
| IP address | 127.0.0.1 |
| Port number | 5763 |

### Scripts

- `simple_goto.py` : Execute a flight path going between waypoints defined in a `.waypoints` file
- `simple_hover.py` : Ascend to an altitude of 1 metre before landing again
- `run_diagnose.py` : Print out flight controller information and status
- `helpers.py` : Library of auxiliary functions to support the codebase

## Folder overview

| Script name | Description |
| --- | --- |
| [camera_software](#camera_software) | Handles the capture of images with the thermal camera |
| [legacy](#legacy) | Unused code |
| [stitching_poc](#stitching_poc) | Proof of concepts of image stitching |

## camera_software

[:open_file_folder: View folder](https://github.com/DeadRed6/es410-droneproject/tree/master/camera_software)

[:arrow_up: Back to folder overview](#folder-overview)

This folder contains python files from [GroupGets' GitHub repo](https://github.com/groupgets/purethermal1-uvc-capture/tree/master) detailing how to interact with the PureThermal 3 I/O module.


### Scripts/Usage

For details on scripts/usage in this folder, please see the [GroupGets' GitHub repo ReadMe](https://github.com/groupgets/purethermal1-uvc-capture/blob/master/readme.md). These files have been edited for use in a graphical user interface [in the DronePi GUI repo](https://github.com/sftgunner/dronepi-gui). Please refer to this repo for how these files were utilised in the scope of this project.


## stitching_poc

[:open_file_folder: View folder](https://github.com/DeadRed6/es410-droneproject/tree/master/stitching_poc)

[:arrow_up: Back to folder overview](#folder-overview)

Various approaches to image stitching with various combinations of libraries, feature tagging algorithms, and stitching algorithms

### Scripts

- `Image_Stitchingv1.py` Using image stitcher function from OpenCV to stitch images.
- `ORB_stitching_bf.py`  Using the ORB algorithm with a brute force matcher to stitch images.
- `ORB_stitching_FLANN.py` Using the ORB algorithm with FLANN to stitch images (used as final project output).
- `SIFT_stitching_FLANN.py` Using the SIFT algorithm with FLANN to stitch images.


## legacy

[:open_file_folder: View folder](https://github.com/DeadRed6/es410-droneproject/tree/master/legacy)

[:arrow_up: Back to folder overview](#folder-overview)

A folder containing code that was thought useful, but for various reasons did not end up being part of the project.
- `parsing_waypoints.py` : a first pass at reading in a .waypoints file, work has been adapted and merged into helpers.py
- `pathing_algorithms.py` : code to find the shortest path between a set of GPS co-ordinates using the A* search algorithm. This was not used, since functionality already existed in Mission Planner to plot routes automatically. 
