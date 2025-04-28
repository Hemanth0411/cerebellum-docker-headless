FROM femtopixel/google-chrome-headless:latest

USER root

RUN apt-get update && apt-get install -y python3 python3-pip

RUN apt-get install -y wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install
RUN apt-get -f install -y

COPY chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

RUN chmod +x /usr/local/bin/chromedriver

RUN pip3 install --no-cache-dir --break-system-packages --ignore-installed seleniumbase cerebellum

COPY login.py /app/login.py
COPY monkey_patch.py /app/monkey_patch.py
COPY state_tracker.py /app/state_tracker.py

WORKDIR /app

EXPOSE 9222

CMD ["python3", "/app/login.py"]