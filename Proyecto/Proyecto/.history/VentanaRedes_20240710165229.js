function openInNewTab(url) {
    var width = 600;
    var height = 400;
    var left = (screen.width - width) / 2;
    var top = (screen.height - height) / 2;

    window.open(url, '_blank', `toolbar=yes,scrollbars=yes,resizable=yes,top=${top},left=${left},width=${width},height=${height}`);
}