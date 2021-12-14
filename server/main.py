import webview
from server import server

if __name__ == '__main__':
    window = webview.create_window('SHALF', server)
    webview.start(debug=False)