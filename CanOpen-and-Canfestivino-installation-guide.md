# CanOpen and Canfestivino installation guide
This document will guide you on how to set up the higher level CanOpen protocol over a canbus network. To test the included example, you will need the following*:

### Software*:
Please consult the install guides of each respective system.

*  Ubuntu 16.04 or later
*  Git
*  Python 2.7
*  Python 3.X
*  pip

### Hardware*
* 2x Joy-it SBC-CAN01 (MCP2515 Can Modules)
* Raspberry Pi 3 or 4 (with all necessary accessories, ie keyboard, mouse, HDMI)
* Ardunio Uno
* Jumper cables (Male-male, male-female, female-female)
* Potentiometer
* Servo (SG90)
* Breadboard

*) The implementation is not limited to this specific hardware and software, but was not tested with other systems. It might be possible to eg. use Windows Subsystem for Linux (WSL), or other CANBUS interfaces such as the PiCAN shield.

## Wiring guide
As the Raspberry Pi GPIO pins are only rated for 3.3V, it's important to wire the SBC-CAN01 correctly. The SBC-CAN01 is designed in such a way that the SPI interface is powered via the VCC pin, and thus uses 3.3V for SPI.
However, the CAN transceiver chip requires 5V, which is supplied via the VCC1 pin. See the datasheet for the SBC-CAN01 for more details.

On the Arduino Uno, it's okay to supply 5V to both VCC and VCC1.

\#TODO add wiring diagram

## Raspberry Setup
###CANBUS Setup

To install the necessary extensions and to be able to use the CAN module with a Raspberry Pi using CanOpen, please update the package list and install the extensions can-ultis:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install can-utils
```

Next, use the following command to get the kernel version of your Raspberry Pis. This is necessary for the further configuration of the system.
```
uname -a
```
You will be shown the current kernel version (e.g. "4.4.41-v7").

Next, open and edit the `config.txt` file with the following command:

```
sudo nano /boot/config.txt
```
If your kernel version is 4.4.x or newer, please add the following lines to the end of the file:

```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=sp1-1cs
```
However, if your Raspberry Pi runs with an older kernel version, please add the following lines to the end of the file instead:

```
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=sp1-bcm2835-overlay
```

The `16000000` stands that the MCP2515 operates with a clock of 16 MHz. This depends on the quartz used and may need to be adjusted. The SBC-CAN01 uses a 16MHz clock, so you can leave this unchanged.
 Save the file with the key combination `CTRL+O`, confirm the saving process with `Enter`, and exit the editor with the combination `CTRL+X`.
Restart your Raspberry Pi with the following command:

```
sudo reboot
```

After the restart has been completed, you can now start the CAN interface:

```
 sudo ip link set can0 up type can bitrate 500000
```
If you get errors saying that the buffer is full, extend it using the following command:

```
sudo ifconfig can0 txqueuelen 10000
```

The system should now be ready. You can now start a first send attempt. First, open a *new* terminal window and start candump with the following command:

```
candump can0
```
Then in the *other* terminal, run the following command:

```
cansend can0 127#DEADBEEF
```
In the windown running candump, you should see something similar to the following:

```
pi@raspberrypi:~ $ candump can0
  can0  127    [4]  DE AD BE EF
```
Stop running candump with the key combination `CTRL+C`

###CanOpen Setup
We're almost ready to start running the example CanOpen network. First, install CanOpen for Python with the following command:

```
pip install canopen
```
Now, open `canopen_master_example.py` in Thonny or your favorite IDE. If you were to run this, you will get `SdoCommunicationError("No SDO response received")`. This is because we still need to setup our Ardunio slave node

##Ardunio Slave Node setup
Check that the Arduino is wired properly according to the wiring guide. Now, open `slave_node_example.ino` with the Arduino IDE and upload the sketch to the Uno. Once its finished uploading, open the Serial Monitor.

##Running the complete CanOpen network example
###On the Raspberry Pi
Run candump using the following command:

```
candump can0
```

You should see the following repeated messages come in:

```
...
can0  705   [1]  7F
can0  705   [1]  7F 
can0  705   [1]  7F 
```

This is the so-called *heartbeat* of the slave node, letting us know that it's still alive.
> Note that in this example, the master does not check if a heartbeat is received. This is purely for debugging purposes to confirm that messages are being received with `candump`.

In Thonny, open `can_open_master_example.py` if you haven't done so already and click on `Run`. The servo should move to the position relative to the potentiometer position.

In `candump`, you should see the values change accordingly when you turn the potentiometer

###On the Arduino Uno
Turn the knob on the potmeter and the servo should turn accordingly. Using the Arduino IDE Serial Monitor, it's possible to see which values are being sent and received (these should both be the same).

##Editing the slave node .EDS
> In a more complex CanOpen network, the master node would be able to request a slave node's .EDS file at runtime. It would also be able to edit the .EDS eg. to change the node ID. Embedded devices, such as the Arduino lack the resources to parse a large text file at runtime, so we must do this manually. This also means that every time the EDS changes, it will need to be generated, compiled and uploaded.

Now that the example is working, you'll want to edit the sketch to add your own components that fit your own project. To do this, we will need to edit the .EDS file and generate new `.cpp` and `.h` files for the Ardunio sketch. We'll be doing this using a somewhat dated GUI application written and run in Python 2.7. We got this working in Ubuntu, as the GUI package used was not compatible with macOS nor Raspbian. It was not tested in WLS.

###Installing the dependancies
Make sure you're in the `objdictgen` folder. If not, use the following command:

```
cd objdictgen
```
Unpack the Gnosis Utils and go the folder with the following commands:

```
tar xzvf Gnosis_Utils-current.tar.gz
cd Gnosis_Utils-current/Gnosis_Utils-1.2.2/
```
Then run the setup using python2 with the following command:

```
sudo python2 setup.py install
```
Now install the wx dependancies for the GUI

```
sudo apt-get install python-wxtools
```
Finally, start the editor by running the following command from within the `objdictgen` folder:

```
python2 objdictedit.py
```

###Starting objdictedit.py and opening the .EDS
From the `objdictgen` folder, run the editor with the following command:

```
python2 objdictedit.py
```
Import a `.eds` file with `File > Import EDS file`.
Open a `.od` file with `File > Open`
There are some example files in `/examples`. `slave_node_example.od` is the same node file used by the Arduino sketch.

###Changing .eds to fit your network
First, be sure to change the name and ID of your node with `Edit > Node infos`
> The CanOpen protocol gives the highest priority to the lowest ID number. Be sure to number your nodes accordingly

####Adding or changing your own inputs and outputs
Under `0x2000-0x5FFF Manufacturer Specific` you can edit the existing `Sensor` and `Actuator` by `Right-Click > Rename` on either, and clicking on them and editing their fields on the right.
However we recommend deleting these and adding new components according to the specifications of your devices.
> Be sure to have the checkbox `Have callbacks` enables. If not, you won't be able to write callback functions in the Arduino sketch. When you have finished adding your components, we must then map the Transmit and Receive PDO's

####Mapping the Receive PDO's (node inputs)
Receive PDO's are the commands received from the network to the node. These are eg. values to move an actuator such as a servo.

On the top left, click on `0x1600-17FF Receive PDO Mapping`.
On the bottom left, click on `0x1600 Receive PDO 1 Mapping`. If this does not exist, click `Add: PDO Receive`
On the bottom right, make sure `Have Callbacks` is checked
On `subindex 0x01`, change the `value` to map to the desired `Manufacturer Specific` object by double-clicking on it and selecting the desired object from the dropdown list.
Continue adding `PDO Receive`s for all of your expecting incoming messages, remembering to check `Have Callbacks`.

####Mapping the Transmit PDO's (node outputs)
Transmit PDO's is the data transmitted from the node to the network after receiving a request for said data. These are eg. values read from a sensor such as a distance or temperature sensor.

On the top left, click on `0x1A00-1BFF Transmit PDO Mapping`.
On the bottom left, click on `0x1A00 Transmit PDO 1 Mapping`. If this does not exist, click `Add: PDO Transmit`
On the bottom right, make sure `Have Callbacks` is checked
On `subindex 0x01`, change the `value` to map to the desired `Manufacturer Specific` object by double-clicking on it and selecting the desired object from the dropdown list.
Continue adding `PDO Transmit`s for all of your expecting outgoing messages, remembering to check `Have Callbacks`.

###Other Settings
You can use the Objdictedit to also change other CanOpen parameters, such as `0x1016 Consumer Heartbeat time`, where you can shorten or lengthen the interval between heartbeat messages.

##Exporting .EDS, .OD, .CPP and .H files
When you're done, be sure to save your new `.od` file (`File > Save` or `File Save As...`) and export your `.eds` (`File > Export to EDS file`).

The most important step necessary for the Arduino sketch is the `Build Dictionary` option. This will generate the `.cpp` and `.h` files needed in the sketch. Do so, giving it a fitting name.

##Including the .CPP and .H files in .INO sketch
If you don't have your own slave sketch already, open the `Arduino/slave_node_example` folder. Copy the `.cpp` and `.h` files your generated from objdictgen into this folder and delete or move the `slave_node_example.cpp` and `slave_node_example.h` files.
> If you move these files, be sure to move them *out* of the sketch folder or any of its subfolders
Then open `slave_example_node.ino` in the Arduino IDE.
> All files and files in subfolders of the sketch folder will also open in Arduino IDE. If you change the filenames of your generated `.cpp` and `.h` files, you must therefore close the sketch and reopen the `.ino` to have the correct files for compilation. If you get compile errors, this is likely the cause.

###Updating the sketch
####Changing the includes
The first step you must do is to change the includes to match the filename of your generated `.cpp` and `.h` files. Change the line:

```
#include "slave_node_example.h" //generated using objdictedit.py
```

To reflect the name you gave your generated `.h` file. For example:

```
#include "my_new_slave_node.h" //generated using objdictedit.py
```
####Write your callback functions
Using the exising callback functions `readSensorCallback` and `writeActuatorCallback` as a template, write your own callback functions. Give them descriptive names, making it clear which components they will be accessing. You're free to name the functions whatever you wish.
> Received data is saved under the same variable as the name of your `Manufacturer Specific` object

####Mapping callback functions
In the `void setup()`, you must now map your callback functions to the corrosponding object indices and subindices, much like as is done in the example. The syntax is:

```
RegisterSetODentryCallBack([index], [subindex], [callback function])
```
Where `index` is the index number of the Manufacturer Specific object you defined in the .od/.eds.
`subindex` should be 0, unless you defined a subindex
`callback function` is the callback function you defined earlier in the step above.

In the example, these are enclosed in print statements, as these will return an error code if something went wrong (otherwise simply `0` if it was successful.

###Final Steps
Now simply compile the sketch and upload it to the Arduino and it should start sending it's heartbeat over the CANBUS network.

##Preparing the master node

> As explained in the "Editing a slave node .EDS" section, the master node cannot request or change the slave node's .EDS file at runtime. Therefore we need to make sure it has all necessary information beforehand. The major downside to this is that any changes made to a slave node or to the network must also be reflected in all of the corresponding files.
> 
>  This also means that you must also manually keep track of all nodes ID's in your network, as there are no built-in checks for conflicting ID's.
> 
> It is especially important in the following steps that Node ID's correspond to the ID defined in the .OD
> 
> Our recommendation is to have some kind of system that makes it easy to find the ID of a node, such putting it filenames.

###Generating the master OD/EDS with Networkedit
Make sure you're in the `objdictgen` folder. If not, use the following command:

```
cd objdictgen
```

Then run networkedit with the following command:

```
python2 networkedit.py
```

Go to `File > Open` and open the folder containing your slave node `.eds` files. This should open `0x00 MasterNode` on the left colomn.
Optionaly, click on `0x1000-0x1029 Communication Parameters` and then `0x1018 Identity` and fill in the Vendor ID, Product code etc.

We will now add the slave nodes. Go to `Network > Add slave node` and fill in the exact same `Slave Name` and `Slave Node ID` as you did in the previous section. Click on the dropdown arrow on `EDS file` and choose the appropriate file from the list. If the `.eds` is not in the folder you chose to open, you can import this with the `Import EDS` button, then use the dropdown menu to choose the correct file.

Once you have added all slave nodes belonging to your network, go to `File > Save`. It will seem like nothing has happened, however, in the folder you opened, you will find two new files: `master.od` and `nodelist.cpj`.

`canopen-python` is unable to read this file however, so we must convert this to a `.eds` using `objdictedit.py`. To do this, exit out of Networkedit, and run the following command in the terminal:
```
python2 objdictedit.py
```

Go to `File > Open` and choose the `master.od` file we just created above. The go to `File > Export to EDS file`. Save this to the same folder as all of your other `.eds` files.

###Editing the CanOpen Master Example
First, make sure all of the `.eds` files of your master and slave nodes are in the same folder as the `canopen_master_example.py`. Then, open `canopen_master_example.py` in your favorite editor.

Define the master and each slave node as demonstrated in the example.

Please refer to the comments or the [canopen documentation](https://canopen.readthedocs.io/en/latest/od.html#canopen.ObjectDictionary) for further explaination.
