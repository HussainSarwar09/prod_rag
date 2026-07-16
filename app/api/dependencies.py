"""
API dependency providers.
"""

from app.core.container import container
from app.loaders.factory import LoaderFactory


def get_loader_factory() -> LoaderFactory:
    """
    Return the shared LoaderFactory instance.
    """
    return container.loader_factory
