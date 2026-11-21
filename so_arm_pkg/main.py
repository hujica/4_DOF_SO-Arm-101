#!/usr/bin/env python3
import sys
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from so_arm_pkg.controller.arm_controller import ArmController
from so_arm_pkg.ROS.ros_runtime import RosRuntime
from so_arm_pkg.gui.main_gui import SOArm101GUI

SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 1000000


def main():
    ros = RosRuntime()
    controller = ArmController(port=SERIAL_PORT, baudrate=BAUDRATE)
    controller.initialize_arm()                  # falls back to SIMULATION if no servos

    root = tk.Tk()
    app = SOArm101GUI(root, controller, ros.node)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.on_close()
    finally:
        for step in (controller.shutdown, ros.shutdown):    # zero commands + close port, stop ROS
            try:
                step()
            except Exception:
                pass


if __name__ == "__main__":
    main()
