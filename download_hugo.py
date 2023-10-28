import requests,os

b="sasd".startswith

a=requests.get("https://api.github.com/repos/gohugoio/hugo/releases/latest").json()
for i in a["assets"]:
    if i["name"].endswith("linux-amd64.deb") and "extended" in i["name"]:
        package_url=i["browser_download_url"]

os.system("wget -O ${{ runner.temp }}/hugo.deb {}".format(a))