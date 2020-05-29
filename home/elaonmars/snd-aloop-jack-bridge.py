#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Put this python script in your $PATH (e. g. /usr/local/bin)
# It should function also with pulseaudio.
# Script friendly fetched from http://gamesplusone.com/alsa_to_jack.html and 
# originally hosted on the WineHQ Sound wiki page http://wiki.winehq.org/Sound
# and written and developed by falkTX of KXStudio http://kxstudio.sourceforge.net/Main_Page .


# How to use:
# -----------
# * Start JACK (you need JACK2 not JACK1)
# * Run this script in your terminal to activate the snd-aloop bridge. Running it in qjackctl will crash qjackctl
#   without crashing jackd.
#
# You system and capture ports are connect now. 
# "It will also auto-adapt to jack buffer size changes while running. This has been tested and 
# proved to work with multiple ALSA streams playing at the same time."

# If you stop the script the sound output will stop for sure.



# Imports (Global)
from ctypes import *
from os import system
from sys import version_info
from signal import signal, SIGINT, SIGTERM
from time import sleep

# --------------------------------------------------
# Test for python 3.x
if (version_info >= (3,0)):
  PYTHON3 = True
else:
  PYTHON3 = False

# --------------------------------------------------
# Global loop check
global doLoop, doRunNow
doLoop   = True
doRunNow = True

# --------------------------------------------------
# Global JACK variables
global sample_rate, buffer_size
sample_rate = 44100
buffer_size = 1024

# --------------------------------------------------
# JACK ctypes implementation
jacklib = cdll.LoadLibrary("libjack.so.0")

class jack_client_t(Structure):
  _fields_ = []

jack_nframes_t = c_uint32

JackBufferSizeCallback = CFUNCTYPE(c_int, jack_nframes_t, c_void_p)
JackShutdownCallback = CFUNCTYPE(None, c_void_p)

def jack_client_open(client_name, options, status):
  if (PYTHON3): client_name = client_name.encode("ascii")
  jacklib.jack_client_open.argtypes = [c_char_p, c_int, POINTER(c_int)]
  jacklib.jack_client_open.restype = POINTER(jack_client_t)
  return jacklib.jack_client_open(client_name, options, status)

def jack_client_close(client):
  jacklib.jack_client_close.argtypes = [POINTER(jack_client_t)]
  jacklib.jack_client_close.restype = c_int
  return jacklib.jack_client_close(client)

def jack_activate(client):
  jacklib.jack_activate.argtypes = [POINTER(jack_client_t)]
  jacklib.jack_activate.restype = c_int
  return jacklib.jack_activate(client)

def jack_deactivate(client):
  jacklib.jack_deactivate.argtypes = [POINTER(jack_client_t)]
  jacklib.jack_deactivate.restype = c_int
  return jacklib.jack_deactivate(client)

def jack_connect(client, source_port, destination_port):
  if (PYTHON3): source_port = source_port.encode("ascii")
  if (PYTHON3): destination_port = destination_port.encode("ascii")
  jacklib.jack_connect.argtypes = [POINTER(jack_client_t), c_char_p, c_char_p]
  jacklib.jack_connect.restype = c_int
  return jacklib.jack_connect(client, source_port, destination_port)

def jack_get_sample_rate(client):
  jacklib.jack_get_sample_rate.argtypes = [POINTER(jack_client_t)]
  jacklib.jack_get_sample_rate.restype = jack_nframes_t
  return jacklib.jack_get_sample_rate(client)

def jack_get_buffer_size(client):
  jacklib.jack_get_buffer_size.argtypes = [POINTER(jack_client_t)]
  jacklib.jack_get_buffer_size.restype = jack_nframes_t
  return jacklib.jack_get_buffer_size(client)

def jack_on_shutdown(client, shutdown_callback, arg):
  global _shutdown_callback
  _shutdown_callback = JackShutdownCallback(shutdown_callback)
  jacklib.jack_on_shutdown.argtypes = [POINTER(jack_client_t), JackShutdownCallback, c_void_p]
  jacklib.jack_on_shutdown.restype = None
  jacklib.jack_on_shutdown(client, _shutdown_callback, arg)

def jack_set_buffer_size_callback(client, bufsize_callback, arg):
  global _bufsize_callback
  _bufsize_callback = JackBufferSizeCallback(bufsize_callback)
  jacklib.jack_set_buffer_size_callback.argtypes = [POINTER(jack_client_t), JackBufferSizeCallback, c_void_p]
  jacklib.jack_set_buffer_size_callback.restype = c_int
  return jacklib.jack_set_buffer_size_callback(client, _bufsize_callback, arg)

# --------------------------------------------------
# quit on SIGINT or SIGTERM
def signal_handler(sig, frame=0):
  global doLoop
  doLoop = False

# --------------------------------------------------
# listen to jack shutdown
def shutdown_callback(arg):
  global doLoop
  doLoop = False

# --------------------------------------------------
# listen to jack buffer size changes
def buffer_size_callback(new_buffer_size, arg):
  global doRunNow, buffer_size
  buffer_size = new_buffer_size
  doRunNow = True
  return 0

# --------------------------------------------------
# run alsa_in and alsa_out
def run_alsa_bridge():
  global sample_rate, buffer_size
  system("killall alsa_in alsa_out pulseaudio")
  system("env JACK_SAMPLE_RATE=%i JACK_PERIOD_SIZE=%i alsa_in -j alsa_in -dcloop -q 1 2>&1 1> /dev/null &" % (sample_rate, buffer_size))
  system("env JACK_SAMPLE_RATE=%i JACK_PERIOD_SIZE=%i alsa_out -j alsa_out -dploop -q 1 2>&1 1> /dev/null &" % (sample_rate, buffer_size))

  # Pause it for a bit, and connect to the proper system ports
  sleep(1)
  jack_connect(client, "alsa_in:capture_1", "system:playback_1")
  jack_connect(client, "alsa_in:capture_2", "system:playback_2")
  jack_connect(client, "system:capture_1", "alsa_out:playback_1")
  jack_connect(client, "system:capture_2", "alsa_out:playback_2")

#--------------- main ------------------
if __name__ == '__main__':

  # Init JACK client
  client = jack_client_open("jack-aloop-daemon", 0, None)

  if (not client):
    quit()

  jack_on_shutdown(client, shutdown_callback, None)
  jack_set_buffer_size_callback(client, buffer_size_callback, None)
  jack_activate(client)

  # Quit when requested
  signal(SIGINT, signal_handler)
  signal(SIGTERM, signal_handler)

  # Get initial values
  sample_rate = jack_get_sample_rate(client)
  buffer_size = jack_get_buffer_size(client)

  # Keep running until told otherwise
  while (doLoop):
    if (doRunNow):
      run_alsa_bridge()
      doRunNow = False
    sleep(1)

  # Close JACK client
  jack_deactivate(client)
  jack_client_close(client)


