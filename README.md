# Domain Adaptation of Transformers for English Word Segmentation

Supporting code for the paper "Domain Adaptation of Transformers for English Word Segmentation".

This is a only slightly modified version of the original repository to work with Western languages.

In order to reproduce our results, please utilize the BERT-Mini model made available at [googleresearch/bert](https://github.com/google-research/bert) instead of BERT-Base Chinese.

For more information about this project, please refer to the [original README](https://github.com/jiangpinglei/BERT_ChineseWordSegment), which is also reproduced below.

# BERT_ChineseWordSegment ( original README )

Try to implement a Chinese word segment work based on Google BERT!

The corpus is extracted from The People's Daily (Chinese: 人民日报, Renmin Ribao).

  <br />
  
First git clone https://github.com/google-research/bert.git

Second put the three scripts:  modeling.py、optimization.py、tokenization.py into this project, structure is as follows:

    BERT_ChinesewordSegment

        |____ PEOPLEdata
        |____ output
        |____ modeling.py
        |____ optimization.py
        |____ tokenization.py
        |____ run_cut.py
        |____ evaluation.py

Third download the Chinese pre-trained bert model [BERT-Base, Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)

And then set pre-trained model path and data path environment: $BERT_CHINESE_DIR、$PEOPLEcut

## run

```
python3 run_cut.py   --task_name="people"   --do_train=True   --do_predict=True  --data_dir=$PEOPLEcut    --vocab_file=$BERT_CHINESE_DIR/vocab.txt   --bert_config_file=$BERT_CHINESE_DIR/bert_config.json   --init_checkpoint=$BERT_CHINESE_DIR/bert_model.ckpt    --max_seq_length=128    --train_batch_size=32    --learning_rate=2e-5   --num_train_epochs=3.0    --output_dir=./output/result_cut/
```

It will take about 28 minutes with 3 epochs on a GPU.

This will produce an evaluate output like this:

```
INFO:tensorflow:***** Eval results *****
INFO:tensorflow:  count = 9925
INFO:tensorflow:  precision_avg = 0.9794
INFO:tensorflow:  recall_avg = 0.9780
INFO:tensorflow:  f1_avg = 0.9783
INFO:tensorflow:  error_avg = 0.0213
```
And the word segmentation results will be seen in ./output/result_cut/seg_result.txt

If you want learn more details, see the code analysis(in Chinese)[简书:BERT系列（五）——中文分词实践...](https://www.jianshu.com/p/be0a951445f4)
