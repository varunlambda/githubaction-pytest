from os import environ
import pytest
from appium import webdriver
from requests import request

@pytest.fixture(scope='function')
def test_setup(request):
    test_name = request.node.name
    build = environ.get('BUILD', "Sample PY Build")
    caps = {}
    caps["deviceName"] = "Galaxy S21 Ultra 5G"
    caps["platformName"] = "Android"
    caps["platformVersion"] = "11"
    caps["app"] = "app_URL"
    caps["isRealMobile"] = True
    caps['build'] = "GA-pytest"
    caps['name'] = test_name
    driver = webdriver.Remote("https://varunkumarb:doLbtRzYpWdpD1xxcIQdByQ1b7kmqMNg43DrpsYwGxbPBtphNU@mobile-hub.lambdatest.com/wd/hub",caps)
    request.cls.driver = driver
    
    yield driver
    
    def fin():
        #browser.execute_script("lambda-status=".format(str(not request.node.rep_call.failed if "passed" else "failed").lower()))
        if request.node.rep_call.failed:
            driver.execute_script("lambda-status=failed")
        else:
            driver.execute_script("lambda-status=passed")
            driver.quit()
    request.addfinalizer(fin)
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

