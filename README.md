### SENTENCE TRANSFORMER MODEL (all-MiniLM-L6-v2)

• High level (Project Idea) – built a local semantic intent classification system using sentence embeddings 
and a vector database, with confidence-based workflow routing. Exposed the semantic search system 
via a REST API and tested it using Postman with query parameters. 

• Given a user query → 
1. Find the most similar intent from Banking77 (sample dataset used) using semantic search 
2. Return Top-K intents 
3. Compute confidence score 
4. Decide next workflow based on confidence

• Architecture Overview

This project implements a semantic intent-matching pipeline using sentence embeddings and a vector database to power confident workflow decisions.

HuggingFace Dataset (PolyAI / Banking77)

            ↓
            
Sentence Transformer (Model: all-MiniLM-L6-v2)

            ↓
            
Vector Embeddings (384-d)

            ↓
            
Qdrant Vector Database (Cosine Similarity, Local / SQLite / Docker)

            ↓
            
User Query

            ↓
            
Query Embedding (384-d)

            ↓
            
Top-K Semantic Search (k = 3)

            ↓
            
Confidence Scoring (Boost if top-k labels match)

            ↓
            
Workflow Decision Engine

• Dataset  - 
- PolyAI/Bnaking 77, There are 77 intents related to banking sector
- Multiple utterances of each intent (10-13k queries) 
- Ex = “text” = “How do I change my card pin?” 
  “label” = 12 
- Store each utterance as a separate vector with intent_label, intent_name, utterance_text.

• Requirements - 
- sentence-transformers
- datasets 
- qdrant-client 
- fastapi 
- uvicorn 
- numpy 
- scikit-learn 
- torch
  
• Loading Dataset - 
- Each record has text, label.
- Later we’ll map label to intent_name. 
- Using load_datasets function
  
• Generate Embeddings - 
- From all the available model to test and understand the concept “all-MiniLM-L6-v2” is a good model, fast and accuracy-based judgement.
- Embeddings are normalized to ensure cosine function works properly (0-1)

• Ingesting dataset to Vector embedded DB 

• User Query  - 
- Returned result contains Similarity_score and payload. 
- Similarity_score = shows the cosine similarity 
- Payload = intent info 

• Confidence Score (Logic) - 
- Normalized is preferred as returning only the very first would have been naïve and there could have been better outcomes further. 
- It considers the absolute similarity & relative gap between the top and second top outcome. 

• Suggested Outcome  - 
- Hardcoded the sample workflows and let the system classify the text according to confidence_scores. 
- If >=0.75, then follow the desired workflow or else if >=0.50 & <0.75, ask for clarification or else fallback to human agent.

• Positive Aspects  - 
- Avoided traditional classifiers which relies on keywords, and regex matching. Rather focused on semantic searches using cosine similarity function which doesn’t rely on the magnitude rather judges on the basis of direction of vector as well. So, instead of referring to exactly same matchings, it refers to similar (similar in direction aka meaning) matchings as well. 
- The confidence-based routing was done to improve the confidence visibility. If all the top k results give the same intent (all scores 0.95 or above) then confidence is boosted by – min/max(0.95, top). So, that the system shows 95-100% confidence in the result. Ambiguity is intra-intent, not inter-intent. 
- Using the cosine similarity matching it scales to unseen intents as well without the need to retrain the model. 
- Cases when score is high but confidence is low, Cosine similarity measures semantic closeness, but confidence measures intent separability. If multiple intents score similarly, the system avoids auto-execution and safely falls back. Because your confidence ≠ similarity.  Your confidence logic measures how unique the best match is, not how good it is. 
