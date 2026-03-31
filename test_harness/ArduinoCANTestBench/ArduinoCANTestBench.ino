/* This code is heavily based off of the SEEED Studio library send_random.ino example.

* It sends mapped analog data captured from a potentiometer and a joystick to simulate
* actual data captured from UCR's Highlander Racing FSAE team's VCU.
* This data is then captured by a dashboard programming running from an STM32F7 discovery board.
*
* Author: Justin Im
*/

#include <SPI.h>

#define CAN_2515

// For Arduino MCP2515 Hat:
// the cs pin of the version after v1.1 is default to D9
// v0.9b and v1.0 is default D10
const int SPI_CS_PIN = 9;
const int CAN_INT_PIN = 2;

#ifdef CAN_2515
#include "mcp2515_can.h"
mcp2515_can CAN(SPI_CS_PIN); // Set CS pin
#define MAX_DATA_SIZE 6
#endif

void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    while (!SERIAL_PORT_MONITOR) {}

    while (CAN_OK != CAN.begin(CAN_500KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN init ok!");
}

uint32_t id = 0x61;
uint8_t  type; // bit0: ext, bit1: rtr
unsigned len = 6;
byte cdata[MAX_DATA_SIZE] = {};

void loop() {
    // Sends a message of id, standard 11 bit identifier format, data length 6, and data array "cdata" 
    cdata[0] = random(250);
    cdata[1] = random(250);
    cdata[2] = random(250);
    cdata[3] = random(250);
    cdata[4] = random(250);
    cdata[5] = random(250);
    CAN.sendMsgBuf(id, 0, len, cdata);
    SERIAL_PORT_MONITOR.println(cdata[0]);

    unsigned d = random(30);
    delay(d);
}