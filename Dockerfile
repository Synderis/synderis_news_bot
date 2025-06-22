# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements and source code
COPY requirements.txt ./
COPY . ./

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the Lambda handler
CMD ["main.lambda_handler"]
