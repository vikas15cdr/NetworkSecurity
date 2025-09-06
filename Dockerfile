FROM python:3.10-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements FIRST to use Docker's cache.
# (This assumes you added 'awscli' to your requirements.txt file, as we discussed)
COPY requirements.txt .

# 4. Install all Python packages using pip.
# This one command REPLACES both of your broken 'RUN' commands (lines 5 and 7).
# This is the correct way to install awscli.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Set your run command (replace "app.py" with your main file)
CMD ["python", "app.py"]
