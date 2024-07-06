FROM python:3.9-slim

WORKDIR /app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir 'requests<2.29.0' 'urllib3<2.0' -r requirements.txt

EXPOSE 8000

ENV SQL_USER=test
ENV SQL_PASSWORD=Fang!0211
ENV PRIVATE_KEY_PATH=/app/secrets/private_key.pem
ENV PUBLIC_KEY_PATH=/app/secrets/private_key.pem
ENV REDIS_PASSWORD=Fang!0211
ENV TAP_PARTNER_KEY=partner_E6Bsl2R4FnCjBnNNoafMjMc355FuPhGcqgMfdkVPrFuzMwT9w3wa94j0
ENV MERCHANT_ID=tppf_raphaelfang_GP_POS_2

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]