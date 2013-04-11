#encoding: utf-8
import collections
import re


'''
message = ur'帮我放忘情水'
pattern = ur'(帮我)?((播放)|(放))忘情水'
#re.match 从头开始匹配,必须从字符串的第一个字符开始就相符。
match = re.match(pattern, message).group()
if match:
	print match

message = ur' help    = 1'
pattern = ur'^.+='
match = re.match(pattern, message).group()
if match:
	match = match.strip(' =')
	print match
'''
#pattern的正则表达
class PatternRegexSet:
	variable = collections.defaultdict(lambda:0)
	action = []

#解析pattern文件
class Parser:
	
	RegexSet = PatternRegexSet()

	def ProcessSentence(self, sentence):
		pattern = ur'^.+='
		match = re.match(pattern, sentence)
		if match:
			key = self.FetchKey(match.group())

			#print match.end()
			#print sentence[match.end():].strip()
			value = self.FetchValue(sentence[match.end():].strip())
			if(value != '' and key != u'<action>'):
				value = self.ProcessValue(value)
				print value
				self.RegexSet.variable[key] = value
				self.PostProcessValue(value)

	#替换value中的变量
	def PostProcessValue(self, value):
		pattern = ur'<.*>'
		match = re.search(pattern, value)
		if match:
			print match.group()

	#记录]位置
	def ProcessValue(self, value):
		length = len(value)
		lst = []
		val = u'('
		for i in range(length):
			if value[i] == u'[':
				val = val + u'('
			elif value[i] == u']':
				val = val + u')?'
			else:
				val = val + value[i]
		val = val + u')'
		return val

	def LoadPattern(self, f):
		for line in file(f):
			line = line.replace('\n','')
			line = line.decode('utf-8')
			self.ProcessSentence(line)


	def FetchKey(self, key):
		key = key.strip(' =')
		return key

	def FetchValue(self, value):
		return value

if __name__ == '__main__':
	parser = Parser()
	parser.LoadPattern('pattern.txt')
	print parser.RegexSet.variable