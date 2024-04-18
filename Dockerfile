# Base image for build stage
# AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python@sha256:10dbb67ede15b5fd516be87dd71c3f7968904b0b840235720486476b34ef9b67 as build

# Metadata for the image
LABEL maintainer="nailtongsilva@gmail.com" \
    version="1.0" \
    description="Selenium with Firefox on AWS Lambda"

# Environment variables to hold URLs for Firefox binaries
# https://ftp.mozilla.org/pub/firefox/releases/117.0/linux-x86_64/en-US/firefox-117.0.tar.bz2
ENV URL_FIREFOX="https://ftp.mozilla.org/pub/firefox/releases/125.0.1/linux-x86_64/en-US/firefox-125.0.1.tar.bz2" \
    URL_GECKODRIVER="https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz" \
    LOCALPATH_FIREFOX="/tmp/firefox-125.0.1.tar.bz2" \
    # Set screen size
    SCREEN_WIDTH=1920 \
    SCREEN_HEIGHT=1080

# Install dependencies required for Selenium and browsers
RUN yum -y -q install unzip gzip tar bzip2 && \
    # Install Firefox and GeckoDriver
    mkdir -p /opt/firefox && \
    curl -Lo ${LOCALPATH_FIREFOX} ${URL_FIREFOX} && \
    tar -jxf ${LOCALPATH_FIREFOX} --strip-components=1 -C "/opt/firefox/" && \
    mkdir -p "/opt/geckodriver" && \
    curl -Lo "/opt/geckodriver/geckodriver-v0.33.0-linux64.tar.gz" ${URL_GECKODRIVER} && \
    tar -zxf "/opt/geckodriver/geckodriver-v0.33.0-linux64.tar.gz" -C "/opt/geckodriver/" && \
    chmod +x "/opt/geckodriver/geckodriver" && \
    ln -s /tmp/firefox/firefox /usr/bin/firefox && \
    ln -s /tmp/geckodriver/geckodriver /usr/bin/geckodriver && \
    rm -rf ${LOCALPATH_FIREFOX} && \
    # Cleanup
    yum remove -y unzip tar bzip2 gzip && \
    yum clean all -y && \
    rm -rf /var/cache/yum /tmp/*

# Second phase with a new base image
# AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python@sha256:10dbb67ede15b5fd516be87dd71c3f7968904b0b840235720486476b34ef9b67

# Install dependencies required for Selenium and browsers
RUN yum -y -q install \
    atk \
    cups-libs \
    dbus-glib \
    dbus-glib-devel \
    gtk3 \
    gtk3-devel \
    libXScrnSaver \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXext \
    libXi \
    libXinerama.x86_64 \
    libXrandr \
    libXt \
    libX11 \
    libx11-xcb-dev \
    libXtst \
    lsb \
    pango \
    procps \
    xorg-x11-server-Xvfb \
    xorg-x11-xauth xdpyinfo \ \
    # cleanup
    && yum clean all \
    && rm -rf /var/cache/yum

# Install Python Dependencies
RUN pip install --no-cache-dir \
    boto3>=1.34 \
    pyvirtualdisplay>=3.0 \
    requests>=2.31.0 \
    selenium>=4.19 > /dev/null

# Copy downloaded binaries from the first phase
COPY --from=build /opt/firefox /tmp/firefox
COPY --from=build /opt/geckodriver /tmp/geckodriver
# Copy main Python script and entrypoint script
COPY main.py ./
# To activate virtual display
COPY entrypoint.sh /

# Set entrypoint for AWS Lambda
CMD [ "main.handler" ]
ENTRYPOINT ["/entrypoint.sh"]