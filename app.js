

/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , swig = require('swig');

var app = module.exports = express.createServer();

// Configuration
app.register(".html",swig);

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'html');
  app.set('view options', {layout: false});
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(__dirname + '/public'));
});
swig.init({ 
        root: __dirname + '/views',
        allowErrors: true
});
app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
});

app.configure('production', function(){
  app.use(express.errorHandler());
});

// Routes
app.get('/',routes.index);

app.listen(3000, function(){
  console.log("Express server listening on port %d in %s mode", app.address().port, app.settings.env);
});
