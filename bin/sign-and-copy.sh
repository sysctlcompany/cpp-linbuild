#!/bin/bash

SRC=.
DEST=/efs/shibwww/mirror/yum
COMP=shibresolver
VER=3.5.0
CP="cp -av"

SIGN=1
COPY=1

ARCH=aarch64
#ARCH=i686
#ARCH=noarch

if [ $SIGN == 1 ] ; then
find $SRC/os -name "*${COMP}*${VER}*" | xargs rpmsign --addsign
fi

if [ $COPY == 1 ] ; then

$CP $SRC/os/amazonlinux2/products/SRPMS/*${COMP}*${VER}* $DEST/amazonlinux2/src/
$CP $SRC/os/amazonlinux2/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/amazonlinux2/$ARCH/

$CP $SRC/os/amazonlinux2023/products/SRPMS/*${COMP}*${VER}* $DEST/amazonlinux2023/src/
$CP $SRC/os/amazonlinux2023/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/amazonlinux2023/$ARCH/

$CP $SRC/os/centos7/products/SRPMS/*${COMP}*${VER}* $DEST/CentOS_7/src/
$CP $SRC/os/centos7/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/CentOS_7/$ARCH/

$CP $SRC/os/centos8/products/SRPMS/*${COMP}*${VER}* $DEST/CentOS_8/src/
$CP $SRC/os/centos8/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/CentOS_8/$ARCH/

$CP $SRC/os/rockylinux8/products/SRPMS/*${COMP}*${VER}* $DEST/rockylinux8/src/
$CP $SRC/os/rockylinux8/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/rockylinux8/$ARCH/

$CP $SRC/os/rockylinux9/products/SRPMS/*${COMP}*${VER}* $DEST/rockylinux9/src/
$CP $SRC/os/rockylinux9/products/RPMS/$ARCH/*${COMP}*${VER}* $DEST/rockylinux9/$ARCH/

fi
