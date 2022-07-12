FROM python:3.10

WORKDIR /app

COPY docker/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN rm ./requirements.txt

COPY ./backend ./backend

# You can uncomment and use the given command instead of the last one.
# (This isn't necessary though, this file can be safely deleted).
CMD [ "python", "-m", "backend.launch"]
# CMD [ "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000" ]
