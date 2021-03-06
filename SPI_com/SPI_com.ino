
#include <SPI.h>

//When Using the SPI library, you only have to worry
//about picking your slave select
//By Default, 11 = MOSI, 12 = MISO, 13 = CLK
int SSpin = 7;   //SPI Slave Select
int RESET = 5;
int datach1 = 0;
int datach2 = 0;
int datach3 = 0;
int datach4 = 0;
int datach5 = 0;
int datach6 = 0;
int datach7 = 0;
int datach8 = 0;

int dataout1 = 0;
int dataout2 = 0;
int dataout3 = 0;
int dataout4 = 0;
int dataout5 = 0;
int dataout6 = 0;
int dataout7 = 0;
int dataout8 = 0;


int data1 = 0;
int data2 = 0;
int data3 = 0;
int dataout = 0;

void setup()
{
  pinMode (9, OUTPUT); 
  pinMode (19, OUTPUT); 
  pinMode (6, OUTPUT); 
  digitalWrite(19,HIGH);
  digitalWrite(6,HIGH);
  // set up Timer 1
  TCCR1A = bit (COM1A0);  // toggle OC1A on Compare Match
  TCCR1B = bit (WGM12) | bit (CS10);   // CTC, no prescaling
  OCR1A =  0;       // output every cycle
  //Set Pin Direction
  //Again, the other SPI pins are configured automatically
  pinMode(SSpin, OUTPUT);
  pinMode(RESET, OUTPUT);
  
  Serial.begin(115200);
  
  //Initialize SPI
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  SPI.setDataMode(SPI_MODE1);
  SPI.setBitOrder(MSBFIRST);
  digitalWrite(SSpin, HIGH);
  digitalWrite(RESET, LOW);
  delay(10);
  digitalWrite(RESET, HIGH);
}

//This will set 1 LED to the specififed level
void setLed(int reg, int level)
{
  digitalWrite(SSpin, LOW);
  SPI.transfer(reg);
  SPI.transfer(level);
  digitalWrite(SSpin, HIGH);
}

void loop()
{
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000100);
  data2 = SPI.transfer(0b10000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach1 = (data3) + ((data2 & 0b00001111) << 8) ;

  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000101);
  data2 = SPI.transfer(0b00000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach2 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000101);
  data2 = SPI.transfer(0b10000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach3 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000110);
  data2 = SPI.transfer(0b00000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach4 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000110);
  data2 = SPI.transfer(0b10000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach5 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000111);
  data2 = SPI.transfer(0b00000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach6 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000111);
  data2 = SPI.transfer(0b10000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach7 = (data3) + ((data2 & 0b00001111) << 8) ;
  
  digitalWrite(SSpin, LOW);
  data1 = SPI.transfer(0b00000100);
  data2 = SPI.transfer(0b00000000);
  data3 = SPI.transfer(0b00000000);
  digitalWrite(SSpin, HIGH);
  datach8 = (data3) + ((data2 & 0b00001111) << 8) ;
//  Serial.print(data1,BIN); 
//  Serial.print(" ");

//  dataout1 = dataout1*0.99 + datach1 *0.01;
//  dataout2 = dataout2*0.99 + datach2 *0.01;
//  dataout3 = dataout3*0.99 + datach3 *0.01;
//  dataout4 = dataout4*0.99 + datach4 *0.01;
//  dataout5 = dataout5*0.99 + datach5 *0.01;
//  dataout6 = dataout6*0.99 + datach6 *0.01;
//  dataout7 = dataout7*0.99 + datach7 *0.01;
//  dataout8 = dataout8*0.99 + datach8 *0.01;


  dataout1 = datach1;
  dataout2 = datach2;
  dataout3 = datach3;
  dataout4 = datach4;
  dataout5 = datach5;
  dataout6 = datach6;
  dataout7 = datach7;
  dataout8 = datach8;
  
  
  Serial.print(dataout1);
  Serial.print(" ");
  Serial.print(dataout2);
  Serial.print(" ");
  Serial.print(dataout3);
  Serial.print(" ");
  Serial.print(dataout4);
  Serial.print(" ");  
  Serial.print(dataout5);
  Serial.print(" ");
  Serial.print(dataout6);
  Serial.print(" ");
  Serial.print(dataout7);
  Serial.print(" ");
  Serial.print(dataout8);
  Serial.println(" ");
}
