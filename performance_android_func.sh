#!/bin/bash

if [ -z "$1" ]; then
  echo "Please input func_type (0-funcA, 1-funcB)."
  exit 1
fi
if [ -z "$2" ]; then
  echo "Please input output_filename."
  exit 1
fi

ANDROID_DEVICE="xxxxx"
PACKAGE_NAME="xx.xx.xx"
ACTIVITY="xx.xx.xx.xxActivity"
FILE_ON_SDCARD="/sdcard/status"
FILE_LOCAL="status"
OUTPUT_FILE=$2

# Initialize metric counters
CPU_TOTAL=0
PSS_TOTAL=0
POWER_TOTAL=0
TRAFFIC_TOTAL=0
SAMPLE_COUNT=0

check_last_line() {
  expected_line=$1
  adb -s $ANDROID_DEVICE pull $FILE_ON_SDCARD .
  if [ ! -f "$FILE_LOCAL" ]; then
    echo "File not found: $FILE_LOCAL"
    return 1
  fi

  last_line=$(tail -n 1 "$FILE_LOCAL")
  if [ "$last_line" == "$expected_line" ]; then
    echo "The last line matches the expected value."
  else
    echo "The last line does not match the expected value."
    echo "Expected: $expected_line"
    echo "Actual: $last_line"
    return 1
  fi
}

# 1. Close the app using adb
adb -s $ANDROID_DEVICE shell am force-stop $PACKAGE_NAME
sleep 2

# 2. Start the app using adb
adb -s $ANDROID_DEVICE shell am start -n $PACKAGE_NAME/$ACTIVITY
sleep 2
PID=$(adb -s $ANDROID_DEVICE shell pidof $PACKAGE_NAME)
if [ -z "$PID" ]; then
  echo "The app is not running. Please start the app and try again."
  exit 1
fi

# 4.init function
adb -s $ANDROID_DEVICE shell am start -a 'xxx.intent.action.test.setup' -c 'android.intent.category.DEFAULT' --ez startXXX true
while true; do
  check_last_line "xx started"
  if [ $? -eq 0 ]; then
    break
  else
    sleep 2
  fi
done

# 5. Start test
rm $OUTPUT_FILE
adb -s $ANDROID_DEVICE shell rm /sdcard/result.json
adb -s $ANDROID_DEVICE shell am start -a 'xxx.intent.action.test.setup' -c 'android.intent.category.DEFAULT' --ez functionxxx true
START_TIME=$(date +%s)

# 6. Check whether the func is completed
while true; do
  check_last_line "finish"
  if [ $? -eq 0 ]; then
    # 8. If the function is completed, stop recording performance and calculate the executing time
    END_TIME=$(date +%s)
    EXECUTING_TIME=$((END_TIME - START_TIME))

    # Calculate average values
    CPU_AVG=$(echo "scale=2; $CPU_TOTAL / $SAMPLE_COUNT" | bc)
    PSS_AVG=$(echo "scale=2; $PSS_TOTAL / $SAMPLE_COUNT" | bc)
    POWER_AVG=$(echo "scale=2; $POWER_TOTAL / $SAMPLE_COUNT" | bc)
    TRAFFIC_AVG=$(echo "scale=2; $TRAFFIC_TOTAL / $SAMPLE_COUNT" | bc)

    echo "Function completed. Executing time: $EXECUTING_TIME seconds" >> $OUTPUT_FILE
    echo "Average metrics: CPU: $CPU_AVG, PSS: $PSS_AVG, Power: $POWER_AVG, Traffic: $TRAFFIC_AVG" >> $OUTPUT_FILE
    break
  else
    # 7. If the function has not completed, record the app's CPU, PSS, power, and traffic
    CPU_USAGE=$(adb -s $ANDROID_DEVICE shell top -b -n 1 | grep $PID | awk '{print $9}')
    PSS=$(adb -s $ANDROID_DEVICE shell dumpsys meminfo $PACKAGE_NAME | grep "TOTAL:" | awk '{print $2}')
    POWER=$(adb -s $ANDROID_DEVICE shell dumpsys batterystats --charged | grep "$PACKAGE_NAME" | awk '{print $6}')
    TRAFFIC=$(adb -s $ANDROID_DEVICE shell dumpsys netstats | grep "$PACKAGE_NAME" | awk '{print $5}')

    echo "CPU: $CPU_USAGE, PSS: $PSS, Power: $POWER, Traffic: $TRAFFIC" >> $OUTPUT_FILE

    # Update metric counters
    CPU_TOTAL=$(echo "$CPU_TOTAL + $CPU_USAGE" | bc)
    PSS_TOTAL=$(echo "$PSS_TOTAL + $PSS" | bc)
    if [ -n "$POWER" ]; then
      POWER_TOTAL=$(echo "$POWER_TOTAL + $POWER" | bc)
    fi
    if [ -n "$TRAFFIC" ]; then
      TRAFFIC_TOTAL=$(echo "$TRAFFIC_TOTAL + $TRAFFIC" | bc)
    fi
    SAMPLE_COUNT=$((SAMPLE_COUNT + 1))

    sleep 2
  fi
done
