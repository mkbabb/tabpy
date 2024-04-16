FROM poetry-base

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml .

WORKDIR /tabpy

COPY tabpy.conf .

RUN poetry install --no-dev

EXPOSE 9004
