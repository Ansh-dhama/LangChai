from langchain_huggingface import HuggingFaceEmbeddings 

embedding = HuggingFaceEmbeddings(model_name ="google/embeddinggemma-300m",encode_kwargs={
        "truncate_dim": 128,
        "normalize_embeddings": True
    })
text = "what is india capital"
result = embedding.embed_query(text)

print(result)
