FROM python:3.10.6-buster
COPY car_damage /car_damage
# COPY requirements.txt /requirements.txt
COPY requirements_prod.txt /requirements_prod.txt
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN pip install -r requirements_prod.txt
CMD uvicorn car_damage.api.fast_api_prod:app --host 0.0.0.0
