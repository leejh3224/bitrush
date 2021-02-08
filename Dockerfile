FROM public.ecr.aws/lambda/python:3.8
ENV LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"

# timezone setting
RUN echo 'Asia/Seoul' | tee /etc/timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# linux packages
RUN yum -y install wget && \
    yum -y install tar && \
    yum -y install gzip && \
    yum -y install gcc && \
    yum -y install make && \
    yum -y install mysql-devel

# install Ta-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

COPY requirements.txt pyproject.toml ${LAMBDA_TASK_ROOT}/
RUN pip3 install -r requirements.txt -t ${LAMBDA_TASK_ROOT}

COPY lib ${LAMBDA_TASK_ROOT}/lib
COPY *.py ${LAMBDA_TASK_ROOT}/

CMD ["trader.main"]
