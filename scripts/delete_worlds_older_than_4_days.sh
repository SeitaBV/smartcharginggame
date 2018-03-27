#!/bin/bash
#
# This script deletes all pickled worlds older than four days.
# Useful to keep the size of the worlds/ directory in check (e.g. when used as a cron job).
#

SCRIPT_DIR=`dirname $(readlink -f "$0")`
find $SCRIPT_DIR/../worlds/*.pickle -mtime +4 -print -exec rm {} \;
