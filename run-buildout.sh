#!/bin/sh
./bin/buildout $@ 2>&1 | tee buildout.log
