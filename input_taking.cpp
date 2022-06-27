
// This #include statement was automatically added by the Particle IDE.
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"



#define REPORTING_PERIOD_MS 3000

PulseOximeter percent;

uint32_t tsLastReport = 0;


void setup() 
{
  Wire.begin();

  
} 

void loop() 
{
    percent.update();
    
    
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) 
    {
        int temperat = random(34,40);
        String tempe = String(temperat);
        
        Particle.publish("oxygen",String(percent.getSpO2()),PRIVATE );
        Particle.publish("tempe",tempe,PRIVATE );
        tsLastReport = millis();
        if (( temperat > 42 ) and ( percent.getSpO2() < 60 ))
        {
            Particle.publish("danger","High temperature",PRIVATE );
        }
    }
}
