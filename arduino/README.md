To use the tapkick arduino you must follow these steps:

1. Upload the arduino code to your arduino Mega

Make sure that you do not have the RFID tag plugged into RX pin D0.  You will 
get an error uploading if you do.

2. Install the following libraries to your system:

    $ pip install pyserial

3. Run the python code to read from the serial port

    $ ./tapkick.py

4. Watch the output
