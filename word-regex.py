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
	intention = []

#解析pattern文件
class Parser:

	RegexSet = PatternRegexSet()

	def ProcessSentence(self, sentence):
		#<aa> = 你好
		pattern = ur'\s*\{[a-zA-Z]\w*\}\s*='
		match = re.match(pattern, sentence)
		#print match.group()
		if match:
			key = self.FetchKey(match.group())

			#print match.end()
			#print sentence[match.end():].strip()
			value = self.FetchValue(sentence[match.end():].strip())
			if(value != '' and key != u'{action}'):
				self.RegexSet.variable[key] = value
			if(value != '' and key == u'{action}'):
				self.RegexSet.action.append(value)
		#print self.RegexSet.action
	#有些<>被计算了多次 需要refine,可能递归引用次数更好
	#valpara 里可能还有空格
	def DFS(self, valpara):
		retval = u''
		temp = self.RegexSet.variable.get(valpara)
		#找不到none
		if temp:
			temp = self.RegexSet.variable[valpara]
		else:
			temp = valpara
		temp = temp.split()

		for value in temp:
			val = u'('
			i = 0
			while i < len(value):
				#不允许一句<>里还有<>
				if value[i] != u'{':
					val = val + value[i]
				else:
					j = i
					while j < len(value):
						if value[j] == u'}':
							break;
						j = j + 1
					if j == len(value):
						print 'wrong pattern',valpara	
						return ''
					elif value[i: j + 1] == valpara:	
						print 'wrong pattern',valpara	
						return ''
					else:
						val = val + self.DFS(value[i: j + 1])
						i = j
				i = i + 1
			val = val + u')'
			retval = retval + val
		return retval


	#替换value中的变量
	def PostProcessValue(self):
		for key in self.RegexSet.variable:
			value = self.RegexSet.variable[key]
			sentence = u''
			value = value.split()
			for v in value:	
				PostValue = u''
				PostValue = PostValue + self.DFS(v)
				sentence = sentence + PostValue
			#print sentence


	def ProcessAction(self):
		for intention in self.RegexSet.action:

			#print '+', intention
			temp = self.DFS(intention) 
			val = u''
			for char in temp:
				if char == u']':
					val = val + u')?'
				elif char == u'[':
					val = val + u'('
				else:
					val = val + char
			
			val = val + u'$'
		#	print val			
			self.RegexSet.intention.append(val)

	def LoadPattern(self, f):
		for line in file(f):
			line = line.replace('\n','')
			line = line.decode('utf-8')		
			#print u'action' + line
			if line[0] == u'/':
				continue
			self.ProcessSentence(line)

		self.PostProcessValue()
		self.ProcessAction()

	def FetchKey(self, key):
		key = key.strip(' =')
		return key

	def FetchValue(self, value):
		value = value.strip()
		return value

if __name__ == '__main__':
	parser = Parser()
	parser.LoadPattern('pattern.txt')
	for line in file('sentence.txt'):
		line = line.replace('\n','')
		line = line.decode('utf-8')	
		line = line.strip()
		flag = 1
		for pattern in parser.RegexSet.intention:
			match = re.match(pattern, line)
			#print pattern
			if match:
				print match.group()
				flag = 0
		if flag:
			print line, 'match fail'

	#print parser.RegexSet.variable