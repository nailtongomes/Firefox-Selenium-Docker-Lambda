"""
Legal Productivity Automation

This Python project automates legal productivity tasks such as downloading and running scripts, 
communicating with servers, and controlling web browsers. It is intended to be used with AWS Lambda and Docker 
and is suitable for legal professionals who work in both law and software development.

Key Features:
- Script Downloading: Downloads Python scripts from a server, checks if they already exist locally, and saves 
  them in a specified directory.
- Dynamic Importing: Dynamically imports Python modules for use in the project.
- Script Requesting: Formats and sends requests to a server to download specific Python scripts.
- Local Script Saving: Checks if a script already exists in a local directory and saves it if it does not.
- Web Browser Automation: Uses Selenium to control web browsers for tasks such as logging into websites.
- Environment Setup: Sets up the running environment, which can be either AWS Lambda or Docker.

Modules:
- Selenium: For controlling web browsers and automating web tasks.
- Boto3: For interacting with Amazon Web Services.
- urllib: For sending HTTP requests.
- shutil, tempfile, os, pathlib: For file and directory operations.
- logging: For generating logs for debugging and record-keeping.
- importlib, sys: For importing Python modules.
- datetime: For dealing with dates and times.
- pyvirtualdisplay: For creating a virtual display in memory.

This project is designed to be flexible and adaptable to different workflows. 
For instance, you can specify the script to be downloaded and the task to be automated via the 'event' dictionary.

Note: To adapt this project to your specific needs, you may need to change certain variables or logic in the 
code, such as the paths, URLs, and server requests.

Author: Nailton Gomes Silva | nailtongsilva@gmail.com
"""
import time
import os
import tempfile
from pathlib import Path
import logging
import resource

# This is the path to the Firefox driver and binary in the Docker container.
F_DRIVER_PATH = '/tmp/geckodriver/geckodriver'
F_BINARY_PATH = '/tmp/firefox/firefox'

# if you want to use the AWS Lambda environment variables, uncomment the lines below
# OPEN_AI_KEY=os.environ.get('OPEN_AI_KEY', "")
# AWS_ACCESS_KEY=os.environ.get('AWS_ACCESS_KEY','')
# AWS_TOKEN_KEY=os.environ.get('AWS_TOKEN_KEY', '')
# BOT_TELEGRAM=os.environ.get('BOT_TELEGRAM','')

# This is the path to the folder where the custom scripts will be saved.
# /root/LegalWizard
HOME_FOLDER = os.path.normpath(os.path.join(Path.home(), "LegalWizard"))
# /root/LegalWizard/src
SCRIPTS_FOLDER = os.path.normpath(os.path.join(HOME_FOLDER, "src"))
if not os.path.isdir(SCRIPTS_FOLDER): os.makedirs(SCRIPTS_FOLDER, exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info(f'HOME_FOLDER: {HOME_FOLDER}')
logger.info(f'SCRIPTS_FOLDER: {SCRIPTS_FOLDER}')


def log_resource_usage():
	"""
	Function to check the memory and disk usage of the Lambda function.	
	"""
	try:
		# check memory usage	
		print(f"[INFO] Memory Usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss} KB")
		# check disk usage
		print(f"[INFO] Disk Usage: {os.statvfs('/tmp').f_bavail * os.statvfs('/tmp').f_frsize / 1024} KB")
	except Exception as e:
		print(f"[ERROR] {e}")

# third party libraries
try:
	from selenium import webdriver
	from selenium.webdriver.firefox.options import Options as OptionsFirefox
	from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
	from selenium.webdriver.firefox.service import Service as FirefoxService
	SELENIUM_OK = True
except:	
	SELENIUM_OK = False
	logger.info('NOK Selenium: pip install selenium')

try:
	import boto3
	BOTO3_OK = True
except:
	BOTO3_OK = False
	logger.info('NOK boto3: pip install boto3')

try:
	from pyvirtualdisplay import Display
	VIRTUAL_DISPLAY_OK = True
except:
	VIRTUAL_DISPLAY_OK = False
	logger.info('NOK pyvirtualdisplay: pip install pyvirtualdisplay')


def custom_script_dir(custom_script='ngs.py'):

	"""
	:param custom_script: (str) name of the custom script
	:return: (str) path to the directory where the custom scripts are saved
	"""

	pass


def get_custom_script(script_name='ngs.py'):

	"""
	:param script_name: (str) name of the custom script
	:return: (str) path to the custom script
	"""
	pass


def import_module(module_name:str, location:str):
	
	"""
	Function to import a Python module dynamically.
	:param module_name: (str) name of the module
	:param location: (str) path to the module
	:return: (module) imported module
	"""

	pass


def download_test_script(script_name='ngs.py', use_s3=False):
	
	"""
	Function to download a Python script from a server.
	:param script_name: (str) name of the script
	:param use_s3: (bool) whether to use AWS S3
	:return: (str) path to the script
	"""

	if use_s3 is True:
		script_path = f'/{SCRIPTS_FOLDER}/{script_name}'
		s3 = boto3.client(
			's3',
			aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
			aws_secret_access_key=os.environ.get('AWS_TOKEN_KEY')
		)
		s3.download_file(os.environ.get('AWS_BUCKET', 'AWS_BUCKET'), f'{script_name}.py', script_path)
	else:
		code, script_path = get_custom_script(script_name)
	return script_path


def options_for_firefox(
	needs_download_file,
	download_folder='',
	user_agent_custom=None
):

	"""
	Function to set the options for the Firefox browser.
	:param needs_download_file: (bool) whether the browser needs to download files
	:param download_folder: (str) path to the folder where the browser will download files
	:param user_agent_custom: (str) custom user agent for the browser
	:return: (OptionsFirefox) Firefox options
	"""

	options = OptionsFirefox()
	options.set_preference("privacy.popups.policy", 1)
	options.set_preference("browser.preferences.instantApply", True)
	options.set_preference("browser.link.open_newwindow", 3)
	options.set_preference("browser.link.open_newwindow.restriction", 0)
	options.set_preference("dom.webdriver.enabled", False)
	options.set_preference('useAutomationExtension', False)
	
	if user_agent_custom:
		options.set_preference("general.useragent.override", user_agent_custom)

	if needs_download_file is True:
		options.set_preference("browser.safebrowsing.downloads.enabled", False)
		if download_folder:
			options.set_preference("browser.download.dir", download_folder)
		else:
			options.set_preference("browser.download.dir", '')

		options.set_preference("browser.download.useDownloadDir", True)
		options.set_preference("browser.download.folderList", 2)
		options.set_preference("browser.download.viewableInternally.enabledTypes", "")
		options.set_preference("browser.download.animateNotifications", False)
		options.set_preference("browser.download.manager.showWhenStarting", False)
		options.set_preference("browser.download.manager.alertOnEXEOpen", False)
		options.set_preference("browser.download.manager.focusWhenStarting", False)
		options.set_preference("browser.download.manager.useWindow", False)
		options.set_preference("browser.download.manager.showAlertOnComplete", False)
		options.set_preference("browser.download.manager.closeWhenDone", False)
		options.set_preference("browser.download.forbid_open_with", True)
		options.set_preference("browser.helperApps.alwaysAsk.force", False)
		options.set_preference(
			"browser.helperApps.neverAsk.saveToDisk",
			"application/pdf;application/octet-stream;application/binary;application/text;application/csv;text/csv;application/vnd.ms-excel"
			)
		options.set_preference(
			"browser.helperApps.neverAsk.openFile",
			"application/pdf;application/octet-stream;application/binary;application/text;application/csv;text/csv;application/vnd.ms-excel"
			)
		options.set_preference("pdfjs.disabled", True)

	return options


def make_options_for_webdriver(
	is_firefox,
	needs_download_file,
	download_folder='',
	user_agent_custom="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
):

	"""
	Function to set the options for the web driver.
	:param is_firefox: (bool) whether the browser is Firefox
	:param needs_download_file: (bool) whether the browser needs to download files
	:param download_folder: (str) path to the folder where the browser will download files
	:param user_agent_custom: (str) custom user agent for the browser
	:return: (OptionsFirefox) Firefox options
	"""

	if is_firefox is True:
		options = options_for_firefox(
			needs_download_file=needs_download_file,
			download_folder=download_folder,
			user_agent_custom=user_agent_custom
		)

	else:

		...

	return options


def make_ffox_profile(profile_folder=None):

	profile = FirefoxProfile(profile_folder)

	return profile


def create_firefox_driver(
		headless_mode=True, 
		options=None, 
		driver_path=None, 
		binary_path=None, 
		needs_download_file=None, 
		clean_init=False
	):

	"""
	Function to create a Firefox web driver.
	:param headless_mode: (bool) whether the browser is headless
	:param options: (OptionsFirefox) browser options
	:param driver_path: (str) path to the Firefox driver
	:param binary_path: (str) path to the Firefox binary
	:param needs_download_file: (bool) whether the browser needs to download files
	:param clean_init: (bool) whether to download the driver from the internet
	:return: (WebDriver) web driver
	"""

	if options is None:
		options = make_options_for_webdriver(
			is_firefox=True, 
			needs_download_file=needs_download_file, 
			download_folder=tempfile.mkdtemp(), 
			# user_agent_custom=""
		)

	if headless_mode is True:
		options.headless = True

	profile = make_ffox_profile(tempfile.mkdtemp())
	options.profile = profile


	if clean_init is True:
		# https://www.selenium.dev/documentation/selenium_manager/
		print('>>> Firefox with Selenium Manager <<<')
		driver = webdriver.Firefox(
			service=FirefoxService(),
			options=options
		)
		return driver

	else:
		print('>>> Firefox <<<')
		if driver_path:
			service = FirefoxService(
				executable_path=driver_path
			)
		else:
			service = FirefoxService()

		if binary_path:
			options.binary_location = binary_path

		driver = webdriver.Firefox(
			service=service,
			options=options
		)

		return driver


def handler(event:dict={}, context=None):

	"""
	Function to handle the Lambda event.
	:param event: (dict) Event from Lambda
	:param context: (dict) Context from Lambda
	:return: (dict) result of the script execution
	"""	
	try:
		custom_script = None
		display = None

		if event.get('headless_mode', None) is False:
			
			s_width = os.environ.get('SCREEN_WIDTH', 1920)
			s_height = os.environ.get('SCREEN_HEIGHT', 1080)
			
			display = Display(visible=0, size=(s_width, s_height))
			display.start()

			print('>>> DISPLAY: OK!')
			logger.info('>>> DISPLAY: OK!')
		else:
			print('>>> DISPLAY: NOK!')
			logger.info('>>> DISPLAY: NOK!')

		logger.info(f'\n>>> ENVIRONMENT VARIABLES: {os.environ}')
		logger.info(f'\n>>> EVENT: {event}')

		print('\n--- CUSTOM SCRIPT IMPORT ---\n')
		script_name = event.get('script_name', '')
		if script_name:
			location = download_test_script(script_name, use_s3=event.get('use_s3', False))
			custom_script = import_module("custom_script", location)

			if custom_script:
				# needs return a dict
				# you can use the event to pass parameters to the custom script
				return custom_script.main(event, context)
		
		else:
			try: 
				start = time.perf_counter()

				# executar o script
				print("\n>>> RPA SCRIPT: RUNNING...")
				
				log_resource_usage()
				results = run_rpa_script(event)
				
				log_resource_usage()
				end = time.perf_counter()
				
				elapsed = end - start
				if type(results) is dict:
					results['elapsed'] = elapsed
				
				logger.info(f'>>> RESULTS: {results}')

			except Exception as e:
				return {
					"status": "error",
					"message": str(e)  
				}
		
			return results
	finally:

		if display:
			display.stop()


def run_rpa_script(event:dict={}) -> dict:

	"""
	Function to run the RPA script.
	:param event: (dict) Event from Lambda
	:return: (dict) result of the script execution
	"""

	if event.get('clean_init', False) is False:

		# using the driver and binary in the container
		firefox = create_firefox_driver(
			headless_mode=event.get('headless_mode', True),
			options=None,
			driver_path=F_DRIVER_PATH,
			binary_path=F_BINARY_PATH,
			needs_download_file=event.get('needs_download_file', False),
			clean_init=False,
		)
	else:

		# download the driver from the internet
		firefox = create_firefox_driver(
			headless_mode=event.get('headless_mode', True),
			needs_download_file=event.get('needs_download_file', False),
			clean_init=True,
		)

	firefox.get("https://www.google.com/")
	results = {
		"status": "ok",
		"message": "Firefox is running",
		"text": firefox.title # Google
	}

	firefox.quit()

	return results

if __name__ == '__main__':

	...
	# To call the Lambda function locally, use the following commands:
	# Below is an example of a test event that can be used to invoke the Lambda function.
	# PowerShell:
	# Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method POST -Body '{"headless_mode": false, "needs_download_file": false, "clean_init": false, "script_name": null}'
	# CMD:
	# curl -X POST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{\"headless_mode\": false, \"needs_download_file\": false, \"clean_init\": false, \"script_name\": null}"
