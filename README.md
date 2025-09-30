# filetree_dls

This unoptimized script attempts to create a filetree from a Ransomware DLS (Data Leak Site)

> [!IMPORTANT]
> Won' work if there is a Captcha

# Install dependencies

```
pip install -r requirements.txt
```

# Install and start tor (Linux only)

```
sudo apt install tor -y
```

```
# start without daemon - run in a separate terminal
tor --runasdaemon 0
```

# Edit the script with the website

```
# Set base folder for enumeration
start_url = "http://website.onion/dls"
```

# Run the script 

```
python3 extract_filetree.py
```
