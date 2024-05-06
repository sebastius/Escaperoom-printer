# Circuitpython on RP2040

import board
import busio
import adafruit_thermal_printer
import random
import digitalio
import time

# Printersettings
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
printerRX = board.GP13
printerTX = board.GP12
printeruart = busio.UART(printerTX, printerRX, baudrate=9600)
printer = ThermalPrinter(printeruart, auto_warm_up=False)
printer.warm_up()

# Other pinouts
encoder1 = digitalio.DigitalInOut(board.GP8)
encoder1.switch_to_input(pull=digitalio.Pull.UP)
encoder2 = digitalio.DigitalInOut(board.GP9)
encoder2.switch_to_input(pull=digitalio.Pull.UP)
encoder3 = digitalio.DigitalInOut(board.GP10)
encoder3.switch_to_input(pull=digitalio.Pull.UP)
encoder4 = digitalio.DigitalInOut(board.GP11)
encoder4.switch_to_input(pull=digitalio.Pull.UP)
button = digitalio.DigitalInOut(board.GP7)
button.switch_to_input(pull=digitalio.Pull.UP)

while True:
    print("Druk toch op die groene knop!")
    while button.value:
        time.sleep(0.1)
    encoder = (
        ((not (encoder1.value)) * 1)
        + ((not (encoder2.value)) * 2)
        + ((not (encoder3.value)) * 4)
        + ((not (encoder4.value)) * 8)
    )
    print(f"De ingestelde waarde is {encoder}")
    print()
    printer.size = adafruit_thermal_printer.SIZE_MEDIUM
    printer.bold = True
    printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
    printer.print("Staartdelingbaas")
    printer.underline = None
    printer.bold = False
    printer.size = adafruit_thermal_printer.SIZE_SMALL

    printer.print("Pak steeds het laatste cijfer van elk van de drie antwoorden.")

    printer.print(f"Jullie ingevoerde code is {encoder}")

    printer.feed(1)

    basecode = 469
    offset = (10 * encoder) + (10 - encoder)
    number = basecode + offset
    print(f"basecode={basecode}, offset={offset}, number={number}")
    digits_array = [int(digit) for digit in str(number)]
    printer.size = adafruit_thermal_printer.SIZE_LARGE
    printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
    for x in range(0, 3):
        deler = random.randint(3, 40)
        antwoord = (random.randint(999, 99999) * 10) + digits_array[x]
        deelgetal = deler * antwoord

        printer.print(f"{deler} / {deelgetal} \ ")
        print(f"{deelgetal} : {deler} = {antwoord} -> {digits_array[x]}")
        printer.feed(1)
    printer.size = adafruit_thermal_printer.SIZE_SMALL
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
    printer.print("----")
    for z in range(0, 8):
        printer.feed(1)
        printer.feed(1)

    while button.value:
        time.sleep(0.1)
