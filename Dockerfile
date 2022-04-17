FROM alpine
RUN apk add python3 py3-pip bash curl  build-base python3-dev libffi-dev
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install kubernetes
RUN python3 -m pip install -U pytest
RUN python3 -m pip install -U paramiko

RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
COPY wrcp/ wrcp/
COPY kubernetestestcases.py k8s-test.py

