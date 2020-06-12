# ALSA-only-Jack-Archlinux-Audio-Config

Here I like to share my realtime audio configuration on a (pulseaudio-free) Archlinux system. I use a Lenovo laptop with Intel chipset and a Presonus AudioBox VSL. My configuration is not perfect and lacks some functions. But this is due to some missing configurations. Actually I have a (partly) functional Alsa-Jack-Loopback-System which also works in the garden where I do not have the USB audiobox.

The configurations and files which are needed for this setup may be found in the subfolders like /etc/ or /home/elaonmars/.


My personal (and unfinished) ALSA-to-Jack-Bridge configuration is based on the great tutorial of markc: https://alsa.opensrc.org/Jack_and_Loopback_device_as_Alsa-to-Jack_bridge   
     
As addition to the setup by markc I like to add the setup of falkTX of KXStudio (https://github.com/falkTX).
falkTX's script and .asoundrc friendly fetched from http://gamesplusone.com/alsa_to_jack.html which was 
originally hosted on the WineHQ Sound wiki page http://wiki.winehq.org/Sound
and written and developed by falkTX of KXStudio http://kxstudio.sourceforge.net/Main_Page .

---

## This repository hosts several different GitHub branches:
* One with the 'falkTX' version and 
* the other with the 'markc' version. 
* snd-aloop_in-progress: In progress :: A new sound setup (multiple sound devices) from scratch

---

The actual status of this configuration of this repository branch is as follows:

PRO:
  - Realtime audio via loopback audio devices WITHOUT using the physical jack of the laptop.
  - A script helps to initialize the loopback devices in qjackctl's graph editor automatically.
  
    <img src="./qjackctl-Loopback-connection.png" width=80%>
  
  - When turning off the external audio box I can use the built-in audio hardware nearly on-the-fly. I only need to change
    the audio device in qjackctl.
  - Built-in microphone (Intel HDA PCH) works too, when configured correctly in 'qjackctl' 
    (see -> qjackctl- configuration.README_in_German)
  
To Do:
  - There is no master 'Loopback' volume for increasing or lowering the audio volume. It needs to choose the corresponding
    audio hardware like 'VSL' or 'PCH' separately.
    
    <img src="./alsamixer-capturesettings.png" width="80%">
    
  - __!!! Sound volume and sound mute button on the laptop doesn't work anymore.__

---

This is my setup:

## Sound device list
```
# aplay -l
**** Liste der Hardware-Geräte (PLAYBACK) ****
Karte 0: Loopback [Loopback], Gerät 0: Loopback PCM [Loopback PCM]
  Sub-Geräte: 7/8
  Sub-Gerät #0: subdevice #0
  Sub-Gerät #1: subdevice #1
  Sub-Gerät #2: subdevice #2
  Sub-Gerät #3: subdevice #3
  Sub-Gerät #4: subdevice #4
  Sub-Gerät #5: subdevice #5
  Sub-Gerät #6: subdevice #6
  Sub-Gerät #7: subdevice #7
Karte 0: Loopback [Loopback], Gerät 1: Loopback PCM [Loopback PCM]
  Sub-Geräte: 7/8
  Sub-Gerät #0: subdevice #0
  Sub-Gerät #1: subdevice #1
  Sub-Gerät #2: subdevice #2
  Sub-Gerät #3: subdevice #3
  Sub-Gerät #4: subdevice #4
  Sub-Gerät #5: subdevice #5
  Sub-Gerät #6: subdevice #6
  Sub-Gerät #7: subdevice #7
Karte 1: VSL [AudioBox 44 VSL], Gerät 0: USB Audio [USB Audio]
  Sub-Geräte: 0/1
  Sub-Gerät #0: subdevice #0
Karte 2: PCH [HDA Intel PCH], Gerät 0: ALC269VC Analog [ALC269VC Analog]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 2: PCH [HDA Intel PCH], Gerät 3: HDMI 0 [HDMI 0]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 2: PCH [HDA Intel PCH], Gerät 7: HDMI 1 [HDMI 1]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 2: PCH [HDA Intel PCH], Gerät 8: HDMI 2 [HDMI 2]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
```
