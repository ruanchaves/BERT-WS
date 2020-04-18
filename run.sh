ENTRYPOINT=training.sh CUDA_VISIBLE_DEVICES=0 ENV_LIST=envlist/env1.list bash start.sh
ENTRYPOINT=training.sh CUDA_VISIBLE_DEVICES=0 ENV_LIST=envlist/env2.list bash start.sh
ENTRYPOINT=training.sh CUDA_VISIBLE_DEVICES=0 ENV_LIST=envlist/env3.list bash start.sh
ENTRYPOINT=training.sh CUDA_VISIBLE_DEVICES=0 ENV_LIST=envlist/env4.list bash start.sh