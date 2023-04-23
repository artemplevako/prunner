FROM alpine as build-env
RUN apk add --no-cache build-base
WORKDIR /code
COPY timer.c /code
RUN gcc -o /code/timer /code/timer.c

FROM alpine
COPY --from=build-env /code/timer /code/timer
RUN apk add --no-cache python3
RUN python3 -m ensurepip
WORKDIR /code
COPY requirements.txt /code
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY main.py /code
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
