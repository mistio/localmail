#!/bin/bash
twistd localmail
python -m unittest discover -s localmail -b
sh kill_localmail.sh
