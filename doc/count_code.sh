#!/bin/bash

BASEDIR=$(dirname "$0")

cd "$BASEDIR"/

cloc ../ --exclude-ext=xml --exclude-dir=json,mjlog_pf4-20_n1,mjlog_pf4-20_n2,mjlog_pf4-20_n3,mjlog_pf4-20_n4,mjlog_pf4-20_n5,mjlog_pf4-20_n6,mjlog_pf4-20_n7,mjlog_pf4-20_n8,mjlog_pf4-20_n9,mjlog_pf4-20_n10,mjlog_pf4-20_n11,mjlog_pf4-20_n12

