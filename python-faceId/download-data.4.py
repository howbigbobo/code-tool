import requests
import zipfile
import io

link_list = [
    "http://vap.aau.dk/wp-content/uploads/VAPRBGD/(2012-05-18)(151650).zip"]

print(len(link_list))

for link in link_list:
    print("downloading....{}".format(link))
    r = requests.get(link, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("faceid_train")
    print("extracted....{}".format(link))

# for link in val_list:
#     print("downloading....{}".format(link))
#     r = requests.get(link, stream=True)
#     z = zipfile.ZipFile(io.BytesIO(r.content))
#     z.extractall("faceid_val")
#     print("extracted....{}".format(link))
