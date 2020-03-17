wget https://infufg.s3.amazonaws.com/ws-corpora.zip
unzip ws-corpora.zip
mkdir portuguese-bert-large
cd portuguese-bert-large
wget https://neuralmind-ai.s3.us-east-2.amazonaws.com/nlp/bert-large-portuguese-cased/bert-large-portuguese-cased_tensorflow_checkpoint.zip
wget https://neuralmind-ai.s3.us-east-2.amazonaws.com/nlp/bert-large-portuguese-cased/vocab.txt
unzip bert-large-portuguese-cased_tensorflow_checkpoint.zip

mv model.ckpt-1000000.data-00000-of-00001 bert_model.ckpt.data-00000-of-00001
mv model.ckpt-1000000.index bert_model.ckpt.index
mv model.ckpt-1000000.meta bert_model.ckpt.meta

rm bert-large-portuguese-cased_tensorflow_checkpoint.zip
cd ..
rm ws-corpora.zip