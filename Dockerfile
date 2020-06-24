FROM alpine:3.12

RUN apk add --update --no-cache gcc musl-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev curl-dev make python3 python3-dev tzdata git curl \
&& python3 -m pip install  --upgrade pip \

RUN python3 -m pip install -r requirements.txt
