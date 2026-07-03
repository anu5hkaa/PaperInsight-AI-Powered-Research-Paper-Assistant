# ==========================================================
# QUESTION ANSWERING PROMPT
# ==========================================================

def build_qa_prompt(question, context):

    prompt = f"""
You are an expert AI Research Assistant.

Answer the user's question ONLY using the provided research paper context.

Instructions:

- Answer accurately.
- Do NOT hallucinate.
- If the answer is not present, clearly say:
  "The provided context does not contain enough information."
- Explain the concept in simple language.
- Mention important technical terms where necessary.
Keep the response under 700 words.

Be concise.

Avoid repeating the same information.

End with a 5-line conclusion
======================
Context
======================

{context}

======================
Question
======================

{question}

"""

    return prompt


# ==========================================================
# SUMMARIZATION PROMPT
# ==========================================================

def build_summary_prompt(context):

    prompt = f"""
You are an expert AI Research Assistant.

Below is an entire research paper.

Generate a comprehensive summary.

Your summary must include:

1. Paper Objective

2. Problem Statement

3. Methodology

4. Model Architecture

5. Training Procedure

6. Dataset Used

7. Experiments

8. Results

9. Advantages

10. Limitations

11. Applications

12. Future Work

13. Final Conclusion

Rules:

• Use ONLY the provided paper.
• Do NOT add information outside the paper.
• If some section is unavailable, explicitly state that the paper does not provide sufficient information.
• Write in proper paragraphs.
• Use headings.
Keep the response under 700 words.

Be concise.

Avoid repeating the same information.

End with a 5-line conclusion
======================
Research Paper
======================

{context}

"""

    return prompt


# ==========================================================
# COMPARISON PROMPT
# ==========================================================

def build_comparison_prompt(context):

    return f"""
You are an expert research assistant.

Compare these two research papers.
Keep the response under 700 words.

Be concise.

Avoid repeating the same information.

End with a 5-line conclusion
Context:

{context}

Generate a structured comparison with the following sections:

# Overview

# Objective

# Proposed Method

# Architecture

# Training

# Dataset

# Results

# Advantages

# Limitations

# Applications

# Similarities

# Differences

# Conclusion

Use markdown headings.

Only use the provided summaries.

Do not hallucinate.
"""



# ==========================================================
# CITATION PROMPT
# ==========================================================

def build_citation_prompt(question, context):

    prompt = f"""
You are an expert AI Research Assistant.
Keep the response under 700 words.

Be concise.

Avoid repeating the same information.

End with a 5-line conclusion
Answer the user's question using ONLY the provided context.

After every important statement,

append its citation using the format:

[Paper Name | Page Number]

Never invent citations.

======================
Context
======================

{context}

======================
Question
======================

{question}

"""

    return prompt


# ==========================================================
# FIGURE UNDERSTANDING PROMPT
# ==========================================================

def build_figure_prompt(question, context):

    prompt = f"""
You are an expert AI Research Assistant.
Keep the response under 700 words.

Be concise.

Avoid repeating the same information.

End with a 5-line conclusion
The context below contains extracted figures,
captions and nearby explanations.

Explain the requested figure.

Include:

1. What the figure represents

2. What each component means

3. Why the figure is important

4. Relation with the paper

Use ONLY the provided context.

======================
Context
======================

{context}

======================
Question
======================

{question}

"""

    return prompt

def build_specific_comparison_prompt(question, context):

    prompt = f"""
You are an expert AI Research Scientist.

You are given retrieved passages from TWO research papers.

Your task is to compare them in detail.

User Question:
{question}

Context:

{context}

Instructions:
{
  "comparision": "The retrieved passages describe the BERT model (Paper A) and the Transformer model introduced in \"Attention Is All You Need\" (Paper B). BERT's architecture is explicitly stated to be a multi-layer bidirectional Transformer encoder based on the original implementation described in Vaswani et al. (2017), which is Paper B. Therefore, BERT leverages the core Transformer encoder architecture. The comparison will highlight the foundational aspects of the Transformer and BERT's specific adaptations.\n\n---\n\n## 1. Paper Objective\n\n**BERT (Paper A):**\nThe main goal of BERT is to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. The pre-trained BERT model can then be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks without substantial task-specific architecture modifications.\n\n**Attention Is All You Need (Paper B):**\nThe main goal of this paper is to propose the Transformer, a model architecture that eschews recurrence and convolutions, relying entirely on attention mechanisms to draw global dependencies. The aim is to achieve significantly more parallelization and faster training while reaching a new state of the art in translation quality.\n\n---\n\n## 2. Problem Addressed\n\n**BERT (Paper A):**\nBERT addresses the problem of needing heavily-engineered task-specific architectures for various NLP tasks. It aims to provide a unified architecture that, through pre-training deep bidirectional representations, reduces the need for such customization and achieves state-of-the-art performance across a large suite of tasks by simple fine-tuning. It also addresses the limitations of previous representation models like OpenAI GPT (which uses left-to-right attention) and ELMo (which uses shallow concatenation of independently trained LMs).\n\n**Attention Is All You Need (Paper B):**\nThis paper addresses the limitations of sequence transduction models that rely on recurrent or convolutional layers, particularly their sequential nature, which hinders parallelization and slows down training. It seeks to overcome these challenges by introducing a model based solely on attention mechanisms, allowing for faster training and better performance by modeling dependencies regardless of their distance.\n\n---\n\n## 3. Model Architecture\n\n**BERT (Paper A):**\n*   **Encoder:** BERT's model architecture is a multi-layer bidirectional Transformer **encoder**. It is based on the original implementation described in Vaswani et al. (2017).\n*   **Decoder:** Not mentioned in the retrieved context as part of BERT's core pre-training architecture. BERT is presented as an encoder-only model for representation learning.\n*   **Attention mechanism:** Uses **bidirectional self-attention**, meaning every token can attend to context to both its left and right. This is a critical distinction from OpenAI GPT, which uses constrained left-to-right attention. It also uses self-attention to unify the encoding of concatenated text pairs, effectively including bidirectional cross-attention between sentences.\n*   **Layers:** Multi-layer Transformer encoder. Two model sizes are mentioned: BERTBASE has L=12 layers, and BERTLARGE has L=24 layers. Each layer's feed-forward/filter size is 4H (e.g., 3072 for H=768).\n*   **Embeddings:** Mentions \"Input/Output Representations\" to handle various downstream tasks, implying token embeddings.\n*   **Positional Encoding:** Not explicitly detailed in the retrieved context, beyond being part of the \"Input/Output Representations\".\n*   **Bidirectionality:** A distinctive feature. BERT is designed to pre-train deep **bidirectional** representations by jointly conditioning on both left and right context in all layers.\n\n**Attention Is All You Need (Paper B):**\n*   **Encoder:** The Transformer uses an encoder-decoder structure. The encoder maps an input sequence of symbol representations to a sequence of continuous representations. It consists of N=6 identical layers. Each layer has two sub-layers: a multi-head self-attention mechanism and a position-wise fully connected feed-forward network.\n*   **Decoder:** The decoder also consists of N=6 identical layers. Each decoder layer has three sub-layers: a masked multi-head self-attention layer (which prevents attending to subsequent positions), an encoder-decoder multi-head attention layer (where queries come from the previous decoder layer, and keys/values come from the encoder output), and a position-wise fully connected feed-forward network.\n*   **Attention mechanism:**\n    *   **Scaled Dot-Product Attention:** The fundamental attention function is `Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V`. This scaled dot-product attention is faster and more space-efficient than additive attention.\n    *   **Multi-Head Attention:** Employs `h=8` parallel attention layers (heads). Each head uses `d_k = d_v = d_model/h = 64`. Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions.\n    *   **Applications of Multi-Head Attention:** Used in three ways:\n        1.  **Encoder Self-Attention:** All queries, keys, and values come from the output of the previous layer in the encoder.\n        2.  **Masked Decoder Self-Attention:** All queries, keys, and values come from the output of the previous layer in the decoder, but masking is applied to prevent attending to future positions.\n        3.  **Encoder-Decoder Attention:** Queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder.\n*   **Layers:** Both the encoder and decoder are composed of N=6 identical layers. Each layer includes residual connections and layer normalization.\n*   **Embeddings:** Uses \"learned embeddings\" for input tokens.\n*   **Positional Encoding:** Positional encodings are added to the input embeddings at the bottom of the encoder and decoder stacks. The paper primarily uses **sinusoidal positional embeddings**, which may allow the model to extrapolate to sequence lengths longer than those encountered during training. Learned positional embeddings were also experimented with and yielded nearly identical results.\n*   **Bidirectionality:** The encoder's self-attention is bidirectional. However, the decoder's self-attention is explicitly **masked** to be unidirectional (left-to-right) to ensure that predictions for a given position depend only on known outputs at earlier positions.\n\n---\n\n## 4. Training Methodology\n\n**BERT (Paper A):**\n*   **Pretraining:** BERT is designed to pre-train deep bidirectional representations from unlabeled text. It uses specific pre-training tasks (mentioned as Section 3.1, but details not fully provided in context). One mentioned task, Masked Language Model (MLM), converges marginally slower than left-to-right models but offers significant empirical improvements. Another task, Next Sentence Prediction, is also mentioned.\n*   **Fine-tuning:** Fine-tuning is straightforward. Users simply plug in task-specific inputs and outputs into BERT and fine-tune all parameters end-to-end. It generally requires only one additional output layer.\n*   **Loss Function:** Not mentioned in the retrieved context.\n*   **Optimization:** Not mentioned in the retrieved context.\n\n**Attention Is All You Need (Paper B):**\n*   **Pretraining:** Not mentioned. The paper describes training for specific translation tasks from scratch, rather than a separate pre-training phase.\n*   **Fine-tuning:** Not mentioned in the retrieved context.\n*   **Loss Function:** Not mentioned in the retrieved context.\n*   **Optimization:** Not mentioned in the retrieved context.\n\n---\n\n## 5. Dataset\n\n**BERT (Paper A):**\nFor evaluation and fine-tuning, BERT achieves state-of-the-art results on:\n*   GLUE benchmark\n*   MultiNLI (MNLI)\n*   SQuAD v1.1 question answering\n*   SQuAD v2.0\n\nThe specific unlabeled text corpus used for pre-training is not detailed in the retrieved context, beyond being a \"large text corpus\" similar to OpenAI GPT.\n\n**Attention Is All You Need (Paper B):**\nThe Transformer was trained and evaluated on:\n*   WMT 2014 English-to-German translation task\n*   WMT 2014 English-to-French translation task\n\n---\n\n## 6. Experimental Results\n\n**BERT (Paper A):**\n*   Achieves new state-of-the-art results on eleven natural language processing tasks.\n*   Pushes the GLUE score to 80.5% (a 7.7% absolute improvement).\n*   MultiNLI accuracy to 86.7% (a 4.6% absolute improvement).\n*   SQuAD v1.1 Test F1 to 93.2 (a 1.5 point absolute improvement).\n*   SQuAD v2.0 Test F1 to 83.1.\n*   BERTBASE and BERTLARGE substantially outperform all prior systems on all tasks mentioned. BERTLARGE significantly outperforms BERTBASE.\n\n**Attention Is All You Need (Paper B):**\n*   Achieves a new state of the art on both WMT 2014 English-to-German and WMT 2014 English-to-French translation tasks.\n*   For English-to-German, their best model outperforms even all previously reported ensembles.\n*   Achieves 28.4 BLEU on the WMT 2014 English-to-German task.\n*   Demonstrates significantly faster training times compared to recurrent or convolutional architectures.\n\n---\n\n## 7. Advantages\n\n**BERT (Paper A):**\n*   **Deep Bidirectional Representations:** Jointly conditions on left and right context in all layers, offering a richer representation.\n*   **Unified Architecture:** Provides a minimal difference between pre-trained and final downstream architectures, reducing the need for heavily-engineered task-specific models.\n*   **Empirically Powerful:** Achieves new state-of-the-art performance on a wide range of NLP tasks.\n*   **Fine-tuning Approach:** Simplifies adaptation to various tasks with just one additional output layer.\n*   **Conceptual Simplicity:** Easy to understand and apply.\n\n**Attention Is All You Need (Paper B):**\n*   **Dispenses with Recurrence and Convolutions:** Relies entirely on attention, addressing the limitations of prior architectures.\n*   **High Parallelization:** Allows for significantly more parallel computation, leading to faster training times.\n*   **Superior Quality:** Achieves new state-of-the-art translation quality.\n*   **Global Dependencies:** Models dependencies regardless of their distance in the input or output sequences.\n*   **Extrapolation to Longer Sequences:** Sinusoidal positional encoding may allow the model to generalize to sequence lengths longer than encountered during training.\n\n---\n\n## 8. Limitations\n\n**BERT (Paper A):**\n*   **MLM Training Cost:** The Masked Language Model (MLM) pre-training task converges marginally slower than left-to-right models, implying increased training cost.\n\n**Attention Is All You Need (Paper B):**\n*   **Sensitivity to Attention Heads:** Model quality drops if too few or too many attention heads are used.\n*   **Attention Key Size:** Reducing the attention key size (`dk`) hurts model quality, suggesting that determining compatibility is complex and the dot product might be too simplistic for compatibility function in some cases.\n\n---\n\n## 9. Applications\n\n**BERT (Paper A):**\n*   Question Answering (e.g., SQuAD)\n*   Language Inference (e.g., MultiNLI)\n*   General Language Understanding (e.g., GLUE benchmark)\n*   Sentence-level and token-level tasks broadly.\n\n**Attention Is All You Need (Paper B):**\n*   Machine Translation (e.g., WMT 2014 English-to-German, English-to-French).\n*   The authors express excitement about applying attention-based models to other tasks.\n\n---\n\n## 10. Key Differences\n\n| Feature               | BERT (Paper A)                                                                                                    | Attention Is All You Need (Paper B)                                                                           |\n| :-------------------- | :---------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |\n| **Primary Goal**      | Pre-train deep bidirectional language representations for fine-tuning on various downstream NLP tasks.            | Introduce the Transformer architecture, relying solely on attention, for sequence transduction (e.g., translation) with high parallelism. |\n| **Architecture Type** | Multi-layer bidirectional Transformer **Encoder** only.                                                           | Encoder-Decoder Transformer architecture.                                                                     |\n| **Bidirectionality**  | **Fully bidirectional** in all layers of the encoder (jointly conditions on left and right context).              | Encoder is bidirectional. Decoder uses **masked self-attention** (strictly left-to-right/unidirectional).     |\n| **Training Paradigm** | Pre-training (unlabeled text) followed by fine-tuning (task-specific data).                                     | Trained from scratch for specific tasks (e.g., translation); pre-training not mentioned.                      |\n| **Key Innovation**    | Applying the bidirectional Transformer encoder effectively for pre-training and fine-tuning general language understanding. | Proposing the Transformer model that completely eschews recurrence and convolutions in favor of attention.    |\n| **Positional Encoding** | Not explicitly detailed in the context.                                                                           | Primarily uses **sinusoidal positional embeddings** (also experimented with learned ones).                     |\n| **Specific Attention Masks** | Bidirectional self-attention.                                                                                     | Masked self-attention in the decoder to prevent attending to future tokens.                                   |\n| **Model Sizes**       | BERTBASE (L=12, H=768), BERTLARGE (L=24, H=1024).                                                                 | Encoder/Decoder each have N=6 layers. Multi-head attention uses h=8 heads, dk=dv=64.                         |"
}
1. Use ONLY the provided context.
2. Do NOT hallucinate.
3. If some information is missing, explicitly say:
   "Not mentioned in the retrieved context."

Compare the papers under ALL relevant headings whenever information is available.

## 1. Paper Objective

Explain the main goal of each paper.

---

## 2. Problem Addressed

What problem does each paper solve?

---

## 3. Model Architecture

Compare:

- Encoder
- Decoder
- Attention mechanism
- Layers
- Embeddings
- Positional Encoding
- Bidirectionality

---

## 4. Training Methodology

Compare:

- Pretraining
- Fine-tuning
- Loss Function
- Optimization

---

## 5. Dataset

Which datasets were used?

---

## 6. Experimental Results

Compare performance.

---

## 7. Advantages

List strengths of each paper.

---

## 8. Limitations

List limitations.

---

## 9. Applications

Mention practical applications.

---

## 10. Key Differences

Provide a concise comparison table.

Use markdown.

Return the answer in a clean structured format.

"""
    return prompt

