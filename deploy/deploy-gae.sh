#! /bin/bash

# deploys to app engine
if [ ! -f ${HOME}/google-cloud-sdk ]; then
    curl https://sdk.cloud.google.com | bash;
fi
# authenticate
gcloud auth activate-service-account --key-file client-secret.json

# and deploy, add extra modules here
gcloud -q preview app deploy app.yaml msg/msg.yaml
# run end-to-end tests?
