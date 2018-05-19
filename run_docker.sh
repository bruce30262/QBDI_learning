#!/usr/bin/env sh
work_dir=$1
docker run -e TERM --privileged --security-opt seccomp:unconfined -v $work_dir:/mnt/files --name=qbdi -it bruce30262/qbdi:ubuntu_lts_16.04 /bin/bash
