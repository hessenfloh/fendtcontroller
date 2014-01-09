var pings = 0;
var pingback;

function pingTractorServer()
{
    $.get("pingTractor",
	  { action: "connect" },
          function(data)
           {
               pings ++;
               $("#pingresponse").text(data + " number " + pings);
           })
}
$().ready(function() {
$("#connect").click(function () 
                    { 
                        var current = $("#connect").text();
                        if(current == "Connect")
                        {
                            $("#connect").text("Disconnect");
                            pingback=setInterval(pingTractorServer, 1500); 
                        }
                        else
                        {
                            clearInterval(pingback);
                            $("#connect").text("Connect");
                        }
                    });
$("#forward").click(function () {
$.get("moveForward",
       function(data){
           $("#serverresponse").text(data)
       })
});

$("#forwardleft").click(function () {
$.get("moveForwardLeft",
       function(data){
           $("#serverresponse").text(data)
       })
});

$("#forwardright").click(function () {
$.get("moveForwardRight",
       function(data){
           $("#serverresponse").text(data)
       })
});
$("#backward").click(function () {
$.get("moveBackward",
       function(data){
           $("#serverresponse").text(data)
       })
});

$("#backwardleft").click(function () {
$.get("moveBackwardLeft",
       function(data){
           $("#serverresponse").text(data)
       })
});

$("#backwardright").click(function () {
$.get("moveBackwardRight",
       function(data){
           $("#serverresponse").text(data)
       })
});

});
