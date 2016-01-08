#! /bin/sh
echo "GAE deployment starting..."
# deploys to app engine
# this is pretty much taken from travis-dpl except that
# it works for more than one module
BASE='https://dl.google.com/dl/cloudsdk/channels/rapid/'
NAME='google-cloud-sdk'
EXT='.tar.gz'
INSTALL=$HOME
BOOTSTRAP="${INSTALL}/${NAME}/bin/bootstrapping/install.py"
GCLOUD="${INSTALL}/${NAME}/bin/gcloud"
URL=${BASE}${NAME}${EXT}

if [ ! -d $HOME/google-cloud-sdk ]; then
    echo "downloading from $URL"
    curl -L "$URL" | gzip -d | tar -x -C $INSTALL

    echo "bootstrapping"
    $BOOTSTRAP --usage-reporting=false --command-completion=false --path-update=false
fi
# authenticate
echo "authenticating"
$GCLOUD auth activate-service-account --key-file client-secret.json

# and deploy, add extra modules here
echo "deploying"
$GCLOUD -q preview app deploy $@
# run end-to-end tests?
# or probably do that in after_script
