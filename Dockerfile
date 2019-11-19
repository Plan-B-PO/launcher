FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
ENV STATIC_URL /src/templates
ENV FLASK_APP launcher.py
WORKDIR /launcher
COPY ./ /launcher
RUN pip install --trusted-host pypi.python.orh -r requirements.txt
EXPOSE 5001
CMD ["python", "launcher/launcher.py"]