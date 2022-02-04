import globalPluginHandler
import ui
import urllib.request
import urllib.parse
import api
import json
import wx
import gui
from gui import nvdaControls
import config

#shorten url using yourls api
def shortenUrl(url):
	#get api key
	apiKey = config.conf["NvdaYourls"]["apiKey"]
	#get api url
	apiUrl = config.conf["NvdaYourls"]["urlInstal"]+"/yourls-api.php"
	#set up api parameters
	params = urllib.parse.urlencode({"signature": apiKey, "action": "shorturl", "url": url, "format": "json"})
	#set up api request
	req = urllib.request.Request(apiUrl + "/shorturl?" + params)
	#open request
	response = urllib.request.urlopen(req)
	#get response
	response = response.read()
	#parse response
	response = json.loads(response)
	#get short url
	shortUrl = response["shorturl"]
	#return short url
	return shortUrl

#delet url fron yourls api
def deleteUrl(url):
	#get api key
	apiKey = config.conf["NvdaYourls"]["apiKey"]
	#get api url
	apiUrl = config.conf["NvdaYourls"]["urlInstal"]+"/yourls-api.php"
	#set up api parameters
	params = urllib.parse.urlencode({"signature": apiKey, "action": "delete", "shorturl": url, "format": "json"})
	#set up api request
	req = urllib.request.Request(apiUrl + "/delete?" + params)
	#open request
	response = urllib.request.urlopen(req)
	#get response
	response = response.read()
	#parse response
	response = json.loads(response)
	#get short url
	shortUrl = response["message"]
	#return short url
	return shortUrl

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		confspec = {
			'apiKey': 'string(default=Insira sua chave api aqui:)',
			'urlInstal': 'string(default=Insira a URL de onde seu YOURLS está instalado:)'
		}
		config.conf.spec['NvdaYourls'] = confspec
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(NvdaYourlsSettingsPanel)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(NvdaYourlsSettingsPanel)

	def script_encurtaLink(self, gesture):
		clipboardText = api.getClipData()
		send=shortenUrl(clipboardText)
		api.copyToClip(str(send))
		ui.message(str(send))

	def script_deleteLink(self, gesture):
		clipboardText = api.getClipData()
		send=deleteUrl(clipboardText)
		api.copyToClip(str(send))
		ui.message(str(send))

	__gestures={
		"kb:NVDA+shift+U": "encurtaLink",
		"kb:NVDA+control+U": "deleteLink"
	}

class NvdaYourlsSettingsPanel(gui.SettingsPanel):
	title = 'NVDA Yourls'

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._apiKeyLabel = sHelper.addLabeledControl("Informe a sua chave da api do YOURLS:", wx.TextCtrl)
		self._urlInstalLabel = sHelper.addLabeledControl("Informe a URL de onde o YOURLS está instalado:", wx.TextCtrl)
		self._setValues()

	def _setValues(self):
		self._apiKeyLabel.SetValue(str(config.conf['NvdaYourls']['apiKey']))
		self._urlInstalLabel.SetValue(config.conf['NvdaYourls']['urlInstal'])

	def onSave(self):
		config.conf['NvdaYourls']['apiKey'] = self._apiKeyLabel.GetValue()
		config.conf['NvdaYourls']['urlInstal'] = self._urlInstalLabel.GetValue()
