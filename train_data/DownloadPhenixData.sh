#!/bin/bash

set -e

#wget http://tenhou.net/0/log/mjlog_pf4-20_n1.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n2.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n3.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n4.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n5.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n6.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n7.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n8.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n9.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n10.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n11.zip
#wget http://tenhou.net/0/log/mjlog_pf4-20_n12.zip

unzip mjlog_pf4-20_n1.zip
unzip mjlog_pf4-20_n2.zip
unzip mjlog_pf4-20_n3.zip
unzip mjlog_pf4-20_n4.zip
unzip mjlog_pf4-20_n5.zip
unzip mjlog_pf4-20_n6.zip
unzip mjlog_pf4-20_n7.zip
unzip mjlog_pf4-20_n8.zip
unzip mjlog_pf4-20_n9.zip
unzip mjlog_pf4-20_n10.zip
unzip mjlog_pf4-20_n11.zip
unzip mjlog_pf4-20_n12.zip

rm mjlog_pf4-20_n*.zip

echo
echo "Successfully extracted zip files, now decompress mjlog(NTFS gzip) files..."
gzip -d -r mjlog_pf4-20_n*/ -S .mjlog
echo "Done."

