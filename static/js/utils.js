$(initializeClipboard);
$(initializePDF);

window.onload = hideQueryInURL;

function hideAlert(){
    $("#alert-message").fadeOut(1000);
}

var clipboard;
var doc;

function initializeClipboard(){
    clipboard = new ClipboardJS('.copybtn');
}

function initializePDF(){
    doc = new jsPDF();
}

function showCopied(){
    clipboard.on('success', function(e) {
        var tool = document.getElementById('tooltipid');
        tool.setAttribute('data-tip', 'Copied');
        setTimeout(function(){
            tool.setAttribute('data-tip', 'Copy to Clipboard');
        }, 1000);
    });
}


function downloadAsText(){
    var textcontent = document.getElementById("maintextarea").value;
    var downloadableLink = document.createElement('a');
    downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textcontent));
    downloadableLink.download = "decoded_text" + ".txt";
    document.body.appendChild(downloadableLink);
    downloadableLink.click();
    document.body.removeChild(downloadableLink);
}

function downloadAsPDF(){
    var textcontent = document.getElementById("maintextarea").value;
    
    doc.text(textcontent, 20, 20);
    doc.save("decoded_text.pdf");
}

function goBack(){
    location.href = location.origin;
}

function hideQueryInURL(){
    window.history.pushState('', '', location.origin);
}