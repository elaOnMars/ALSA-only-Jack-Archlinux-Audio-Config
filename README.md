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

# Steps to set up a sound system:

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


## 3. Load the module _snd_ at startup

Create a file _snd.conf_ in _/etc/modules-load.de/_ with the following word:

```
snd
```
Save and close the file.



__Important: Reboot and check, that the _snd_ module was loaded amd the built-in sound card has _index 0_. 
Use the follwing command:__
```
_modinfo -p snd
```


## 4. Sound- and recording-check

Not all applications which can be used to play audio are "ALSA-friendly". Webrowsers like _Firefox_ or _Chromium_ will not work at this moment. But you can hear sound when usind "ALSA-friendly" players like ___aplay___ (sound) or ___mplayer___ (video).


### 4.1 Sound-check of the on-board sound

We'll integrate the external sound device later by using the user's _.asoundrc_ file. But first we'll playing some sample sounds with "ALSA-friendly" applications. Open a terminal and enter the following:

```
aplay /usr/share/sounds/alsa/*
```

If you can hear sound, than everything is okay and we can go further.


### 4.2 Recording-check of the on-board sound

The default configuration of ALSA should allow you to record sound with the built-in microphone. 
Test your capture device (built-in, not the USB device) with:

```
arecord -d 4 -f cd  test6.wav && aplay test6.wav
```
The parameter _-f cd_ records in CD quality.


### 4.2 Sound-check of the external USB audio device

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


```...```

---

## This repository hosts different GitHub branches:
* One with the 'falkTX' version and 
* the other with the 'markc' version. 
* snd-aloop_in-progress: In progress :: A new sound setup (multiple sound devices) from scratch

---

## Helpful links:
* wiki.gentoo.org/wiki/ALSA#Configuration
