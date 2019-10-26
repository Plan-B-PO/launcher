import unittest
from unittest.mock import patch
import json

from Mod import Downloader, Launcher, AppInfo, CTManager

class TestMod(unittest.TestCase):

    def setUp(self):
        self.downloader = Downloader()
        self.launcher = Launcher()
        self.ctm = CTManager()

    def tearDown(self):
        pass

    def test_downloadAppData(self):
        with open('exampleResponse.json') as json_file:
            mockedResponse = json.load(json_file)

        with patch('Mod.requests.get') as mocked_get:
            mocked_get.return_value = mockedResponse

            appInfos = self.downloader.downloadAppData('/library/launcher/applications')
            self.assertTrue(appInfos)

    def test_createCT(self):
        UserID = 123
        AppInfo = {
            "id": 1234,
            "name": "SuperApp1",
            "description": "This app allows multiplying large matrices",
            "icon": "https://imgur.com/exapmle1",
            "schema": [
                  {
                      "name": "Variable X",
                      "type": "int",
                      "defaultValue": 1
                  },

                  {
                      "name": "Variable Y",
                      "type": "int",
                      "defaultValue": 2
                  },

                  {
                      "name": "Variable Z",
                      "type": "int",
                      "defaultValue": 3
                  }
              ]
        }
        
        formInfo = {
            "name": "testname",
            "param1": "xxx",
            "param2": "yyy",
            "logger": "loggertest"
        }

        ct = self.ctm.createCT(formInfo, AppInfo, UserID)
        self.assertTrue(ct)
