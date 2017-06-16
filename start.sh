#!/bin/sh

export PYTHONPATH="${PYTHONPATH}:/home/pi/speech"

python recognizer.py &
python intentworker.py &
python sayclient.py &
python openhabconn.py &

