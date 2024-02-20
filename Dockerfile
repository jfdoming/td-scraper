# syntax = edrevo/dockerfile-plus

FROM --platform=linux/amd64 umihico/aws-lambda-selenium-python:3.12.0-selenium4.17.2-chrome121.0.6167.184

INCLUDE+ Dockerfile.common
