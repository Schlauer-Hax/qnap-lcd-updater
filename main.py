import subprocess
from qnapdisplay import QnapDisplay
import time
import socket

display = QnapDisplay()

count = 0
show = 0

if display.Init:
    while True:
        if show == 0:
            display.Write(0, "Uptime:")
            display.Write(1, time.strftime('%H:%M:%S', time.gmtime(time.monotonic())))
        if show == 1:
            display.Write(0, "Hostname:")
            display.Write(1, socket.gethostname())
        if show == 2:
            # mdadm --detail /dev/md0 | grep "Resync Status :"
            result = subprocess.run(['mdadm', '--detail', '/dev/md0'], stdout=subprocess.PIPE)
            result = result.stdout.decode('utf-8').split('\n')
            for line in result:
                if "Resync Status :" in line:
                    display.Write(0, "RAID:")
                    display.Write(1, line.split(':')[1].strip())
                    break

        count += 1
        if count == 10:
            show += 1
            count = 0
        if show == 3:
            show = 0
        time.sleep(1)