ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

RUN curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

RUN pip install poetry pytest pre-commit bumpversion wheel keyring artifacts-keyring twine

RUN wget https://releases.hashicorp.com/terraform/1.2.9/terraform_1.2.9_linux_amd64.zip

RUN unzip terraform_1.2.9_linux_amd64.zip && mv terraform /usr/local/bin/

RUN wget https://download.visualstudio.microsoft.com/download/pr/5ac82fcb-c260-4c46-b62f-8cde2ddfc625/feb12fc704a476ea2227c57c81d18cdf/dotnet-sdk-8.0.404-linux-arm64.tar.gz \
    && mkdir -p /usr/share/dotnet \
    && tar -zxf dotnet-sdk-8.0.404-linux-arm64.tar.gz -C /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet \
    && rm dotnet-sdk-8.0.404-linux-arm64.tar.gz

# Establecer variables de entorno para .NET
ENV DOTNET_ROOT=/usr/share/dotnet
ENV PATH=$PATH:/usr/share/dotnet

# Configurar permisos para el usuario `vscode`
RUN chown -R vscode:vscode /usr/share/dotnet
