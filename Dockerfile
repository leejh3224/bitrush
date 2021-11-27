FROM public.ecr.aws/lambda/python:3.8
ENV LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# timezone setting
RUN echo 'Asia/Seoul' | tee /etc/timezone && ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# linux packages
RUN yum clean all && \
    yum -y install wget-1.14-18.amzn2.1.x86_64 && \
    yum -y install tar-1.26-35.amzn2.x86_64 && \
    yum -y install gzip-1.5-10.amzn2.x86_64 && \
    yum -y install gcc-7.3.1-12.amzn2.x86_64 && \
    yum -y install make-3.82-24.amzn2.x86_64 && \
    yum -y install mariadb-devel.x86_64 1:5.5.68-1.amzn2

# install Ta-Lib
RUN wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz

WORKDIR $LAMBDA_TASK_ROOT/ta-lib

RUN ./configure --prefix=/usr && \
  make && \
  make install

WORKDIR $LAMBDA_TASK_ROOT

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

COPY requirements.txt pyproject.toml ./
RUN pip3 install --no-cache-dir -r requirements.txt -t .

COPY lib lib
COPY *.py ./

CMD ["trader_app.main"]
