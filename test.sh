#!/bin/bash

run_old()
{
    echo -n "Running $1..."
    python $1 &> .log
    if [ $? -eq 0 ]
    then
        echo "passed"
    else
        echo "failed"
        echo "Log: "
        cat .log
    fi
    rm -f .log
}

echo -n "Starting localmail..."
twistd localmail
echo "done"

echo "Running new funtional tests"
python -m unittest discover -s localmail -b

run_old localmail/tests/simple.py
sh kill_localmail.sh

# starts up it's own server
run_old localmail/tests/thread.py
