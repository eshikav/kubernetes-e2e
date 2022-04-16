FROM alpine
RUN apk add python3 py3-pip
RUN apk add bash
RUN apk add curl wget
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.18.0/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mv ./kubectl /usr/local/bin/kubectl
RUN python3 -m pip install kubernetes
RUN python3 -m pip install -U pytest
COPY wrcp/ wrcp/
COPY kubernetestestcases.py k8s-test.py

