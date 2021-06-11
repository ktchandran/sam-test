FROM public.ecr.aws/lambda/python:3.8

#RUN yum install -y git openssh
#RUN pip install \
#        awslambdaric \
#        apig-wsgi \
#        aws-encryption-sdk-cli \
#        awscli --upgrade
#RUN pip install \
#        aws-encryption-sdk-cli \
#        awscli --upgrade

COPY hello_world requirements.txt ./

RUN python3.8 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
