# Domain Adaptation of Transformers for English Word Segmentation

Supporting code for the paper "Domain Adaptation of Transformers for English Word Segmentation".

This is a only slightly modified version of the original repository to work with Western languages.

In order to reproduce our results, please utilize the BERT-Mini model made available at [googleresearch/bert](https://github.com/google-research/bert) instead of BERT-Base Chinese.

For more information about this project, please refer to the [original README](https://github.com/jiangpinglei/BERT_ChineseWordSegment).

# Citation

```
@InProceedings{10.1007/978-3-030-61377-8_33,
author="Rodrigues, Ruan Chaves
and Rocha, Acquila Santos
and Inuzuka, Marcelo Akira
and do Nascimento, Hugo Alexandre Dantas",
editor="Cerri, Ricardo
and Prati, Ronaldo C.",
title="Domain Adaptation of Transformers for English Word Segmentation",
booktitle="Intelligent Systems",
year="2020",
publisher="Springer International Publishing",
address="Cham",
pages="483--496",
abstract="Word segmentation can contribute to improve the results of natural language processing tasks on several problem domains, including social media sentiment analysis, source code summarization and neural machine translation. Taking the English language as a case study, we fine-tune a Transformer architecture which has been trained through the Pre-trained Distillation (PD) algorithm, while comparing it to previous experiments with recurrent neural networks. We organize datasets and resources from multiple application domains under a unified format, and demonstrate that our proposed architecture has competitive performance and superior cross-domain generalization in comparison with previous approaches for word segmentation in Western languages.",
isbn="978-3-030-61377-8"
}
```
