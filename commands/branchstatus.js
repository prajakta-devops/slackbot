var request = require('request'),
	util 	= require('../util');

module.exports = function (param) {
	var	channel		= param.channel,
		endpoint	= param.commandConfig.bitbucketendpoint;
		
	request({
        url : endpoint,
        headers : {
            "Authorization" : "<add authorization>"
        }
    }, function (err, response, body) {
		var info = [];
     	var branchStatus="Unlocked"
		if (!err && response.statusCode === 200) {
			body = JSON.parse(body);
			var branchRestrictionId = null;
			branchRestrictionId = body.values.filter(function (chain) {
    									return chain.kind === 'push' && chain.pattern === param.args[0];
										})
			console.log("branch rest"+branchRestrictionId)
			if(branchRestrictionId != null && branchRestrictionId.length > 0){
				console.log("branch"+branchRestrictionId)
				branchStatus="Locked"
			}
			info.push('Branch Status: ' + branchStatus);
			
		}
		else {
			info = ['Branch not found'];
		}

		util.postMessage(channel, info.join('\n\n'));
	});

};