# 📖 Technical Overview

## 🌟 Reward Models
- ### BertScore

    Based on the paper [BERTSCORE: EVALUATING TEXT GENERATION WITH BERT](https://arxiv.org/pdf/1904.09675.pdf). It utilizes [BertScore](https://github.com/Tiiiger/bert_score) for evaluating translated text.
- ### VectorSim

    Inspired by the STransQuest technique from [TransQuest: Translation Quality Estimation with  Cross-lingual Transformers](https://aclanthology.org/2020.coling-main.445.pdf). But, instead of using XLM-RoBERTa we used [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) to compute the similarity of the source and translated texts.

## 📚 Datasets
Validators use text from following datasets as a prompt for a text generation model that produces text which is then sent to miners. 


- ### BitTranslate Datasets
    **Source:** Open-sourced datasets for 7 languages on BitTranslate.<br>
    **Hugging Face:** [datasets](https://huggingface.co/BitTranslate)<br>
    **Used For:** Estonian, Persian, Finnish, French, Korean, Swedish, Ukrainian.

- ### Exams
    **Paper:** [EXAMS: A Multi-subject High School Examinations Dataset for Cross-lingual and Multilingual Question Answering](https://aclanthology.org/2020.emnlp-main.438.pdf)<br>
    **Hugging Face:** [exams](https://huggingface.co/datasets/exams)<br>
    **Used For:** Bulgarian, Chinese, Hungarian, Italian, Polish, Portuguese, Turkish, Vietnamese.

- ### GermanQuAD
    **Paper:** [GermanQuAD and GermanDPR: Improving Non-English Question Answering and Passage Retrieval](https://aclanthology.org/2021.mrqa-1.4.pdf)<br>
    **Hugging Face:** [deepset/germanquad](https://huggingface.co/datasets/deepset/germanquad)<br>
    **Used For:** German.
    
- ### PeerSum
    **Paper:** [Summarizing Multiple Documents with Conversational Structure for Meta-review Generation](https://arxiv.org/pdf/2305.01498.pdf)<br>
    **Hugging Face:** [oaimli/PeerSum](https://huggingface.co/datasets/oaimli/PeerSum)<br>
    **Used For:** English.

- ### xQuAD
    **Paper:** [On the cross-lingual transferability of monolingual representations](https://arxiv.org/pdf/1910.11856.pdf)<br>
    **Hugging Face:** [xquad](https://huggingface.co/datasets/xquad)<br>
    **Used For:** Arabic, Chinese, English, German, Greek, Spanish, Hindi, Romanian, Russian, Thai, Turkish, Vietnamese.

- ### MKQA
    **Paper:** [MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering](https://arxiv.org/pdf/2007.15207.pdf)<br>
    **Hugging Face:** [mkqa](https://huggingface.co/datasets/mkqa)<br>
    **Used For:** French.

## 🤖 Models
### mGPT
- **Paper:** [mGPT: Few-Shot Learners Go Multilingual](https://arxiv.org/pdf/2204.07580.pdf)
- **Hugging Face:** [ai-forever/mGPT](https://huggingface.co/ai-forever/mGPT)
- **Purpose:** Validators use this model to generate original text that's sent to miners.

### Wenzhong-GPT2-110M
- **Paper:** [Fengshenbang 1.0: Being the Foundation of Chinese Cognitive Intelligence](https://arxiv.org/pdf/2209.02970.pdf)
- **Hugging Face:** [IDEA-CCNL/Wenzhong-GPT2-110M](https://huggingface.co/IDEA-CCNL/Wenzhong-GPT2-110M)
- **Purpose:** Primarily used for producing Chinese text, serving a similar function as mGPT.

### M2M-100
- **Paper:** [Beyond English-Centric Multilingual Machine Translation](https://arxiv.org/pdf/2010.11125.pdf)
- **Hugging Face:** [facebook/m2m100_1.2B](https://huggingface.co/facebook/m2m100_1.2B)
- **Purpose:** The default model for miners to perform translations.

### Aya
- **Paper:** [Aya Model: An Instruction Finetuned Open-Access Multilingual Language Model](https://arxiv.org/pdf/2402.07827.pdf)
- **Hugging Face:** [CohereForAI/aya-101](https://huggingface.co/CohereForAI/aya-101)
- **Purpose:** An alternative model over M2M to perform translations.
