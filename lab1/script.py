import requests

print("requests version:")
print(requests.__version__)

r = requests.get("https://www.google.com")
print("google:")
print(r.text)

r = requests.get("https://raw.githubusercontent.com/amohamed11/cmput-404-labs/lab1/script.py")
print("github script:")
print(r.text)
