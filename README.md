# yiff-dl
Download pools and comics easily from either E621 or Yiffer.xyz with this handy script!

The yifferx.xyz downloading code was found on a repo a while ago and subsequently modified by me, while the E621 download logic is brand new

<h1>Requirements</h1>
This script requires python 3.8 and above with the following packages:
```
img2pdf
BeautifulSoup
PIL
```

<h1>Usage</h1>

The script creates a directory for each comic

Normal usage:
```
python yiff-dl.py <url1> <url2> <url3>...   #As simple as that!
```
you can also supply a .txt file to batch download comics by adding -b before the .txt address:

```
python yiff-dl.py -b link.txt
```
