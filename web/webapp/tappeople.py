import glob
import optparse
import os
import sys
import time

import serial

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from beer.models import User


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
        time.sleep(10.0)
    except serial.SerialException, e:
        print 'Serial connection could not be established:\n\t', e
        sys.exit()

    person_list = ['chris']

    for person in xrange(0, 600):
        print 'Tap an rfid card for %s' % person

        # Continuously check the serial port
        while 1:

            try:
                # Confirm that value was received
                data = ser.readline().strip()

                if data and ':' in data:
                    rfid = data.split(':')[0]

                    # Get or Create the user for the system
                    user, created = User.objects.get_or_create(rfid=rfid)
                    if created:
                        user.name = person
                        user.save()
                        print '\tWelcome to Tapkick %s, your RFID is %s' % (person, rfid)
                        break
                    else:
                        print '\tCard belongs to %s, try again' % (user.name)

            except Exception, e:
                print e
