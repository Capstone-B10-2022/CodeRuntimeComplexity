### app.py file ###

# Packages needed for all 10 features in the article

import yaml
import streamlit as st
import contextlib
import os
import subprocess
import sys
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import pandas as pd
import datetime
import pickle
import base64
from sys import platform
import matplotlib.pyplot as plt
import numpy as np
import ast
import glob
import time
import signal
import psutil
import re
import json
import shutil
from pathlib import Path
import socket

# Import app configurations

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), configs_file)) as f:
    configs = yaml.load(f.read())
configs['APP_BASE_DIR'] = os.path.dirname(os.path.realpath(__file__))

# Helper functions

## Sessions state implementation, taken from here: 
## https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074/48

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()

    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False

        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)

def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")

    return session_info.session

def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_stat

## My functions

def autosave_session(state):
   # The session file is saved in the path saved in the state key called state.session_autosave_file_abs, which is declared in the beginning of the script
    with open(str(state.session_autosave_file_abs), 'wb') as outf:
        pickle.dump(state._state['data'], outf)
        
def is_shutdown_line(shutdown_line):
    return "Shutting down" in shutdown_line

def get_last_n_lines_of_file(file, n):
    with open(file, "r") as file:
        lines = file.readlines()
    return lines[-n:]

def was_session_shutdown(state):
    # If an unexpected shutdown happened and the session was restarted, the debug log 24th or 25th lines will have a shutdown message (at least in my case)
    list_of_files = glob.glob(
        configs['APP_BASE_DIR'] + '/logs/streamlit_logs/*')
    state.streamlit_log = max(list_of_files, key=os.path.getmtime)
    last_25_streamlit_log_lines = get_last_n_lines_of_file(state.streamlit_log, 25)
    shutdown_session_line = last_25_streamlit_log_lines[0]
    shutdown_session_line_after = last_25_streamlit_log_lines[1]
    session_was_shutdown = is_shutdown_line(shutdown_session_line) or is_shutdown_line(shutdown_session_line_after)
    return session_was_shutdown

def load_autosaved_session(state, login=False):
    try:
            with open(str(state.session_autosave_file_abs), 'rb') as inf:
                state._state['data'] = pickle.load(inf)
                if not login:
                    # logout user if security policy requires
                    state.user = ''
                    state.password = ''
                    state.authenticated = False
    except FileNotFoundError:  # someone deleted the sessions file
        pass
    
# Implementation

if __name__ == "__main__":
    state = _get_state()
    session_was_shutdown = was_session_shutdown(state)
    state.session_autosave_file_abs = os.path.join(configs['APP_BASE_DIR'], configs['MODELS_DIR'], '') + str("\~session_auto_save.pickle")
    if session_was_shutdown:  
        load_autosaved_session(state)