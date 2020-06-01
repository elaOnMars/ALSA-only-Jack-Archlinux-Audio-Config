# In progress :: A new sound setup (multiple sound devices) from scratch 
### with ALSA, Loopback devices, USB Audio, built-in HDA Audio and Jack

In contrast to the other branches this branch describes the steps to set up a working and 
solid ALSA based sound system from scratch

## Which capatibilies my sound system should have?
* Switching easily between on-board sound and the external USB sound device.
* Hearing sound in every (non-ALSA) capable webrowser.
* Using the microphone in most applications. In parallel I like to mix different sound channels with recording software like Ardour. That means: I like to fetch every real sound which are on several loopback devices.


## Sound devices:
* HDA Intel (model ALC269-dmic)
* PreSonus AudioBox 44VSL
* ALSA Loopback devices

---

# Steps to set up a sound system:

__1. Start with a unchanged ALSA configuration__

If you start re-configuring ALSA from scratch you should initialize the ALSA driver to a default state with:
```
alsactl init
```

__2. Define the order of the sound cards loaded globally__

Creata a module file _snd.conf_ in _/etc/modprobe.d/_ with the following content:
```
# 1. HDA Intel (PCH) - index=0    # change the model to your sound card model or to _model=auto_.
# 2. USB AUdio (VSL) - index=1
# 3. Loopback - index=2

options snd slots=snd-hda-intel index=0 snoop=1 model=alc269-dmic,slots=snd-usb-audio index=1,slots=snd-aloop index=2
```
Hint: You can define in your _~/.asoundrc_ which card shall be used as the default sound card.


__3. Load the module _snd_ at startup__

Create a file _snd.conf_ in _/etc/modules-load.de/_ with the following word:

```
snd
```
Save and close the file.

Reboot and check that the module was loaded with _modinfo -p snd_.

__3. ... __

```...```

---

## This repository hosts different GitHub branches:
* One with the 'falkTX' version and 
* the other with the 'markc' version. 
* snd-aloop_in-progress: In progress :: A new sound setup (multiple sound devices) from scratch
