from textsplitter import ChineseTextSplitter, combine_sentences, zh_title_enhance, combine_title_paragraph
from langchain.document_loaders import UnstructuredMarkdownLoader
from config import *

mdpath = "/Users/smart_boy/Nutstore Files/何志勇的坚果云/审计/知识库/人事与薪酬/薪酬舞弊调查方法与防范.md"

loader = UnstructuredMarkdownLoader(mdpath)
textsplitter = ChineseTextSplitter(pdf=False, sentence_size=SENTENCE_SIZE)

docs = loader.load_and_split(text_splitter=textsplitter)

print(docs)
print("-------------------------")
zh_enhanced_docs = zh_title_enhance(docs)

o = combine_title_paragraph(zh_enhanced_docs)

print(o)
