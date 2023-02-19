FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH="/code"
RUN mkdir /code
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /code
COPY req.txt /code/
COPY req.txt /code/
RUN pip install -r req.txt
RUN apt install curl
COPY . /code/
CMD [ "python", "./tg_bot.py"]