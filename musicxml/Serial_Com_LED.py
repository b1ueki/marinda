#coding:utf-8

#シリアル通信で文字をArduino側に送信
#aが押されたら通信を中止するプログラム

import serial

def main():
    with serial.Serial('/dev/cu.usbmodem14541', 9600, timeout = 1) as ser:
        while True:
            flag = bytes(input(), 'utf-8')
            ser.write(flag)
            if(flag == bytes('a', 'utf-8')):
                break;
        ser.close()

if __name__ == "__main__":
    main()
