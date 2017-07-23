#coding:utf-8

#シリアル通信でデータをArduino側に送信

import serial
import time

def main():
    with serial.Serial('/dev/cu.usbmodem92', 9600, timeout = 1) as ser:
        f = open('lg-203466147999847691/main.txt', 'r')
        data = f.read()
        f.close()
        str = data.split(' ')
        counter = 0;
        for i in str:
            if counter % 3 == 0:
                time.sleep(0.25)
            counter += 1
            ser.write(i)
            print i

if __name__ == "__main__":
    main()
