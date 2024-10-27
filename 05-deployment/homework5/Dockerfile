FROM svizor/zoomcamp-model:3.11.5-slim

RUN pip --no-cache-dir install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --deploy --system && \
    rm -rf /root/.cache

COPY ["q6_predict.py", "./"]

EXPOSE 9698

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9698", "q6_predict:app"]