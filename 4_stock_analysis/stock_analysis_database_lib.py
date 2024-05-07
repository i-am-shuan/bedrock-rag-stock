import json
import os
import sys
import boto3
import sqlite3
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from pathlib import Path

## database
stock_ticker_data=[ 
    {
        "symbol" : "PRAA",
        "name" : "PRA Group, Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "AMZN",
        "name" : "Amazon.com, Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "TSLA",
        "name" : "Tesla Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "PAAS",
        "name" : "Pan American Silver Corp.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "PAAC",
        "name" : "Proficient Alpha Acquisition Corp.",
        "currency" : "USD",
        "stockExchange" : "NasdaqCM",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "RYAAY",
        "name" : "Ryanair Holdings plc",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "MPAA",
        "name" : "Motorcar Parts of America, Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "STAA",
        "name" : "STAAR Surgical Company",
        "currency" : "USD",
        "stockExchange" : "NasdaqGM",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "RBCAA",
        "name" : "Republic Bancorp, Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "AABA",
        "name" : "Altaba Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGS",
        "exchangeShortName" : "NASDAQ"    
    }, 
    {
        "symbol" : "AAXJ",
        "name" : "iShares MSCI All Country Asia ex Japan ETF",
        "currency" : "USD",
        "stockExchange" : "NasdaqGM",
        "exchangeShortName" : "NASDAQ"
    }, 
    {
        "symbol" : "ZNWAA",
        "name" : "Zion Oil & Gas, Inc.",
        "currency" : "USD",
        "stockExchange" : "NasdaqGM",
        "exchangeShortName" : "NASDAQ"
    },
	{
  "symbol": "095570.KS",
  "name": "AJ네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006840.KS",
  "name": "AK홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027410.KS",
  "name": "BGF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "282330.KS",
  "name": "BGF리테일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138930.KS",
  "name": "BNK금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001460.KS",
  "name": "BYC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001465.KS",
  "name": "BYC우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001040.KS",
  "name": "CJ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079160.KS",
  "name": "CJ CGV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00104K.KS",
  "name": "CJ4우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000120.KS",
  "name": "CJ대한통운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011150.KS",
  "name": "CJ씨푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011155.KS",
  "name": "CJ씨푸드1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001045.KS",
  "name": "CJ우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097950.KS",
  "name": "CJ제일제당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097955.KS",
  "name": "CJ제일제당 우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000480.KS",
  "name": "CR홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000590.KS",
  "name": "CS홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012030.KS",
  "name": "DB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016610.KS",
  "name": "DB금융투자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005830.KS",
  "name": "DB손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000990.KS",
  "name": "DB하이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139130.KS",
  "name": "DGB금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001530.KS",
  "name": "DI동일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000210.KS",
  "name": "DL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000215.KS",
  "name": "DL우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "375500.KS",
  "name": "DL이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "37550L.KS",
  "name": "DL이앤씨2우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "37550K.KS",
  "name": "DL이앤씨우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007340.KS",
  "name": "DN오토모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004840.KS",
  "name": "DRB동일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "155660.KS",
  "name": "DSR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069730.KS",
  "name": "DSR제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017860.KS",
  "name": "DS단석",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017940.KS",
  "name": "E1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "365550.KS",
  "name": "ESR켄달스퀘어리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "383220.KS",
  "name": "F&F",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007700.KS",
  "name": "F&F홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "114090.KS",
  "name": "GKL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078930.KS",
  "name": "GS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006360.KS",
  "name": "GS건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001250.KS",
  "name": "GS글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007070.KS",
  "name": "GS리테일",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078935.KS",
  "name": "GS우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012630.KS",
  "name": "HDC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039570.KS",
  "name": "HDC랩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089470.KS",
  "name": "HDC현대EP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "294870.KS",
  "name": "HDC현대산업개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009540.KS",
  "name": "HD한국조선해양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267250.KS",
  "name": "HD현대",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267270.KS",
  "name": "HD현대건설기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010620.KS",
  "name": "HD현대미포",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "322000.KS",
  "name": "HD현대에너지솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042670.KS",
  "name": "HD현대인프라코어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267260.KS",
  "name": "HD현대일렉트릭",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "329180.KS",
  "name": "HD현대중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097230.KS",
  "name": "HJ중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014790.KS",
  "name": "HL D&I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003580.KS",
  "name": "HLB글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "204320.KS",
  "name": "HL만도",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "060980.KS",
  "name": "HL홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011200.KS",
  "name": "HMM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035000.KS",
  "name": "HS애드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003560.KS",
  "name": "IHQ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "175330.KS",
  "name": "JB금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "234080.KS",
  "name": "JW생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001060.KS",
  "name": "JW중외제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001067.KS",
  "name": "JW중외제약2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001065.KS",
  "name": "JW중외제약우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096760.KS",
  "name": "JW홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105560.KS",
  "name": "KB금융",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "432320.KS",
  "name": "KB스타리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002380.KS",
  "name": "KCC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "344820.KS",
  "name": "KCC글라스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009070.KS",
  "name": "KCTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009440.KS",
  "name": "KC그린홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "119650.KS",
  "name": "KC코트렐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092220.KS",
  "name": "KEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003620.KS",
  "name": "KG모빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016380.KS",
  "name": "KG스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001390.KS",
  "name": "KG케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033180.KS",
  "name": "KH 필룩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015590.KS",
  "name": "KIB플러그에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001940.KS",
  "name": "KISCO홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025000.KS",
  "name": "KPX케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092230.KS",
  "name": "KPX홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000040.KS",
  "name": "KR모터스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044450.KS",
  "name": "KSS해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030200.KS",
  "name": "KT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033780.KS",
  "name": "KT&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058850.KS",
  "name": "KTcs",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058860.KS",
  "name": "KTis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093050.KS",
  "name": "LF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003550.KS",
  "name": "LG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034220.KS",
  "name": "LG디스플레이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051900.KS",
  "name": "LG생활건강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051905.KS",
  "name": "LG생활건강우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "373220.KS",
  "name": "LG에너지솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003555.KS",
  "name": "LG우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032640.KS",
  "name": "LG유플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011070.KS",
  "name": "LG이노텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066570.KS",
  "name": "LG전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066575.KS",
  "name": "LG전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037560.KS",
  "name": "LG헬로비전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051910.KS",
  "name": "LG화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051915.KS",
  "name": "LG화학우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079550.KS",
  "name": "LIG넥스원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006260.KS",
  "name": "LS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010120.KS",
  "name": "LS ELECTRIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000680.KS",
  "name": "LS네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "229640.KS",
  "name": "LS에코에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108320.KS",
  "name": "LX세미콘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001120.KS",
  "name": "LX인터내셔널",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108670.KS",
  "name": "LX하우시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "108675.KS",
  "name": "LX하우시스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "383800.KS",
  "name": "LX홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "38380K.KS",
  "name": "LX홀딩스1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023150.KS",
  "name": "MH에탄올",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035420.KS",
  "name": "NAVER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "181710.KS",
  "name": "NHN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "400760.KS",
  "name": "NH올원리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005940.KS",
  "name": "NH투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005945.KS",
  "name": "NH투자증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "338100.KS",
  "name": "NH프라임리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034310.KS",
  "name": "NICE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030190.KS",
  "name": "NICE평가정보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008260.KS",
  "name": "NI스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004250.KS",
  "name": "NPC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004255.KS",
  "name": "NPC우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "456040.KS",
  "name": "OCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010060.KS",
  "name": "OCI홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "178920.KS",
  "name": "PI첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005490.KS",
  "name": "POSCO홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010950.KS",
  "name": "S-Oil",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010955.KS",
  "name": "S-Oil우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034120.KS",
  "name": "SBS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005090.KS",
  "name": "SGC에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001380.KS",
  "name": "SG글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004060.KS",
  "name": "SG세계물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001770.KS",
  "name": "SHD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002360.KS",
  "name": "SH에너지화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009160.KS",
  "name": "SIMPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123700.KS",
  "name": "SJM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025530.KS",
  "name": "SJM홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034730.KS",
  "name": "SK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011790.KS",
  "name": "SKC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018670.KS",
  "name": "SK가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001740.KS",
  "name": "SK네트웍스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006120.KS",
  "name": "SK디스커버리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006125.KS",
  "name": "SK디스커버리우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "210980.KS",
  "name": "SK디앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "395400.KS",
  "name": "SK리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "302440.KS",
  "name": "SK바이오사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "326030.KS",
  "name": "SK바이오팜",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "402340.KS",
  "name": "SK스퀘어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "361610.KS",
  "name": "SK아이이테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100090.KS",
  "name": "SK오션플랜트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "03473K.KS",
  "name": "SK우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096770.KS",
  "name": "SK이노베이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "096775.KS",
  "name": "SK이노베이션우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "475150.KS",
  "name": "SK이터닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001510.KS",
  "name": "SK증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001515.KS",
  "name": "SK증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "285130.KS",
  "name": "SK케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "28513K.KS",
  "name": "SK케미칼우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017670.KS",
  "name": "SK텔레콤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000660.KS",
  "name": "SK하이닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003570.KS",
  "name": "SNT다이내믹스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "064960.KS",
  "name": "SNT모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100840.KS",
  "name": "SNT에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036530.KS",
  "name": "SNT홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005610.KS",
  "name": "SPC삼립",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011810.KS",
  "name": "STX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "465770.KS",
  "name": "STX그린로지스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "077970.KS",
  "name": "STX엔진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071970.KS",
  "name": "STX중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002820.KS",
  "name": "SUN&L",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084870.KS",
  "name": "TBH글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002710.KS",
  "name": "TCC스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069260.KS",
  "name": "TKG휴켐스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002900.KS",
  "name": "TYM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024070.KS",
  "name": "WISCOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037270.KS",
  "name": "YG PLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000500.KS",
  "name": "가온전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000860.KS",
  "name": "강남제비스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035250.KS",
  "name": "강원랜드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011420.KS",
  "name": "갤럭시아에스엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002100.KS",
  "name": "경농",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009450.KS",
  "name": "경동나비엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267290.KS",
  "name": "경동도시가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012320.KS",
  "name": "경동인베스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000050.KS",
  "name": "경방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214390.KS",
  "name": "경보제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012610.KS",
  "name": "경인양행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009140.KS",
  "name": "경인전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013580.KS",
  "name": "계룡건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012200.KS",
  "name": "계양전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012205.KS",
  "name": "계양전기우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002140.KS",
  "name": "고려산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010130.KS",
  "name": "고려아연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002240.KS",
  "name": "고려제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009290.KS",
  "name": "광동제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017040.KS",
  "name": "광명전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017900.KS",
  "name": "광전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "037710.KS",
  "name": "광주신세계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030610.KS",
  "name": "교보증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "339770.KS",
  "name": "교촌에프앤비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007690.KS",
  "name": "국도화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005320.KS",
  "name": "국동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001140.KS",
  "name": "국보",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002720.KS",
  "name": "국제약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "083420.KS",
  "name": "그린케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014530.KS",
  "name": "극동유화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014280.KS",
  "name": "금강공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014285.KS",
  "name": "금강공업우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008870.KS",
  "name": "금비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001570.KS",
  "name": "금양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002990.KS",
  "name": "금호건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002995.KS",
  "name": "금호건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011780.KS",
  "name": "금호석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011785.KS",
  "name": "금호석유우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214330.KS",
  "name": "금호에이치티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001210.KS",
  "name": "금호전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "073240.KS",
  "name": "금호타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092440.KS",
  "name": "기신정기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000270.KS",
  "name": "기아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024110.KS",
  "name": "기업은행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013700.KS",
  "name": "까뮤이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004540.KS",
  "name": "깨끗한나라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004545.KS",
  "name": "깨끗한나라우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001260.KS",
  "name": "남광토건",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008350.KS",
  "name": "남선알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008355.KS",
  "name": "남선알미우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004270.KS",
  "name": "남성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003920.KS",
  "name": "남양유업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003925.KS",
  "name": "남양유업우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025860.KS",
  "name": "남해화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005720.KS",
  "name": "넥센",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005725.KS",
  "name": "넥센우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002350.KS",
  "name": "넥센타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002355.KS",
  "name": "넥센타이어1우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092790.KS",
  "name": "넥스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "251270.KS",
  "name": "넷마블",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090350.KS",
  "name": "노루페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090355.KS",
  "name": "노루페인트우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000320.KS",
  "name": "노루홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000325.KS",
  "name": "노루홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006280.KS",
  "name": "녹십자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005250.KS",
  "name": "녹십자홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005257.KS",
  "name": "녹십자홀딩스2우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004370.KS",
  "name": "농심",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "072710.KS",
  "name": "농심홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058730.KS",
  "name": "다스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030210.KS",
  "name": "다올투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023590.KS",
  "name": "다우기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145210.KS",
  "name": "다이나믹디자인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019680.KS",
  "name": "대교",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019685.KS",
  "name": "대교우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006370.KS",
  "name": "대구백화점",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008060.KS",
  "name": "대덕",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00806K.KS",
  "name": "대덕1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "353200.KS",
  "name": "대덕전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "35320K.KS",
  "name": "대덕전자1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000490.KS",
  "name": "대동",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008110.KS",
  "name": "대동전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005750.KS",
  "name": "대림B&Co",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006570.KS",
  "name": "대림통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001680.KS",
  "name": "대상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001685.KS",
  "name": "대상우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084690.KS",
  "name": "대상홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084695.KS",
  "name": "대상홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "128820.KS",
  "name": "대성산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "117580.KS",
  "name": "대성에너지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016710.KS",
  "name": "대성홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003540.KS",
  "name": "대신증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003547.KS",
  "name": "대신증권2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003545.KS",
  "name": "대신증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009190.KS",
  "name": "대양금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014160.KS",
  "name": "대영포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047040.KS",
  "name": "대우건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009320.KS",
  "name": "대우부품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003090.KS",
  "name": "대웅",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069620.KS",
  "name": "대웅제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000430.KS",
  "name": "대원강업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006340.KS",
  "name": "대원전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006345.KS",
  "name": "대원전선우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003220.KS",
  "name": "대원제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024890.KS",
  "name": "대원화성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002880.KS",
  "name": "대유에이텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000300.KS",
  "name": "대유플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012800.KS",
  "name": "대창",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015230.KS",
  "name": "대창단조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001070.KS",
  "name": "대한방직",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006650.KS",
  "name": "대한유화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001440.KS",
  "name": "대한전선",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084010.KS",
  "name": "대한제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001790.KS",
  "name": "대한제당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001795.KS",
  "name": "대한제당우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001130.KS",
  "name": "대한제분",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003490.KS",
  "name": "대한항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003495.KS",
  "name": "대한항공우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005880.KS",
  "name": "대한해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003830.KS",
  "name": "대한화섬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016090.KS",
  "name": "대현",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069460.KS",
  "name": "대호에이엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192080.KS",
  "name": "더블유게임즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012510.KS",
  "name": "더존비즈온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004830.KS",
  "name": "덕성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004835.KS",
  "name": "덕성우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024900.KS",
  "name": "덕양산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145720.KS",
  "name": "덴티움",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002150.KS",
  "name": "도화엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "460850.KS",
  "name": "동국씨엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "460860.KS",
  "name": "동국제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001230.KS",
  "name": "동국홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023450.KS",
  "name": "동남합성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004140.KS",
  "name": "동방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007590.KS",
  "name": "동방아그로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005960.KS",
  "name": "동부건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005965.KS",
  "name": "동부건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026960.KS",
  "name": "동서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002210.KS",
  "name": "동성제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102260.KS",
  "name": "동성케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000640.KS",
  "name": "동아쏘시오홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "170900.KS",
  "name": "동아에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028100.KS",
  "name": "동아지질",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "282690.KS",
  "name": "동아타이어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001520.KS",
  "name": "동양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001527.KS",
  "name": "동양2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084670.KS",
  "name": "동양고속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "082640.KS",
  "name": "동양생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001525.KS",
  "name": "동양우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008970.KS",
  "name": "동양철관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092780.KS",
  "name": "동양피스톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "049770.KS",
  "name": "동원F&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018500.KS",
  "name": "동원금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006040.KS",
  "name": "동원산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030720.KS",
  "name": "동원수산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014820.KS",
  "name": "동원시스템즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014825.KS",
  "name": "동원시스템즈우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111380.KS",
  "name": "동인기연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "163560.KS",
  "name": "동일고무벨트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004890.KS",
  "name": "동일산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002690.KS",
  "name": "동일제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000020.KS",
  "name": "동화약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000150.KS",
  "name": "두산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000157.KS",
  "name": "두산2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "454910.KS",
  "name": "두산로보틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "241560.KS",
  "name": "두산밥캣",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034020.KS",
  "name": "두산에너빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000155.KS",
  "name": "두산우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "336260.KS",
  "name": "두산퓨얼셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33626K.KS",
  "name": "두산퓨얼셀1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33626L.KS",
  "name": "두산퓨얼셀2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016740.KS",
  "name": "두올",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192650.KS",
  "name": "드림텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024090.KS",
  "name": "디씨엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003160.KS",
  "name": "디아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "092200.KS",
  "name": "디아이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377190.KS",
  "name": "디앤디플랫폼리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013570.KS",
  "name": "디와이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "210540.KS",
  "name": "디와이파워",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "115390.KS",
  "name": "락앤락",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032350.KS",
  "name": "롯데관광개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089860.KS",
  "name": "롯데렌탈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "330590.KS",
  "name": "롯데리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000400.KS",
  "name": "롯데손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023530.KS",
  "name": "롯데쇼핑",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020150.KS",
  "name": "롯데에너지머티리얼즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "280360.KS",
  "name": "롯데웰푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "286940.KS",
  "name": "롯데이노베이트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004000.KS",
  "name": "롯데정밀화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004990.KS",
  "name": "롯데지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00499K.KS",
  "name": "롯데지주우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005300.KS",
  "name": "롯데칠성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005305.KS",
  "name": "롯데칠성우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011170.KS",
  "name": "롯데케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071840.KS",
  "name": "롯데하이마트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027740.KS",
  "name": "마니커",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357430.KS",
  "name": "마스턴프리미어리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001080.KS",
  "name": "만호제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088980.KS",
  "name": "맥쿼리인프라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "094800.KS",
  "name": "맵스리얼티1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138040.KS",
  "name": "메리츠금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090370.KS",
  "name": "메타랩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017180.KS",
  "name": "명문제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009900.KS",
  "name": "명신산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012690.KS",
  "name": "모나리자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005360.KS",
  "name": "모나미",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009680.KS",
  "name": "모토닉",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009580.KS",
  "name": "무림P&P",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009200.KS",
  "name": "무림페이퍼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033920.KS",
  "name": "무학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008420.KS",
  "name": "문배철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025560.KS",
  "name": "미래산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007120.KS",
  "name": "미래아이앤지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "396690.KS",
  "name": "미래에셋글로벌리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357250.KS",
  "name": "미래에셋맵스리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "085620.KS",
  "name": "미래에셋생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006800.KS",
  "name": "미래에셋증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00680K.KS",
  "name": "미래에셋증권2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006805.KS",
  "name": "미래에셋증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002840.KS",
  "name": "미원상사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "268280.KS",
  "name": "미원에스씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "107590.KS",
  "name": "미원홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "134380.KS",
  "name": "미원화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003650.KS",
  "name": "미창석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377740.KS",
  "name": "바이오노트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003610.KS",
  "name": "방림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001340.KS",
  "name": "백광산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035150.KS",
  "name": "백산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002410.KS",
  "name": "범양건영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007210.KS",
  "name": "벽산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002760.KS",
  "name": "보락",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003850.KS",
  "name": "보령",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000890.KS",
  "name": "보해양조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003000.KS",
  "name": "부광약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001270.KS",
  "name": "부국증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001275.KS",
  "name": "부국증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026940.KS",
  "name": "부국철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011390.KS",
  "name": "부산산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005030.KS",
  "name": "부산주공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002070.KS",
  "name": "비비안",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100220.KS",
  "name": "비상교육",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090460.KS",
  "name": "비에이치",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030790.KS",
  "name": "비케이탑스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005180.KS",
  "name": "빙그레",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003960.KS",
  "name": "사조대림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008040.KS",
  "name": "사조동아원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007160.KS",
  "name": "사조산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014710.KS",
  "name": "사조씨푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006090.KS",
  "name": "사조오양",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001470.KS",
  "name": "삼부토건",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028050.KS",
  "name": "삼성E&A",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "448730.KS",
  "name": "삼성FN리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006400.KS",
  "name": "삼성SDI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006405.KS",
  "name": "삼성SDI우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006660.KS",
  "name": "삼성공조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028260.KS",
  "name": "삼성물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "02826K.KS",
  "name": "삼성물산우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "207940.KS",
  "name": "삼성바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032830.KS",
  "name": "삼성생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018260.KS",
  "name": "삼성에스디에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009150.KS",
  "name": "삼성전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009155.KS",
  "name": "삼성전기우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005930.KS",
  "name": "삼성전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005935.KS",
  "name": "삼성전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001360.KS",
  "name": "삼성제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010140.KS",
  "name": "삼성중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016360.KS",
  "name": "삼성증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "068290.KS",
  "name": "삼성출판사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029780.KS",
  "name": "삼성카드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000810.KS",
  "name": "삼성화재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000815.KS",
  "name": "삼성화재우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006110.KS",
  "name": "삼아알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145990.KS",
  "name": "삼양사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145995.KS",
  "name": "삼양사우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003230.KS",
  "name": "삼양식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002170.KS",
  "name": "삼양통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272550.KS",
  "name": "삼양패키징",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000070.KS",
  "name": "삼양홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000075.KS",
  "name": "삼양홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003720.KS",
  "name": "삼영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002810.KS",
  "name": "삼영무역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005680.KS",
  "name": "삼영전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023000.KS",
  "name": "삼원강재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004380.KS",
  "name": "삼익THK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002450.KS",
  "name": "삼익악기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004440.KS",
  "name": "삼일씨엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000520.KS",
  "name": "삼일제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009770.KS",
  "name": "삼정펄프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005500.KS",
  "name": "삼진제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004690.KS",
  "name": "삼천리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010960.KS",
  "name": "삼호개발",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004450.KS",
  "name": "삼화왕관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009470.KS",
  "name": "삼화전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011230.KS",
  "name": "삼화전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001820.KS",
  "name": "삼화콘덴서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000390.KS",
  "name": "삼화페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001290.KS",
  "name": "상상인증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "041650.KS",
  "name": "상신브레이크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "075180.KS",
  "name": "새론오토모티브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007540.KS",
  "name": "샘표",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "248170.KS",
  "name": "샘표식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007860.KS",
  "name": "서연",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "200880.KS",
  "name": "서연이화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017390.KS",
  "name": "서울가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004410.KS",
  "name": "서울식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004415.KS",
  "name": "서울식품우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021050.KS",
  "name": "서원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008490.KS",
  "name": "서흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007610.KS",
  "name": "선도전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "136490.KS",
  "name": "선진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014910.KS",
  "name": "성문전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014915.KS",
  "name": "성문전자우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003080.KS",
  "name": "성보화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004980.KS",
  "name": "성신양회",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004985.KS",
  "name": "성신양회우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011300.KS",
  "name": "성안머티리얼스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000180.KS",
  "name": "성창기업지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002420.KS",
  "name": "세기상사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004360.KS",
  "name": "세방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004365.KS",
  "name": "세방우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004490.KS",
  "name": "세방전지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001430.KS",
  "name": "세아베스틸지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "306200.KS",
  "name": "세아제강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003030.KS",
  "name": "세아제강지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019440.KS",
  "name": "세아특수강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058650.KS",
  "name": "세아홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013000.KS",
  "name": "세우글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "091090.KS",
  "name": "세원이앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021820.KS",
  "name": "세원정공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "067830.KS",
  "name": "세이브존I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033530.KS",
  "name": "세종공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "075580.KS",
  "name": "세진중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "068270.KS",
  "name": "셀트리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "336370.KS",
  "name": "솔루스첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33637K.KS",
  "name": "솔루스첨단소재1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "33637L.KS",
  "name": "솔루스첨단소재2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "248070.KS",
  "name": "솔루엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004430.KS",
  "name": "송원산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "126720.KS",
  "name": "수산인더스트리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017550.KS",
  "name": "수산중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "053210.KS",
  "name": "스카이라이프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "204210.KS",
  "name": "스타리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "026890.KS",
  "name": "스틱인베스트먼트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "134790.KS",
  "name": "시디즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016590.KS",
  "name": "신대양제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029530.KS",
  "name": "신도리코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004970.KS",
  "name": "신라교역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011930.KS",
  "name": "신성이엔지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005390.KS",
  "name": "신성통상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004170.KS",
  "name": "신세계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035510.KS",
  "name": "신세계 I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034300.KS",
  "name": "신세계건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031430.KS",
  "name": "신세계인터내셔날",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031440.KS",
  "name": "신세계푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006880.KS",
  "name": "신송홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005800.KS",
  "name": "신영와코루",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001720.KS",
  "name": "신영증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001725.KS",
  "name": "신영증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009270.KS",
  "name": "신원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002700.KS",
  "name": "신일전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002870.KS",
  "name": "신풍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019170.KS",
  "name": "신풍제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019175.KS",
  "name": "신풍제약우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "404990.KS",
  "name": "신한서부티엔디리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "293940.KS",
  "name": "신한알파리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "055550.KS",
  "name": "신한지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004080.KS",
  "name": "신흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102280.KS",
  "name": "쌍방울",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003410.KS",
  "name": "쌍용C&E",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004770.KS",
  "name": "써니전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "403550.KS",
  "name": "쏘카",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004920.KS",
  "name": "씨아이테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "112610.KS",
  "name": "씨에스윈드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "308170.KS",
  "name": "씨티알모빌리티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008700.KS",
  "name": "아남전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002790.KS",
  "name": "아모레G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00279K.KS",
  "name": "아모레G3우(전환)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002795.KS",
  "name": "아모레G우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090430.KS",
  "name": "아모레퍼시픽",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090435.KS",
  "name": "아모레퍼시픽우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002030.KS",
  "name": "아세아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "183190.KS",
  "name": "아세아시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002310.KS",
  "name": "아세아제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012170.KS",
  "name": "아센디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "267850.KS",
  "name": "아시아나IDT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020560.KS",
  "name": "아시아나항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "122900.KS",
  "name": "아이마켓코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010780.KS",
  "name": "아이에스동서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139990.KS",
  "name": "아주스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001780.KS",
  "name": "알루코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018250.KS",
  "name": "애경산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161000.KS",
  "name": "애경케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011090.KS",
  "name": "에넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "137310.KS",
  "name": "에스디바이오센서",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "118000.KS",
  "name": "에스메디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005850.KS",
  "name": "에스엘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010580.KS",
  "name": "에스엠벡셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012750.KS",
  "name": "에스원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023960.KS",
  "name": "에쓰씨엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298690.KS",
  "name": "에어부산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "140910.KS",
  "name": "에이리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078520.KS",
  "name": "에이블씨엔씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015260.KS",
  "name": "에이엔피",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007460.KS",
  "name": "에이프로젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003060.KS",
  "name": "에이프로젠바이오로직스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "244920.KS",
  "name": "에이플러스에셋",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "278470.KS",
  "name": "에이피알",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "450080.KS",
  "name": "에코프로머티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036570.KS",
  "name": "엔씨소프트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "085310.KS",
  "name": "엔케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "900140.KS",
  "name": "엘브이엠씨홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "066970.KS",
  "name": "엘앤에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "097520.KS",
  "name": "엠씨넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014440.KS",
  "name": "영보화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111770.KS",
  "name": "영원무역",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009970.KS",
  "name": "영원무역홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003520.KS",
  "name": "영진약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000670.KS",
  "name": "영풍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006740.KS",
  "name": "영풍제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012280.KS",
  "name": "영화금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012160.KS",
  "name": "영흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015360.KS",
  "name": "예스코홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007310.KS",
  "name": "오뚜기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002630.KS",
  "name": "오리엔트바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271560.KS",
  "name": "오리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001800.KS",
  "name": "오리온홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011690.KS",
  "name": "와이투솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "070960.KS",
  "name": "용평리조트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "316140.KS",
  "name": "우리금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006980.KS",
  "name": "우성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017370.KS",
  "name": "우신시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105840.KS",
  "name": "우진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010400.KS",
  "name": "우진아이엔에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "049800.KS",
  "name": "우진플라임",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016880.KS",
  "name": "웅진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "095720.KS",
  "name": "웅진씽크빅",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005820.KS",
  "name": "원림",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010600.KS",
  "name": "웰바이오텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008600.KS",
  "name": "윌비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033270.KS",
  "name": "유나이티드제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014830.KS",
  "name": "유니드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "446070.KS",
  "name": "유니드비티플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000910.KS",
  "name": "유니온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047400.KS",
  "name": "유니온머티리얼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011330.KS",
  "name": "유니켐",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "077500.KS",
  "name": "유니퀘스트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002920.KS",
  "name": "유성기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000700.KS",
  "name": "유수홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003470.KS",
  "name": "유안타증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003475.KS",
  "name": "유안타증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "072130.KS",
  "name": "유엔젤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000220.KS",
  "name": "유유제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000225.KS",
  "name": "유유제약1우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000227.KS",
  "name": "유유제약2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001200.KS",
  "name": "유진투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000100.KS",
  "name": "유한양행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000105.KS",
  "name": "유한양행우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003460.KS",
  "name": "유화증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003465.KS",
  "name": "유화증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008730.KS",
  "name": "율촌화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008250.KS",
  "name": "이건산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025820.KS",
  "name": "이구산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214320.KS",
  "name": "이노션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088260.KS",
  "name": "이리츠코크렙",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "139480.KS",
  "name": "이마트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "457190.KS",
  "name": "이수스페셜티케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007660.KS",
  "name": "이수페타시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005950.KS",
  "name": "이수화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015020.KS",
  "name": "이스타코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093230.KS",
  "name": "이아이디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "074610.KS",
  "name": "이엔플러스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "102460.KS",
  "name": "이연제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "084680.KS",
  "name": "이월드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "350520.KS",
  "name": "이지스레지던스리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "334890.KS",
  "name": "이지스밸류리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000760.KS",
  "name": "이화산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014990.KS",
  "name": "인디에프",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "101140.KS",
  "name": "인바이오젠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006490.KS",
  "name": "인스코비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023800.KS",
  "name": "인지컨트롤스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034590.KS",
  "name": "인천도시가스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "129260.KS",
  "name": "인터지스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023810.KS",
  "name": "인팩",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "249420.KS",
  "name": "일동제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000230.KS",
  "name": "일동홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013360.KS",
  "name": "일성건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003120.KS",
  "name": "일성아이에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003200.KS",
  "name": "일신방직",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007110.KS",
  "name": "일신석재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007570.KS",
  "name": "일양약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007575.KS",
  "name": "일양약품우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008500.KS",
  "name": "일정실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "081000.KS",
  "name": "일진다이아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020760.KS",
  "name": "일진디스플",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "103590.KS",
  "name": "일진전기",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271940.KS",
  "name": "일진하이솔루스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015860.KS",
  "name": "일진홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "226320.KS",
  "name": "잇츠한불",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "317400.KS",
  "name": "자이에스앤디",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033240.KS",
  "name": "자화전자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000950.KS",
  "name": "전방",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "348950.KS",
  "name": "제이알글로벌리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "194370.KS",
  "name": "제이에스코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025620.KS",
  "name": "제이준코스메틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "030000.KS",
  "name": "제일기획",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "271980.KS",
  "name": "제일약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001560.KS",
  "name": "제일연마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002620.KS",
  "name": "제일파마홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006220.KS",
  "name": "제주은행",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "089590.KS",
  "name": "제주항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004910.KS",
  "name": "조광페인트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004700.KS",
  "name": "조광피혁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001550.KS",
  "name": "조비",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "462520.KS",
  "name": "조선내화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120030.KS",
  "name": "조선선재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018470.KS",
  "name": "조일알미늄",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002600.KS",
  "name": "조흥",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "185750.KS",
  "name": "종근당",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "063160.KS",
  "name": "종근당바이오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001630.KS",
  "name": "종근당홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "109070.KS",
  "name": "주성코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044380.KS",
  "name": "주연테크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013890.KS",
  "name": "지누스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013870.KS",
  "name": "지엠비코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071320.KS",
  "name": "지역난방공사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088790.KS",
  "name": "진도",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003780.KS",
  "name": "진양산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010640.KS",
  "name": "진양폴리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "100250.KS",
  "name": "진양홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051630.KS",
  "name": "진양화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272450.KS",
  "name": "진에어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011000.KS",
  "name": "진원생명과학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002780.KS",
  "name": "진흥기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002787.KS",
  "name": "진흥기업2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002785.KS",
  "name": "진흥기업우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009310.KS",
  "name": "참엔지니어링",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000650.KS",
  "name": "천일고속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012600.KS",
  "name": "청호ICT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "033250.KS",
  "name": "체시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "035720.KS",
  "name": "카카오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "323410.KS",
  "name": "카카오뱅크",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "377300.KS",
  "name": "카카오페이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006380.KS",
  "name": "카프로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001620.KS",
  "name": "케이비아이동국실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "029460.KS",
  "name": "케이씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "281820.KS",
  "name": "케이씨텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "381970.KS",
  "name": "케이카",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "145270.KS",
  "name": "케이탑리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "417310.KS",
  "name": "코람코더원리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "357120.KS",
  "name": "코람코라이프인프라리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007815.KS",
  "name": "코리아써우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007810.KS",
  "name": "코리아써키트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00781K.KS",
  "name": "코리아써키트2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003690.KS",
  "name": "코리안리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192820.KS",
  "name": "코스맥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "044820.KS",
  "name": "코스맥스비티아이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005070.KS",
  "name": "코스모신소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005420.KS",
  "name": "코스모화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071950.KS",
  "name": "코아스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002020.KS",
  "name": "코오롱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003070.KS",
  "name": "코오롱글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003075.KS",
  "name": "코오롱글로벌우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "450140.KS",
  "name": "코오롱모빌리티그룹",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "45014K.KS",
  "name": "코오롱모빌리티그룹우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002025.KS",
  "name": "코오롱우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120110.KS",
  "name": "코오롱인더",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "120115.KS",
  "name": "코오롱인더우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "138490.KS",
  "name": "코오롱플라스틱",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "021240.KS",
  "name": "코웨이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036420.KS",
  "name": "콘텐트리중앙",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "024720.KS",
  "name": "콜마홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "031820.KS",
  "name": "콤텍시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "192400.KS",
  "name": "쿠쿠홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "284740.KS",
  "name": "쿠쿠홈시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "264900.KS",
  "name": "크라운제과",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "26490K.KS",
  "name": "크라운제과우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005740.KS",
  "name": "크라운해태홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005745.KS",
  "name": "크라운해태홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "259960.KS",
  "name": "크래프톤",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020120.KS",
  "name": "키다리스튜디오",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039490.KS",
  "name": "키움증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014580.KS",
  "name": "태경비케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015890.KS",
  "name": "태경산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006890.KS",
  "name": "태경케미컬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003240.KS",
  "name": "태광산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011280.KS",
  "name": "태림포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004100.KS",
  "name": "태양금속",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004105.KS",
  "name": "태양금속우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009410.KS",
  "name": "태영건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009415.KS",
  "name": "태영건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001420.KS",
  "name": "태원물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007980.KS",
  "name": "태평양물산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "055490.KS",
  "name": "테이팩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "078000.KS",
  "name": "텔코웨어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "214420.KS",
  "name": "토니모리",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019180.KS",
  "name": "티에이치엔",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "363280.KS",
  "name": "티와이홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "36328K.KS",
  "name": "티와이홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "091810.KS",
  "name": "티웨이항공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004870.KS",
  "name": "티웨이홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005690.KS",
  "name": "파미셀",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036580.KS",
  "name": "팜스코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004720.KS",
  "name": "팜젠사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "028670.KS",
  "name": "팬오션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010820.KS",
  "name": "퍼스텍",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016800.KS",
  "name": "퍼시스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001020.KS",
  "name": "페이퍼코리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "090080.KS",
  "name": "평화산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010770.KS",
  "name": "평화홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "022100.KS",
  "name": "포스코DX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "058430.KS",
  "name": "포스코스틸리온",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047050.KS",
  "name": "포스코인터내셔널",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003670.KS",
  "name": "포스코퓨처엠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017810.KS",
  "name": "풀무원",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "103140.KS",
  "name": "풍산",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005810.KS",
  "name": "풍산홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "950210.KS",
  "name": "프레스티지바이오파마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009810.KS",
  "name": "플레이그램",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "086790.KS",
  "name": "하나금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "293480.KS",
  "name": "하나제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "039130.KS",
  "name": "하나투어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "352820.KS",
  "name": "하이브",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071090.KS",
  "name": "하이스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "019490.KS",
  "name": "하이트론",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000080.KS",
  "name": "하이트진로",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000087.KS",
  "name": "하이트진로2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000140.KS",
  "name": "하이트진로홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000145.KS",
  "name": "하이트진로홀딩스우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "152550.KS",
  "name": "한국ANKOR유전",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "036460.KS",
  "name": "한국가스공사",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005430.KS",
  "name": "한국공항",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071050.KS",
  "name": "한국금융지주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "071055.KS",
  "name": "한국금융지주우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010040.KS",
  "name": "한국내화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025540.KS",
  "name": "한국단자",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010100.KS",
  "name": "한국무브넥스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004090.KS",
  "name": "한국석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002200.KS",
  "name": "한국수출포장",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002960.KS",
  "name": "한국쉘석유",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000240.KS",
  "name": "한국앤컴퍼니",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123890.KS",
  "name": "한국자산신탁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "015760.KS",
  "name": "한국전력",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006200.KS",
  "name": "한국전자홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "027970.KS",
  "name": "한국제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "023350.KS",
  "name": "한국종합기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025890.KS",
  "name": "한국주강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000970.KS",
  "name": "한국주철관",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "104700.KS",
  "name": "한국철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017960.KS",
  "name": "한국카본",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161890.KS",
  "name": "한국콜마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "161390.KS",
  "name": "한국타이어앤테크놀로지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "034830.KS",
  "name": "한국토지신탁",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "007280.KS",
  "name": "한국특강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "168490.KS",
  "name": "한국패러랠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "047810.KS",
  "name": "한국항공우주",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "123690.KS",
  "name": "한국화장품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003350.KS",
  "name": "한국화장품제조",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011500.KS",
  "name": "한농화성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002390.KS",
  "name": "한독",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "053690.KS",
  "name": "한미글로벌",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042700.KS",
  "name": "한미반도체",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008930.KS",
  "name": "한미사이언스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "128940.KS",
  "name": "한미약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009240.KS",
  "name": "한샘",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "020000.KS",
  "name": "한섬",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003680.KS",
  "name": "한성기업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "105630.KS",
  "name": "한세실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069640.KS",
  "name": "한세엠케이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016450.KS",
  "name": "한세예스24홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010420.KS",
  "name": "한솔PNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009180.KS",
  "name": "한솔로지스틱스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "213500.KS",
  "name": "한솔제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014680.KS",
  "name": "한솔케미칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004710.KS",
  "name": "한솔테크닉스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004150.KS",
  "name": "한솔홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "025750.KS",
  "name": "한솔홈데코",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004960.KS",
  "name": "한신공영",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011700.KS",
  "name": "한신기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001750.KS",
  "name": "한양증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001755.KS",
  "name": "한양증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "018880.KS",
  "name": "한온시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009420.KS",
  "name": "한올바이오파마",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "014130.KS",
  "name": "한익스프레스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "300720.KS",
  "name": "한일시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002220.KS",
  "name": "한일철강",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006390.KS",
  "name": "한일현대시멘트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003300.KS",
  "name": "한일홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "051600.KS",
  "name": "한전KPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "052690.KS",
  "name": "한전기술",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "130660.KS",
  "name": "한전산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002320.KS",
  "name": "한진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003480.KS",
  "name": "한진중공업홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "180640.KS",
  "name": "한진칼",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "18064K.KS",
  "name": "한진칼우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005110.KS",
  "name": "한창",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009460.KS",
  "name": "한창제지",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "372910.KS",
  "name": "한컴라이프케어",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000880.KS",
  "name": "한화",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "00088K.KS",
  "name": "한화3우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "452260.KS",
  "name": "한화갤러리아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "45226K.KS",
  "name": "한화갤러리아우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "451800.KS",
  "name": "한화리츠",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "088350.KS",
  "name": "한화생명",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000370.KS",
  "name": "한화손해보험",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009830.KS",
  "name": "한화솔루션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "009835.KS",
  "name": "한화솔루션우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "272210.KS",
  "name": "한화시스템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012450.KS",
  "name": "한화에어로스페이스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "082740.KS",
  "name": "한화엔진",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "042660.KS",
  "name": "한화오션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000885.KS",
  "name": "한화우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003530.KS",
  "name": "한화투자증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003535.KS",
  "name": "한화투자증권우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "195870.KS",
  "name": "해성디에스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "101530.KS",
  "name": "해태제과식품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "143210.KS",
  "name": "핸즈코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000720.KS",
  "name": "현대건설",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000725.KS",
  "name": "현대건설우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "453340.KS",
  "name": "현대그린푸드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "086280.KS",
  "name": "현대글로비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "064350.KS",
  "name": "현대로템",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079430.KS",
  "name": "현대리바트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "012330.KS",
  "name": "현대모비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "069960.KS",
  "name": "현대백화점",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004560.KS",
  "name": "현대비앤지스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004310.KS",
  "name": "현대약품",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "017800.KS",
  "name": "현대엘리베이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "307950.KS",
  "name": "현대오토에버",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011210.KS",
  "name": "현대위아",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004020.KS",
  "name": "현대제철",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005440.KS",
  "name": "현대지에프홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005380.KS",
  "name": "현대차",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005387.KS",
  "name": "현대차2우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005389.KS",
  "name": "현대차3우B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005385.KS",
  "name": "현대차우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001500.KS",
  "name": "현대차증권",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "011760.KS",
  "name": "현대코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "227840.KS",
  "name": "현대코퍼레이션홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "126560.KS",
  "name": "현대퓨처넷",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "001450.KS",
  "name": "현대해상",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "057050.KS",
  "name": "현대홈쇼핑",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093240.KS",
  "name": "형지엘리트",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003010.KS",
  "name": "혜인",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "111110.KS",
  "name": "호전실업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008770.KS",
  "name": "호텔신라",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "008775.KS",
  "name": "호텔신라우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "002460.KS",
  "name": "화성산업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "378850.KS",
  "name": "화승알앤에이",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "241590.KS",
  "name": "화승엔터프라이즈",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "006060.KS",
  "name": "화승인더",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "013520.KS",
  "name": "화승코퍼레이션",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010690.KS",
  "name": "화신",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "133820.KS",
  "name": "화인베스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "010660.KS",
  "name": "화천기계",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000850.KS",
  "name": "화천기공",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "016580.KS",
  "name": "환인제약",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "032560.KS",
  "name": "황금에스티",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "004800.KS",
  "name": "효성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "094280.KS",
  "name": "효성ITX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298040.KS",
  "name": "효성중공업",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298050.KS",
  "name": "효성첨단소재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298020.KS",
  "name": "효성티앤씨",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "298000.KS",
  "name": "효성화학",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "093370.KS",
  "name": "후성",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "081660.KS",
  "name": "휠라홀딩스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005870.KS",
  "name": "휴니드",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "079980.KS",
  "name": "휴비스",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "005010.KS",
  "name": "휴스틸",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000540.KS",
  "name": "흥국화재",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "000545.KS",
  "name": "흥국화재우",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "003280.KS",
  "name": "흥아해운",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSPI"
 },
 {
  "symbol": "366030.KD",
  "name": "09WOMEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "159580.KD",
  "name": "0TO7",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060310.KD",
  "name": "3S KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389140.KD",
  "name": "4by4",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "262260.KD",
  "name": "A Pro",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013310.KD",
  "name": "A-JIN INDUSTRY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071670.KD",
  "name": "A-Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036010.KD",
  "name": "ABEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "129890.KD",
  "name": "ABKO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298380.KD",
  "name": "ABL Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203400.KD",
  "name": "ABN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "102120.KD",
  "name": "ABOV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052790.KD",
  "name": "ACTOZ SOFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "179530.KD",
  "name": "ADBIOTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054630.KD",
  "name": "ADChips",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187660.KD",
  "name": "ADM Korea",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200710.KD",
  "name": "ADTechnology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "312610.KD",
  "name": "AFW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013990.KD",
  "name": "AGABANG&CO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001540.KD",
  "name": "AHN-GOOK PHA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053800.KD",
  "name": "AHNLAB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059120.KD",
  "name": "AJINEXTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027360.KD",
  "name": "AJU IB INVESTMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "354320.KD",
  "name": "ALMAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297570.KD",
  "name": "ALOYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "172670.KD",
  "name": "ALT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "074430.KD",
  "name": "AMINOLOGICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "125210.KD",
  "name": "AMOGREENTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123860.KD",
  "name": "ANAPASS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455900.KD",
  "name": "ANGEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310200.KD",
  "name": "ANIPLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121600.KD",
  "name": "ANP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065660.KD",
  "name": "ANTEROGEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109960.KD",
  "name": "AP Healthcare",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265520.KD",
  "name": "AP Systems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200470.KD",
  "name": "APACT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054620.KD",
  "name": "APS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "211270.KD",
  "name": "APSI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "159010.KD",
  "name": "ASFLOW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "127710.KD",
  "name": "ASIA BUSINESS DAILY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "154030.KD",
  "name": "ASIA SEED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050860.KD",
  "name": "ASIA TECHNOLOGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445090.KD",
  "name": "ASICLAND",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136410.KD",
  "name": "ASSEMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246720.KD",
  "name": "ASTA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067390.KD",
  "name": "ASTK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241840.KD",
  "name": "ASTORY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "453860.KD",
  "name": "ASTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089530.KD",
  "name": "AT semicon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045660.KD",
  "name": "ATEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "224110.KD",
  "name": "ATEC MOBILITY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "158430.KD",
  "name": "ATON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "355690.KD",
  "name": "ATUM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039830.KD",
  "name": "AURORA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "322310.KD",
  "name": "AUROSTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031510.KD",
  "name": "AUSTEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "353590.KD",
  "name": "AUTO&",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083930.KD",
  "name": "AVACO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "149950.KD",
  "name": "AVATEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "356680.KD",
  "name": "AXGATE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032080.KD",
  "name": "AZTECHWB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "174900.KD",
  "name": "AbClon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195990.KD",
  "name": "Abpro Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950130.KD",
  "name": "Access Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088800.KD",
  "name": "Ace Technologies",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003800.KD",
  "name": "AceBed",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290740.KD",
  "name": "ActRo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "205500.KD",
  "name": "Action Square",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347860.KD",
  "name": "Alchera",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238120.KD",
  "name": "Aligned",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "117670.KD",
  "name": "Alpha Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196170.KD",
  "name": "Alteogen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085810.KD",
  "name": "Alticast",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123750.KD",
  "name": "Alton",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900100.KD",
  "name": "Ameridge",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092040.KD",
  "name": "Amicogen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357580.KD",
  "name": "Amosense",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052710.KD",
  "name": "Amotech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025980.KD",
  "name": "Ananti",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299910.KD",
  "name": "Anic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196300.KD",
  "name": "AnyGen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "397030.KD",
  "name": "AprilBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "293780.KD",
  "name": "Aptabio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "291650.KD",
  "name": "Aptamer Sciences",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260660.KD",
  "name": "Arlico",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096690.KD",
  "name": "Aroot",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321820.KD",
  "name": "Artist United",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021080.KD",
  "name": "Atinum Investment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067170.KD",
  "name": "Autech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230980.KD",
  "name": "B.U Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307870.KD",
  "name": "B2En",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267790.KD",
  "name": "BARREL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318410.KD",
  "name": "BBC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451250.KD",
  "name": "BBIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "146320.KD",
  "name": "BCNC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200780.KD",
  "name": "BCWORLDPHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148140.KD",
  "name": "BDI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "406820.KD",
  "name": "BEAUTYSKIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148780.KD",
  "name": "BECUAI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206400.KD",
  "name": "BENO TNR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "139050.KD",
  "name": "BFLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046310.KD",
  "name": "BG T&A",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126600.KD",
  "name": "BGF Ecomaterials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382900.KD",
  "name": "BHF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083650.KD",
  "name": "BHI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238200.KD",
  "name": "BIFIDO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251120.KD",
  "name": "BIO-FD&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "314930.KD",
  "name": "BIODYNE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208710.KD",
  "name": "BIOLOG DEVICE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064550.KD",
  "name": "BIONEER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419540.KD",
  "name": "BISTOS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032850.KD",
  "name": "BITComputer",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050090.KD",
  "name": "BK Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044480.KD",
  "name": "BLADE Ent",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065170.KD",
  "name": "BLPT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033560.KD",
  "name": "BLUECOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439580.KD",
  "name": "BLUEMTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086670.KD",
  "name": "BMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "256840.KD",
  "name": "BNC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445360.KD",
  "name": "BNK SPAC 1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "473370.KD",
  "name": "BNK SPAC 2",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008470.KD",
  "name": "BOOSTER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250000.KD",
  "name": "BORATR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006910.KD",
  "name": "BOSUNG POWER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288330.KD",
  "name": "BRIDGE BIOTHERAPEUTICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064480.KD",
  "name": "BRIDGETEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066410.KD",
  "name": "BUCKET STUDIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032980.KD",
  "name": "BYON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018700.KD",
  "name": "Barunson",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035620.KD",
  "name": "Barunson E&A",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424760.KD",
  "name": "Bellock",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053030.KD",
  "name": "Binex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086820.KD",
  "name": "Bio Solution Co.,Ltd.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199730.KD",
  "name": "BioInfra",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099430.KD",
  "name": "BioPlus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038460.KD",
  "name": "BioSmart",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086040.KD",
  "name": "Biotoxtech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357880.KD",
  "name": "Bitnine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093190.KD",
  "name": "Bixolon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "369370.KD",
  "name": "Blitzway Studios",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225530.KD",
  "name": "BoKwang Industry",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206640.KD",
  "name": "Boditech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226340.KD",
  "name": "Bonne",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099390.KD",
  "name": "Brainzcompany",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "337930.KD",
  "name": "BrandXcorp",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014470.KD",
  "name": "Bubang",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138580.KD",
  "name": "BusinessOn",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352480.KD",
  "name": "C&C INTERNATIONAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "264660.KD",
  "name": "C&G Hitech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094360.KD",
  "name": "C&M",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "359090.KD",
  "name": "C&R Research",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109670.KD",
  "name": "C-SITE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078340.KD",
  "name": "C2S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "258610.KD",
  "name": "CAELUM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016790.KD",
  "name": "CANARIABIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064820.KD",
  "name": "CAPEind",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317530.KD",
  "name": "CARRIESOFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140430.KD",
  "name": "CATIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072020.KD",
  "name": "CAVAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013720.KD",
  "name": "CBI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049960.KD",
  "name": "CBT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066790.KD",
  "name": "CCS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049180.KD",
  "name": "CELLUMED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037760.KD",
  "name": "CENIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222420.KD",
  "name": "CENOTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083790.KD",
  "name": "CGIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085660.KD",
  "name": "CHA Biotech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "261780.KD",
  "name": "CHA Vaccine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052670.KD",
  "name": "CHEIL BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199820.KD",
  "name": "CHEIL ELECTRIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089010.KD",
  "name": "CHEMTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047820.KD",
  "name": "CHOROKBAEM MEDIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "362320.KD",
  "name": "CHUNGDAMGLOBAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222080.KD",
  "name": "CIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "311690.KD",
  "name": "CJ Bioscience",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035760.KD",
  "name": "CJ ENM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051500.KD",
  "name": "CJ FW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214150.KD",
  "name": "CLASSYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "237880.KD",
  "name": "CLIO Cosmetics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263700.KD",
  "name": "CLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "384470.KD",
  "name": "CLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058820.KD",
  "name": "CMG Pharmaceutical",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023460.KD",
  "name": "CNH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115530.KD",
  "name": "CNPLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056730.KD",
  "name": "CNT85",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352700.KD",
  "name": "CNTUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036690.KD",
  "name": "COMMAX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307930.KD",
  "name": "COMPANY K PARTNERS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451760.KD",
  "name": "CONTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "322780.KD",
  "name": "COPUS KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027050.KD",
  "name": "COREANA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "166480.KD",
  "name": "CORESTEMCHEMON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222040.KD",
  "name": "COSMAX NBT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241710.KD",
  "name": "COSMECCA KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448710.KD",
  "name": "COTS Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056360.KD",
  "name": "COWEAVER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033290.KD",
  "name": "COWELL F\/S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "282880.KD",
  "name": "COWIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "360350.KD",
  "name": "COXEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101240.KD",
  "name": "CQV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065770.KD",
  "name": "CS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297090.KD",
  "name": "CS BEARING",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083660.KD",
  "name": "CSA Cosmic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052300.KD",
  "name": "CT property",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060590.KD",
  "name": "CTC BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260930.KD",
  "name": "CTK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071850.KD",
  "name": "CTK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115480.KD",
  "name": "CU MEDICAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376290.KD",
  "name": "CU TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "182360.KD",
  "name": "CUBEENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021650.KD",
  "name": "CUBIC KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340810.KD",
  "name": "CUBOX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060280.KD",
  "name": "CUREXO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051780.KD",
  "name": "CUROHOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "355390.KD",
  "name": "CWORKS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900120.KD",
  "name": "CXI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "160980.KD",
  "name": "CYMECHS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042000.KD",
  "name": "Cafe24 Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050110.KD",
  "name": "CammSys",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452300.KD",
  "name": "Capstone Partners",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214370.KD",
  "name": "Caregen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016920.KD",
  "name": "Cas",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "308100.KD",
  "name": "Castelbajac",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "331920.KD",
  "name": "Celemics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318160.KD",
  "name": "Cell Bio Human Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068940.KD",
  "name": "Cellfie Global",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299660.KD",
  "name": "Cellid",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "268600.KD",
  "name": "Cellivery",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068760.KD",
  "name": "Celltrionph",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "004650.KD",
  "name": "Changhae Ethanol",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "220260.KD",
  "name": "Chemtros",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066360.KD",
  "name": "Cherrybro",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033100.KD",
  "name": "CheryongElec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "147830.KD",
  "name": "CheryongInd",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "034940.KD",
  "name": "ChoA Pharm.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "278280.KD",
  "name": "Chunbo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045520.KD",
  "name": "Clean & Science",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352770.KD",
  "name": "Clinomics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036170.KD",
  "name": "Cloud Air",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045970.KD",
  "name": "CoAsia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196450.KD",
  "name": "CoAsia CM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047770.KD",
  "name": "Codes Combine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900310.KD",
  "name": "Coloray",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063080.KD",
  "name": "Com2uS Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119860.KD",
  "name": "Connectwave",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104540.KD",
  "name": "Corentec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082660.KD",
  "name": "Cosnine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "110790.KD",
  "name": "CreaS F&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040350.KD",
  "name": "CreoSG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096240.KD",
  "name": "Creverse",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041460.KD",
  "name": "Crosscert",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900250.KD",
  "name": "Crystal New Material",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445680.KD",
  "name": "Curiox Biosystems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "372320.KD",
  "name": "Curocell",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "356890.KD",
  "name": "CyberOne",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217330.KD",
  "name": "Cytogen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263720.KD",
  "name": "D&C MEDIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347850.KD",
  "name": "D&D Pharmatech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290670.KD",
  "name": "DAE BO MAGNETIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045390.KD",
  "name": "DAEATI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078600.KD",
  "name": "DAEJOO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "120240.KD",
  "name": "DAEJUNG C&M",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317850.KD",
  "name": "DAEMO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007720.KD",
  "name": "DAEMYUNG SONOSEASON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048470.KD",
  "name": "DAESCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007680.KD",
  "name": "DAEWON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048910.KD",
  "name": "DAEWON MEDIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131220.KD",
  "name": "DAIHAN Scientific",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064260.KD",
  "name": "DANAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032190.KD",
  "name": "DAOU DATA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066900.KD",
  "name": "DAP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039560.KD",
  "name": "DASANNetwork",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196490.KD",
  "name": "DAT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263800.KD",
  "name": "DATASOLUTION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068240.KD",
  "name": "DAWONSYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108380.KD",
  "name": "DAYANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "456440.KD",
  "name": "DB Finance No.11 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099410.KD",
  "name": "DBSM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033130.KD",
  "name": "DChosun",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079810.KD",
  "name": "DE&T",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376300.KD",
  "name": "DEARU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "315640.KD",
  "name": "DEEPNOID",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "261200.KD",
  "name": "DENTIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263600.KD",
  "name": "DERKWOO ELECTRONICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067990.KD",
  "name": "DEUTSCH MOTORS INC.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043360.KD",
  "name": "DGI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060900.KD",
  "name": "DGP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290120.KD",
  "name": "DH AUTOLEAD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067080.KD",
  "name": "DH PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025440.KD",
  "name": "DHAUTOWARE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054670.KD",
  "name": "DHNP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020180.KD",
  "name": "DIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131180.KD",
  "name": "DILLI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039840.KD",
  "name": "DIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "110990.KD",
  "name": "DIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263020.KD",
  "name": "DK&D",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "105740.KD",
  "name": "DK-Lok",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290550.KD",
  "name": "DKT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389260.KD",
  "name": "DMENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016670.KD",
  "name": "DMOA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068790.KD",
  "name": "DMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "127120.KD",
  "name": "DNALINK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092070.KD",
  "name": "DNF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088130.KD",
  "name": "DONG A ELTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041930.KD",
  "name": "DONGAHWASUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109860.KD",
  "name": "DONGIL METAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005290.KD",
  "name": "DONGJIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005160.KD",
  "name": "DONGKUK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "075970.KD",
  "name": "DONGKUK R&S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033500.KD",
  "name": "DONGSUNG FINETEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025900.KD",
  "name": "DONGWHA ENTERPRISE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088910.KD",
  "name": "DONGWOO FARM TO TABLE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094170.KD",
  "name": "DONGWOON ANATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079960.KD",
  "name": "DONGYANG E&P",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131970.KD",
  "name": "DOOSAN TESNA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "362990.KD",
  "name": "DREAMINSIGHT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263690.KD",
  "name": "DRGEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214680.KD",
  "name": "DRTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241520.KD",
  "name": "DSC Investment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "077360.KD",
  "name": "DSHM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109740.KD",
  "name": "DSK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036480.KD",
  "name": "DSMBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096350.KD",
  "name": "DSOL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "383930.KD",
  "name": "DT&CRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066670.KD",
  "name": "DTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "213420.KD",
  "name": "DUK SAN NEOLUX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073190.KD",
  "name": "DUOBACK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "180400.KD",
  "name": "DXVX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060380.KD",
  "name": "DY S·TEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310870.KD",
  "name": "DYC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219550.KD",
  "name": "DYD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104460.KD",
  "name": "DYPNF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290380.KD",
  "name": "Dae Yu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140520.KD",
  "name": "DaeChang Steel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078140.KD",
  "name": "Daebongls",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008830.KD",
  "name": "DaedongGear",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020400.KD",
  "name": "DaedongMetal",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003310.KD",
  "name": "Daejoo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017650.KD",
  "name": "DaelimPaper",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "004780.KD",
  "name": "Daeryuk",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065150.KD",
  "name": "Daesan F&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104040.KD",
  "name": "Daesung Fine Tec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "129920.KD",
  "name": "Daesung Hi-Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027830.KD",
  "name": "Daesung PE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005710.KD",
  "name": "Daewonsanup",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006580.KD",
  "name": "DaeyangPaper",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023910.KD",
  "name": "DaihanPharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438220.KD",
  "name": "DaishinBalanceNo.13 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442310.KD",
  "name": "DaishinBalanceNo.14 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457390.KD",
  "name": "DaishinBalanceNo.15 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457630.KD",
  "name": "DaishinBalanceNo.16 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "471050.KD",
  "name": "DaishinBalanceNo.17 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "154040.KD",
  "name": "Dasan Solueta",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340360.KD",
  "name": "Davolink",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "223310.KD",
  "name": "DeepMind",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187870.KD",
  "name": "Device ENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "194480.KD",
  "name": "Devsisters",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206560.KD",
  "name": "Dexter studios",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "113810.KD",
  "name": "Dgenx",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217620.KD",
  "name": "Didim E&F",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "197140.KD",
  "name": "DigiCAP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068930.KD",
  "name": "Digital DS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006620.KD",
  "name": "DongKoo Bio & Pharma",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086450.KD",
  "name": "DongKook Pharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023790.KD",
  "name": "DongilSteel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032960.KD",
  "name": "DongilTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100130.KD",
  "name": "Dongkuk S&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025950.KD",
  "name": "DongshinE&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013120.KD",
  "name": "Dongwon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030350.KD",
  "name": "Dragonfly",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203650.KD",
  "name": "Dream Security",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "223250.KD",
  "name": "DreamCIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060570.KD",
  "name": "Dreamus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187220.KD",
  "name": "Dt&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317330.KD",
  "name": "Duksan Techopia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090410.KD",
  "name": "Dukshinepc",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096040.KD",
  "name": "E-TRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024810.KD",
  "name": "E.T.I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418620.KD",
  "name": "E8IGHT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039020.KD",
  "name": "EAGON HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "353810.KD",
  "name": "EASYBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230360.KD",
  "name": "ECHO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "128540.KD",
  "name": "ECOCAB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448280.KD",
  "name": "ECOEYE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038110.KD",
  "name": "ECOPLASTIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086520.KD",
  "name": "ECOPRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "383310.KD",
  "name": "ECOPRO HN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "247540.KD",
  "name": "ECOPROBM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067010.KD",
  "name": "ECS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "245620.KD",
  "name": "EDGC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037370.KD",
  "name": "EG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377330.KD",
  "name": "EGT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041520.KD",
  "name": "ELC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037950.KD",
  "name": "ELCOMTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063760.KD",
  "name": "ELP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065440.KD",
  "name": "ELUON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091120.KD",
  "name": "EM-Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095190.KD",
  "name": "EMKOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123570.KD",
  "name": "EMNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058970.KD",
  "name": "EMRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083470.KD",
  "name": "EMnI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352940.KD",
  "name": "ENBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019990.KD",
  "name": "ENERTORK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "102710.KD",
  "name": "ENF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419080.KD",
  "name": "ENJET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317870.KD",
  "name": "ENVIONEER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "183490.KD",
  "name": "ENZYCHEM LSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039030.KD",
  "name": "EO Technics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294090.KD",
  "name": "EOFlow",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "160600.KD",
  "name": "EQUIPMENTS CELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050120.KD",
  "name": "ES CUBE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069510.KD",
  "name": "ESTec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047560.KD",
  "name": "ESTsoft",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023410.KD",
  "name": "EUGENE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131400.KD",
  "name": "EV.A.M.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088290.KD",
  "name": "EWON COMFORT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054940.KD",
  "name": "EXA E&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092870.KD",
  "name": "EXICON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031310.KD",
  "name": "EYESVISION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044960.KD",
  "name": "Eagle Vet. Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263540.KD",
  "name": "Earth & Aerospace",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900110.KD",
  "name": "East Asia Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035810.KD",
  "name": "EasyHoldings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "097780.KD",
  "name": "Eco Volt",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101360.KD",
  "name": "Eco&Dream",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038870.KD",
  "name": "EcoBio Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001840.KD",
  "name": "Eehwa",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "264850.KD",
  "name": "Elensys",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054210.KD",
  "name": "Elentec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "169330.KD",
  "name": "Embrain",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208860.KD",
  "name": "EnGIS Technologies",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348370.KD",
  "name": "Enchem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950140.KD",
  "name": "Englewood Lab",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058450.KD",
  "name": "Enterpartners",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043340.KD",
  "name": "Essen Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "206650.KD",
  "name": "EuBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442130.KD",
  "name": "Eugene SPAC IX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388800.KD",
  "name": "Eugene SPAC VII",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "413630.KD",
  "name": "Eugene SPAC VIII",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "468760.KD",
  "name": "Eugene SPAC X",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084370.KD",
  "name": "Eugenetech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263050.KD",
  "name": "Eutilex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "270660.KD",
  "name": "Everybot",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "185490.KD",
  "name": "Eyegene",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440110.KD",
  "name": "FADU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "150900.KD",
  "name": "FASOO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "368770.KD",
  "name": "FIBERPRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049120.KD",
  "name": "FINE DNC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036810.KD",
  "name": "FINE SEMITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038950.KD",
  "name": "FINEDIGITAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "106240.KD",
  "name": "FINETECHNIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131760.KD",
  "name": "FINETEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "163730.KD",
  "name": "FINGER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "300080.KD",
  "name": "FLITTO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "173940.KD",
  "name": "FNC Ent.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083500.KD",
  "name": "FNS TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "331380.KD",
  "name": "FOCUS HNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290720.KD",
  "name": "FOODNAMOO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005670.KD",
  "name": "FOODWELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189690.KD",
  "name": "FORCS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119500.KD",
  "name": "FORMETAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073540.KD",
  "name": "FRTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214270.KD",
  "name": "FSN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032800.KD",
  "name": "Fantagio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027710.KD",
  "name": "FarmStory",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225590.KD",
  "name": "Fashion Platform",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032580.KD",
  "name": "Fidelix",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "441270.KD",
  "name": "Fine M-Tec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "127980.KD",
  "name": "Finecircuit",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417180.KD",
  "name": "Finger Story",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041590.KD",
  "name": "Flask",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064850.KD",
  "name": "FnGuide",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053160.KD",
  "name": "Freems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377220.KD",
  "name": "From Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "370090.KD",
  "name": "Furonteer",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "220100.KD",
  "name": "Futurechem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382480.KD",
  "name": "G.I.Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053270.KD",
  "name": "G.Y.TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388050.KD",
  "name": "G2Power",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079940.KD",
  "name": "GABIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051160.KD",
  "name": "GAEASOFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036620.KD",
  "name": "GAMSUNG Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "399720.KD",
  "name": "GAONCHIPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "144510.KD",
  "name": "GC CELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142280.KD",
  "name": "GCMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234690.KD",
  "name": "GCWB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109820.KD",
  "name": "GENEMATRIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263860.KD",
  "name": "GENIANS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389030.KD",
  "name": "GENINUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225220.KD",
  "name": "GENOLUTION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122310.KD",
  "name": "GENORAY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036190.KD",
  "name": "GEUMHWA PSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "407400.KD",
  "name": "GGUMBI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "130500.KD",
  "name": "GH Advanced Materials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950190.KD",
  "name": "GHOSTS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "358570.KD",
  "name": "GI Innovation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "289220.KD",
  "name": "GIANTSTEP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049080.KD",
  "name": "GIGALANE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019660.KD",
  "name": "GLOBON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204840.KD",
  "name": "GLPT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119850.KD",
  "name": "GNCENERGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065060.KD",
  "name": "GNCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "311320.KD",
  "name": "GO Element",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215000.KD",
  "name": "GOLFZON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121440.KD",
  "name": "GOLFZON NEWDIN HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033340.KD",
  "name": "GOODPEOPLE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114450.KD",
  "name": "GREEN LIFESCIENCE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204020.KD",
  "name": "GRITEE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900290.KD",
  "name": "GRT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053050.KD",
  "name": "GSE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900070.KD",
  "name": "GSMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083450.KD",
  "name": "GST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219750.KD",
  "name": "GTG Wellness",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036180.KD",
  "name": "GWV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094480.KD",
  "name": "GalaxiaMoneytree",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082270.KD",
  "name": "GemVax",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064800.KD",
  "name": "Gemvaxlink",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072520.KD",
  "name": "GenNBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "229000.KD",
  "name": "Gencurix",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086060.KD",
  "name": "GeneBioTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217190.KD",
  "name": "Genesem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "363250.KD",
  "name": "Genesystem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095700.KD",
  "name": "Genexine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123330.KD",
  "name": "Genic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043610.KD",
  "name": "Genie Music",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187420.KD",
  "name": "GenoFocus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "361390.KD",
  "name": "Genohco",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "314130.KD",
  "name": "Genome&Company",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228760.KD",
  "name": "Genomictree",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "270520.KD",
  "name": "Geolit Energy",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "420770.KD",
  "name": "GigaVis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204620.KD",
  "name": "Global Tax Free",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382800.KD",
  "name": "GnBS eco",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035290.KD",
  "name": "Gold&S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900280.KD",
  "name": "Golden Century",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035080.KD",
  "name": "Gradiant",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "402490.KD",
  "name": "Green Resource",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357230.KD",
  "name": "H.PIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066130.KD",
  "name": "HAATZ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299030.KD",
  "name": "HANA TECHNOLOGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "406760.KD",
  "name": "HANA21SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418170.KD",
  "name": "HANA22SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430230.KD",
  "name": "HANA24SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030520.KD",
  "name": "HANCOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "220180.KD",
  "name": "HANDYSOFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007770.KD",
  "name": "HANILCHEMIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "198940.KD",
  "name": "HANJOO LIGHT METAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053590.KD",
  "name": "HANKOOK Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092460.KD",
  "name": "HANLA IMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052600.KD",
  "name": "HANNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042520.KD",
  "name": "HANS BIOMED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226440.KD",
  "name": "HANSONGNEOTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452280.KD",
  "name": "HANSUN ENGINEERING",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066980.KD",
  "name": "HANSUNG CLEANTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455310.KD",
  "name": "HANWHA PLUS NO 4 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "386580.KD",
  "name": "HANWHAPLUSNO2SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430460.KD",
  "name": "HANWHAPLUSNO3SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078350.KD",
  "name": "HANYANG DIGI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045100.KD",
  "name": "HANYANG ENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136480.KD",
  "name": "HARIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440290.KD",
  "name": "HB Investment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "297890.KD",
  "name": "HB SOLUTION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078150.KD",
  "name": "HB Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452190.KD",
  "name": "HBL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047080.KD",
  "name": "HBS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072990.KD",
  "name": "HCT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048410.KD",
  "name": "HDBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "256150.KD",
  "name": "HDCTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "170030.KD",
  "name": "HDI21",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037440.KD",
  "name": "HEERIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900270.KD",
  "name": "HENG SHENG GROUP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010240.KD",
  "name": "HEUNGKUK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "230240.KD",
  "name": "HFR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "400840.KD",
  "name": "HI-7 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "450050.KD",
  "name": "HI-8 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238490.KD",
  "name": "HIMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "221840.KD",
  "name": "HIZEAERO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044780.KD",
  "name": "HK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195940.KD",
  "name": "HK inno.N",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023760.KD",
  "name": "HKCapital",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037230.KD",
  "name": "HKPAK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "028300.KD",
  "name": "HLB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046210.KD",
  "name": "HLB PANAGENE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115450.KD",
  "name": "HLB Therapeutics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024850.KD",
  "name": "HLB innoVation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067630.KD",
  "name": "HLBLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047920.KD",
  "name": "HLBPHARMA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "278650.KD",
  "name": "HLBbioStep",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "239610.KD",
  "name": "HLSCIENCE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "462020.KD",
  "name": "HMCIB No.6SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101680.KD",
  "name": "HNK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "403870.KD",
  "name": "HPSP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036640.KD",
  "name": "HRS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039610.KD",
  "name": "HS VALVE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "106190.KD",
  "name": "HTP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "175140.KD",
  "name": "HUMAN TECHNOLOGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "205470.KD",
  "name": "HUMASIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115160.KD",
  "name": "HUMAX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "028080.KD",
  "name": "HUMAX Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290270.KD",
  "name": "HUNESION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "061250.KD",
  "name": "HWAIL PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126640.KD",
  "name": "HWASHIN PRECISION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013030.KD",
  "name": "HY-LOKCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "097870.KD",
  "name": "HYOSUNG ONB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "106080.KD",
  "name": "HYSONIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148930.KD",
  "name": "HYTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078590.KD",
  "name": "HYULIM A-TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052260.KD",
  "name": "HYUNDAI BIOLAND",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041440.KD",
  "name": "HYUNDAI EVERDIGM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090850.KD",
  "name": "HYUNDAI EZWEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039010.KD",
  "name": "HYUNDAI HT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "460930.KD",
  "name": "HYUNDAI HYMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "319400.KD",
  "name": "HYUNDAI MOVEX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011080.KD",
  "name": "HYUNGJI I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092300.KD",
  "name": "HYUNWOO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "034810.KD",
  "name": "HaeSung",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "03481K.KD",
  "name": "HaeSung(1P)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "076610.KD",
  "name": "Haesung Optics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059270.KD",
  "name": "Haisung Aero-Robotics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025550.KD",
  "name": "HanSun",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446750.KD",
  "name": "Hana 26 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448370.KD",
  "name": "Hana 27 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "454750.KD",
  "name": "Hana 28 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "454640.KD",
  "name": "Hana 29 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "469880.KD",
  "name": "Hana 30 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "469900.KD",
  "name": "Hana 31 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "475240.KD",
  "name": "Hana 32 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "475250.KD",
  "name": "Hana 33 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "166090.KD",
  "name": "Hana Materials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067310.KD",
  "name": "Hana Micron",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "435620.KD",
  "name": "Hana25SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079170.KD",
  "name": "Hanchang",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054920.KD",
  "name": "Hancom WITH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005860.KD",
  "name": "HanilFeed",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024740.KD",
  "name": "HanilForging",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114810.KD",
  "name": "Hansol IONES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "070590.KD",
  "name": "Hansol Intic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430690.KD",
  "name": "Hanssak",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002680.KD",
  "name": "Hantop",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091440.KD",
  "name": "Hanwool MS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003380.KD",
  "name": "Harim Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234340.KD",
  "name": "Hecto Financial",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214180.KD",
  "name": "Hecto Innovation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084990.KD",
  "name": "Helixmith",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024060.KD",
  "name": "Heungu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365590.KD",
  "name": "HiDeep",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "149980.KD",
  "name": "Hironic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060560.KD",
  "name": "Home Center Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263920.KD",
  "name": "HuM&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215090.KD",
  "name": "Hucentech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "145020.KD",
  "name": "Hugel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200670.KD",
  "name": "Humedix",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "243070.KD",
  "name": "Huons",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084110.KD",
  "name": "Huons Global",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "353190.KD",
  "name": "Hurum",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065510.KD",
  "name": "Huvitz",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126700.KD",
  "name": "HyVISION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101670.KD",
  "name": "Hydro Lithium",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065650.KD",
  "name": "Hyper Corporation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090710.KD",
  "name": "Hyulim ROBOT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192410.KD",
  "name": "Hyulimnetworks",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189980.KD",
  "name": "Hyungkuk F&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138360.KD",
  "name": "Hyupjin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052860.KD",
  "name": "I&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "339950.KD",
  "name": "IBKIMYOUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439730.KD",
  "name": "IBKS No.20 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442770.KD",
  "name": "IBKS No.21 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448760.KD",
  "name": "IBKS No.22 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "467930.KD",
  "name": "IBKS No.23 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "469480.KD",
  "name": "IBKS No.24 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059100.KD",
  "name": "IC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040910.KD",
  "name": "ICD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "368600.KD",
  "name": "ICH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143160.KD",
  "name": "IDIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054800.KD",
  "name": "IDIS Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332370.KD",
  "name": "IDP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114840.KD",
  "name": "IFAMILYSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067920.KD",
  "name": "IGLOO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307180.KD",
  "name": "IL SCIENCE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "333430.KD",
  "name": "IL SEUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094820.KD",
  "name": "ILJIN POWER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "164060.KD",
  "name": "ILOODA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "178780.KD",
  "name": "ILWOUL GML",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101390.KD",
  "name": "IM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115610.KD",
  "name": "IMAGIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "461030.KD",
  "name": "IMBdx",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451220.KD",
  "name": "IMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083640.KD",
  "name": "INCON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071200.KD",
  "name": "INFINITT Healthcare",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115310.KD",
  "name": "INFOvine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452400.KD",
  "name": "INICS Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053350.KD",
  "name": "INITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215790.KD",
  "name": "INNO INSTRUMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "303530.KD",
  "name": "INNODEP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "344860.KD",
  "name": "INNOGENE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "302430.KD",
  "name": "INNOMETRY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "296640.KD",
  "name": "INNORULES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "274400.KD",
  "name": "INNOSIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088390.KD",
  "name": "INNOX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "272290.KD",
  "name": "INNOX Advanced Materials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277410.KD",
  "name": "INSAN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060150.KD",
  "name": "INSUN ENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033230.KD",
  "name": "INSUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064290.KD",
  "name": "INTEKPLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051370.KD",
  "name": "INTERFLEX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119610.KD",
  "name": "INTEROJO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049070.KD",
  "name": "INTOPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079950.KD",
  "name": "INVENIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037330.KD",
  "name": "INZI DISPLAY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078860.KD",
  "name": "IOK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "262840.KD",
  "name": "IQUEST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009730.KD",
  "name": "IREM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "351330.KD",
  "name": "ISAAC Engineering",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095340.KD",
  "name": "ISC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069920.KD",
  "name": "ISE Commerce",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086890.KD",
  "name": "ISU ABXIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "124500.KD",
  "name": "ITCEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "119830.KD",
  "name": "ITEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "372800.KD",
  "name": "ITEYES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084850.KD",
  "name": "ITM Semiconductor",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052770.KD",
  "name": "ITOXI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099520.KD",
  "name": "ITX-AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389470.KD",
  "name": "IVTG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "175250.KD",
  "name": "Icure Pharm. Inc.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019540.KD",
  "name": "IljiTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041830.KD",
  "name": "InBody",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "211050.KD",
  "name": "Incar Financial Service",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "216050.KD",
  "name": "Incross",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039290.KD",
  "name": "InfoBank",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101930.KD",
  "name": "Inhwa Precision",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049550.KD",
  "name": "InkTec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056090.KD",
  "name": "Innosys",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073490.KD",
  "name": "Innowireless",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "450520.KD",
  "name": "Inswave Systems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189300.KD",
  "name": "Intellian Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017250.KD",
  "name": "Interm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "150840.KD",
  "name": "IntroMedic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100030.KD",
  "name": "Inzisoft",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "026040.KD",
  "name": "J.ESTINA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "420570.KD",
  "name": "J2KBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "000440.KD",
  "name": "JA Enervis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049630.KD",
  "name": "JAEYOUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090470.KD",
  "name": "JASTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137950.KD",
  "name": "JC Chemical",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033320.KD",
  "name": "JCH Systems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "412540.KD",
  "name": "JEIL M&S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038010.KD",
  "name": "JEIL TECHNOS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418550.KD",
  "name": "JEIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036930.KD",
  "name": "JEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "216080.KD",
  "name": "JETEMA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417500.KD",
  "name": "JI-Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036890.KD",
  "name": "JINSUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007370.KD",
  "name": "JINYANGPHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "285800.KD",
  "name": "JINYOUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "110020.KD",
  "name": "JJBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "322510.KD",
  "name": "JLK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033050.KD",
  "name": "JMI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094970.KD",
  "name": "JMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452160.KD",
  "name": "JNB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126880.KD",
  "name": "JNK Global",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204270.KD",
  "name": "JNTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044060.KD",
  "name": "JOKWANG ILI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051980.KD",
  "name": "JOONGANG AM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208350.KD",
  "name": "JS.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080220.KD",
  "name": "JSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023440.KD",
  "name": "JSCO Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089790.KD",
  "name": "JT Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950170.KD",
  "name": "JTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208140.KD",
  "name": "JUNGDAWN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054950.KD",
  "name": "JVM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067290.KD",
  "name": "JW SHINYAK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035900.KD",
  "name": "JYP Ent.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "174880.KD",
  "name": "JangWon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "287410.KD",
  "name": "Jeisys Medical",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "276730.KD",
  "name": "Jeju Beer Company",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067000.KD",
  "name": "JoyCity",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018120.KD",
  "name": "JrDistiller",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417840.KD",
  "name": "Justem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "102370.KD",
  "name": "K Auction",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053080.KD",
  "name": "K-ENSOL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039240.KD",
  "name": "K-Steel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017890.KD",
  "name": "KAI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "284620.KD",
  "name": "KAINOSMED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014200.KD",
  "name": "KANGLIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217730.KD",
  "name": "KANGSTEM BIOTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114190.KD",
  "name": "KANGWON ENERGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078890.KD",
  "name": "KAON Group",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424140.KD",
  "name": "KB No.21 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455250.KD",
  "name": "KB No.25 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "458320.KD",
  "name": "KB No.26 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "464680.KD",
  "name": "KB No.27 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024120.KD",
  "name": "KBA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318000.KD",
  "name": "KBG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200130.KD",
  "name": "KBH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024840.KD",
  "name": "KBI METAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038530.KD",
  "name": "KBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025880.KD",
  "name": "KC FEED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021320.KD",
  "name": "KCC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036670.KD",
  "name": "KCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054040.KD",
  "name": "KCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115500.KD",
  "name": "KCS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089150.KD",
  "name": "KCT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044180.KD",
  "name": "KD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "221980.KD",
  "name": "KDCHEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011040.KD",
  "name": "KDPharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079190.KD",
  "name": "KESPION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053260.KD",
  "name": "KEUM KANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054780.KD",
  "name": "KEYEAST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123410.KD",
  "name": "KFTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "151860.KD",
  "name": "KG Eco Solution",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035600.KD",
  "name": "KGINICIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046440.KD",
  "name": "KGMBLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226360.KD",
  "name": "KH Construction",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "111870.KD",
  "name": "KH ELECTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060720.KD",
  "name": "KH VATEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053300.KD",
  "name": "KICA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025770.KD",
  "name": "KICC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039740.KD",
  "name": "KIES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093320.KD",
  "name": "KINX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039420.KD",
  "name": "KL-Net",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "102940.KD",
  "name": "KLS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083550.KD",
  "name": "KM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225430.KD",
  "name": "KMP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032500.KD",
  "name": "KMW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058400.KD",
  "name": "KNN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199430.KD",
  "name": "KNR SYSTEMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "432470.KD",
  "name": "KNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "105330.KD",
  "name": "KNW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "015710.KD",
  "name": "KOCOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046070.KD",
  "name": "KODACO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080530.KD",
  "name": "KODI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "029960.KD",
  "name": "KOENTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049430.KD",
  "name": "KOMELON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041960.KD",
  "name": "KOMIPHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052400.KD",
  "name": "KONA I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "190650.KD",
  "name": "KOREA ASSET SEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "198440.KD",
  "name": "KOREA CEMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032300.KD",
  "name": "KOREA PHARMA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014570.KD",
  "name": "KOREAN DRUG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052330.KD",
  "name": "KORTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049720.KD",
  "name": "KORYOINFO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089890.KD",
  "name": "KOSES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "355150.KD",
  "name": "KOSTECSYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121850.KD",
  "name": "KOYJ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024880.KD",
  "name": "KPF",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042040.KD",
  "name": "KPM TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "256940.KD",
  "name": "KPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054410.KD",
  "name": "KPTU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "034950.KD",
  "name": "KR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093640.KD",
  "name": "KRM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043650.KD",
  "name": "KSDB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073010.KD",
  "name": "KSP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078130.KD",
  "name": "KUK-IL PAPER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066620.KD",
  "name": "KUKBO DESIGN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060480.KD",
  "name": "KUKIL METAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307750.KD",
  "name": "KUKJEON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006050.KD",
  "name": "KUKYOUNGG&M",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068100.KD",
  "name": "KWR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122450.KD",
  "name": "KX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052900.KD",
  "name": "KX HITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "282720.KD",
  "name": "KYGP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053950.KD",
  "name": "KYUNG NAM PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "293490.KD",
  "name": "Kakao Games",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "274090.KD",
  "name": "Kencoa Aerospace",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "139670.KD",
  "name": "KineMaster",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035460.KD",
  "name": "KisanTelecom",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "413600.KD",
  "name": "Kiwoom No.6 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "433530.KD",
  "name": "Kiwoom No.7 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446840.KD",
  "name": "Kiwoom No.8 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "272110.KD",
  "name": "KnJ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348150.KD",
  "name": "KoBioLabs",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "183300.KD",
  "name": "KoMiCo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098460.KD",
  "name": "Koh Young",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950160.KD",
  "name": "Kolon TissueGene",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "402030.KD",
  "name": "Konan Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039340.KD",
  "name": "Korea Economic Broadcasting",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "436610.KD",
  "name": "Korea No.11 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "458610.KD",
  "name": "Korea No.12 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "464440.KD",
  "name": "Korea No.13 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "004590.KD",
  "name": "KoreaFurni",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "391710.KD",
  "name": "Kornic Automation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192250.KD",
  "name": "Ksign",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "026910.KD",
  "name": "KwangjinInd",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "029480.KD",
  "name": "Kwangmu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "421800.KD",
  "name": "Kyobo 12 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440790.KD",
  "name": "Kyobo 13 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "456490.KD",
  "name": "Kyobo 14 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "465320.KD",
  "name": "Kyobo 15 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024910.KD",
  "name": "Kyungchang",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290650.KD",
  "name": "L&C BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "156100.KD",
  "name": "L&K BIOMED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "281740.KD",
  "name": "LAKE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "309960.KD",
  "name": "LB Investment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376190.KD",
  "name": "LB Lusem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "061970.KD",
  "name": "LB SEMICON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "141080.KD",
  "name": "LCB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096870.KD",
  "name": "LDT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012700.KD",
  "name": "LEADCORP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016100.KD",
  "name": "LEADERS COSMETICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058470.KD",
  "name": "LEENO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294140.KD",
  "name": "LEMON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069540.KD",
  "name": "LIGHTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171120.KD",
  "name": "LION CHEMTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225190.KD",
  "name": "LK SAMYANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073110.KD",
  "name": "LMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067730.KD",
  "name": "LOGISYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060240.KD",
  "name": "LONGTU KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "083310.KD",
  "name": "LOT Vacuum",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060370.KD",
  "name": "LS Marine Solution",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417200.KD",
  "name": "LS Materials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347700.KD",
  "name": "LSCORP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "170920.KD",
  "name": "LTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038060.KD",
  "name": "LUMENS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084650.KD",
  "name": "LabGen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "300120.KD",
  "name": "LaonPeople",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199550.KD",
  "name": "Laseroptek",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "412350.KD",
  "name": "Laserssel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388790.KD",
  "name": "LiComm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277070.KD",
  "name": "Lindeman Asia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "193250.KD",
  "name": "Linked",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219420.KD",
  "name": "Linkgenesis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073570.KD",
  "name": "Lithium-for-earth",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "328130.KD",
  "name": "Lunit",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001810.KD",
  "name": "M.S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347890.KD",
  "name": "M2I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033310.KD",
  "name": "M2N",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "087260.KD",
  "name": "MA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "005990.KD",
  "name": "MAEIL HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093520.KD",
  "name": "MAKUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021880.KD",
  "name": "MASON CAPITAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377480.KD",
  "name": "MAUM.AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377030.KD",
  "name": "MAXST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098120.KD",
  "name": "MCS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086960.KD",
  "name": "MDS Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241770.KD",
  "name": "MECARO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014100.KD",
  "name": "MED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041920.KD",
  "name": "MEDIANA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054180.KD",
  "name": "MEDICOX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078160.KD",
  "name": "MEDIPOST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058110.KD",
  "name": "MEKICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059210.KD",
  "name": "META",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "323230.KD",
  "name": "MFM KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032790.KD",
  "name": "MGEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424980.KD",
  "name": "MICRO2NANO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "373170.KD",
  "name": "MICUBE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "218150.KD",
  "name": "MILAE BIORESOURCES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "408900.KD",
  "name": "MIR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "254490.KD",
  "name": "MIRAI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038340.KD",
  "name": "MIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "179290.KD",
  "name": "MITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033160.KD",
  "name": "MKElectron",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095500.KD",
  "name": "MNtech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288980.KD",
  "name": "MOADATA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142760.KD",
  "name": "MOALife",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033200.KD",
  "name": "MOATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101330.KD",
  "name": "MOBASE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012860.KD",
  "name": "MOBASE ELECTRONICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348030.KD",
  "name": "MOBIRIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "333050.KD",
  "name": "MOCOMSYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080160.KD",
  "name": "MODETOUR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "434480.KD",
  "name": "MONITORAPP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "118990.KD",
  "name": "MOTREX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123040.KD",
  "name": "MS AUTOTECH CO., LTD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009780.KD",
  "name": "MSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "413640.KD",
  "name": "MTX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019590.KD",
  "name": "MVENTURE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038290.KD",
  "name": "Macrogen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267980.KD",
  "name": "Maeil Dairies",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "195500.KD",
  "name": "Maniker F&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439090.KD",
  "name": "Manyo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222980.KD",
  "name": "Mcnulty",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "201490.KD",
  "name": "Me2on",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "235980.KD",
  "name": "MedPacto",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "279600.KD",
  "name": "MediaZen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086900.KD",
  "name": "MedyTox",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "133750.KD",
  "name": "MegaMD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446540.KD",
  "name": "Megatouch",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100590.KD",
  "name": "Mercury",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "408920.KD",
  "name": "Messe eSang",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140410.KD",
  "name": "Mezzion Pharma",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058630.KD",
  "name": "Mgame",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "059090.KD",
  "name": "MiCo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214610.KD",
  "name": "MiCo Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "305090.KD",
  "name": "Micro Digital",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418470.KD",
  "name": "Millie",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452200.KD",
  "name": "Mintech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "442900.KD",
  "name": "Mirae Asset Dream SPAC 1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100790.KD",
  "name": "Mirae Asset Venture",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "412930.KD",
  "name": "Mirae Asset Vision SPAC 1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446190.KD",
  "name": "Mirae Asset Vision SPAC 2",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448830.KD",
  "name": "Mirae Asset Vision SPAC3",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "363260.KD",
  "name": "Mobidays",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250060.KD",
  "name": "Mobiis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080420.KD",
  "name": "Moda-InnoChips",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417970.KD",
  "name": "Model Solution",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006920.KD",
  "name": "Mohenz",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "207760.KD",
  "name": "Mr. Blue",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067280.KD",
  "name": "Multicampus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101400.KD",
  "name": "N CITRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054050.KD",
  "name": "N.W BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "227950.KD",
  "name": "N2TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153460.KD",
  "name": "NABLE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "242040.KD",
  "name": "NAMU TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "190510.KD",
  "name": "NAMUGA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187790.KD",
  "name": "NANO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "286750.KD",
  "name": "NANOBRICK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "247660.KD",
  "name": "NANOCMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405920.KD",
  "name": "NARA CELLAR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051490.KD",
  "name": "NARA M&D",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137080.KD",
  "name": "NARAE NANOTECH CORP.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007390.KD",
  "name": "NATURECELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "293580.KD",
  "name": "NAU IB Capital",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "236810.KD",
  "name": "NBT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092600.KD",
  "name": "NC&",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "238090.KD",
  "name": "NDFOS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053290.KD",
  "name": "NE Neungyule",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290660.KD",
  "name": "NEOFECT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "212560.KD",
  "name": "NEOOTO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094860.KD",
  "name": "NEORIGIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085910.KD",
  "name": "NEOTIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095660.KD",
  "name": "NEOWIZ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042420.KD",
  "name": "NEOWIZ HOLDINDS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033640.KD",
  "name": "NEPES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348340.KD",
  "name": "NEUROMEKA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "160550.KD",
  "name": "NEW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "085670.KD",
  "name": "NEWFLEX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "225570.KD",
  "name": "NEXON Games",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396270.KD",
  "name": "NEXTCHIP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348210.KD",
  "name": "NEXTIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089140.KD",
  "name": "NEXTURNBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265740.KD",
  "name": "NFC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "354200.KD",
  "name": "NGeneBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "391060.KD",
  "name": "NH SPAC 20",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "422040.KD",
  "name": "NH SPAC 23",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "437780.KD",
  "name": "NH SPAC 24",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438580.KD",
  "name": "NH SPAC 25",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439410.KD",
  "name": "NH SPAC 26",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440820.KD",
  "name": "NH SPAC 27",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "451700.KD",
  "name": "NH SPAC 29",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "466910.KD",
  "name": "NH SPAC 30",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104200.KD",
  "name": "NHN BUGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060250.KD",
  "name": "NHN KCP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138610.KD",
  "name": "NIBEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "130580.KD",
  "name": "NICE D&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063570.KD",
  "name": "NICE TCM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036800.KD",
  "name": "NICEI&T",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "182400.KD",
  "name": "NKMAX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043910.KD",
  "name": "NNE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332290.KD",
  "name": "NOUSBO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "194700.KD",
  "name": "NOVAREX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "285490.KD",
  "name": "NOVATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "291230.KD",
  "name": "NP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "198080.KD",
  "name": "NPD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048830.KD",
  "name": "NPK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "144960.KD",
  "name": "NPP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222160.KD",
  "name": "NPX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012340.KD",
  "name": "NUINTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123840.KD",
  "name": "NUON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060260.KD",
  "name": "NUVOTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067570.KD",
  "name": "NVH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "267320.KD",
  "name": "Naintech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091590.KD",
  "name": "Nam Hwa Const Co., Ltd.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "111710.KD",
  "name": "Namhwa Industrial",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091970.KD",
  "name": "Nano Chem Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417010.KD",
  "name": "NanoTIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039860.KD",
  "name": "NanoenTek",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089600.KD",
  "name": "Nasmedia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "168330.KD",
  "name": "NaturalendoTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "311390.KD",
  "name": "Neo Cremar",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950220.KD",
  "name": "NeoImmuneTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "306620.KD",
  "name": "Neontech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092730.KD",
  "name": "Neopharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253590.KD",
  "name": "Neosem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330860.KD",
  "name": "Nepes Ark",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217270.KD",
  "name": "Neptune",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214870.KD",
  "name": "NewGLAB Pharma",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "270870.KD",
  "name": "Newtree",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137940.KD",
  "name": "NextEye",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "106520.KD",
  "name": "Noble M&B",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065560.KD",
  "name": "Nokwon C & I",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376930.KD",
  "name": "Noul",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "333620.KD",
  "name": "Nsys",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040160.KD",
  "name": "NuriFlex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069140.KD",
  "name": "Nuriplan",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417860.KD",
  "name": "OBZEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039200.KD",
  "name": "OCT Inc.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080520.KD",
  "name": "ODTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138080.KD",
  "name": "OE Solutions",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "309930.KD",
  "name": "OHEIM & Company",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045060.KD",
  "name": "OKONG Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080580.KD",
  "name": "OKins",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "173130.KD",
  "name": "OPASNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014940.KD",
  "name": "OPCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109080.KD",
  "name": "OPTICIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082210.KD",
  "name": "OPTRONTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131030.KD",
  "name": "OPTUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900300.KD",
  "name": "ORGANIC TEA COSMETICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010470.KD",
  "name": "ORICOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036220.KD",
  "name": "OSANG HEALTHCARE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053980.KD",
  "name": "OSANGJAIEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "368970.KD",
  "name": "OSP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226400.KD",
  "name": "OSTEONIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052420.KD",
  "name": "OSUNG ADVANCED MATERIALS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "227610.KD",
  "name": "OUTIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352910.KD",
  "name": "Obigo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226950.KD",
  "name": "OliX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "244460.KD",
  "name": "Olipass",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057540.KD",
  "name": "Omnisystem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "382840.KD",
  "name": "Onejoon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049480.KD",
  "name": "Openbase",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "394280.KD",
  "name": "Openedges Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "440320.KD",
  "name": "Openknowl",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "380540.KD",
  "name": "Opticore",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153710.KD",
  "name": "Optipharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046120.KD",
  "name": "Orbitech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065500.KD",
  "name": "Orient Precision Industries",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "239890.KD",
  "name": "P&H TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347740.KD",
  "name": "P&K Skin Research Center",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "137400.KD",
  "name": "P&T",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065690.KD",
  "name": "PAKERS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "271830.KD",
  "name": "PAMTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068050.KD",
  "name": "PAN ENTERTAINMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058530.KD",
  "name": "PANACEA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091700.KD",
  "name": "PARTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043200.KD",
  "name": "PARU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037070.KD",
  "name": "PASECO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "177830.KD",
  "name": "PAVONINE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051380.KD",
  "name": "PCD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241820.KD",
  "name": "PCL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "168360.KD",
  "name": "PEMTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "087010.KD",
  "name": "PEPTRON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043370.KD",
  "name": "PHA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057880.KD",
  "name": "PHC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "161580.KD",
  "name": "PHILOPTICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347770.KD",
  "name": "PIMS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006140.KD",
  "name": "PJ Electro",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "128660.KD",
  "name": "PJ METAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "075130.KD",
  "name": "PLANTYNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023770.KD",
  "name": "PLAYWITH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035200.KD",
  "name": "PLUMB FAST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "237750.KD",
  "name": "PNC Technologies",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024940.KD",
  "name": "PNPOONGNYUN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "257370.KD",
  "name": "PNT Ms",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318020.KD",
  "name": "POINT MOBILE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "256630.KD",
  "name": "POINTENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "114630.KD",
  "name": "POLARIS UNO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "472850.KD",
  "name": "POND GROUP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "371950.KD",
  "name": "POONGWON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "105760.KD",
  "name": "POSBANK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009520.KD",
  "name": "POSCO M-TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "047310.KD",
  "name": "POWER LOGICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037030.KD",
  "name": "POWERNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "062970.KD",
  "name": "PPI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321260.KD",
  "name": "PRO2000",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053610.KD",
  "name": "PROTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "303360.KD",
  "name": "PROTIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "319660.KD",
  "name": "PSK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031980.KD",
  "name": "PSK HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002230.KD",
  "name": "PSTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094940.KD",
  "name": "PULOON TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251970.KD",
  "name": "PUM-TECH KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093380.KD",
  "name": "PUNGKANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007330.KD",
  "name": "PUREUN S.BK.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222110.KD",
  "name": "PanGen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054300.KD",
  "name": "Panstar Enterprise",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "034230.KD",
  "name": "Paradise",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033540.KD",
  "name": "Paratech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140860.KD",
  "name": "Park Systems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263750.KD",
  "name": "PearlAbyss",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "304840.KD",
  "name": "PeopleBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208340.KD",
  "name": "PharmAbcine",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214450.KD",
  "name": "PharmaResearch",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "318010.KD",
  "name": "Pharmsville",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388870.KD",
  "name": "Pharos",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "378340.KD",
  "name": "Philenergy",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376180.KD",
  "name": "Picogram",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "291810.KD",
  "name": "Pintel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "170790.KD",
  "name": "Piolink",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "087600.KD",
  "name": "Pixelplus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405000.KD",
  "name": "Plasmapp",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "367000.KD",
  "name": "Plateer",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "237820.KD",
  "name": "PlayD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019570.KD",
  "name": "Plutus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039980.KD",
  "name": "Polaris AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041910.KD",
  "name": "Polaris AI Pharma",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041020.KD",
  "name": "Polaris Office",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "335810.KD",
  "name": "Precision Biosensor",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "334970.KD",
  "name": "Prestige Biologics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "147760.KD",
  "name": "Protec Mems Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950200.KD",
  "name": "Psomagen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023900.KD",
  "name": "Pungguk Ethanol",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445180.KD",
  "name": "Purit",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016600.KD",
  "name": "QCP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405100.KD",
  "name": "QRT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066310.KD",
  "name": "QSI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "227100.KD",
  "name": "QTON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "432720.KD",
  "name": "QUALITAS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078940.KD",
  "name": "QUANTAPIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317690.KD",
  "name": "QuantaMatrix",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348080.KD",
  "name": "Quratis",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115180.KD",
  "name": "Qurient",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171010.KD",
  "name": "RAM TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317120.KD",
  "name": "RANIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232680.KD",
  "name": "RAONTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418420.KD",
  "name": "RAONTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214260.KD",
  "name": "RAPHAS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228850.KD",
  "name": "RAYENCE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "361570.KD",
  "name": "RBW",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377450.KD",
  "name": "REFINE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "302550.KD",
  "name": "REMED",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "327260.KD",
  "name": "RF Materials",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "218410.KD",
  "name": "RFHIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "061040.KD",
  "name": "RFTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096610.KD",
  "name": "RFsemi",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200350.KD",
  "name": "RMRI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148250.KD",
  "name": "RN2 Technologies",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108490.KD",
  "name": "ROBOTIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071280.KD",
  "name": "RORZE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "314140.KD",
  "name": "RPBO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140670.KD",
  "name": "RS Automation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131370.KD",
  "name": "RSUPPORT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217500.KD",
  "name": "RUSSELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "191410.KD",
  "name": "RYUK-IL C&S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277810.KD",
  "name": "Rainbow Robotics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042510.KD",
  "name": "RaonSecure",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228670.KD",
  "name": "Ray",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038390.KD",
  "name": "RedcapTour",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "443250.KD",
  "name": "Revu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042500.KD",
  "name": "RingNet",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215100.KD",
  "name": "RoboRobo",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090360.KD",
  "name": "Robostar",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900260.KD",
  "name": "Rothwell",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096630.KD",
  "name": "S Connect",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050760.KD",
  "name": "S polytech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "260970.KD",
  "name": "S&D",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091340.KD",
  "name": "S&K",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101490.KD",
  "name": "S&S TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "103230.KD",
  "name": "S&W Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095910.KD",
  "name": "S-ENERGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "304360.KD",
  "name": "S.Biomedics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122690.KD",
  "name": "SAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053060.KD",
  "name": "SAE DONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "304100.KD",
  "name": "SALTLUX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023600.KD",
  "name": "SAMBO CORR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009620.KD",
  "name": "SAMBO IND",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053700.KD",
  "name": "SAMBO MOTORS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024950.KD",
  "name": "SAMCHULY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419530.KD",
  "name": "SAMG ENTERTAINMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046390.KD",
  "name": "SAMHWA NWS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "437730.KD",
  "name": "SAMHYUN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002290.KD",
  "name": "SAMIL ENTERPRISE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037460.KD",
  "name": "SAMJI ELECT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054090.KD",
  "name": "SAMJIN LND",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122350.KD",
  "name": "SAMKEE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419050.KD",
  "name": "SAMKEE EV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018310.KD",
  "name": "SAMMOK S-FORM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038500.KD",
  "name": "SAMPYO Cement",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017480.KD",
  "name": "SAMSCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "468510.KD",
  "name": "SAMSUNG SPAC IX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "425290.KD",
  "name": "SAMSUNG SPAC VI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "439250.KD",
  "name": "SAMSUNG SPAC VII",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "448740.KD",
  "name": "SAMSUNG SPAC VIII",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031330.KD",
  "name": "SAMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "361670.KD",
  "name": "SAMYOUNG S&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "411080.KD",
  "name": "SANDS LAB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "091580.KD",
  "name": "SANGSIN EDP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "188260.KD",
  "name": "SANIGEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452430.KD",
  "name": "SAPIEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "351320.KD",
  "name": "SAT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060540.KD",
  "name": "SAT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "088280.KD",
  "name": "SAWNICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389500.KD",
  "name": "SBB TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "950110.KD",
  "name": "SBI FinTech Solutions",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019550.KD",
  "name": "SBI Investment KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027580.KD",
  "name": "SBK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086710.KD",
  "name": "SBS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "151910.KD",
  "name": "SBW Life Sciences",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080470.KD",
  "name": "SCAutotech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042110.KD",
  "name": "SCD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "000250.KD",
  "name": "SCD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036120.KD",
  "name": "SCI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246960.KD",
  "name": "SCL Science",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298060.KD",
  "name": "SCM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217480.KD",
  "name": "SDBIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099220.KD",
  "name": "SDN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121890.KD",
  "name": "SDSYSTEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011560.KD",
  "name": "SEBO MEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232830.KD",
  "name": "SECUCEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131090.KD",
  "name": "SECUVE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "096530.KD",
  "name": "SEEGENE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067770.KD",
  "name": "SEJINTS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "258830.KD",
  "name": "SEJONG MEDICAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036630.KD",
  "name": "SEJONG TELECOM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039310.KD",
  "name": "SEJOONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053450.KD",
  "name": "SEKONIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108860.KD",
  "name": "SELVAS AI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208370.KD",
  "name": "SELVAS Healthcare",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "252990.KD",
  "name": "SEMCNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "347000.KD",
  "name": "SENKO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035890.KD",
  "name": "SEOHEE CONSTRUCTION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "178320.KD",
  "name": "SEOJIN SYSTEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018680.KD",
  "name": "SEOUL PHARMA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092190.KD",
  "name": "SEOUL VIOSYS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043710.KD",
  "name": "SEOULEAGUER",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019770.KD",
  "name": "SEOYON TOPMETAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340440.KD",
  "name": "SERIM B&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042600.KD",
  "name": "SERONICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "027040.KD",
  "name": "SET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049830.KD",
  "name": "SEUNG IL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "252500.KD",
  "name": "SEWHA P&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100700.KD",
  "name": "SEWOONMEDICAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056190.KD",
  "name": "SFA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036540.KD",
  "name": "SFASemicon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "288620.KD",
  "name": "SFC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089980.KD",
  "name": "SFTC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "255220.KD",
  "name": "SG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040610.KD",
  "name": "SG&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049470.KD",
  "name": "SGA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "184230.KD",
  "name": "SGA Solutions",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "016250.KD",
  "name": "SGC E&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "162300.KD",
  "name": "SHIN STEEL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290520.KD",
  "name": "SHINDO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "243840.KD",
  "name": "SHINHEUNG SEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056700.KD",
  "name": "SHINWHA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086980.KD",
  "name": "SHOWBOX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "472220.KD",
  "name": "SHT-10 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430220.KD",
  "name": "SHT-8 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "445970.KD",
  "name": "SHT-9 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099320.KD",
  "name": "SI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065420.KD",
  "name": "SI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010280.KD",
  "name": "SICC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "020710.KD",
  "name": "SIGONG TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025870.KD",
  "name": "SILLA SG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222800.KD",
  "name": "SIMMTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036710.KD",
  "name": "SIMMTECH HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "138070.KD",
  "name": "SINJIN SM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "002800.KD",
  "name": "SINSIN PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290560.KD",
  "name": "SINSIWAY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189860.KD",
  "name": "SJEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "306040.KD",
  "name": "SJG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457940.KD",
  "name": "SK Securities No.10 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "472230.KD",
  "name": "SK Securities No.11 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "435870.KD",
  "name": "SK Securities No.8 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "455910.KD",
  "name": "SK Securities No.9 SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014620.KD",
  "name": "SKB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "276040.KD",
  "name": "SKONEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214310.KD",
  "name": "SL Energy",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246250.KD",
  "name": "SLSBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048550.KD",
  "name": "SM C&C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063440.KD",
  "name": "SM Life Design",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007820.KD",
  "name": "SMC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041510.KD",
  "name": "SME",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099440.KD",
  "name": "SMEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100660.KD",
  "name": "SMI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038680.KD",
  "name": "SNET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080000.KD",
  "name": "SNU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "258790.KD",
  "name": "SOFTCAMP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032680.KD",
  "name": "SOFTCEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032685.KD",
  "name": "SOFTCEN(1P)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "035610.KD",
  "name": "SOLBORN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043100.KD",
  "name": "SOLCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290690.KD",
  "name": "SOLUX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066910.KD",
  "name": "SONOKONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067160.KD",
  "name": "SOOP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050960.KD",
  "name": "SOOSAN INT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "058610.KD",
  "name": "SPG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317830.KD",
  "name": "SPSystems",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "443670.KD",
  "name": "SPsoft",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046890.KD",
  "name": "SSC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065350.KD",
  "name": "SSDELTATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101000.KD",
  "name": "SSII",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "275630.KD",
  "name": "SSR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "237690.KD",
  "name": "ST Pharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115570.KD",
  "name": "STARFLEX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052020.KD",
  "name": "STCUBE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "039440.KD",
  "name": "STI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "098660.KD",
  "name": "STO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204630.KD",
  "name": "STUDIO SANTA CLAUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234300.KD",
  "name": "STraffic",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "031860.KD",
  "name": "SU-Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "003100.KD",
  "name": "SUN KWANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037350.KD",
  "name": "SUNGDO ENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043260.KD",
  "name": "SUNGHO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "081580.KD",
  "name": "SUNGWOO ELEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045300.KD",
  "name": "SUNGWOOTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "171090.KD",
  "name": "SUNIC SYSTEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321370.KD",
  "name": "SV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "289080.KD",
  "name": "SV INVESTMENT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "015750.KD",
  "name": "SW HITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "093920.KD",
  "name": "SWIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "109610.KD",
  "name": "SY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365330.KD",
  "name": "SY STEEL TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054540.KD",
  "name": "SYMTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "269620.KD",
  "name": "SYSWORK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "328380.KD",
  "name": "Saltware",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "009300.KD",
  "name": "Sam-A Pharm.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032280.KD",
  "name": "SamIl",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032750.KD",
  "name": "Samjin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014970.KD",
  "name": "Samryoong",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065570.KD",
  "name": "Samyung ENC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "419120.KD",
  "name": "Sandoll",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042940.KD",
  "name": "Sangji Construction",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038540.KD",
  "name": "Sangsangin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "415580.KD",
  "name": "Sangsangin SPAC III",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452670.KD",
  "name": "Sangsangin SPAC IV",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263810.KD",
  "name": "Sangshin Electronics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143240.KD",
  "name": "Saramin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "148150.KD",
  "name": "Se Gyung Hi Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396300.KD",
  "name": "SeA Mechanics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "107600.KD",
  "name": "Sebitchem",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418250.KD",
  "name": "SecuLetter",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017510.KD",
  "name": "SemyungElec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "006730.KD",
  "name": "Seobu T&D",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011370.KD",
  "name": "Seohan",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065710.KD",
  "name": "Seoho",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079650.KD",
  "name": "Seosan",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038070.KD",
  "name": "SeouLin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "063170.KD",
  "name": "Seoul Auction",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "222810.KD",
  "name": "Setopia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234100.KD",
  "name": "Sewon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024830.KD",
  "name": "SewonCorp",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "378800.KD",
  "name": "Shaperon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "187270.KD",
  "name": "Shin Hwa Contech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "418210.KD",
  "name": "Shinhan 10th SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "452980.KD",
  "name": "Shinhan 11th SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "474660.KD",
  "name": "Shinhan 12th SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "474930.KD",
  "name": "Shinhan 13th SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "405640.KD",
  "name": "Shinhan 9th SPAC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012790.KD",
  "name": "Shinil Pharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "416180.KD",
  "name": "Shinsung ST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "017000.KD",
  "name": "ShinwonConst",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "429270.KD",
  "name": "Sigetronics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033170.KD",
  "name": "Signetics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "257720.KD",
  "name": "Silicon2",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215600.KD",
  "name": "SillaJen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "001000.KD",
  "name": "SillaTextile",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "159910.KD",
  "name": "Skin&Skin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033790.KD",
  "name": "Skymoons Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "424960.KD",
  "name": "Smart Radar System",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136510.KD",
  "name": "Smart Solutions",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "050890.KD",
  "name": "Solid",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060230.KD",
  "name": "Sonid",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084180.KD",
  "name": "Soosung Webtoon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357780.KD",
  "name": "Soulbrain",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036830.KD",
  "name": "Soulbrain Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "013810.KD",
  "name": "Speco",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203690.KD",
  "name": "Sphere Power",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192440.KD",
  "name": "Spigen Korea",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330730.KD",
  "name": "Stonebridge Ventures",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "352090.KD",
  "name": "Stormtec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253450.KD",
  "name": "Studio Dragon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "415380.KD",
  "name": "Studio Samick",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294630.KD",
  "name": "SuNAM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "253840.KD",
  "name": "Sugentech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "357550.KD",
  "name": "Sukgyung",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067370.KD",
  "name": "SunBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365340.KD",
  "name": "SungEel HiTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "236200.KD",
  "name": "Suprema",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094840.KD",
  "name": "Suprema HQ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298830.KD",
  "name": "Suresoft",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "140070.KD",
  "name": "SurplusGLOBAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048870.KD",
  "name": "Synergy Innovation",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "025320.KD",
  "name": "Synopex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "226330.KD",
  "name": "SyntekaBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057680.KD",
  "name": "T Scientific",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340570.KD",
  "name": "T&L",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246710.KD",
  "name": "T&R Biofab",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "117730.KD",
  "name": "T-ROBOTICS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "204610.KD",
  "name": "T3",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "323280.KD",
  "name": "TAESUNG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044490.KD",
  "name": "TAEWOONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053620.KD",
  "name": "TAEYANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "033830.KD",
  "name": "TBC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064760.KD",
  "name": "TCK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "200230.KD",
  "name": "TELCON RF PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "425040.KD",
  "name": "TEMC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241790.KD",
  "name": "TEMC CNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073640.KD",
  "name": "TERA SCIENCE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095610.KD",
  "name": "TES",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "425420.KD",
  "name": "TFE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "224060.KD",
  "name": "THE CODI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089230.KD",
  "name": "THE E&M",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "161570.KD",
  "name": "THE MIDONG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066700.KD",
  "name": "THERAGEN ETEX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "322180.KD",
  "name": "THiRA-UTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032540.KD",
  "name": "TJ MEDIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104480.KD",
  "name": "TK CHEMICAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "023160.KD",
  "name": "TKCORP.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "022220.KD",
  "name": "TKG AIKANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "356860.KD",
  "name": "TLB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "062860.KD",
  "name": "TLi",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131100.KD",
  "name": "TN entertainment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "298540.KD",
  "name": "TNH CO., LTD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079970.KD",
  "name": "TOBESOFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215480.KD",
  "name": "TOEBOX KOREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "393210.KD",
  "name": "TOMATOSYSTEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "228340.KD",
  "name": "TONGYANG PILE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065130.KD",
  "name": "TOP ENG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "360070.KD",
  "name": "TOP MATERIAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "108230.KD",
  "name": "TOPTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051360.KD",
  "name": "TOVIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048770.KD",
  "name": "TPC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "130740.KD",
  "name": "TPC Global",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "417790.KD",
  "name": "TRUEN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "105550.KD",
  "name": "TRUWIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043220.KD",
  "name": "TS Nexgen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317240.KD",
  "name": "TS Trillion",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045340.KD",
  "name": "TSB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "026150.KD",
  "name": "TSConstruct",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "131290.KD",
  "name": "TSE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "277880.KD",
  "name": "TSI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "246690.KD",
  "name": "TSInvestment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "290090.KD",
  "name": "TWIM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "124560.KD",
  "name": "Taewoong Logistics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "010170.KD",
  "name": "TaihanFiberoptics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064520.KD",
  "name": "TechL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089030.KD",
  "name": "Techwing",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "191420.KD",
  "name": "Tego",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054450.KD",
  "name": "Telechips",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032860.KD",
  "name": "The Lamy",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043090.KD",
  "name": "The Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084730.KD",
  "name": "Thinkware",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "208640.KD",
  "name": "Thumbage",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "219130.KD",
  "name": "TigerElec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "321550.KD",
  "name": "TiumBio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "199800.KD",
  "name": "ToolGen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "134580.KD",
  "name": "Topco Media",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "081150.KD",
  "name": "Tplex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069330.KD",
  "name": "U.I.DISPLAY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "221800.KD",
  "name": "U2BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032620.KD",
  "name": "UBCARE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "084440.KD",
  "name": "UBION",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089850.KD",
  "name": "UBIVELOX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049520.KD",
  "name": "UIL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065680.KD",
  "name": "UJU",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "011320.KD",
  "name": "UNICK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080720.KD",
  "name": "UNION KOREA PHARM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036200.KD",
  "name": "UNISEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018000.KD",
  "name": "UNISON",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "241690.KD",
  "name": "UNITEKNO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "263770.KD",
  "name": "UST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "179900.KD",
  "name": "UTI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "264450.KD",
  "name": "Ubiquoss",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078070.KD",
  "name": "Ubiquoss Holdings",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "086390.KD",
  "name": "UniTest",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "203450.KD",
  "name": "Union community",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "142210.KD",
  "name": "Unitrontech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251630.KD",
  "name": "V-ONE TECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "301300.KD",
  "name": "VAIV company",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "331520.KD",
  "name": "VALOFE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043150.KD",
  "name": "VATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365900.KD",
  "name": "VC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065450.KD",
  "name": "VICTEK",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "126340.KD",
  "name": "VINATECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "335890.KD",
  "name": "VIOL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "438700.KD",
  "name": "VIRNECT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072950.KD",
  "name": "VISSEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082920.KD",
  "name": "VITCELL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082800.KD",
  "name": "VIVOZON PHARMACEUTICAL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "089970.KD",
  "name": "VM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "310210.KD",
  "name": "VRNI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018290.KD",
  "name": "VT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "338220.KD",
  "name": "VUNO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "323990.KD",
  "name": "Vaxcell-Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019010.KD",
  "name": "VenueG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "094850.KD",
  "name": "Very Good Tour",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "177350.KD",
  "name": "Vessel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "308080.KD",
  "name": "ViGenCell",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "141000.KD",
  "name": "Viatron",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "210120.KD",
  "name": "Victents",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "121800.KD",
  "name": "Vidente",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "100120.KD",
  "name": "Vieworks",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "042370.KD",
  "name": "Vitzro Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054220.KD",
  "name": "VitzroSys",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215360.KD",
  "name": "W.I.C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072470.KD",
  "name": "W.I.H.C",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "196700.KD",
  "name": "WAPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079000.KD",
  "name": "WATOS COREA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "095270.KD",
  "name": "WAVE ELECTRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "393890.KD",
  "name": "WCP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "403490.KD",
  "name": "WDG Farm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "076080.KD",
  "name": "WELCRON HANTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "043590.KD",
  "name": "WELKEEPS HITECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064090.KD",
  "name": "WESTRISE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "313760.KD",
  "name": "WILLINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104830.KD",
  "name": "WIMCO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "900340.KD",
  "name": "WING YIP FOOD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "335870.KD",
  "name": "WINGS FOOT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "071460.KD",
  "name": "WINIA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "377460.KD",
  "name": "WINIA AID",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "044340.KD",
  "name": "WINIX",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "320000.KD",
  "name": "WINTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065370.KD",
  "name": "WISE iTech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "348350.KD",
  "name": "WITHTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038620.KD",
  "name": "WIZ",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036090.KD",
  "name": "WIZIT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "014190.KD",
  "name": "WONIK CUBE Corp.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030530.KD",
  "name": "WONIK HOLDINGS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "240810.KD",
  "name": "WONIK IPS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "217820.KD",
  "name": "WONIK PNE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "074600.KD",
  "name": "WONIK QnC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "336570.KD",
  "name": "WONTECH",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "018620.KD",
  "name": "WOOGENE B&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "457550.KD",
  "name": "WOOJIN Ntec",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215380.KD",
  "name": "WOOJUNG BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "082850.KD",
  "name": "WOOREE BIO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "153490.KD",
  "name": "WOOREE E&L",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "037400.KD",
  "name": "WOOREE ENTERPRISE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101170.KD",
  "name": "WOORIM PTS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046970.KD",
  "name": "WOORIRO",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "073560.KD",
  "name": "WOORISON F&G",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "103840.KD",
  "name": "WOOYANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "396470.KD",
  "name": "WOT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008290.KD",
  "name": "WPMulsan",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066590.KD",
  "name": "WSA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299170.KD",
  "name": "WSI",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "041190.KD",
  "name": "WTIC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "299900.KD",
  "name": "WYSIWYG STUDIOS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "376980.KD",
  "name": "Wanted Lab",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "336060.KD",
  "name": "Wavus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053580.KD",
  "name": "WebCash",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069080.KD",
  "name": "Webzen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065950.KD",
  "name": "Welcron",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "112040.KD",
  "name": "Wemade",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101730.KD",
  "name": "Wemade Max",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123420.KD",
  "name": "Wemade Play",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "332570.KD",
  "name": "WiPAM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122990.KD",
  "name": "WiSoL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "065530.KD",
  "name": "Wiable",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "192390.KD",
  "name": "Winhitech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "097800.KD",
  "name": "Winpac",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "136540.KD",
  "name": "Wins",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "273060.KD",
  "name": "Wise birds",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "330350.KD",
  "name": "Withus Pharm",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032940.KD",
  "name": "WonIk",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "307280.KD",
  "name": "Wonbiogen",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "012620.KD",
  "name": "Wonil",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "008370.KD",
  "name": "Wonpoong",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "115440.KD",
  "name": "WooriNet",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "032820.KD",
  "name": "WooriTG, Inc.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "046940.KD",
  "name": "Woowon Development",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "101160.KD",
  "name": "Worldex",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "254120.KD",
  "name": "XAVIS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "189330.KD",
  "name": "XIIlab",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "205100.KD",
  "name": "XM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "070300.KD",
  "name": "Xcure",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "317770.KD",
  "name": "Xperix",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "373200.KD",
  "name": "Xplus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "338840.KD",
  "name": "Y-Biologics",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "067900.KD",
  "name": "Y-ENTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "066430.KD",
  "name": "Y-OPTICS MANUFACTURE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "255440.KD",
  "name": "YAS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "057030.KD",
  "name": "YBM NET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "104620.KD",
  "name": "YBTOUR",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "232140.KD",
  "name": "YCC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "112290.KD",
  "name": "YCCHEM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "146060.KD",
  "name": "YCPIPE",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "053280.KD",
  "name": "YES24",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122640.KD",
  "name": "YEST",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "340930.KD",
  "name": "YET",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "122870.KD",
  "name": "YG Entertainment",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "019210.KD",
  "name": "YG-1",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "265560.KD",
  "name": "YHTEC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "432430.KD",
  "name": "YLAB",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "007530.KD",
  "name": "YM",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "273640.KD",
  "name": "YM Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "155650.KD",
  "name": "YMC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "251370.KD",
  "name": "YMT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "024800.KD",
  "name": "YOOSUNG T&S",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036560.KD",
  "name": "YPPC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "372170.KD",
  "name": "YSFC Co.,Ltd",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040300.KD",
  "name": "YTN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "388720.KD",
  "name": "YUIL",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "240600.KD",
  "name": "YUJIN TECHNOLOGY",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048430.KD",
  "name": "YURA TECH.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "051390.KD",
  "name": "YW CO.,LTD",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "143540.KD",
  "name": "YWDSP",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "030960.KD",
  "name": "Yangjisa",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "250930.KD",
  "name": "YeSUN Tech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036000.KD",
  "name": "YeaRimDang",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "054930.KD",
  "name": "Yooshin",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "060850.KD",
  "name": "YoungLimWon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "435380.KD",
  "name": "Yuanta SPAC 10",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "444920.KD",
  "name": "Yuanta SPAC 11",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "446150.KD",
  "name": "Yuanta SPAC 12",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "449020.KD",
  "name": "Yuanta SPAC 13",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "450940.KD",
  "name": "Yuanta SPAC 14",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "473050.KD",
  "name": "Yuanta SPAC 15",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "474490.KD",
  "name": "Yuanta SPAC 16",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "430700.KD",
  "name": "Yuanta SPAC 9",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "056080.KD",
  "name": "Yujin Robot",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072770.KD",
  "name": "Yulho",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "079370.KD",
  "name": "ZEUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "239340.KD",
  "name": "ZUMinternet",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "045510.KD",
  "name": "ZWNS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "234920.KD",
  "name": "Zaigle",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "389020.KD",
  "name": "Zaram Technology",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "303030.KD",
  "name": "Zinitix Co.,Ltd.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "294570.KD",
  "name": "coocon",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021040.KD",
  "name": "dhSteel",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "021045.KD",
  "name": "dhSteel(1P)",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "092130.KD",
  "name": "e-Credible",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "134060.KD",
  "name": "e-future",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "078020.KD",
  "name": "eBEST IS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "080010.KD",
  "name": "eSANG",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099750.KD",
  "name": "ezCaretech",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "186230.KD",
  "name": "greenplus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "064240.KD",
  "name": "homecast",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "099190.KD",
  "name": "i-SENS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "289010.KD",
  "name": "i-Scream Edu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "214430.KD",
  "name": "i3system",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "038880.KD",
  "name": "iA",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052460.KD",
  "name": "iCRAFT",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "052220.KD",
  "name": "iMBC",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "048530.KD",
  "name": "iNtRON Bio",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "090150.KD",
  "name": "iWIN",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "123010.KD",
  "name": "iWIN PLUS",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "068330.KD",
  "name": "ilShinbiobase Co., Ltd.",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "181340.KD",
  "name": "isMedia",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "040420.KD",
  "name": "jls",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "036030.KD",
  "name": "kt alpha",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "049950.KD",
  "name": "meerecompany",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "072870.KD",
  "name": "megastudy",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "215200.KD",
  "name": "megastudyEdu",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "259630.KD",
  "name": "mplus",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "069410.KD",
  "name": "nTels",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 },
 {
  "symbol": "365270.KD",
  "name": "the curacle",
  "currency": "KRW",
  "exchangeShortName": "KRX",
  "stockExchange": "KOSDAQ"
 }
]

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except FileExistsError as e:
        print(e)

    return conn
    
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except RuntimeError as e:
        print(e)
        

def initial_database():
    db_name = "stock_ticker_database.db"
    if(os.path.isfile(db_name)):
        return
    conn = create_connection(db_name)

    create_table_sql = """CREATE TABLE IF NOT EXISTS stock_ticker (
	    symbol text PRIMARY KEY,
	    name text NOT NULL,
    	currency text,
	    stockExchange text, 
        exchangeShortName text
    );"""
    create_table(conn, create_table_sql)
    
    for item in stock_ticker_data:
        conn.execute("INSERT INTO stock_ticker (symbol, name, currency,stockExchange, exchangeShortName ) VALUES (?, ?, ?, ?,?)", 
                    (item["symbol"], item["name"], item["currency"], item["stockExchange"],item["exchangeShortName"]))
    conn.commit()
    conn.close()

    
