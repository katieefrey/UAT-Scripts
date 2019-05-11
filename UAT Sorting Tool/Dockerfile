ARG PYTHON_VERSION="2.7"
FROM python:${PYTHON_VERSION}
# copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["uatapi.py"]