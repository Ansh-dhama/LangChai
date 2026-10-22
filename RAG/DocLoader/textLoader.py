from langchain_community.document_loaders import TextLoader


loader = TextLoader('dhama.txt',encoding ='utf-8')

dist = loader.load()
print(dist)