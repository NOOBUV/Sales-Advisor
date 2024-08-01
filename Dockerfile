FROM node:22 as client_build

WORKDIR /code
COPY ./client /code
RUN npm install
RUN npm run build


FROM python:3.12.3
WORKDIR /code
COPY server/requirements.txt /code/requirements.txt
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY --from=client_build /code/build/assets/ /code/static/
COPY --from=client_build /code/build/ /code/static/
COPY ./server /code

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "salesAdvisor.wsgi:application"]