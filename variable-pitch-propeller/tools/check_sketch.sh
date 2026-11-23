#!/usr/bin/env bash
# Compile one Arduino sketch for an Arduino Uno (ATmega328P, 16 MHz) with plain avr-gcc,
# to check that it builds. Needs: avr-gcc, avr-libc, and (in $EXT) clones of
# arduino/ArduinoCore-avr, arduino-libraries/Servo, olkal/HX711_ADC, johnrickman/LiquidCrystal_I2C.
#   tools/check_sketch.sh path/to/sketch.ino [build dir]
set -euo pipefail
INO="$1"; OUT="${2:-/tmp/sketchbuild}/$(basename "${INO%.ino}")"; EXT="${EXT:-$HOME/arduino-ext}"
CORE="$EXT/ArduinoCore-avr"; mkdir -p "$OUT"
MCU="-mmcu=atmega328p -DF_CPU=16000000L -DARDUINO=10819 -DARDUINO_AVR_UNO -DARDUINO_ARCH_AVR"
INC="-I$CORE/cores/arduino -I$CORE/variants/standard -I$CORE/libraries/EEPROM/src -I$CORE/libraries/Wire/src
     -I$CORE/libraries/Wire/src/utility -I$EXT/Servo/src -I$EXT/HX711_ADC/src -I$EXT/LiquidCrystal_I2C"
CF="-Os -w -ffunction-sections -fdata-sections -flto"
# the IDE adds #include <Arduino.h> and prototypes for the sketch's functions; do the same
python3 - "$INO" "$OUT/sketch.cpp" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
protos = re.findall(r'^\s*((?:void|int|float|long|bool|boolean|byte|char|unsigned long|double)\s+\w+\s*\([^;{]*\))\s*\{', src, re.M)
protos = [p for p in protos if not re.match(r'.*\b(setup|loop)\s*\(', p)]
open(sys.argv[2], 'w').write('#include <Arduino.h>\n' + ''.join(p + ';\n' for p in protos) + '#line 1\n' + src)
PY
objs=()
for f in "$CORE"/cores/arduino/*.c "$CORE"/cores/arduino/*.cpp "$EXT/Servo/src/avr/Servo.cpp" \
         "$EXT/HX711_ADC/src/HX711_ADC.cpp" "$EXT/LiquidCrystal_I2C/LiquidCrystal_I2C.cpp" \
         "$CORE/libraries/Wire/src/Wire.cpp" "$CORE/libraries/Wire/src/utility/twi.c" "$OUT/sketch.cpp"; do
  o="$OUT/$(basename "$f").o"
  case "$f" in *.c) avr-gcc $MCU $CF -std=gnu11 $INC -c "$f" -o "$o";;
               *)   avr-g++ $MCU $CF -std=gnu++11 -fno-exceptions -fno-threadsafe-statics $INC -c "$f" -o "$o";; esac
  objs+=("$o")
done
avr-gcc $MCU -Os -flto -Wl,--gc-sections "${objs[@]}" -lm -o "$OUT/sketch.elf"
avr-size -C --mcu=atmega328p "$OUT/sketch.elf" | grep -E "Program|Data" | tr -s ' ' | sed "s|^|$(basename "$INO"): |"
