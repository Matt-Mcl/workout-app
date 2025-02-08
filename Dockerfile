FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./workoutapp .

EXPOSE 8007

CMD [ "./start.sh" ]