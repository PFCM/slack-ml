#! /bin/sh
echo "GAE deployment starting..."
# deploys to app engine
if [ ! -d $HOME/google-cloud-sdk ]; then
    echo "installing gcloud"
    curl https://sdk.cloud.google.com | bash;
fi
# authenticate
echo "authenticating"
gcloud auth activate-service-account --key-file client-secret.json

# and deploy, add extra modules here
echo "deploying"
gcloud -q preview app deploy app.yaml msg/msg.yaml
# run end-to-end tests?
