from textsplitter import ChineseTextSplitter, combine_sentences
from langchain.document_loaders import UnstructuredMarkdownLoader

mdpath = "/Users/smart_boy/Nutstore Files/何志勇的坚果云/审计/知识库/人事与薪酬/薪酬舞弊调查方法与防范.md"

loader = UnstructuredMarkdownLoader(mdpath)
textsplitter = ChineseTextSplitter(pdf=False, sentence_size=SENTENCE_SIZE)

docs = loader.load_and_split(text_splitter=textsplitter)

o = combine_sentences(10, docs)

print(o)
