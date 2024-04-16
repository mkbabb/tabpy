FROM poetry-base as deployment

# copy the poetry file and install dependencies
WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml .

RUN poetry install --no-dev

# copy the config files
COPY tabpy.conf /

EXPOSE 9004
