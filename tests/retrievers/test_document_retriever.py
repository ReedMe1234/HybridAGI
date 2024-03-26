from hybridagi import FileSystem
from hybridagi import FakeEmbeddings
from hybridagi import DocumentRetriever

def test_forward():
    emb = FakeEmbeddings(dim=250)
    memory = FileSystem(
        index_name="test",
        embeddings=emb,
        wipe_on_start=True,
    )
    text = "This the a test text"
    text_name = "test_text"

    memory.add_texts(
        texts = [text],
        ids = [text_name]
    )

    retriever = DocumentRetriever(
        index_name = "test",
        embeddings = emb,
    )

    assert len(retriever.forward("test").passages) == 1

def test_forward_multiple():
    emb = FakeEmbeddings(dim=250)
    memory = FileSystem(
        index_name="test",
        embeddings=emb,
        wipe_on_start=True,
    )
    text = "This the a test text"
    text_name = "test_text"

    memory.add_texts(
        texts = [text],
        ids = [text_name]
    )

    retriever = DocumentRetriever(
        index_name = "test",
        embeddings = emb,
    )

    assert len(retriever.forward(["test", "test2"]).passages) == 2

def test_forward_more_than_k():
    emb = FakeEmbeddings(dim=250)
    memory = FileSystem(
        index_name="test",
        embeddings=emb,
        wipe_on_start=True,
    )
    text = "This the a test text"
    text_name = "test_text"

    memory.add_texts(
        texts = [text],
        ids = [text_name]
    )

    retriever = DocumentRetriever(
        index_name = "test",
        embeddings = emb,
        k = 3,
    )

    assert len(retriever.forward(["test", "test2", "test3", "test4"]).passages) == 3