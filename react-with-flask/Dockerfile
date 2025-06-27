FROM python:3.13

WORKDIR /app

COPY api/ .

RUN pip install torchvision --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

COPY dist/ ../dist/

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
