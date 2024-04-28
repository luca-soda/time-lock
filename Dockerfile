FROM python:3.12-slim

WORKDIR /app

RUN useradd -ms /bin/bash user
USER user

COPY --chown=user ./src .
COPY --chown=user ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD python -m uvicorn main:app --host 0.0.0.0


