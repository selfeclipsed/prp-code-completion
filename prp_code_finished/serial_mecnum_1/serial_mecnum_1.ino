/***************************************************
  Motor Test - Confirm the direction of the motor.
             - 确认电机方向
  观察实际运行，通过 .setMotorDirReverse()函数设置电机运行方向。

  YFROBOT ZL
  yfrobot@qq.com
  WWW.YFROBOT.COM
  08/19/2020
 ****************************************************/
char comdata;
#include <MotorDriver_PCA9685.h>

// called this way, it uses the default address 0x40
MotorDriver_PCA9685 motorDriver = MotorDriver_PCA9685();

void setup() {
  Serial.begin(9600);
  motorDriver.begin();
  // motorDriver.setPWMFreq(1600);       // This is the maximum PWM frequency
  // motorDriver.setMotorDirReverse(0);  // 设置所有电机方向, 0-默认,1-反向.
  motorDriver.setMotorDirReverse(0, 1, 0, 1);  // 设置M1,M2,M3,M4电机方向, 0-默认,1-反向.
  motorDriver.setMotor(0, 0, 0, 0);
}

void loop() {
  String cmd = "";
  while (Serial.available() > 0)  //串口接收到数据
  {
    char comdata = char(Serial.read());  //获取串口接收到的数据
    if (comdata >= '0' && comdata <= '9') {
      cmd += comdata;
    }
  }
  Serial.flush();
  if (cmd.length() > 0) {
    int dir = atoi(cmd.c_str());
    if (dir == 0)  //如果上位机发送的为字符，则改为'0'
    {
      motorDriver.setMotor(0, 0, 0, 0);  // 电机M1/M2/M3/M4停止
      //delay(1000);
      Serial.println("Stop");            //向上位机发送信息
    }
    if (dir == 1)  //向前
    {
      motorDriver.setMotor(700,700,700,700);
      Serial.println("Move forward");  //向上位机发送信息
    }
    if (dir == 5)  //向后
    {
      motorDriver.setMotor(-700,-700,-700,-700);
      Serial.println("Move backward");  //向上位机发送信息
    }
    if (dir == 3)  //向左
    {
      motorDriver.setMotor(-700,700,700,-700);
      Serial.println("Move left");  //向上位机发送信息
    }
    if (dir == 7)  //向右
    {
      motorDriver.setMotor(700,-700,-700,700);
      Serial.println("Move right");  //向上位机发送信息
    }
    if (dir == 2)  //left turn
    {
      motorDriver.setMotor(-400, 400, -400, 400);
      Serial.println("left turn");  //向上位机发送信息
    }
    if (dir == 8)  //right turn
    {
      motorDriver.setMotor(400, -400, 400, -400);
      Serial.println("right turn");  //向上位机发送信息
    }
    if (dir == 4)  //左后
    {
      motorDriver.setMotor(-1000, 0, 0, -1000);
      Serial.println("Move left-backward");  //向上位机发送信息
    }
    if (dir == 6)  //右后
    {
      motorDriver.setMotor(0, -1000, -1000, 0);
      Serial.println("Move right-backward");  //向上位机发送信息
    }
    if (dir == 9)  //右转
    {
      motorDriver.setMotor(1000, -1000, 1000, -1000);
      Serial.println("Move right-round");  //向上位机发送信息
    }
    if (dir == 10)  //左转
    {
      motorDriver.setMotor(-1000, 1000, -1000, 1000);
      Serial.println("Move left-round");  //向上位机发送信息
    }
    if (dir == 11)  //右转
    {
      motorDriver.setMotor(500, -500, 500, -500);
      Serial.println("Move right-round");  //向上位机发送信息
    }
    if (dir == 12)  //左转
    {
      motorDriver.setMotor(-500, 500, -500, 500);
      Serial.println("Move left-round");  //向上位机发送信息
    }
  }
}
