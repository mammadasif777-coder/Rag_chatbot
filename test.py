from rag import add_document, answer

print(add_document("sample.pdf", "sample.pdf"), "chunks stored")
print(answer("What is this document about?"))