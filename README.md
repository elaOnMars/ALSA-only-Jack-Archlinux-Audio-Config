# In progress :: A new sound setup (multiple sound devices) from scratch 
### with ALSA, Loopback devices, USB Audio, built-in HDA Audio and Jack

In contrast to the other branches this branch describes the steps to set up a working and 
solid ALSA based sound system from scratch

## Which capatibilies my sound system should have?
* Switching easily between on-board sound and the external USB sound device.
* Hearing sound in every (non-ALSA) capable webrowser.
* Using the microphone in most applications. In parallel I like to mix different sound channels with recording software like Ardour. That means: I like to fetch every real sound which are on several loopback devices.


## Sound devices:
* HDA Intel (model ALC269-dmic). Pretty name: __PCH__.
* PreSonus AudioBox 44VSL. Pretty name: __VSL__.
* ALSA Loopback devices. Pretty name: __Loopback__.

---

# Steps to set up a sound system

Before you start using your sound devices you should mute the built-in microphone of your __playback__ device - not of the __capture__ devices! Otherwise you'll have feedback noise. You can hear it if you tap with your finger on your headphones.
Use __alsamixer__ for this task.

Normally your built-in sound card should be visible as the first device in __alsamixer__.

* Open __alsamixer__ and press _F3_. Decrease the volume of the microphone to _zero_ or _mute_ it by pressing the button _m_.
* Change to the capture device by pressing the button _F4_. Check that the _capture_ device is _ON_. Switching ON/OFF by pressing the space bar.



## 1. Start with a unchanged ALSA configuration

If you start re-configuring ALSA from scratch you should initialize the ALSA driver to a default state with:
```
alsactl init
```

## 2. Define the order of the sound cards loaded globally

The on-board sound card is used as the primary sound device.

Create a module file _snd.conf_ in _/etc/modprobe.d/_ with the following content:

```
# Get your device names with:
#    aplay -l

# 1. HDA Intel (PCH) - index=0    # change the model to your sound card model or to _model=auto_.
# 2. USB AUdio (VSL) - index=1
# 3. Loopback - index=2

options snd slots=snd-hda-intel index=0 snoop=1 model=alc269-dmic,slots=snd-usb-audio index=1,slots=snd-aloop index=2
```
Hint: In your ~/.asoundrc you can define which sound card shall be used as the default sound card.

Now tell the system that it should load the individual _snd_ module at startup. Create a file _snd.conf_ in _/etc/modules-load.de/_ with the following word:

```
snd
```
Save and close the file.



__Important: Reboot now and check, that the _snd_ module was loaded amd the built-in sound card has _index 0_. 
Use the follwing command:__
```
_modinfo -p snd
```


## 3. Sound- and recording-check

Not all applications which can be used to play audio are "ALSA-friendly". Webrowsers like _Firefox_ or _Chromium_ will not work at this moment. But you can hear sound when usind "ALSA-friendly" players like ___aplay___ (sound) or ___mplayer___ (video).


### 3.1 Sound-check of the on-board sound device

We'll integrate the external sound device later by using the user's _.asoundrc_ file. But first we'll playing some sample sounds with "ALSA-friendly" applications. Open a terminal and enter the following:

```
aplay /usr/share/sounds/alsa/*
```

If you can hear sound, than everything is okay and we can go further.


### 3.2 Recording-check of the on-board sound device

The default configuration of ALSA should allow you to record sound with the built-in microphone. 
Test your capture device (built-in, not the USB device) with:

```
arecord -d 4 -f cd  test6.wav && aplay test6.wav
```
The parameter _-f cd_ records in CD quality.


### 3.3 Sound-check of the external USB audio device

First power-on your USB audio devices and identify the index and the pretty names of your 
external sound devices. You should avoid using indices in ALSA configurations. 
Because this may result in unexpected results and you won't hear anything again.

My system has identified the following sound devices automatically:
```
**** Liste der Hardware-Geräte (PLAYBACK) ****
Karte 0: PCH [HDA Intel PCH], Gerät 0: ALC269VC Analog [ALC269VC Analog]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 0: PCH [HDA Intel PCH], Gerät 3: HDMI 0 [HDMI 0]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 0: PCH [HDA Intel PCH], Gerät 7: HDMI 1 [HDMI 1]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 0: PCH [HDA Intel PCH], Gerät 8: HDMI 2 [HDMI 2]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
Karte 1: VSL [AudioBox 44 VSL], Gerät 0: USB Audio [USB Audio]
  Sub-Geräte: 1/1
  Sub-Gerät #0: subdevice #0
```

As the sound-check with the default device __PCH__ was successsfully I can now do a 
sound-check with my USB audio device named __VSL__.

To not accidentally overwrite a working _.asoundrc_ you should handle symbolic links instead.

Set-up your $HOME directory for ALSA-debugging:

```
# change into the $HOME directory
cd ~

# create folders for ALSA-debugging
mkdir asoundrc-working
mkdir asoundrc-debugging

# create a new configuration file for ALSA
cat > asoundrc-debugging/.asoundrc_default-card
# Change default card and device  \
defaults.pcm.!card VSL    # here should be written your USB audio device \
defaults.pcm.!device 0  \
defaults.pcm.!ctl VSL     # same here...  \

```

Enter _Strg+C_ to interrupt the _cat_ command. The file _~/asoundrc-debugging/.asoundrc_default-card_ 
has been written to disk.

Now change into your _$HOME_ directory and create a symbolic link to your first _.asoundrc_ ALSA configuration file:

```
cd ~
ln -s asoundrc-debugging/.asoundrc_default-card .asoundrc
```

Check that your symbolic link has been created:

```
ls -la .asoundrc
```

The output should look like this:

```
lrwxrwxrwx 1 elaonmars elaonmars 65  1. Jun 14:24 .asoundrc -> asoundrc-debugging/.asoundrc_default-card
```

__Now do a sound-check again with your USB audio device__:

```
aplay /usr/share/sounds/alsa/*
```

Your external USB audio device should now playback the sample sounds perfectly.

Now you should copy your configuration file into the folder with working configuration files:

```
cp -a $HOME/asoundrc-debugging/.asoundrc_default-card $HOME/asoundrc-sorking/
```


## 4. Including configuration files

From this point on you should __include__ ALSA configuration files instead of filling them up with more configurations.

The positive effect of this is, that you know exactly which part of your _.asoundrc_ file is doing what.

Let us create a new .asoundrc configuration file which refers to the configuration file created in the steps before:

Change directory:
```
cd ~/asoundrc-debug
```
Create a new configuration file _.asoundrc_default-card-by-referencing_ with the follwing content:
```
</home/elaonmars/asoundrc-debug/.asoundrc-01_default-card-and-device_ALSA.org.gentoo.wiki>
```
__Hint: '$HOME' or '~' instead of '/home/elaonmars' won't work.__

Change into your $HOME directory and remove the symbolic link to _.asoundrc_ with:

```
rm .asoundrc
```

Now reload your ALSA configuration by soft linking to the new config file:

```
ln -s debug/.asoundrc_default-card-by-referencing .asoundrc
```

To test if everything is working just do a sound-check again:

```
aplay /usr/share/sounds/alsa/*
```

Your default sound card should play the sample sounds yet.

If you don't hear anything please start with the configuration again. Also check if the file you are referencing to is valid.


```...```

---

## This repository hosts different GitHub branches:
* One with the 'falkTX' version and 
* the other with the 'markc' version. 
* snd-aloop_in-progress: In progress :: A new sound setup (multiple sound devices) from scratch

---

## Helpful links:
* wiki.gentoo.org/wiki/ALSA#Configuration
* wiki.archlinux.org/index.php/Advanced_Linux_Sound_Architecture#Including_configuration_files
* fossies.org/linux/alsa-lib/doc/asoundrc.txt
