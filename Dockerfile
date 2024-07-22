# Stage 1
FROM python:3.11.9-slim-bullseye AS builder

WORKDIR /app
 
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
RUN pip install flask scikit-learn gunicorn flask-cors
 
# Stage 2
FROM python:3.11.9-slim-bullseye AS runner
 
WORKDIR /app
 
COPY --from=builder /app/venv venv
COPY stunting_model.sav app.py .
# COPY app.py app.py
 
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app/app.py
 
EXPOSE 8000
 
CMD ["gunicorn", "--bind" , ":8000", "app:app"]
