ARG STACTOOLS_VERSION=latest
FROM ghcr.io/stac-utils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/stactools-gpw

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/gpw/__init__.py src/stactools/gpw/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/gpw

COPY src ./src
RUN pip install .
