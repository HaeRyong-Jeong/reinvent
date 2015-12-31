# -*- coding: utf-8 -*-

import re
import time
import urllib
import socket
import urlparse
from datetime import timedelta

import requests
from tornado.iostream import IOStream

#  from store import r as r_store, RedisQueue


#  rq = RedisQueue(r_store, 'proxy')


CONTENT = """
<tbody><tr><td>165.139.149.169</td><td>3128</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>205.189.170.150</td><td>80</td><td>CA</td><td>Canada</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>42.117.7.158</td><td>8080</td><td>VN</td><td>Vietnam</td><td>anonymous</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>118.238.25.61</td><td>80</td><td>JP</td><td>Japan</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>103.197.252.132</td><td>80</td><td></td><td>Unknown</td><td>anonymous</td><td>yes</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>62.180.27.25</td><td>80</td><td>DE</td><td>Germany</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>31.173.74.73</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>anonymous</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>54.254.182.14</td><td>80</td><td>SG</td><td>Singapore</td><td>anonymous</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>175.126.192.92</td><td>80</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>151.80.195.189</td><td>8080</td><td>FR</td><td>France</td><td>anonymous</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>61.93.246.50</td><td>8080</td><td>HK</td><td>Hong Kong</td><td>elite proxy</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>50.30.35.62</td><td>3128</td><td>US</td><td>United States</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>177.159.200.100</td><td>3128</td><td>BR</td><td>Brazil</td><td>anonymous</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>31.210.10.34</td><td>8080</td><td>TR</td><td>Turkey</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>200.223.212.108</td><td>80</td><td>BR</td><td>Brazil</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>61.93.246.49</td><td>8080</td><td>HK</td><td>Hong Kong</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>113.30.102.91</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>61.38.252.13</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>183.111.169.207</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>177.21.255.22</td><td>80</td><td>BR</td><td>Brazil</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>192.240.46.126</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>62.201.200.17</td><td>80</td><td>IQ</td><td>Iraq</td><td>elite proxy</td><td>yes</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>103.53.16.6</td><td>8080</td><td>AF</td><td>Afghanistan</td><td>anonymous</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>91.106.42.22</td><td>80</td><td>IQ</td><td>Iraq</td><td>elite proxy</td><td>yes</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>192.99.20.92</td><td>3128</td><td>CA</td><td>Canada</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>183.111.169.201</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 seconds ago</td></tr>
<tr><td>188.165.141.151</td><td>80</td><td>FI</td><td>Finland</td><td>anonymous</td><td>no</td><td>no</td><td>3 seconds ago</td></tr>
<tr><td>121.88.249.28</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>19 seconds ago</td></tr>
<tr><td>87.236.214.93</td><td>3128</td><td>GB</td><td>United Kingdom</td><td>anonymous</td><td>yes</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>46.51.175.89</td><td>3129</td><td>IE</td><td>Ireland</td><td>anonymous</td><td>yes</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>195.135.213.121</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>211.23.248.22</td><td>8080</td><td>TW</td><td>Taiwan</td><td>anonymous</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>184.73.182.184</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>no</td><td>1 minute ago</td></tr>
<tr><td>85.143.24.70</td><td>80</td><td>RU</td><td>Russian Federation</td><td>anonymous</td><td>no</td><td>no</td><td>1 minute ago</td></tr>
<tr><td>52.25.29.56</td><td>9999</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>87.98.218.86</td><td>3128</td><td>FR</td><td>France</td><td>anonymous</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>36.226.249.62</td><td>80</td><td>TW</td><td>Taiwan</td><td>elite proxy</td><td>no</td><td>no</td><td>1 minute ago</td></tr>
<tr><td>192.240.46.123</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>198.50.248.220</td><td>3128</td><td>CA</td><td>Canada</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 minute ago</td></tr>
<tr><td>36.235.154.193</td><td>8888</td><td>TW</td><td>Taiwan</td><td>anonymous</td><td>yes</td><td>yes</td><td>10 minutes ago</td></tr>
<tr><td>190.63.174.243</td><td>8081</td><td>EC</td><td>Ecuador</td><td>anonymous</td><td>no</td><td>yes</td><td>10 minutes ago</td></tr>
<tr><td>58.120.96.231</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>10 minutes ago</td></tr>
<tr><td>195.190.122.154</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>no</td><td>10 minutes ago</td></tr>
<tr><td>61.93.246.59</td><td>8080</td><td>HK</td><td>Hong Kong</td><td>elite proxy</td><td>yes</td><td>yes</td><td>10 minutes ago</td></tr>
<tr><td>109.75.117.26</td><td>3128</td><td>IT</td><td>Italy</td><td>anonymous</td><td>no</td><td>yes</td><td>10 minutes ago</td></tr>
<tr><td>183.111.169.206</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>11 minutes ago</td></tr>
<tr><td>58.153.28.214</td><td>80</td><td>HK</td><td>Hong Kong</td><td>elite proxy</td><td>no</td><td>no</td><td>11 minutes ago</td></tr>
<tr><td>153.120.8.207</td><td>80</td><td>JP</td><td>Japan</td><td>anonymous</td><td>no</td><td>yes</td><td>20 minutes ago</td></tr>
<tr><td>36.81.73.184</td><td>8080</td><td>ID</td><td>Indonesia</td><td>elite proxy</td><td>no</td><td>no</td><td>20 minutes ago</td></tr>
<tr><td>190.111.88.194</td><td>8080</td><td>EC</td><td>Ecuador</td><td>elite proxy</td><td>no</td><td>no</td><td>20 minutes ago</td></tr>
<tr><td>110.45.135.229</td><td>8080</td><td>KR</td><td>Korea, Republic of</td><td>anonymous</td><td>no</td><td>no</td><td>20 minutes ago</td></tr>
<tr><td>180.178.135.102</td><td>8080</td><td>PK</td><td>Pakistan</td><td>anonymous</td><td>no</td><td>yes</td><td>20 minutes ago</td></tr>
<tr><td>176.31.237.157</td><td>8888</td><td>FR</td><td>France</td><td>elite proxy</td><td>no</td><td>yes</td><td>20 minutes ago</td></tr>
<tr><td>37.193.122.59</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>no</td><td>21 minutes ago</td></tr>
<tr><td>202.90.68.50</td><td>80</td><td>PF</td><td>French Polynesia</td><td>anonymous</td><td>no</td><td>yes</td><td>30 minutes ago</td></tr>
<tr><td>194.27.128.244</td><td>80</td><td>TR</td><td>Turkey</td><td>elite proxy</td><td>yes</td><td>no</td><td>30 minutes ago</td></tr>
<tr><td>54.157.6.24</td><td>80</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>yes</td><td>30 minutes ago</td></tr>
<tr><td>211.110.142.29</td><td>80</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>30 minutes ago</td></tr>
<tr><td>58.120.96.233</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>30 minutes ago</td></tr>
<tr><td>128.199.129.179</td><td>3128</td><td>SG</td><td>Singapore</td><td>anonymous</td><td>no</td><td>yes</td><td>30 minutes ago</td></tr>
<tr><td>61.38.252.17</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>40 minutes ago</td></tr>
<tr><td>15.126.255.163</td><td>80</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>no</td><td>41 minutes ago</td></tr>
<tr><td>37.1.55.230</td><td>80</td><td>RU</td><td>Russian Federation</td><td>anonymous</td><td>no</td><td>no</td><td>41 minutes ago</td></tr>
<tr><td>115.113.174.21</td><td>80</td><td>IN</td><td>India</td><td>anonymous</td><td>no</td><td>no</td><td>41 minutes ago</td></tr>
<tr><td>122.15.65.133</td><td>3128</td><td>IN</td><td>India</td><td>anonymous</td><td>no</td><td>yes</td><td>50 minutes ago</td></tr>
<tr><td>61.223.160.253</td><td>8888</td><td>TW</td><td>Taiwan</td><td>anonymous</td><td>no</td><td>no</td><td>50 minutes ago</td></tr>
<tr><td>212.29.229.21</td><td>80</td><td>IL</td><td>Israel</td><td>anonymous</td><td>no</td><td>yes</td><td>51 minutes ago</td></tr>
<tr><td>37.187.242.170</td><td>3128</td><td>FR</td><td>France</td><td>anonymous</td><td>no</td><td>yes</td><td>1 hour ago</td></tr>
<tr><td>1.235.185.57</td><td>80</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 hour ago</td></tr>
<tr><td>212.47.240.207</td><td>80</td><td>FR</td><td>France</td><td>anonymous</td><td>no</td><td>no</td><td>1 hour ago</td></tr>
<tr><td>200.87.179.178</td><td>8080</td><td>BO</td><td>Bolivia</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 2 minutes ago</td></tr>
<tr><td>181.63.250.32</td><td>8080</td><td>CO</td><td>Colombia</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 2 minutes ago</td></tr>
<tr><td>82.162.227.134</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 3 minutes ago</td></tr>
<tr><td>195.225.136.11</td><td>8080</td><td>PL</td><td>Poland</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 4 minutes ago</td></tr>
<tr><td>103.253.145.81</td><td>80</td><td>SG</td><td>Singapore</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 4 minutes ago</td></tr>
<tr><td>180.183.225.16</td><td>8080</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 4 minutes ago</td></tr>
<tr><td>82.209.49.200</td><td>8080</td><td>CZ</td><td>Czech Republic</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>202.122.236.225</td><td>8080</td><td>JP</td><td>Japan</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>46.16.226.10</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>190.102.151.235</td><td>3128</td><td>PE</td><td>Peru</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>54.186.105.158</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>61.42.135.135</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>217.103.135.201</td><td>80</td><td>NL</td><td>Netherlands</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>118.170.41.67</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 5 minutes ago</td></tr>
<tr><td>118.171.149.57</td><td>8080</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>1 hour 6 minutes ago</td></tr>
<tr><td>121.120.80.215</td><td>3128</td><td>MY</td><td>Malaysia</td><td>anonymous</td><td>no</td><td>yes</td><td>1 hour 10 minutes ago</td></tr>
<tr><td>107.170.221.9</td><td>8080</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>no</td><td>1 hour 10 minutes ago</td></tr>
<tr><td>107.129.236.145</td><td>8080</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>no</td><td>1 hour 10 minutes ago</td></tr>
<tr><td>183.111.169.205</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>no</td><td>1 hour 10 minutes ago</td></tr>
<tr><td>183.111.169.208</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 hour 20 minutes ago</td></tr>
<tr><td>89.189.2.190</td><td>80</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 hour 31 minutes ago</td></tr>
<tr><td>49.212.130.61</td><td>3128</td><td>JP</td><td>Japan</td><td>elite proxy</td><td>no</td><td>yes</td><td>1 hour 50 minutes ago</td></tr>
<tr><td>80.82.164.32</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>no</td><td>2 hours 1 minute ago</td></tr>
<tr><td>186.94.252.246</td><td>8080</td><td>VE</td><td>Venezuela</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 1 minute ago</td></tr>
<tr><td>46.32.72.192</td><td>80</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>218.49.74.233</td><td>8080</td><td>KR</td><td>Korea, Republic of</td><td>anonymous</td><td>no</td><td>yes</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>89.98.251.129</td><td>80</td><td>NL</td><td>Netherlands</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>113.160.22.38</td><td>8080</td><td>VN</td><td>Vietnam</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>75.126.26.180</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>112.137.164.232</td><td>3128</td><td>MY</td><td>Malaysia</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 20 minutes ago</td></tr>
<tr><td>15.126.207.25</td><td>80</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>no</td><td>2 hours 21 minutes ago</td></tr>
<tr><td>80.242.219.50</td><td>3128</td><td>KZ</td><td>Kazakhstan</td><td>elite proxy</td><td>no</td><td>no</td><td>2 hours 21 minutes ago</td></tr>
<tr><td>186.93.174.204</td><td>8080</td><td>VE</td><td>Venezuela</td><td>anonymous</td><td>no</td><td>yes</td><td>2 hours 30 minutes ago</td></tr>
<tr><td>200.97.134.98</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 31 minutes ago</td></tr>
<tr><td>92.222.237.18</td><td>8888</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 31 minutes ago</td></tr>
<tr><td>190.72.179.93</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 31 minutes ago</td></tr>
<tr><td>190.52.32.126</td><td>80</td><td>AR</td><td>Argentina</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>177.221.64.8</td><td>8090</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>190.15.39.231</td><td>3128</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>190.39.226.95</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>89.46.100.85</td><td>3128</td><td>RO</td><td>Romania</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>202.21.181.110</td><td>3128</td><td>MV</td><td>Maldives</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>124.81.112.131</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>190.181.18.232</td><td>80</td><td>BO</td><td>Bolivia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>82.114.82.58</td><td>8080</td><td>AL</td><td>Albania</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>193.107.152.66</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>91.230.151.186</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>80.232.216.127</td><td>8585</td><td>LV</td><td>Latvia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>23.105.136.75</td><td>8118</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>37.239.46.74</td><td>80</td><td>IQ</td><td>Iraq</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>210.101.131.231</td><td>8080</td><td>KR</td><td>Korea, Republic of</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>93.104.214.124</td><td>8118</td><td>DE</td><td>Germany</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>108.43.225.47</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>178.140.141.235</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>110.74.195.41</td><td>8080</td><td>KH</td><td>Cambodia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>186.91.107.46</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>91.121.148.72</td><td>3128</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>190.200.249.29</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>91.121.121.199</td><td>4444</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>193.232.184.141</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>178.151.149.227</td><td>80</td><td>UA</td><td>Ukraine</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 32 minutes ago</td></tr>
<tr><td>58.96.188.9</td><td>3128</td><td>HK</td><td>Hong Kong</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>202.173.214.28</td><td>8080</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>82.209.49.194</td><td>8080</td><td>CZ</td><td>Czech Republic</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>124.81.226.146</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>67.23.7.7</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>202.154.190.150</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>82.209.49.196</td><td>8080</td><td>CZ</td><td>Czech Republic</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>138.0.89.45</td><td>8080</td><td>CO</td><td>Colombia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>118.96.94.252</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>202.27.212.136</td><td>8080</td><td>NZ</td><td>New Zealand</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>103.14.45.134</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>175.136.239.174</td><td>8080</td><td>MY</td><td>Malaysia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>89.40.196.10</td><td>8080</td><td>RO</td><td>Romania</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>112.78.137.42</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>36.71.232.23</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>118.97.113.170</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>188.166.247.13</td><td>3128</td><td>SG</td><td>Singapore</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>91.185.236.136</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>58.115.108.196</td><td>80</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>115.124.65.34</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>187.18.123.47</td><td>3128</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>173.238.53.47</td><td>3128</td><td>CA</td><td>Canada</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>132.255.73.14</td><td>3128</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>138.0.89.106</td><td>8080</td><td>CO</td><td>Colombia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>1.179.185.249</td><td>8080</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>195.5.109.243</td><td>8080</td><td>UA</td><td>Ukraine</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>202.51.118.164</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>181.112.216.122</td><td>8080</td><td>EC</td><td>Ecuador</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>203.153.214.186</td><td>80</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>178.135.62.4</td><td>8080</td><td>LB</td><td>Lebanon</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>103.7.248.182</td><td>8080</td><td>BD</td><td>Bangladesh</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>89.28.121.179</td><td>8080</td><td>MD</td><td>Moldova, Republic of</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>74.208.205.217</td><td>3128</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>189.126.49.98</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>186.250.96.1</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 33 minutes ago</td></tr>
<tr><td>1.179.134.110</td><td>3128</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>175.103.42.98</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>103.27.67.2</td><td>8080</td><td>VN</td><td>Vietnam</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>200.192.248.74</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>201.219.121.94</td><td>8080</td><td>CO</td><td>Colombia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>103.25.179.12</td><td>8080</td><td>PH</td><td>Philippines</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>36.83.250.130</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>202.134.6.227</td><td>9999</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 35 minutes ago</td></tr>
<tr><td>114.4.9.55</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>86.107.110.120</td><td>8000</td><td>RO</td><td>Romania</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.37.27.31</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>74.208.184.125</td><td>3128</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>201.242.136.25</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>186.92.185.248</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>50.18.210.251</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>62.163.129.14</td><td>80</td><td>NL</td><td>Netherlands</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>37.110.208.82</td><td>80</td><td>UZ</td><td>Uzbekistan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>186.94.49.12</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>78.160.161.113</td><td>8080</td><td>TR</td><td>Turkey</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>180.250.163.34</td><td>8888</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>197.96.72.54</td><td>8080</td><td>ZA</td><td>South Africa</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>179.235.64.217</td><td>12457</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>84.30.71.59</td><td>80</td><td>NL</td><td>Netherlands</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>111.252.143.248</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>37.239.46.18</td><td>80</td><td>IQ</td><td>Iraq</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>198.108.96.38</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>206.125.41.135</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>202.167.248.186</td><td>80</td><td>SG</td><td>Singapore</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>152.26.69.45</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>152.26.69.37</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>177.75.232.8</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>77.222.139.70</td><td>8080</td><td>UA</td><td>Ukraine</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>213.239.214.73</td><td>1571</td><td>DE</td><td>Germany</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>109.111.75.3</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>200.255.122.170</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>177.85.59.23</td><td>80</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>186.92.93.197</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.198.20.86</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.73.215.171</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.204.100.167</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>52.26.154.81</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>186.93.96.201</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>73.155.26.120</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>177.73.72.208</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.205.22.66</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>167.114.98.162</td><td>80</td><td>CA</td><td>Canada</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>114.26.9.134</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>111.252.141.102</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>36.235.40.122</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>202.43.190.11</td><td>8118</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>50.62.134.171</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>92.222.237.95</td><td>8888</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>92.222.237.106</td><td>8888</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>36.83.103.49</td><td>80</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>36.234.81.17</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>41.205.9.92</td><td>8888</td><td>CM</td><td>Cameroon</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.140.172.202</td><td>3128</td><td>PA</td><td>Panama</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>124.122.46.128</td><td>8888</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>77.245.110.213</td><td>8080</td><td>KZ</td><td>Kazakhstan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>198.2.202.45</td><td>8090</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>190.94.221.93</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>128.199.158.186</td><td>8080</td><td>SG</td><td>Singapore</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>186.92.184.214</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>101.99.18.238</td><td>8080</td><td>VN</td><td>Vietnam</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>152.26.69.30</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>181.111.177.115</td><td>8080</td><td>AR</td><td>Argentina</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>27.122.12.45</td><td>3128</td><td>HK</td><td>Hong Kong</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>152.26.69.40</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>91.227.121.11</td><td>8888</td><td>MD</td><td>Moldova, Republic of</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>36.235.42.242</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>2 hours 36 minutes ago</td></tr>
<tr><td>14.139.213.181</td><td>3128</td><td>IN</td><td>India</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 40 minutes ago</td></tr>
<tr><td>118.170.36.107</td><td>8888</td><td>TW</td><td>Taiwan</td><td>anonymous</td><td>no</td><td>yes</td><td>2 hours 40 minutes ago</td></tr>
<tr><td>121.88.249.30</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>anonymous</td><td>no</td><td>no</td><td>2 hours 40 minutes ago</td></tr>
<tr><td>46.137.177.213</td><td>80</td><td>IE</td><td>Ireland</td><td>elite proxy</td><td>no</td><td>no</td><td>2 hours 50 minutes ago</td></tr>
<tr><td>162.13.46.94</td><td>10000</td><td>GB</td><td>United Kingdom</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 hours ago</td></tr>
<tr><td>82.200.81.233</td><td>80</td><td>RU</td><td>Russian Federation</td><td>anonymous</td><td>no</td><td>no</td><td>3 hours ago</td></tr>
<tr><td>89.249.207.65</td><td>3128</td><td>AM</td><td>Armenia</td><td>anonymous</td><td>no</td><td>no</td><td>3 hours 10 minutes ago</td></tr>
<tr><td>52.22.24.25</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>yes</td><td>yes</td><td>3 hours 10 minutes ago</td></tr>
<tr><td>203.174.53.94</td><td>3128</td><td>HK</td><td>Hong Kong</td><td>anonymous</td><td>yes</td><td>yes</td><td>3 hours 10 minutes ago</td></tr>
<tr><td>118.170.40.95</td><td>8888</td><td>TW</td><td>Taiwan</td><td>anonymous</td><td>yes</td><td>yes</td><td>3 hours 10 minutes ago</td></tr>
<tr><td>109.74.6.166</td><td>80</td><td>SE</td><td>Sweden</td><td>anonymous</td><td>no</td><td>no</td><td>3 hours 11 minutes ago</td></tr>
<tr><td>190.213.106.218</td><td>3128</td><td>TT</td><td>Trinidad and Tobago</td><td>elite proxy</td><td>no</td><td>no</td><td>3 hours 20 minutes ago</td></tr>
<tr><td>201.54.5.115</td><td>8080</td><td>BR</td><td>Brazil</td><td>anonymous</td><td>no</td><td>yes</td><td>3 hours 21 minutes ago</td></tr>
<tr><td>5.141.9.86</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 hours 21 minutes ago</td></tr>
<tr><td>54.146.151.194</td><td>8000</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>no</td><td>3 hours 22 minutes ago</td></tr>
<tr><td>186.91.176.154</td><td>8080</td><td>VE</td><td>Venezuela</td><td>transparent</td><td>no</td><td>no</td><td>3 hours 22 minutes ago</td></tr>
<tr><td>61.38.252.15</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 hours 41 minutes ago</td></tr>
<tr><td>181.112.228.71</td><td>80</td><td>EC</td><td>Ecuador</td><td>anonymous</td><td>no</td><td>no</td><td>3 hours 41 minutes ago</td></tr>
<tr><td>183.111.169.204</td><td>3128</td><td>KR</td><td>Korea, Republic of</td><td>elite proxy</td><td>yes</td><td>yes</td><td>3 hours 41 minutes ago</td></tr>
<tr><td>125.212.37.72</td><td>3128</td><td>PH</td><td>Philippines</td><td>anonymous</td><td>no</td><td>no</td><td>3 hours 41 minutes ago</td></tr>
<tr><td>31.7.232.102</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>3 hours 50 minutes ago</td></tr>
<tr><td>37.123.113.3</td><td>80</td><td>GB</td><td>United Kingdom</td><td>transparent</td><td>no</td><td>no</td><td>3 hours 51 minutes ago</td></tr>
<tr><td>31.15.48.12</td><td>80</td><td>SE</td><td>Sweden</td><td>anonymous</td><td>no</td><td>yes</td><td>4 hours ago</td></tr>
<tr><td>52.26.96.247</td><td>80</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>no</td><td>4 hours 10 minutes ago</td></tr>
<tr><td>185.74.229.153</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>no</td><td>4 hours 10 minutes ago</td></tr>
<tr><td>176.56.24.221</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>no</td><td>4 hours 10 minutes ago</td></tr>
<tr><td>52.74.204.171</td><td>80</td><td>SG</td><td>Singapore</td><td>elite proxy</td><td>no</td><td>yes</td><td>4 hours 11 minutes ago</td></tr>
<tr><td>77.241.17.112</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>elite proxy</td><td>no</td><td>yes</td><td>4 hours 30 minutes ago</td></tr>
<tr><td>104.155.12.236</td><td>8888</td><td>US</td><td>United States</td><td>elite proxy</td><td>no</td><td>yes</td><td>4 hours 41 minutes ago</td></tr>
<tr><td>14.139.213.183</td><td>3128</td><td>IN</td><td>India</td><td>anonymous</td><td>no</td><td>no</td><td>4 hours 41 minutes ago</td></tr>
<tr><td>112.203.202.10</td><td>80</td><td>PH</td><td>Philippines</td><td>elite proxy</td><td>no</td><td>no</td><td>4 hours 41 minutes ago</td></tr>
<tr><td>81.84.254.44</td><td>8080</td><td>PT</td><td>Portugal</td><td>anonymous</td><td>yes</td><td>yes</td><td>4 hours 51 minutes ago</td></tr>
<tr><td>52.25.241.52</td><td>80</td><td>US</td><td>United States</td><td>anonymous</td><td>no</td><td>no</td><td>4 hours 51 minutes ago</td></tr>
<tr><td>118.170.34.235</td><td>8888</td><td>TW</td><td>Taiwan</td><td>transparent</td><td>no</td><td>no</td><td>5 hours ago</td></tr>
<tr><td>176.31.111.139</td><td>80</td><td>FR</td><td>France</td><td>transparent</td><td>no</td><td>no</td><td>5 hours ago</td></tr>
<tr><td>77.245.70.109</td><td>3128</td><td>GB</td><td>United Kingdom</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>52.88.81.13</td><td>3128</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>176.227.202.163</td><td>3128</td><td>GB</td><td>United Kingdom</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>198.56.241.194</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>201.55.163.75</td><td>80</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>5.133.13.90</td><td>3128</td><td>PL</td><td>Poland</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>93.123.236.237</td><td>3128</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 2 minutes ago</td></tr>
<tr><td>217.175.34.170</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>76.12.101.212</td><td>3128</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>200.192.252.130</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>91.238.29.192</td><td>9999</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>169.232.101.57</td><td>80</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>202.182.51.138</td><td>80</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>180.183.53.32</td><td>8080</td><td>TH</td><td>Thailand</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>177.74.191.225</td><td>8080</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>177.135.180.180</td><td>3128</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 3 minutes ago</td></tr>
<tr><td>210.1.81.52</td><td>80</td><td>PH</td><td>Philippines</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>146.185.153.200</td><td>3128</td><td>NL</td><td>Netherlands</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>31.28.7.155</td><td>8080</td><td>RU</td><td>Russian Federation</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>104.236.118.56</td><td>3128</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>110.232.95.38</td><td>8080</td><td>ID</td><td>Indonesia</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>47.88.28.47</td><td>3128</td><td>CA</td><td>Canada</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>85.187.115.179</td><td>8080</td><td>BG</td><td>Bulgaria</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>146.255.78.254</td><td>8080</td><td>MK</td><td>Macedonia</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>210.101.131.232</td><td>8080</td><td>KR</td><td>Korea, Republic of</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>159.203.244.73</td><td>8080</td><td>US</td><td>United States</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>189.91.0.24</td><td>3128</td><td>BR</td><td>Brazil</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 6 minutes ago</td></tr>
<tr><td>119.15.94.66</td><td>8080</td><td>KH</td><td>Cambodia</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 7 minutes ago</td></tr>
<tr><td>176.227.202.167</td><td>3128</td><td>GB</td><td>United Kingdom</td><td>transparent</td><td>no</td><td>no</td><td>5 hours 7 minutes ago</td></tr>
</tbody>
"""


class ProxyStream(IOStream):
    def connect(self, address, callback=None, server_hostname=None, timeout=None):
        """
        添加timeout...
        """
        if timeout:
            self.io_loop.add_timeout(timedelta(seconds=timeout), self.handle_timeout)

        super(ProxyStream, self).connect(address, callback, server_hostname)

    def handle_timeout(self):
        self.close()


class FetchProxy(object):
    PROXY_SITE = [
        ('http://free-proxy-list.net/', '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\<\/td\><td\>(\d{2,5})\<\/td\>'),
    ]

    HOST_PORT_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0',
        'Referer': 'https://www.google.com.hk/',
    }

    TEST_URL = 'http://www.baidu.com'
    TIME_OUT = 1

    def __init__(self, url, host_reg=''):
        self.url = url
        self.proxy_reg = host_reg or self.HOST_PORT_PATTERN

    def _fetch_site_by_requests(self, url):
        try:
            r = requests.get(url, headers=self.HEADERS)

            if not r.ok:
                return

            return r.content
        except Exception as e:
            print e.message

    def fetch_proxy(self):
        #  content = self._fetch_site_by_requests(url)
        #  print 'content:', content
        content = CONTENT

        proxies = re.findall(self.proxy_reg, content, re.I)
        print 'to be priority test proxies: %s' % proxies
        print 'to be priority test proxies: %d' % len(proxies)

        for p in proxies:
            proxy = 'http://%s:%s' % p if isinstance(p, tuple) else 'http://%s' % p
            print 'test_proxy:', proxy
            self.test_proxy(proxy)

    #  @staticmethod
    #  def chunks(l, n):
        #  for i in xrange(0, len(l), n):
            #  yield l[i:i+n]

    def test_proxy(self, proxy):
        ip, port = urlparse.urlparse(proxy).netloc.split(':')

        url = self.TEST_URL
        host = urlparse.urlparse(url).netloc

        def tunnel():
            def read_remote_stream(_):
                remote_stream.close()
                print 'proxy: %s - %d' % (proxy, int((time.time() - _start) * 100))
                #  rq.put(proxy)

            remote_stream.read_until_close(streaming_callback=read_remote_stream)
            remote_stream.write("GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (url, host))

            _start = time.time()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        print sock

        #  remote_stream = ProxyStream(sock)
        #  remote_stream.connect((ip, int(port)), tunnel, timeout=2)
        remote_stream = IOStream(sock)
        remote_stream.connect((ip, int(port)), tunnel)


if __name__ == '__main__':
    for url in FetchProxy.PROXY_SITE:
        FetchProxy(*url).fetch_proxy()

    import tornado.ioloop
    tornado.ioloop.IOLoop.current().start()

# def rq_clear_proxy():
#     rq.clear()
#
#
# def rq_get_proxy():
#     if rq.empty():
#         proxies = NobodyProxy.get_all()
#
#         for proxy in proxies:
#             rq.put(proxy)
#
#     return rq.get_nowait()
