# giggl.py

api wrapper for [giggl.app](https://giggl.app/)

i added a temp mail api wrapper for creating and verifying accounts

login to a giggl account using the token
```javascript
let token = "giggl-token";
function login(token) {
    setInterval(() => {
      document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.setItem("giggl-token", `${token}`);
    }, 50);
    setTimeout(() => {
      location.reload();
    }, 1500);
  }

login(token);
```

install:

```
pip install -U git+https://github.com/gagou78/giggl.py
```


exemple:
```py
from giggl import Giggl

giggl = Giggl(proxy='socks5://192.168.1.19:9050')

print(giggl.proxy_verif())
# login with email and password
uwu = giggl.login(email="email", password="password",)

if uwu['success']:
    print("login successful")
else:
    print("epic login fail :skull:")


# login with token
giggl.login(token="cool_secret_token")

# register a new account
giggl.register(
  email="email",
  password="password",
  username="username",)

# or register a new account and auto verify it

giggl.account_generator(username_prefix="gagou", logs=True)

print(giggl.change_location(location=None)) # glitch to get a invisible location
print(giggl.change_website(website=None)) # glitch to get a invisible website

giggl.add_friend(username="admin")

print(giggl.account_information())
```