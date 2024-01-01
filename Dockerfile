FROM python:3.9

WORKDIR /app

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set the default main script (change if your main script has a different name)
ENV FLASK_APP=app.py

CMD ["/app/entrypoint.sh"]

