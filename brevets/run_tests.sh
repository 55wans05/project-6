#!/bin/bash

for t in tests/*.py
do
    nosetests -I $t
done
