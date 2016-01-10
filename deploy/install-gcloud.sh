#! /bin/sh

# installing gcloud

BASE='https://dl.google.com/dl/cloudsdk/channels/rapid/'
NAME='google-cloud-sdk'
EXT='.tar.gz'
INSTALL=$HOME
BOOTSTRAP="${INSTALL}/${NAME}/bin/bootstrapping/install.py"
GCLOUD="${INSTALL}/${NAME}/bin/gcloud"
URL=${BASE}${NAME}${EXT}

if [ ! -d $INSTALL/google-cloud-sdk ]; then
    echo "downloading from $URL"
    curl -L "$URL" | gzip -d | tar -x -C $INSTALL

    echo "bootstrapping"
    $BOOTSTRAP --usage-reporting=false --command-completion=false --path-update=false
    # installing app engine specific components
    $GCLOUD components install app-engine-python -q
fi
