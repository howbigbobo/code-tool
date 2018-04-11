var express = require('express'),
    serveIndex = require('serve-index'), //只能列表目录，不能下载文件？  
    serveStatic = require('serve-static'),
    fs = require('fs');
var https = require('https');
var config = JSON.parse(fs.readFileSync("./config.json"));
/* 
$ brew install node@8.4.0 
不使用package.json的依赖安装方法：以全局模式（-g）安装npm依赖，然后npm link命令创建符号链接 
$ npm install express -g 
$ npm link express 
*/

var LOCAL_BIND_PORT = config.port; //express's port  

var app = express();
app.set('x-powered-by', false);
app.set('strict routing', true); //路径/a与/a/是不一样的（但是/a/*需要单独指出吗？）  
app.set('trust proxy', true); //与Nginx反向代理配合使用？  

//Trick:  
app.getOrPost = function (urlPattern, callback) {
    app.get(urlPattern, callback);
    app.post(urlPattern, callback);
};

var REQUEST_GLOBAL_NUM = 1;
app.use(function requestNumbering(req, res, next) {
    req.request_id = REQUEST_GLOBAL_NUM++; //for dump data file naming;  
    next();
});

app.use(function addServerSideIPAddress(req, res, next) {//log输出req.headers，FIXME：怎么log输出最终的res.headers？  
    //console.log("["+req.request_id+"] logReqHeaders: req.ip=" + req.ip+" req.socket.localAddress="+req.socket.localAddress);  
    //req.socketLocalIPv4Address = req.socket.localAddress.replace("::ffff:","").replace("::1","127.0.0.1")  
    //dirty hack to fix OS IPv6-first to use IPv4 address only  
    console.log("[" + req.request_id + "] req.headers: " + JSON.stringify(req.headers, null, 2));
    next();
});

//目录列表及静态文件下载  
app.get("/", function (req, res) {
    // res.redirect(302, "/f"); //test direct;  
    var catalogs = [];
    config.serveDirs.forEach(function (sd) {
        catalogs.push(`<li style="padding:10px;"><a href="${sd.path}">${sd.name}</a></li>`)
    });
    var catalogStr = catalogs.join(" ");
    var html = `<html>
        <head><title>Static Server</title></head>
        <body>
            <ul>
                ${catalogStr}
            <ul>
        <body>
    </html>`;
    res.send(html);
});

config.serveDirs.forEach(function (sd) {
    app.use(sd.path, serveIndex(sd.dir, { 'icons': true })); //This is Mac OS fs path;  
    var serve = serveStatic(sd.dir);
    app.get(sd.path + '/*', function (req, res) {
        req.url = req.url.substring(sd.path.length); //跳过url中的/abc前缀，把剩余的部分映射为相对于/home/chenzx的文件路径  
        console.log("[" + req.request_id + "] GET static " + req.url);
        serve(req, res)
    });
});

console.log(`Start static file server at ::${LOCAL_BIND_PORT}, Press ^ + C to exit`);
app.listen(LOCAL_BIND_PORT);

if (config.https.enable) {
	const sslOptions = {
	  key: fs.readFileSync(config.https.key),
	  cert: fs.readFileSync(config.https.crt),
	  passphrase: 'changeit'
	};
	const server = https.createServer(sslOptions, app).listen(config.https.port);
	console.log(`Start https static file server at ::${config.https.port}, Press ^ + C to exit`);
}