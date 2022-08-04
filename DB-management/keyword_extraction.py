"""
새로운 태깅 모델을 사용해 DB의 태그를 모두 수정할 때 사용

1. 기존 DB의 tag 데이터를 모두 삭제
2. 태그 모델에서 각 노래에 대한 태그를 추출 후 새로 저장

"""
import os
import requests
from tqdm import tqdm
import json
from utils import get_lyric_by_musicDB,get_all_music_id_list
from utils import save_tag_list_in_db
from utils import init_tag_table_in_db
from utils import is_in_korean
from google.cloud import translate_v2 as translate

assert os.environ.get("DB_HOST") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_USER") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_NAME") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_PASSWORD") is not None, "should register DB account in environment variables."


host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USER")
db = os.environ.get("DB_NAME")
password = os.environ.get("DB_PASSWORD")

print("init tag table..")
init_tag_table_in_db(host,user,db,password)
print("init tag table finish.")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./translate-key.json"
translator=translate.Client()

print("start extraction tag by music id..")
all_music_id_list = get_all_music_id_list(host,user,db,password)
tag_dict={}
for music_id in tqdm(all_music_id_list):
    lyric = get_lyric_by_musicDB(music_id,host,user,db,password)
    if not is_in_korean(lyric):
      lyric = translator.translate(lyric,target_language="ko")['translatedText']
    params = {"musicLyric":lyric}
    tag_list = requests.post(f"http://10.1.3.111:5000/music/tag/extraction",json=params).json()['tagList']
    tag_dict[music_id]=tag_list
    save_tag_list_in_db(tag_list,music_id,host,user,db,password)

with open("./tag_dict.json","w") as f:
    json.dump(tag_dict,f)
print("tag dict is saved in ./tag_dict.json")

print("No keyword list :")
for k,v in tag_dict.items():
    if len(v)==0:
        print("\t music id : ",k)