# -*- coding: gbk -*-
import os
import codecs
import __builtin__
from bs4 import UnicodeDammit


def get_fileencoding(filename, default=None, detail=None):
	encoding = default
	skip_bytes = 0
	if os.path.isfile(filename):
		f = __builtin__.open(filename, "rb")
		try:
			s = f.read(2)
			"""
			ANSI£º				ÎÞ¸ñÊ½¶¨Òå£»
			Unicode£º			Ç°Á½¸ö×Ö½ÚÎªFFFE£»
			Unicode big endian£º	Ç°Á½×Ö½ÚÎªFEFF£»
			UTF-8 with BOM£º		Ç°Èý×Ö½ÚÎªEFBBBF£»
			"""
			if s == chr(0xff) + chr(0xfe):
				encoding = "utf_16_le"
				skip_bytes = 2
			elif s == chr(0xfe) + chr(0xff):
				encoding = "utf_16_be"
				skip_bytes = 2
			elif s == chr(0xef) + chr(0xbb):
				encoding = "utf-8-sig"
				skip_bytes = 3
		except:
			pass
		if not encoding:
			# Ê¹ÓÃBeautifulSoupµÄ±àÂëÊ¶±ð¹¦ÄÜ
			f.seek(0)
			line = f.readline()
			dammit = UnicodeDammit(line)
			# ×¢Òâ£¬ÕâÖÖ·½·¨ÓÐÊ±»ñÈ¡µ½µÄ±àÂëÊÇ'windows-1252'£¨À­¶¡×Ö·û¼¯µÄÒ»ÖÖ£©£¬Òò¶ø²»¿É¿¿¡£
			encoding = dammit.original_encoding
		f.close()
	if isinstance(detail, dict):
		detail["encoding"] = encoding
		detail["skip_bytes"] = skip_bytes
	return encoding


def open(filename, mode="r", encoding=None, skip_bytes=0):
	detail = {}
	if encoding is None:
		encoding = get_fileencoding(filename, detail=detail)
	if encoding is None:
		encoding = "gb18030"
	if not skip_bytes:
		skip_bytes = detail.get("skip_bytes", skip_bytes)

	# ×¢Òâ£ºcodecs.open ²»¹ÜÊÇ·ñÖ¸¶¨ÁËmode£¬×ÜÊÇÒÔ¶þ½øÖÆÄ£Ê½´ò¿ª¡£
	# Òò´ËÐèÒª×ÔÐÐ´¦ÀíÎÄ±¾ÎÄ¼þÖÐµÄ\r\n -> \n
	f = codecs.open(filename, mode=mode, encoding=encoding)
	f.seek(skip_bytes)	# Ìø¹ýÖ¸Ê¾Í·
	# ×¢Òâ£ºf.read()·µ»ØµÄÊÇunicode
	return f


def readfile(filename, encoding="gbk"):
	with open(filename) as f:
		content = f.read()
		content = content.replace(u"\r\n", u"\n")
		if encoding:
			content = content.encode(encoding)
	return content


if __name__ == "__main__":
	print readfile("1.txt")
