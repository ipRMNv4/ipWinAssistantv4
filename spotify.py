import requests
import base64
import webbrowser
import http.server
import socketserver
import schedule
import time

client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
redirect_uri = "http://localhost:8888/callback"

authorization_code = None
access_token = None

def get_authorization_url():
    url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-read-playback-state user-modify-playback-state"
    }
    return f"{url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"

def get_access_token(authorization_code):
    encoded_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    return response.json().get("access_token")

def get_token():
    global authorization_code
    webbrowser.open_new_tab(get_authorization_url())

    class RedirectHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            global authorization_code
            authorization_code = self.path.split("code=")[-1]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Authorization code received. You can close this tab.")

    with socketserver.TCPServer(("", 8888), RedirectHandler) as httpd:
        httpd.handle_request()

    return get_access_token(authorization_code)

def refresh_token():
    global access_token
    access_token = get_token()
    with open("access_token.txt", "w") as file:
        file.write(access_token)
def main():
    refresh_token()
    print("Access token:", access_token)

if __name__ == "__main__":
    main()
