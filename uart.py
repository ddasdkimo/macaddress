import serial as ser
import time
# cmd = [0x57, 0xAB, 0x00, 0x04, 0x07, 0x02, 0x00, 0x40, 0x01, 0x15, 0x02, 0x00, 0x67]# 移動測試
# device_info = [0x57, 0xAB, 0x00, 0x01, 0x00, 0x03,]# 讀取基本訊息
cmderrortest = "57AB00010004"
cmd = "57AB0004070200400115020067"# 移動測試
device_info = "57AB00010003"# 讀取基本訊息
def hard_moveTo(x, y):
    global se
    nx = int(x * 4096 / 1920)
    ny = int(y * 4096 / 1080)

    # 鼠标绝对坐标命令
    cmd = [0x57, 0xAB, 0x00, 0x04, 0x07, 0x02]
    button_val = 0
    low_x = nx & 0xFF
    high_x = (nx >> 8) & 0xFF
    low_y = ny & 0xFF
    high_y = (ny >> 8) & 0xFF
    scroll = 0x00
    data = [button_val, low_x, high_x, low_y, high_y, scroll]
    sum_val = (sum(cmd) + sum(data)) & 0xFF
    data.append(sum_val)

    cmd_move = cmd + data
    se.write(bytes(cmd_move))
    se.flushInput()

    return True
debugx = 0
debugy = 0
def sendCmd(cmdline):
    for cmd in cmdline:
        se.write(b'hello')
        se.write(chr(cmd).encode("utf-8"))    
se = ser.Serial("/dev/ttyTHS1",9600,timeout=1)
if se.is_open:
    while(True):
        hard_moveTo(debugx,debugy)
        debugx += 1
        debugy += 1
        if debugx >= 1024:
            debugx = 0
            debugy = 0

        # data = se.readline()
        # if data != b'':
        #     print(data)
        #     sendCmd(bytes.fromhex(device_info))
        # sendCmd(bytes.fromhex(device_info))
        # data = se.read()
        # if data != b'':
        #     print(data)
        # sendCmd(bytes.fromhex(device_info))
        # data = se.read()
        # if data != b'':
        #     print(data)
        # sendCmd(bytes.fromhex(cmd))
        # data = se.read()
        # if data != b'':
        #     print(data)
        # time.sleep(1)
se.close()



