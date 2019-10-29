FROM python:3.7-slim
WORKDIR /launcher
COPY ./src /launcher
RUN pip install --trusted-host pypi.python.orh -r requirements.txt
EXPOSE 80
CMD ["python", "Webapp.py"]