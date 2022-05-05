![GitHub language count](https://img.shields.io/github/languages/count/amarjin6/proxy-server?logo=python&logoColor=green)
![GitHub repo size](https://img.shields.io/github/repo-size/amarjin6/proxy-server?color=yellow&logo=gitbook)
![GitHub commit merge status](https://img.shields.io/github/commit-status/amarjin6/proxy-server/master/3889565181dc7a5634295efdc7cfb1aa111ee332?color=purple&logo=pypi)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/amarjin6/proxy-server?color=gree&logo=Stackbit&logoColor=orange)
![GitHub watchers](https://img.shields.io/github/watchers/amarjin6/proxy-server?logo=wechat)

# TCP proxy server logging HTTP requests 🎲

## 💡**Main idea**💡
Needed to implement a simple proxy server that logs proxied HTTP requests with the help of sockets API. The program should run as a service and display brief information about proxied requests (URL and response code) as a log.

## 📰**How it works**📰
In computer networks, A proxy server is a server ( A computer system or an application ) that acts as an intermediary for requests from clients seeking resources from other servers. A client connects to the proxy server, requesting some service, such as a file, connection, web page, or other resource available from a different server and the proxy server evaluates the request as a way to simplify and control its complexity. Proxies were invented to add structure and encapsulation to distributed
systems. Today, most proxies are web proxies, facilitating access to content on the World Wide Web and providing anonymity.

What Bob thinks is the server ( i.e the proxy ) asked for the current time, But what Bob didn't know was, Alice asked for the current time but through the proxy server. The proxy server returns the current time to Alice. So we can basically say, Server Bob has been tricked. The proxy server acts as a man in the middle serving two people without revealing their identities to each other, Each person sees only the proxy but not the other end.

## ⚒️**How to Run**⚒️
* **Clone project to your folder:** `git clone https://github.com/amarjin6/proxy-server.git`
* **Check for updates and install all necessary [plugins](https://github.com/amarjin6/proxy-server/tree/master/requirements)**
* **Run project in terminal:** `python proxy.py`
* **Don't forget to turn on [PROXY](https://www.ibm.com/docs/sk/odmoc?topic=services-connecting-proxy-server) on your OS**🔌

## 🥽**Preview**🥽

# Python Socket Proxy