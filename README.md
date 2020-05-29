# ALSA-2-Jack-Archlinux-Audio-Config
Here I like to share my realtime audio configuration on a (pulseaudio-free) Archlinux system. I use a Lenovo laptop with Intel chipset and a Presonus AudioBox VSL. My configuration is not perfect and lacks some functions. But this is due to some missing configurations. Actually I have a (partly) functional Alsa-Jack-Loopback-System which also works in the garden where I do not have the USB audiobox.  

As addition to the setup by markc I like to add the setup of falkTX of KXStudio

I grepped the .asoundrc and the corresponding Python script from this site:

    http://gamesplusone.com/alsa_to_jack.html
    
    
The actual status of this configuration of this repository branch is as follows:

PRO:
  - Realtime audio via loopback audio devices WITHOUT using the physical jack of the laptop.
  - A script helps to initialize the loopback devices in qjackctl's graph editor automatically.
  - When turning off the external audio box I can use the built-in audio hardware nearly on-the-fly. I only need to change
    the audio device in qjackctl and restart the jack server.
  
CONTRA:
  - Bad: Microphone of the laptop cannot be used with this configuration. Maybe it is a very small config error.
    But I haven't read Mark's tutorial completely... :)
  - Increasing or lowering the audio volume with the master 'PCM' is not possible. I need to choose the corresponding
    audio hardware like 'VSL' or 'PCH' in my volume mixer first.
      
        A reason could be the snd-aloop.conf file of markc. I'll need to check it out some time. 
        
        You are welcome to give me some hints. :)
