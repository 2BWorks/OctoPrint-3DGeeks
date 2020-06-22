# OctoPrint-3DGeeks (Coming soon to Play Store)

This plugin is created as a companion plugin to the [3D Geeks](https://www.3dgeeks.app) app. 

It allows you to connect your OctoPrint instance with the 3D Geeks app for quick one-click configuration. Which removes the needs to manually type in IP addresses en port numbers, which is super error-prone.

The plugin also allows you to receive push notifications with a status update from your OctoPrint instance. It currently supports the following events:

- Print started
- Print finished
- Print failed
- Print progress
- Printer connected
- Printer disconnected
- Octoprint startup
- Octoprint shutdown

## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/2BWorks/OctoPrint-3DGeeks/archive/master.zip


## Usage
### Instance configuration
After installation restart OctoPrint, and go to the Settings tab. You should see a new tab named 3D Geeks, go ahead and click that tab. You should be presented with a QR Code.

On your Android powered device open the 3D Geeks app, go to:
```
Settings > OctoPrint settings
```
Press the `+`-Icon in the bottom-right hand corner.

Press the scan icon, scan the QR code you're being presented. If everything goes well all the nesecary fields will be filled in automatically for you. You can now press Test connection for a quick test of the connection to your OctoPrint instance. 

NOTE: Be sure you're Android device is connected to the same network as your OctoPrint instance, as they communicate through the local network. When the test succeeds you can press Create. Your OctoPrint instance is now saved and can receive files from 3D Geeks.

NOTE: You can create as much OctoPrint instances as you desire. When uploading a file, the app will ask you which instance to upload to.

### Push notifications
Enable remote notifications from within the app. And press the `Send test notification`-button from the 3D Geeks OctoPrint settings. If everything is filled in correctly you should receive a test notification on your phone. 

Select the push notification categories which you would like to receive.

Don't forget to save your OctoPrint instance on the app.
