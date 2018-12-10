#include <ArduinoJson.h>

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>
#include <vector>

#include "Gaussian.h"

ESP8266WiFiMulti WiFiMulti;

// Sensor grid generators
constexpr double 
  mean_weight = 5.0,
  sd_weight = .1;
  
Gaussian sensor_11(mean_weight, sd_weight);
Gaussian sensor_12(mean_weight, sd_weight);
Gaussian sensor_21(mean_weight, sd_weight); 
Gaussian sensor_22(mean_weight, sd_weight); 
Gaussian sensor_31(mean_weight, sd_weight); 
Gaussian sensor_32(mean_weight, sd_weight); 


std::vector<double> collect_readings() {
  return {
    sensor_11.random(),
    sensor_12.random(),
    sensor_21.random(),
    sensor_22.random(),
    sensor_31.random(),
    sensor_32.random()
  };
}

String result_to_json(std::vector<double> values) {
  StaticJsonBuffer<250> jsonBuffer;

  JsonObject& root = jsonBuffer.createObject();
  root["value_11"] = values[0];
  root["value_12"] = values[1];
  root["value_21"] = values[2];
  root["value_22"] = values[3];
  root["value_31"] = values[4];
  root["value_32"] = values[5];

  String json;
  root.printTo(json);

  return  json;
}

void post_result(String json) {
  HTTPClient http;

  Serial.print("[HTTP] begin...\n");
  http.begin("http://rkatopodis.pythonanywhere.com/report"); //HTTP
  http.addHeader("Content-Type", "application/json");
  Serial.print("[HTTP] POST...\n");
  
  // start connection and send HTTP header
  int httpCode = http.POST(json);

  // httpCode will be negative on error
  if (httpCode > 0) {
    // HTTP header has been send and Server response header has been handled
    Serial.printf("[HTTP] POST... code: %d\n", httpCode);

    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println(payload);
    }
  } else {
    Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

void setup() {

  Serial.begin(115200);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("katopodis", "katopodis123");

}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    // Collecting sensor data
    auto readings = collect_readings();

    // Creating json string
    auto json = result_to_json(readings);

    // Reporting result
    post_result(json);
  }

  delay(5000);
}

