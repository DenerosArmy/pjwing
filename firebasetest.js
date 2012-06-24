var Firebase = require('./firebase-node');
var myDataReference = new Firebase('http://gamma.firebase.com/Vaishaal/');

myDataReference.on ('child_added', function(snapshot) {
	var data = snapshot.val();
	console.log(data.url);
});

