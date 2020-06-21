FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Install wget
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

# Download the models to the ml_model directory
ENV MODEL_VER '15_june_2020_v1'
RUN mkdir ml_models
RUN wget -P ./ml_models https://storage.googleapis.com/petrichor_models/${MODEL_VER}_tokenizer.pkl
RUN wget -P ./ml_models https://storage.googleapis.com/petrichor_models/${MODEL_VER}_label_encoder.pkl
RUN wget -P ./ml_models https://storage.googleapis.com/petrichor_models/${MODEL_VER}_model.h5

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 app:app
