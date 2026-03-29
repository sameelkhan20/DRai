# Base image
FROM python:3.10

# Working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]