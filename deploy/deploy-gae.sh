#! /bin/sh
echo "GAE deployment starting..."
# deploys to app engine
# this is pretty much taken from travis-dpl except that
# it works for more than one module
BASE='https://dl.google.com/dl/cloudsdk/channels/rapid/'
NAME='google-cloud-sdk'
EXT='.tar.gz'
INSTALL='~'
BOOTSTRAP="${INSTALL}/${NAME}/bin/bootstrapping/install.py"
GCLOUD="${INSTALL}/${NAME}/bin/gcloud"

if [ ! -d $HOME/google-cloud-sdk ]; then
    echo "downloading"
    curl -L ${BASE}${NAME}${EXT} | gzip -d | tar -x -C $INSTALL

    echo "bootstrapping"
    $BOOTSTRAP --usage-reporting=false --command-completion=false --path-update=false
fi
# authenticate
echo "authenticating"
gcloud auth activate-service-account --key-file client-secret.json

# and deploy, add extra modules here
echo "deploying"
gcloud -q preview app deploy $@
# run end-to-end tests?
