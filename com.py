import serial

ser = serial.Serial('/dev/rfcomm0', baudrate=9600)
print("press q to quit the program")
while True:
    cmd = input("Enter command: ")
    if cmd == 'q':
        break
    print("command sent")
    ser.write(cmd.encode('utf-8'))