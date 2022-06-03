import requests, websocket, json, contextlib, time, random, string

class Utils:
    def random_string(n=int):
        return ''.join(random.choice(string.ascii_letters) for _ in range(n))

class Email:
    def __init__(self, proxy: str= None):
        self.base_url = "https://emailtemp.org/en"
        self.giggl_email_from = "Giggl"
        self.s = requests.Session()
        self.s.proxies = {"http": proxy, "https": proxy} if proxy else None

    def get_mail(self):
        return self.s.get('https://emailtemp.org/en/messages').json()['mailbox']

    def get_verif_code(self, logs: int=False):
        a = 0
        while True:
            time.sleep(20)
            if logs:
                a += 1
                print(f'[{a}] fetching messages')
            with contextlib.suppress(Exception):
                resp = self.s.get(f'{self.base_url}/messages').json()
                for message in resp['messages']:
                        code = message['content'].split('https://u17471629.ct.sendgrid.net')[1].split('\"')[0]
                        link = f"https://u17471629.ct.sendgrid.net/{code}"
                        response = requests.get(link)
                        return response.url

class Giggl:
    def __init__(self, proxy: str= None):
        self.base_url = "https://api.giggl.app/v1"
        self.s = requests.Session()
        self.s.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.s.headers.update({'User-agent': 'Mozilla/5.0 (X11; GNU/Linux) AppleWebKit/601.1 (KHTML, like Gecko) Tesla QtCarBrowser Safari/601.1'})

    def login(self, email=None, password=None, token=None):
        global _token
        if email and password:
            payload = '{"email":"'+ email +'","password":"' + password +'"}'
            resp = self.s.post(f"{self.base_url}/auth", data=payload, headers={'Content-Type': 'application/json'}).json()
            _token = resp['token'] if resp['success'] else None
            self.s.headers.update({'authorization': _token})
            return resp
        if token:
            self.s.headers.update({'authorization': token})
            test = self.connections()['success']
            _token = token
            return {"success": test}
        else:
            return "you need a email, password or token to login"


    def register(self, email, username, password):
        payload = {'email': email, 'username': username, 'password': password}
        return self.s.post(f"{self.base_url}/auth/register", json=payload).json()['token']

    def delete_account(self):
        return self.s.delete(f"{self.base_url}/users/@me").json()

    def email_password_to_token(self, email, password):
        payload = '{"email":"'+ email +'","password":"' + password +'"}'
        resp = self.s.post(f"{self.base_url}/auth", data=payload, headers={'Content-Type': 'application/json'}).json()
        return resp['token']

    def account_information(self):
        ws = websocket.create_connection("wss://orbit.giggl.app/ws")
        ws.recv()
        ws.send('{"op":2,"data":{"token":"'+ _token +'"}}')
        result = ws.recv()
        jsonified = json.loads(result)
        ws.close()
        return jsonified

    def devices(self):
        return self.s.get(f"{self.base_url}/users/@me/devices").json()

    def delete_device(self, device):
        return self.s.delete(f"{self.base_url}/users/@me/devices/{device}")

    def connections(self):
        return self.s.get(f"{self.base_url}/users/@me/connections").json()


    def change_email(self, email):
        return self.s.patch(f'{self.base_url}/users/@me', json={'email': email}).json()

    def change_website(self, website):
        return self.s.patch(f'{self.base_url}/users/@me', json={'website': website}).json()

    def change_location(self, location):
        return self.s.patch(f'{self.base_url}/users/@me', json={'location': location}).json()

    def foryou(self, amount):
        return self.s.get(f'{self.base_url}/portals/foryou', params={"limit": f"{amount}"}).json()

    def modify_settings(self, portal_invites_notification: bool=True, friend_req_notification: bool=True, device_login_notification: bool=True, view_nsfw_portals: bool=False, mention_sound: bool=True, dms_friends_restricted: bool=False):
        payload = {
        "portal_invites_notification": portal_invites_notification,
        "friend_req_notification": friend_req_notification,
        "device_login_notification": device_login_notification,
        "view_nsfw_portals": view_nsfw_portals,
        "mention_sound": mention_sound,
        "dms_friends_restricted": dms_friends_restricted
        }
        return self.s.patch(f'{self.base_url}/users/@me/settings', json=payload, headers={'Content-Type': 'application/json'}).json()

    def search_user(self, username):
        return self.s.get(f'{self.base_url}/users/{username}').json()

    def check_email(self, email):
        return self.s.post(f'{self.base_url}/auth/email', json={"email": email}).json()

    def add_friend(self, id: int=None, username: str=None):
        if username:
            id = self.search_user(username)['data']['id']
        return self.s.post(f'{self.base_url}/relationships/@me/friend-request', json={"user_id": id}).json()

    def block_user(self, id):
        return self.s.post(f'{self.base_url}/relationships/@me/block/{id}').json()

    def unblock_user(self, id):
        return self.s.delete(f'{self.base_url}/relationships/@me/block/{id}').json()

    def send_email_verif(self):
        return self.s.post(f'{self.base_url}/emails').json()

    def verify_code(self, code):
        return self.s.post(f'{self.base_url}/emails/verify', json={"token": code}).json()

    def delete_friend(self, id: int=None, username=None):
        if username:
            id = self.search_user(username)['data']['id']
        return self.s.delete(f'{self.base_url}/relationships/@me/friends/{id}').json()

    def accept_friend(self, id: int=None, username=None):
        if username:
            id = self.search_user(username)['data']['id']
        return self.s.patch(f'{self.base_url}/relationships/@me/friends', json={"user_id": f"{id}"}).json()

    def unaccept_friend(self, id: int=None, username=None):
        if username:
            id = self.search_user(username)['data']['id']
        return self.s.delete(f'{self.base_url}/relationships/@me/friends/{id}').json()

    def userid_to_room(self, id: int=None, username=None):
        if username:
            id = self.search_user(username)['data']['id']
        return self.s.post(f'{self.base_url}/users/@me/rooms', json={"recipients":[id]}).json()

    def send_message(self, message, room_id):
        return self.s.post(f'{self.base_url}/rooms/{room_id}/messages', json={"content": f"{message}"}).json()

    def edit_message(self, room_id, message_id, new_message):
        return self.s.patch(f'{self.base_url}/rooms/{room_id}/messages/{message_id}', json={"content": f"{new_message}"}).json()

    def delete_message(self, room_id, message_id) -> None:
        return self.s.delete(f'{self.base_url}/rooms/{room_id}/messages/{message_id}').content

    def create_portal(self, name, type): # type 1 = public, type 2 = private
        payload = {
	"name": name,
	"region": "eu-west",
	"type": type,
	"vanity": False,
	"staging": False,
	"allow_dev_tools": False
}
        return self.s.post(f'{self.base_url}/portals', json=payload).json()

    def create_invite(self, portal_id):
        return self.s.post('https://gig.gl/invite', json={"portal_id": portal_id}).json()

    def portal_info(self, portal_id):
        return self.s.get(f'{self.base_url}/portals/{portal_id}').json

    def close(self) -> None:
        return self.s.close()

    def account_generator(self, username_prefix: str="gagou", logs: bool=False):
            g = Giggl()
            m = Email()
            mail = m.get_mail()
            password = Utils.random_string(16)
            username = f"{username_prefix}_{Utils.random_string(4)}"
            if logs: print("registering: ",mail, username, password)
            register = g.register(mail, username, password)
            if logs: print(register)
            if register['success'] != True:
                return register
            token = register['token']
            if logs:print("token: ",token)
            time.sleep(10)
            verif_link = m.get_verif_code(logs)
            verif_code = verif_link.split('https://canary.giggl.app/auth/verify-email/')[1].split('?code=')[1]
            verified = g.verify_code(verif_code)['success']
            if verified != True:
                return {
                "email": mail,
                "password": password,
                "username": username,
                "token": token,
                "verified": verified
            }
            return {
                "email": mail,
                "password": password,
                "username": username,
                "token": token,
                "verified": verified
            }

    def proxy_verif(self):
        return self.s.get('https://eth0.me').content

    def change_password(self, new_password, old_password):
        self.s.patch(f'{self.base_url}/users/@me', json={"new_password": new_password, "old_password": old_password})