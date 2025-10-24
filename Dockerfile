FROM python:3.14.0-slim-trixie
RUN pip install "elasticsearch>=8.0.0,<9.0.0"
RUN pip install mysql-connector-python
RUN pip install python-dateutil