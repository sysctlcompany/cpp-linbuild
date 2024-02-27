#!/bin/bash

SRC=.
DEST=shibwww@shibboleth.net:mirror/yum
COMP=shibboleth-embedded-ds
VER=1.3.0

scp $SRC/os/amazonlinux2/products/SRPMS/${COMP}*${VER}* $DEST/amazonlinux2/src/
scp $SRC/os/amazonlinux2/products/RPMS/noarch/${COMP}*${VER}* $DEST/amazonlinux2/noarch/

scp $SRC/os/amazonlinux2023/products/SRPMS/${COMP}*${VER}* $DEST/amazonlinux2023/src/
scp $SRC/os/amazonlinux2023/products/RPMS/noarch/${COMP}*${VER}* $DEST/amazonlinux2023/noarch/

scp $SRC/os/centos7/products/SRPMS/${COMP}*${VER}* $DEST/CentOS_7/src/
scp $SRC/os/centos7/products/RPMS/noarch/${COMP}*${VER}* $DEST/CentOS_7/noarch/

scp $SRC/os/centos8/products/SRPMS/${COMP}*${VER}* $DEST/CentOS_8/src/
scp $SRC/os/centos8/products/RPMS/noarch/${COMP}*${VER}* $DEST/CentOS_8/noarch/

scp $SRC/os/rockylinux8/products/SRPMS/${COMP}*${VER}* $DEST/rockylinux8/src/
scp $SRC/os/rockylinux8/products/RPMS/noarch/${COMP}*${VER}* $DEST/rockylinux8/noarch/

scp $SRC/os/rockylinux9/products/SRPMS/${COMP}*${VER}* $DEST/rockylinux9/src/
scp $SRC/os/rockylinux9/products/RPMS/noarch/${COMP}*${VER}* $DEST/rockylinux9/noarch/

