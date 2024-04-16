FROM poetry-base as deployment

# echo the poetry dependencies to a requirements.txt file
RUN poetry export -f requirements.txt --output /cache/requirements.txt

RUN cat /cache/requirements.txt 

COPY config.conf /

EXPOSE 9004