import datetime
import glob
import optparse
import os
import sys
import time

import serial

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from beer.models import Beer, Access, User


def scanports():
    return glob.glob('/dev/tty*')


if __name__ == '__main__':

    usage = 'usage: tapkick [options]'
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-p", "--port",
                      dest="port",
                      default=None,
                      type="string",
                      help="the serial connection port [default: %default]",
                      metavar="PORT")
    parser.add_option("-b", "--baud",
                      dest="baud",
                      default=9600,
                      type="int",
                      help="the serial connection BAUD rate [default: %default]",
                      metavar="BAUD")
    parser.add_option("-t", "--timeout",
                      dest="timeout",
                      default=5,
                      type="int",
                      help="the serial connection TIMEOUT in seconds [default: %default]",
                      metavar="TIMEOUT")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="the debug setting to print more information [default: %default]")
    (options, args) = parser.parse_args()

    # Set up the options
    PORT = options.port
    BAUD = options.baud
    TIMEOUT = options.timeout
    DEBUG = options.debug

    # Scan the ports if none given
    if not PORT:
        for port in scanports():
            for usb in ['usbserial', 'usbmodem', 'acm']:
                if usb.lower() in port.lower():
                    PORT = port
                    break
        if not PORT:
            print 'Port not found, please connect device or set before running'
            sys.exit()

    if DEBUG:
        print 'PORT %s' % PORT
        print 'BAUD %s' % BAUD
        print 'TIMEOUT %s' % TIMEOUT

    # Connect to serial port and wait for arduino reboot and startup
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        time.sleep(5.0)
    except serial.SerialException, e:
        print 'Serial connection could not be established:\n\t', e
        sys.exit()

    # Deal with the temperature sensor weirdness
    min_temp = 0.0
    max_temp = 35.0
    last_temp = [0.0, 0.0]
    temp = [0.0, 0.0]
    flow = [0.0, 0.0]

    # Continuously check the serial port
    while 1:

        try:
            # Confirm that value was received
            data = ser.readline().strip()

            if data:
                rfid = data.split(':')[0]
                data_list = data.split(':')[1].split('/')
                data = ''

                # Print useful information
                print datetime.datetime.now(), rfid, flow, temp

                # Get or Create the user for the system
                user, created = User.objects.get_or_create(rfid=rfid)
                if created:
                    print 'Welcome to Tapkick user %s' % rfid

                # Do work for each tap
                for i in xrange(0, 2):
                    # Get and set the temp
                    temp[i] = float(data_list[i + 2])
                    if not min_temp < temp[i] < max_temp:
                        temp[i] = last_temp[i]

                    # Save the old temperature data
                    last_temp[i] = temp[i]

                    # Get the flow and save an access
                    flow[i] = float(data_list[i])
                    if flow[i] > 0.0:
                        # Create the access object
                        access = Access(user=user)

                        # Select the beer based on flow data
                        beer = Beer.objects.get(tap_number=i + 1)
                        access.amount = flow[i]
                        access.beer = beer

                        # Record access in the database
                        access.save()

        except Exception, e:
            print e
