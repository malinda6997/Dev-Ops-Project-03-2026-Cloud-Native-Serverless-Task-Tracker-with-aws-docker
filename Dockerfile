FROM python:3.9-slim

WORKDIR /app

# Requirements copy කරලා install කරනවා
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ඉතිරි ඔක්කොම කෝඩ් ටික copy කරනවා
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]