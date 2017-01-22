#include <Wire.h>   
#include <MPL3115A2.h> 
#include <HTU21D.h>   
#include <TinyGPS++.h>    
#include <SPI.h>
#include <Time.h>
#include <SoftwareSerial.h>

// This code is a modified version of SparkFun Weather Shield 

//Hardware PINs
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
// digital I/O pins
const byte STAT1 = 7;
const byte STAT2 = 8;
const int chipSelect = 10;
static const int RXPin = 5, TXPin = 4;
const byte GPS_PWRCTL = 6; 

int AvgSound = 0;
const int pinMic = 3;



//const byte WSPEED = 3;
//const byte RAIN = 2;

// analog I/O pins
const byte REFERENCE_3V3 = A3;
const byte LIGHT = A1;
const byte BATT = A2;
const byte WDIR = A0;
int GPSBaud = 9600;

//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


//Global Variables
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
float humidity = 0; // [%]
float temp = 0; // (temperature C)
float tempX = 0; // (temperature C +50 for neg int)
float pressure = 0; 
float batt_lvl = 11.8; 
float light_lvl = 455; 
unsigned int noiseLevel = 0;
byte msg;
double co2;


//Instanses 
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
TinyGPSPlus gps;
SoftwareSerial gpsSerial(RXPin, TXPin); 
SoftwareSerial K_30_Serial(12,13); //Sets up a virtual serial port

MPL3115A2 qPressure; //Create an instance of the pressure sensor
HTU21D qHumidity; //Create an instance of the humidity sensor


 //Using pin 12 for Rx and pin 13 for Tx
byte readCO2[] = {0xFE, 0X44, 0X00, 0X08, 0X02, 0X9F, 0X25}; //Command packet to read Co2 (see app note)
byte response[] = {0,0,0,0,0,0,0}; //create an array to store the response
//multiplier for value. default is 1. set to 3 for K-30 3% and 10 for K-33 ICB
int valMultiplier = 1;

void setup()
{
  // Start the Arduino hardware serial port at 9600 baud
  Serial.begin(9600);
  
  gpsSerial.begin(GPSBaud);
   
  //delay (500);
  Serial.flush();
  
  // Start the software serial port at the GPS's default baud
  //gpsSerial.begin(GPSBaud);

  Serial.println(F("QBox - Mobile Weather Station"));
  Serial.println();
  
  pinMode(STAT1, OUTPUT); //Status LED Blue
  pinMode(STAT2, OUTPUT); //Status LED Green
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
  pinMode(REFERENCE_3V3, INPUT);
  pinMode(LIGHT, INPUT);
  
  
  
  // Start the software serial port at the GPS's default baud
  gpsSerial.begin(GPSBaud);

  //Pressure sensor
  qPressure.begin();
  qPressure.setModeBarometer();
  qPressure.setOversampleRate(7);
  qPressure.enableEventFlags();
  
  // K30
   K_30_Serial.begin(9600);
  
  //Humidity sensor
  qHumidity.begin();
  interrupts();
  
  Serial.println("QBox Starting...");
}


void calcWeather() {
  humidity = qHumidity.readHumidity();
  temp = qPressure.readTemp();
  tempX = temp+50;
  pressure = qPressure.readPressure() / 1000;
  light_lvl = get_light_level();
  batt_lvl = get_battery_level();
  sendRequest(readCO2);
  co2 = getValue(response);
  noiseLevel = getNoiseLevel();
 
  // Get CO2 value from sensor
  //co2 = K_30.getCO2('p');
}

// this would be costly 
//int getNoiseLevel(int SAMPLE_PERIOD){
//	unsigned long start = millis();
//	long totalSamples = 0;
//	long count = 0;
//	
//	while (millis() < (start + SAMPLE_PERIOD) && SAMPLE_PERIOD > 0){
//		int noiseLevel = analogRead(pinMic);
//		totalSamples+= noiseLevel;
//		count += 1;
//	}
//	
//	int average = int(totalSamples/count);
//	return average;
//}

int getNoiseLevel(){
      int noiseLevel = analogRead(pinMic);
}

float get_light_level() {
  float operatingVoltage = analogRead(REFERENCE_3V3);
  float lightSensor = analogRead(LIGHT);
  operatingVoltage = 3.3 / operatingVoltage; //The reference voltage is 3.3V
  lightSensor = operatingVoltage * lightSensor;
  return (lightSensor);
}

float get_battery_level() {
  float operatingVoltage = analogRead(REFERENCE_3V3);
  float rawVoltage = analogRead(BATT);
  operatingVoltage = 3.30 / operatingVoltage; //The reference voltage is 3.3V
  rawVoltage = operatingVoltage * rawVoltage; //Convert the 0 to 1023 int to actual voltage on BATT pin
  rawVoltage *= 4.90; //(3.9k+1k)/1k - multiple BATT voltage by the voltage divider to get actual system voltage
  return (rawVoltage);
}

void printDigits(int digits) {
  // utility function for digital clock display: prints preceding colon and leading 0
  //Serial.print(":");
  if (digits < 10)
    Serial.print('0');
  Serial.print(digits);
}




void printMonitor() {

  calcWeather(); //Go calc all the various sensors
  Serial.print("TIME|"); Serial.print(hour()); Serial.print(":"); printDigits(minute()); Serial.print(":"); printDigits(second()); 
  Serial.print("#HUMIDITY|"); Serial.print(humidity, 2);
  Serial.print("#TEMP|"); Serial.print(temp, 2);
  Serial.print("#PRESSURE|"); Serial.print(pressure, 2);
  Serial.print("#VOLTS|"); Serial.print(batt_lvl, 2);
  Serial.print("#LIGHT|"); Serial.print(light_lvl, 2);
  Serial.print("#CO2|"); Serial.print(co2);
  Serial.print("#NOISE|"); Serial.print(noiseLevel);
  Serial.print("#LOCATION|");Serial.print(gps.location.lat(), 6); Serial.print(":"); Serial.print(gps.location.lng(), 6);Serial.print(":"); Serial.print(gps.altitude.meters());Serial.print(":"); Serial.print(gps.satellites.value());
  Serial.print("#DATE|"); Serial.print(gps.date.month()); Serial.print("/");Serial.print(gps.date.day()); Serial.print("/"); Serial.print(gps.date.year()); Serial.print(" "); Serial.print(gps.time.hour()); Serial.print(":");Serial.print(gps.time.minute()); Serial.print(":"); Serial.print(gps.time.second()); Serial.print(":");  Serial.print(gps.time.centisecond()); 
  
  Serial.println("$");
  //delay(100);
}



void sendRequest(byte packet[])
{
 while(!K_30_Serial.available()) //keep sending request until we start to get a response
 {
 K_30_Serial.write(readCO2,7);
 delay(50);
 }

 int timeout=0; //set a timeoute counter
 while(K_30_Serial.available() < 7 ) //Wait to get a 7 byte response
 {
 timeout++;
 if(timeout > 10) //if it takes to long there was probably an error
 {
 while(K_30_Serial.available()) //flush whatever we have
 K_30_Serial.read();

 break; //exit and try again
 }
 delay(50);
 }

 for (int i=0; i < 7; i++)
 {
 response[i] = K_30_Serial.read();
 }
}
unsigned long getValue(byte packet[])
{
 int high = packet[3]; //high byte for value is 4th byte in packet in the packet
 int low = packet[4]; //low byte for value is 5th byte in the packet

 unsigned long val = high*256 + low; //Combine high byte and low byte with this formula to get value
 return val* valMultiplier;
} 

void loop() {
  
 
 
  
  const unsigned long period = 1 * 30 * 1000UL;
  static unsigned long lastSampleTime = 0 - period;  // initialize such that a reading is due the first time through loop()




  unsigned long now = millis();
  if (now - lastSampleTime >= period)
  {
    lastSampleTime += period;
    digitalWrite(STAT1, HIGH); //Blink stat LED
    printMonitor();
    //delay(100);
    digitalWrite(STAT1, LOW); //Turn off stat LED

  }
  
    while (gpsSerial.available() > 0){
      gps.encode(gpsSerial.read());
    }
    
    
    


}
