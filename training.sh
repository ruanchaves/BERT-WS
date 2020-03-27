cd /home
DATABASE=$DATABASE python run_cut.py \
    --task_name="people" \
    --do_train=True \
    --do_predict=False \
    --data_dir=$DATA_DIR \
    --vocab_file=$MODEL_DIR/vocab.txt \
    --bert_config_file=$MODEL_DIR/bert_config.json \
    --init_checkpoint=$MODEL_DIR/bert_model.ckpt \
    --do_lower_case=False \
    --max_seq_length=128 \
    --train_batch_size=32 \
    --learning_rate=2e-5 \
    --num_train_epochs=4.0 \
    --output_dir=$OUTPUT_DIR