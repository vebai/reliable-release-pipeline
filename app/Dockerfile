# Teaching image: update to an approved base-image digest for hardened use.
FROM python:3.13-slim
WORKDIR /app
COPY shop_api.py /app/shop_api.py
ARG SOURCE_REVISION=unversioned
ARG SOURCE_URL=""
ENV APP_VERSION=${SOURCE_REVISION} PORT=8000
LABEL org.opencontainers.image.source="${SOURCE_URL}" \
      org.opencontainers.image.revision="${SOURCE_REVISION}" \
      org.opencontainers.image.title="Reliable Release Pipeline Shop API"
EXPOSE 8000
USER 65532:65532
CMD ["python", "-u", "/app/shop_api.py"]
