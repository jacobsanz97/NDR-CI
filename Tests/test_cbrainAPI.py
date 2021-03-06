import unittest
import json
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import cbrainAPI
##########################################################################
#At a later stage replace returns of 1 with exceptions and test those.
class TestcbrainAPI(unittest.TestCase):

	def test_cbrain_login_incorrect(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			wrong_user = "wronguser"
			wrong_pass = "123"
			url = 'https://portal.cbrain.mcgill.ca/session'
			headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json',}
			data = {'login': wrong_user, 'password': wrong_pass}
			#set status_code attribute to mock object, test.
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_login(wrong_user, wrong_pass), 1)
			#test if request was posted with given credentials.
			mock_request.assert_called_once_with(url, data=data, headers=headers)
	def test_cbrain_login_correct(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			correct_user = "correctuser"
			correct_pass = "123"
			url = 'https://portal.cbrain.mcgill.ca/session'
			headers = {'Content-Type': 'application/x-www-form-urlencoded','Accept': 'application/json',}
			data = {'login': correct_user, 'password': correct_pass}
			mock_request.return_value.status_code = 200
			expected = {"user_id":123,"cbrain_api_token":"testToken"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_login(correct_user, correct_pass), expected['cbrain_api_token'])
			mock_request.assert_called_once_with(url, data=data, headers=headers)



	def test_cbrain_logout_incorrect(self):
		with patch('cbrainAPI.requests.delete') as mock_request:
			wrongToken = "wrongToken"
			url = 'https://portal.cbrain.mcgill.ca/session'
			headers = {'Accept': 'application/json'}
			params = (('cbrain_api_token', wrongToken),)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_logout(wrongToken), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params)
	def test_cbrain_logout_correct(self):
		with patch('cbrainAPI.requests.delete') as mock_request:
			correctToken = "correctToken"
			url = 'https://portal.cbrain.mcgill.ca/session'
			headers = {'Accept': 'application/json'}
			params = (('cbrain_api_token', correctToken),)
			mock_request.return_value.status_code = 200
			self.assertEqual(cbrainAPI.cbrain_logout(correctToken), 0)
			mock_request.assert_called_once_with(url, headers=headers, params=params)



	def test_cbrain_listDP_incorrect(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			dataprovider_ID = 123
			url = 'https://portal.cbrain.mcgill.ca/data_providers/' + str(dataprovider_ID) + '/browse'
			headers = {'Accept': 'application/json',}
			params = (('id', str(dataprovider_ID)),('cbrain_api_token', token),)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_listDP(dataprovider_ID, token), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params, allow_redirects=True)
	def test_cbrain_listDP_correct(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			dataprovider_ID = 123
			url = 'https://portal.cbrain.mcgill.ca/data_providers/' + str(dataprovider_ID) + '/browse'
			headers = {'Accept': 'application/json',}
			params = (('id', str(dataprovider_ID)),('cbrain_api_token', token),)
			mock_request.return_value.status_code = 200
			expected = {"aJSON":123,"testing":"123"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_listDP(dataprovider_ID, token), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params, allow_redirects=True)



	def test_cbrain_getTaskInfo_incorrect(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			taskID = 123
			url = 'https://portal.cbrain.mcgill.ca/tasks/' + str(taskID)
			headers = {'Accept': 'application/json',}
			params = (('id', str(taskID)),('cbrain_api_token', token),)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_getTaskInfo(token, taskID), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params)
	def test_cbrain_getTaskInfo_correct(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			taskID = 123
			url = 'https://portal.cbrain.mcgill.ca/tasks/' + str(taskID)
			headers = {'Accept': 'application/json',}
			params = (('id', str(taskID)),('cbrain_api_token', token),)
			mock_request.return_value.status_code = 200
			expected = {"aJSON":123,"testing":"123"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_getTaskInfo(token, taskID), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params)



	def test_cbrain_download_text_incorrect(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			fileID = 123
			url = 'https://portal.cbrain.mcgill.ca/userfiles/' + str(fileID) + '/content'
			headers = {'Accept': 'text',}
			params = (('cbrain_api_token', token),)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_download_text(fileID, token), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params, allow_redirects=True)
	def test_cbrain_download_text_correct(self):
		with patch('cbrainAPI.requests.get') as mock_request:
			token = "token"
			fileID = 123
			url = 'https://portal.cbrain.mcgill.ca/userfiles/' + str(fileID) + '/content'
			headers = {'Accept': 'text',}
			params = (('cbrain_api_token', token),)
			mock_request.return_value.status_code = 200
			expected = "return string"
			mock_request.return_value.text = expected
			self.assertEqual(cbrainAPI.cbrain_download_text(fileID, token), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params, allow_redirects=True)



	def test_cbrain_FSLFirst_incorrect(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": {
					'tool_config_id': 721,
					'params': {
						'interface_userfile_ids': [fileID], 
						'input_file': fileID, 
						'prefix': 'output', 
						'brain_extracted': False, 
						'three_stage': False, 
						'verbose': False       
				}, 
				'run_number': None, 
				'results_data_provider_id': 179, 
				'cluster_workdir_size': None, 
				'workdir_archived': True,  
				'description': ''}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_FSLFirst(token, fileID), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)
	def test_cbrain_FSLFirst_correct(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": {
					'tool_config_id': 721,
					'params': {
						'interface_userfile_ids': [fileID], 
						'input_file': fileID, 
						'prefix': 'output', 
						'brain_extracted': False, 
						'three_stage': False, 
						'verbose': False       
				}, 
				'run_number': None, 
				'results_data_provider_id': 179, 
				'cluster_workdir_size': None, 
				'workdir_archived': True,  
				'description': ''}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 200
			expected = {"aJSON":123,"testing":"123"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_FSLFirst(token, fileID), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)


	def test_cbrain_FSLStats_incorrect(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": {
					"tool_config_id": 1698,
					"params": {
						"interface_userfile_ids": [fileID],
						"input_file": fileID,
						"t": False,
						"l": "16.5",
						"u": "17.5",
						"a": False,
						"n": False,
						"r": False,
						"R": False,
						"e": False,
						"E": False,
						"v": False,
						"V": True,
						"m": False,
						"M": False,
						"s": False,
						"S": False,
						"w": False,
						"x": False,
						"X": False,
						"c": False,
						"C": False},
					"run_number": None,
					"results_data_provider_id": 27,
					"cluster_workdir_size": 40960,
					"workdir_archived": False,
					"description": ""}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_FSLStats(token, fileID), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)
	def test_cbrain_FSLFSLStats_correct(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": {
					"tool_config_id": 1698,
					"params": {
						"interface_userfile_ids": [fileID],
						"input_file": fileID,
						"t": False,
						"l": "16.5",
						"u": "17.5",
						"a": False,
						"n": False,
						"r": False,
						"R": False,
						"e": False,
						"E": False,
						"v": False,
						"V": True,
						"m": False,
						"M": False,
						"s": False,
						"S": False,
						"w": False,
						"x": False,
						"X": False,
						"c": False,
						"C": False},
					"run_number": None,
					"results_data_provider_id": 27,
					"cluster_workdir_size": 40960,
					"workdir_archived": False,
					"description": ""}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 200
			expected = {"aJSON":123,"testing":"123"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_FSLStats(token, fileID), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)

	def test_cbrain_SubfolderFileExtractor_incorrect(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			filenameToExtract = "extractMePlz"
			fileNewName = "extractTo"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": { 
        			'tool_config_id': 2094,
        			'params': {
         				'interface_userfile_ids': [fileID],
          				'infolder': fileID,
          				'extracted': filenameToExtract,
          				'new_name': fileNewName},
					'run_number': None, 
					'results_data_provider_id': 179, 
					'cluster_workdir_size': None, 
					'workdir_archived': True, 
					'description': ''}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 401
			self.assertEqual(cbrainAPI.cbrain_SubfolderFileExtractor(token, fileID, filenameToExtract, fileNewName), 1)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)
	def test_cbrain_SubfolderFileExtractor_correct(self):
		with patch('cbrainAPI.requests.post') as mock_request:
			token = "token"
			fileID = "123"
			filenameToExtract = "extractMePlz"
			fileNewName = "extractTo"
			url = 'https://portal.cbrain.mcgill.ca/tasks'
			headers = {'Content-Type': 'application/json', 'Accept': 'application/json',}
			params = (('cbrain_api_token', token),)
			data = {
				"cbrain_task": { 
        			'tool_config_id': 2094,
        			'params': {
         				'interface_userfile_ids': [fileID],
          				'infolder': fileID,
          				'extracted': filenameToExtract,
          				'new_name': fileNewName},
					'run_number': None, 
					'results_data_provider_id': 179, 
					'cluster_workdir_size': None, 
					'workdir_archived': True, 
					'description': ''}
			}
			y = json.dumps(data)
			mock_request.return_value.status_code = 200
			expected = {"aJSON":123,"testing":"123"}
			mock_request.return_value.json.return_value = expected
			self.assertEqual(cbrainAPI.cbrain_SubfolderFileExtractor(token, fileID, filenameToExtract, fileNewName), expected)
			mock_request.assert_called_once_with(url, headers=headers, params=params, data=y)

if __name__ == '__main__':
	unittest.main()
