# ALSA-only-Jack-Archlinux-Audio-Config
Here I like to share my realtime audio configuration on a (pulseaudio-free) Archlinux system. I use a Lenovo laptop with Intel chipset and a Presonus AudioBox VSL. My configuration is not perfect and lacks some functions. But this is due to some missing configurations. Actually I have a (partly) functional Alsa-Jack-Loopback-System which also works in the garden where I do not have the USB audiobox.  

My personal (and unfinished) ALSA-to-Jack-Bridge configuration is based on the great tutorial of markc:

    https://alsa.opensrc.org/Jack_and_Loopback_device_as_Alsa-to-Jack_bridge
    
    
The actual status of my configuration is:

PRO:
  - Realtime audio via loopback audio devices WITHOUT using the physical jack of the laptop.
  - A script helps to initialize the loopback devices in qjackctl's graph editor automatically.
  - When turning of the external audio box I can use the built-in audio hardware nearly on-the-fly. I only need to change
    the audio device in qjackctl and restart the jack server.
  
CONTRA:
  - Bad: Microphone of the laptop cannot be used with this configuration. Maybe it is a very small config error.
    But I haven't read Mark's tutorial completely... :)
  - Increasing or lowering the audio volume with the master 'PCM' is not possible. I need to choose the corresponding
    audio hardware like 'VSL' or 'PCH' in my volume mixer first.
