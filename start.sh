cd "$(dirname "${BASH_SOURCE[0]}")"

CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
PEOPLEcut="./PEOPLEdata"
BERT_CHINESE_DIR="chinese_L-12_H-768_A-12"
DATABASE=$DATABASE

DOCKER_MAJOR_VERSION_STRING=$(docker -v | grep -oP '([0-9]+)' | sed -n 1p)
DOCKER_MINOR_VERSION_STRING=$(docker -v | grep -oP '([0-9]+)' | sed -n 2p)
ps_test=$(docker ps -a)

DOCKER_MAJOR_VERSION=$((10#$DOCKER_MAJOR_VERSION_STRING))
DOCKER_MINOR_VERSION=$((10#$DOCKER_MINOR_VERSION_STRING))

if [[ $DOCKER_MAJOR_VERSION -ge 19  ]]; then
    if [[ $DOCKER_MINOR_VERSION -ge 3 ]]; then
        recent_version=1
    else
        recent_version=0
    fi
else
    recent_version=0
fi 

if [[ ! -z $ps_test ]]; then
    build_test=$(docker image ls | grep 'ruanchaves/bert.*1.0')
else
    build_test=$(sudo docker image ls | grep 'ruanchaves/bert.*1.0')
fi

if [[ -z $build_test ]] && [[ ! -z $ps_test ]]; then 
    docker build -t ruanchaves/bert:1.0 .
elif [[ -z $build_test ]] && [[ -z $ps_test ]]; then
    sudo docker build -t ruanchaves/bert:1.0 .
fi

if [[ -n $ps_test ]] && [[ $recent_version -eq 1 ]]; then
    docker run --gpus all \
        -v `pwd`:/home \
        --env PEOPLEcut=$PEOPLEcut \
        --env BERT_CHINESE_DIR=$BERT_CHINESE_DIR \
        --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
        --env DATABASE=$DATABASE \
        -it --rm ruanchaves/bert:1.0 bash /home/entrypoint.sh
elif [[ -n $ps_test ]] && [[ $recent_version -eq 0 ]]; then
    nvidia-docker run \
        -v `pwd`:/home \
        --env PEOPLEcut=$PEOPLEcut \
        --env BERT_CHINESE_DIR=$BERT_CHINESE_DIR \
        --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
        --env DATABASE=$DATABASE \
        -it --rm ruanchaves/bert:1.0 bash /home/entrypoint.sh
elif [[ -z $ps_test ]] && [[ $recent_version -eq 1 ]]; then
    sudo -E docker run --gpus all \
        -v `pwd`:/home \
        --env PEOPLEcut=$PEOPLEcut \
        --env BERT_CHINESE_DIR=$BERT_CHINESE_DIR \
        --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
        --env DATABASE=$DATABASE \
        -it --rm ruanchaves/bert:1.0 bash /home/entrypoint.sh
elif [[ -z $ps_test ]] && [[ $recent_version -eq 0 ]]; then
    sudo -E nvidia-docker run \
        -v `pwd`:/home \
        --env PEOPLEcut=$PEOPLEcut \
        --env BERT_CHINESE_DIR=$BERT_CHINESE_DIR \
        --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
        --env DATABASE=$DATABASE \
        -it --rm ruanchaves/bert:1.0 bash /home/entrypoint.sh
else
    echo "Not found."
fi