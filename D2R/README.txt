D2R Offline Play Tools v1.0 by SeraphExodus

Contact me: seraphexodus on Discord or trf84 on Reddit

Overview: 

This mini-application allows you to choose, set, and maintain a terror zone in Diablo II Resurrected for an indefinite amount of time. Additionally, it has support for mouse inputs to quickly change the /players setting.

These functions are only usable in single player, offline play. This app will do absolutely nothing if you're playing online ladder or non-ladder.

Method:

The application pulls data from d2emu.com, who have graciously walked every TZ for the next few months to see which one pops when. They update pretty often afaik but I can't make any guarantees that the data continue to be updated into the distant future.

It attempts to pull the remote data every time it runs, and then writes it to a file in the same folder as the exe to be accessible in case the site becomes inaccessible in the future (or in case your internet is down).

When you select a TZ, it searches for the closest instance of that TZ occurring to the current system time, and then changes the system time to the beginning of that TZ's period. When the last minute of that TZ's active time is reached, the script automatically resets the system time back to the minute the TZ started, and will continue to do so until you exit the application.

The UI consists of only 5 elements - a text line displaying the active terror zone, a dropdown menu to select a target terror zone, and 3 buttons. The first button sets the terror zone selected in the dropdown as the active, using the method described in the previous paragraph. The second button resets the system time without closing the application. The third button resets the system time and then closes the application (this can also be achieved by closing the window by hitting the X).

Resetting the system time in any fashion causes the application to access NTP servers in order to obtain the current Unix time, and resets your system time to the correct value based on your time zone setting. 

NOTE: Time reset functionality doesn't work if you aren't connected to the internet, and your system time will either have to be reset to the correct value manually or else reset when your internet connection is restored.

SILLY NOTE: The Epochalypse is coming. Be ready.

Usage:

TZ Setting Function - Simply select a terror zone from the dropdown and click the "Set Terror Zone". It will refresh itself until you change it or reset the time.

/players Setting Function - The player count setting can be controlled using the mouse forward and back buttons as well as the middle mouse button. By default, the player counts it steps between are /players 1, /players 3, /players 5, and /players 8. By pressing the middle mouse button, this can be toggled to cycle through all values 1-8. Pressing the mouse forward button increases the player count setting to the next higher step, and pressing the mouse back button lowers it. The application interfaces with the game via emulated keyboard inputs, so if you are pressing any keys at the same time you increment the player count, the change will not be successful. 

Since the application doesn't actually see any information coming from the game, it doesn't know what your current player count setting is at any time. It defaults to thinking the current setting is /players 1 every time it's started, so even if you are on /players 8, pressing the back button will not decrement the player count until you press the forward button at least once, at which point both the application and the game will be set to /players 3. Don't be afraid to do a little back and forth to make sure you're on the correct player count.

For those who don't know, enemy HP/damage and nodrop rates are determined based on the player count setting when they are first initialized, usually when you're 1-2 screens away from them. As such, player count changes may require you to travel a short distance before you see their effects. Any enemies that are initialized at a given player count will have their stats and loot rates remain at that player count until they die or you leave the game. This is in contrast to the way it worked pre-RotW, where only enemy stats were immutable after initializing and nodrop would be updated if you left the area, changed the player count, and came back a few seconds later, which allowed you to, for example, get p7 nodrop of effectively 0 from a p1 difficulty Andariel. But Blizzard couldn't countenance us having fun in our single-player game, so here we are. /rant

Miscellaneous:

You may need to run the application as Administrator in order for it to function correctly, as it creates and modifies files in addition to changing system time. Since requiring admin privileges is scary to see for anyone attempting to use an app they got from a stranger on the internet, I've made this script entirely open-source. If you don't trust the exe, you can download python and VScode and run the application directly from the script if you so choose.

Dependencies:

The script relies on the following non-native python libraries to function:

-FreeSimpleGUI: A branch of PySimpleGUI that doesn't cost money. Handles the basic UI the application uses since I'm not well-versed in Tkinter.
-ntplib: A module to query NTP servers, allowing us to get an accurate Unix time to reset to when we finish.
-pynput: Enables the mouse functions to allow changing player count easily.
-pywin32: Lets us identify the D2R window for sending keyboard inputs, and enables modifying the system time.
-requests: Simple module to send HTTP requests, used for accessing the TZ json data from d2emu.com.

Acknowledgements:

d2emu.com for doing the legwork to obtain the offline TZ time data, without which this script would be totally bricked. Cannot thank these people enough.