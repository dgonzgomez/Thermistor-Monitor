/* This code is heavily based off of the SEEED Studio library send_random.ino example.
*
* It sends multiple CAN frames that match the IDs in test_harness/test.dbc.
* Each frame contains 6 temperature values (one byte each).
*
* Author: Justin Im, Emad Saadat, and Diego Gonzalez Gomez
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

const uint32_t TEMP_IDS[] = {49, 50, 65, 66, 81, 82, 97, 98};
const size_t TEMP_ID_COUNT = sizeof(TEMP_IDS) / sizeof(TEMP_IDS[0]);

void setup() {
    SERIAL_PORT_MONITOR.begin(115200);
    while (!SERIAL_PORT_MONITOR) {}

    while (CAN_OK != CAN.begin(CAN_500KBPS)) {             // init can bus : baudrate = 500k
        SERIAL_PORT_MONITOR.println("CAN init fail, retry...");
        delay(100);
    }
    SERIAL_PORT_MONITOR.println("CAN init ok!");
}

uint8_t type; // bit0: ext, bit1: rtr
unsigned len = MAX_DATA_SIZE;
byte cdata[MAX_DATA_SIZE] = {};

void sendTemps(uint32_t id) {
    // Populate 6 temperature bytes
    for (int i = 0; i < MAX_DATA_SIZE; i++) {
        cdata[i] = random(20, 90); // 20-89 degC
    }

    CAN.sendMsgBuf(id, 0, len, cdata);
    SERIAL_PORT_MONITOR.print("ID ");
    SERIAL_PORT_MONITOR.print(id, HEX);
    SERIAL_PORT_MONITOR.print(" -> ");
    SERIAL_PORT_MONITOR.println(cdata[0]);
}

void loop() {
    for (size_t i = 0; i < TEMP_ID_COUNT; i++) {
        sendTemps(TEMP_IDS[i]);
        delay(5);
    }

    unsigned d = random(30);
    delay(d);
}
