import requests,os

a=requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest").json()
for i in a["assets"]:
    if i["name"].endswith("linux-amd64.deb") and "extended" in i["name"]:
        package_url=i["browser_download_url"]

# print("wget -O ${{ runner.temp }}/hugo.deb "+package_url)
os.system("wget -O hugo.deb "+package_url)