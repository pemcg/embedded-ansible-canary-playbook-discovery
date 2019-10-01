#!/bin/sh

path="$(pwd)"
init_path="roles"

if ansible-galaxy init --role-skeleton=../ansible-canary-role-development-application-signature-skeleton/ --init-path=$init_path amf-application-signature-$1; then
echo "role amf-application-signature-$1" "created at" $path"/"$init_path/amf-application-signature-$1
else
 :
fi




