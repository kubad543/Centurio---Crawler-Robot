/*
 * https://www.hessmer.org/blog/2013/12/28/ibt-2-h-bridge-with-arduino/
IBT-2 Motor Control Board driven by Arduino.
 
Speed and direction controlled by a potentiometer attached to analog input 0.
One side pin of the potentiometer (either one) to ground; the other side pin to +5V
 
Connection to the IBT-2 board:
IBT-2 pin 1 (RPWM) to Arduino pin 5(PWM)
IBT-2 pin 2 (LPWM) to Arduino pin 6(PWM)
IBT-2 pins 3 (R_EN), 4 (L_EN), 7 (VCC) to Arduino 5V pin
IBT-2 pin 8 (GND) to Arduino GND
IBT-2 pins 5 (R_IS) and 6 (L_IS) not connected
*/
 
int SENSOR_PIN1 = 0; // center pin of the potentiometer
 
int RPWM_Output1 = 5; // Arduino PWM output pin 5; connect to IBT-2 pin 1 (RPWM)
int LPWM_Output1 = 6; // Arduino PWM output pin 6; connect to IBT-2 pin 2 (LPWM)
int dioda = 1;

void setup()
{
  pinMode(RPWM_Output1, OUTPUT);
  pinMode(LPWM_Output1, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  
}
 
void loop()
{
  digitalWrite(12, 1);
  digitalWrite(13,dioda);
  delay(1000);

  if(dioda ==1) dioda =0;
  else dioda =1;
  


  int sensorValue1 = analogRead(SENSOR_PIN1);
 
  // sensor value is in the range 0 to 1023
  // the lower half of it we use for reverse rotation; the upper half for forward rotation
  digitalWrite(13,0);

  if (sensorValue1 < 512)
  {
    // reverse rotation
    int reversePWM1 = -(sensorValue1 - 511) / 2;
    analogWrite(LPWM_Output1, 0);
    analogWrite(RPWM_Output1, reversePWM1);
  }
  else
  {
    // forward rotation
    int forwardPWM1 = (sensorValue1 - 512) / 2;
    analogWrite(RPWM_Output1, 0);
    analogWrite(LPWM_Output1, forwardPWM1);
  }}

