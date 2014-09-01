#!/bin/bash

yum -y install rpmdevtools rpmlint @development-tools fedora-packager mock 

VUSER=vagrant
VIMFILE=/home/$VUSER/.vimrc
(
cat <<EOF
set expandtab
set nu
set tabstop=4
set shiftwidth=4
EOF
) > $VIMFILE

chown $VUSER. $VIMFILE

rpmdev-setuptree
mv /root/rpmbuild /home/$VUSER

setenforce 0

hostnamectl set-hostname "pyvmomi.rpm.local"

cp /$VUSER/*.spec /home/$VUSER/rpmbuild/SPECS
cd /home/$VUSER/rpmbuild/SOURCES
spectool -g ../SPECS/*.spec
chown -R $VUSER. /home/$VUSER/rpmbuild
