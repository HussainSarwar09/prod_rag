from app.core.container import container
from app.loaders.factory import LoaderFactory


def test_container() -> None:
    assert container.settings is not None
    assert container.metadata_extractor is not None
    assert container.document_chunker is not None
    assert container.text_reader is not None
    assert container.pdf_reader is not None

    assert isinstance(
        container.loader_factory,
        LoaderFactory,
    )
