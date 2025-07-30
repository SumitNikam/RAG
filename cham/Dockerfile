FROM europe-west1-docker.pkg.dev/vf-grp-aib-prd-mirror/dockerhub/python:3.10.10
# FROM europe-west3-docker.pkg.dev/vf-de-aib-prd-mc2-aa-buildnl/docker-repository/image-build-cloudrun-orbiter:latest

COPY assets /charm_webapp/assets
COPY app_pages /charm_webapp/app_pages
COPY config /charm_webapp/config
COPY queries /charm_webapp/queries
COPY src /charm_webapp/src
COPY app.py /charm_webapp/app.py
COPY requirements.txt /charm_webapp/requirements.txt

WORKDIR /charm_webapp

RUN pip install --index-url https://europe-west1-python.pkg.dev/vf-grp-aib-prd-mirror/pypi-repository/simple/ -r requirements.txt

CMD python -m streamlit run app.py --server.port=8080 --server.address=0.0.0.0 --server.fileWatcherType="none"
