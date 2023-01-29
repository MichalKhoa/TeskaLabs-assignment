FROM python:3.8
WORKDIR /app
ADD main.py .
ADD sample-data.json .
RUN pip3 install pymongo
CMD ["python", "./main.py", "./sample-data.json" ]
SAVE IMAGE dockerpy
