var pings = 0;
var pingback;

function pingTractorServer()
{
    $.post("/moveForward/",
           {
               html: "Pingback...",
               delay: 1
           },
          function(data, status)
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
$.post("/echo/html/",
       {
           html: "OK! Forward",
           delay: 1
       },
       function(data, status){
           $("#serverresponse").text(data)
       })
});

$("#forwardleft").click(function () {
$.post("/echo/html/",
       {
           html: "OK! Forward Left",
           delay: 1
       },
       function(data, status){
           $("#serverresponse").text(data)
       })
});

$("#forwardright").click(function () {
$.post("/echo/html/",
       {
           html: "OK! Forward Right",
           delay: 1
       },
       function(data, status){
           $("#serverresponse").text(data)
       })
});
});
