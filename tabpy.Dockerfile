FROM poetry-base

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml .

RUN poetry install --no-dev

WORKDIR /tabpy

COPY tabpy.conf .

EXPOSE 9004
