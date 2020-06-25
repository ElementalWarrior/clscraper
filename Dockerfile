FROM python:3.8.3

# RUN apk add --update --no-cache \
#     musl-dev \
#     libffi-dev \
#     libxml2-dev \
#     libxslt-dev \
#     # jpeg-dev \
#     # curl-dev \
#     # make \

RUN apt update && apt install gcc python3-dev curl python3-psycopg2 -y

RUN python3 -m pip install --upgrade pip

WORKDIR /app
COPY . .

RUN python3 -m pip install -r requirements.txt
RUN rm -rf /app/vendor

CMD [ "scrapy", "crawl" ]