#!/usr/bin/env bash

FILES_DIR="/var/ip6.backend/generated"
EXPORT_DIR="$FILES_DIR/pb"
rm -R $EXPORT_DIR
scp -r root@ip6:$EXPORT_DIR $FILES_DIR
ls $EXPORT_DIR