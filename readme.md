Firefox Selenium Lambda Docker Image
============================

Table of Contents
-----------------

1.  [Overview](#overview)
2.  [Maintainer](#maintainer)
3.  [Use Cases](#use-cases)
4.  [Prerequisites](#prerequisites)
5.  [Build and Run](#build-and-run)
6.  [Environment Variables](#environment-variables)
7.  [Dependencies](#dependencies)
8.  [Files](#files)
9.  [Entrypoint](#entrypoint)
10.  [Support](#support)

Overview
--------

This Docker image is designed to run Selenium with Firefox on AWS Lambda. It is built on top of the AWS Lambda Python runtime and includes all necessary dependencies for running Selenium and Firefox. This image is suitable for both technical and non-technical users who wish to automate web browser tasks in a serverless environment.

Maintainer
----------

*   **Email**: [nailtongsilva@gmail.com](mailto:nailtongsilva@gmail.com)
*   **Version**: 1.0

Use Cases
---------

*   **Web Scraping**: Automatically collect data from websites.
*   **Automated Testing**: Run your Selenium-based test suites without needing a dedicated server.
*   **Data Entry Automation**: Automate repetitive data entry tasks.
*   **Browser Automation**: Perform any task you would manually do in a web browser, but automated.

Prerequisites
-------------

*   Docker installed on your machine. If you don't have it, [download Docker here](https://www.docker.com/products/docker-desktop).
*   Basic understanding of command-line operations.

Build and Run
-------------

### Build

#### 1. Build the Docker Image

`docker build --platform linux/amd64 -t selenium-lambda .`

#### 2. Run the Docker Container

`docker run -it --rm -e AWS_LAMBDA_FUNCTION_TIMEOUT=300 -e AWS_LAMBDA_FUNCTION_MEMORY_SIZE=1024 -p 9000:8080 selenium-lambda:latest`

#### 3. Local Testing with

`Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method POST -Body '{"headless_mode": false, "needs_download_file": false, "clean_init": false, "script_name": null}'`

OR

`curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{\"headless_mode\": false, \"needs_download_file\": false, \"clean_init\": false, \"script_name\": null}"`

Environment Variables
---------------------

Variable || Description || Default Value

`AWS_LAMBDA_FUNCTION_TIMEOUT` || AWS Lambda function timeout || 300 (5 minutes)

`AWS_LAMBDA_FUNCTION_MEMORY_SIZE` || AWS Lambda function memory size || 1024 MB

`SCREEN_WIDTH` || Screen width for Selenium || 1920

`SCREEN_HEIGHT` || Screen height for Selenium || 1080

Dependencies
------------

### System Packages

*   Various Linux packages required for running Firefox and Selenium.

### Python Packages

*   Libraries for AWS, OpenAI, Excel manipulation, web requests, and more.

Files
-----

*   `main.py`: The main Python script that AWS Lambda will execute.
*   `entrypoint.sh`: A shell script that sets up the environment before running `main.py`.

Entrypoint
----------

The entry point for AWS Lambda is defined as `main.handler`.


Support Me
----------

For any issues or questions, please contact the maintainer via email.

If you find this project helpful and would like to support its development, consider buying me a coffee or a toy for my children! You can send cryptocurrency to my *Coinbase wallet* using the following details:

*   **Bitcoin (BTC) - Bitcoin Network**: `3KEyAyYAyBfXkciRhrejz6ZmXjigZ5GnLj`
*   **Ethereum (ETH) - Ethereum Network**: `0x842c95127163a3bc05a43215f0D85Fb4361Fd460`
*   **USD Coin (USDC) - Polygon Network**: `0xbFf4f280d008Be5D06Ec83B39A3E390e75FcEf94`
*   **Brazilian Pix**: `nailtongsilva@gmail.com`

To send cryptocurrency:

1.  **Open Your Crypto Wallet**: This could be on an exchange like Binance, Coinbase, or a personal wallet.
2.  **Go to the Send Section**: Usually denoted by a "Send" button.
3.  **Enter the Wallet Address**: Copy and paste the appropriate wallet address from above.
4.  **Confirm the Transaction**: Make sure to double-check the address and amount before sending.

Your support is greatly appreciated!
