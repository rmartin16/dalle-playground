FROM python:3.10.5

EXPOSE 80

WORKDIR /code

COPY . /code

RUN python -m pip install -r requirements.txt

CMD streamlit run app.py
