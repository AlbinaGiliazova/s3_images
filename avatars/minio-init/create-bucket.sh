#!/bin/sh
set -e

mc alias set myminio http://localhost:9000 minioadmin minioadmin
mc mb --ignore-existing myminio/avatars