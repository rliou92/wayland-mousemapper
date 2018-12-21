import subprocess
import re

MOUSE_NAME = "Logitech M720 Triathlon"
keys_map = {"BTN_SIDE": "KEY_PAGEDOWN",
              "BTN_EXTRA": "KEY_PAGEUP"}

cmd = ["sudo", "libinput", "list-devices"]
res = subprocess.run(cmd, capture_output=True)
output = res.stdout.decode('UTF-8').rstrip()

mouse_found = False
lines = output.split("\n")
for line_num,line in enumerate(lines):
	if MOUSE_NAME in line:
		mouse_found = True
		break
	# print(line)
if mouse_found == False:
	raise Exception("Mouse not found")

device = re.findall(r'/dev/input/event\d+',lines[line_num+1])[0]

cmd = ["libinput", "debug-events", "--device", device]
process = subprocess.Popen(["sudo", "stdbuf", "-o0"]+cmd, stdout=subprocess.PIPE,encoding='UTF-8')

#  evemu-event /dev/input/${device} --sync --type ${event_type} --code ${key} --value ${value}
def press_key(key):
    pre_cmd = "sudo evemu-event " + device + " --sync --type EV_KEY --code "
    cmd = pre_cmd + "KEY_LEFTMETA --value 1; "
    cmd += pre_cmd + key + " --value 1; "
    cmd += pre_cmd + key + " --value 0; "
    cmd += pre_cmd + "KEY_LEFTMETA --value 0"
#    print(cmd)
    subprocess.run(cmd,shell=True,encoding='UTF-8')
#    print(res)
    
for output in process.stdout:
    button = re.findall(r'BTN_\S+',output)
    if not button:
        continue
    button = button[0]
    if (button in keys_map.keys()) and ("pressed" in output):
        key = keys_map[button]
        press_key(key)
#        print(button+" pressed")
