from langchain.document_loaders import UnstructuredMarkdownLoader

def input_md(mdpath):
    loader = UnstructuredMarkdownLoader(mdpath)
    #不分割文章
    lp = loader.load_and_split()

    return lp[0].page_content

