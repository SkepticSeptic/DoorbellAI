#README

(skip to line [DONT FORGET TO ENTER LINE] for installation instructions)

Welcome to DoorbellAI!

This is a little script that utilizes AI onboard a Jetson Nano in order to detect people using a camera & send you an email aert about it!

Keep in mind all the code is open source & feel free to modify it in any way




Starter guide:

For this you will need:
An Nvidia Jetson Nano

A CSI Camera for it

An active internet connection for your nano, preferrably through Ethernet

A USB C cable for the nano

& Finally a storage card for the nano






Instructions: 

Configure your nano for AI here:
https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md

From then on out, run:

sudo apt-get update && apt upgrade

Then download the script through the terminal by running:

git clone https://github.com/SkepticSeptic/DoorbellAI.git

From then on, simply cd to the directory:

cd DoorbellAI

& run the script:

python3 doorbellai.py
