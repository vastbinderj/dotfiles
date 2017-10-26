#!/usr/bin/env bash

# set the environment and other vars
GXI_ENV=devint
USER=USERNAME@gxitestmail.com
PASS=PASSWORD
LIMIT=50

# cmds
CMD_GET_TOKEN='curl -s --request POST --header "x-realm: ocean/guests" --url "http://snap-proxy_80.$GXI_ENV.gxicloud.com:9999/auth?username=$USER&password=$PASS" | jq --raw-output .token'
CMD_GET_MEDIA='curl -s -X GET --header "Accept: application/json" --header "AuthToken: $AUTH_TOKEN" --header "X-Realm: ocean/guests" "http://snap-proxy_80.$GXI_ENV.gxicloud.com:9999/media/media/offset/0/limit/$LIMIT" | jq --raw-output ".items[] | .mediaId"'
CMD_DELETE='curl -s -X DELETE --header "Accept: application/json" --header "AuthToken: $AUTH_TOKEN" --header "X-Realm: ocean/guests" "http://snap-proxy_80.$GXI_ENV.gxicloud.com:9999/media-admin/media/$each/version/1" | jq --raw-output ".mediaId"'

# announce env
echo "Using GXI Env: $GXI_ENV"

# get a token
AUTH_TOKEN=$(eval $CMD_GET_TOKEN)
echo "AuthToken: " $AUTH_TOKEN

# create an array to store all media
declare -a mediaId
readarray -t mediaId < <(eval $CMD_GET_MEDIA)

# delete all media items
for each in "${mediaId[@]}"
do
echo "Deleting:" $(eval $CMD_DELETE)
done
