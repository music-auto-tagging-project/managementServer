import pymysql
from pymysql.constants import CLIENT

def init_tag_table_in_db(host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            sql = """
                TRUNCATE TABLE tag_has_music;
                TRUNCATE TABLE user_has_tag;
                SET FOREIGN_KEY_CHECKS = 0; -- Disable foreign key checking.
                TRUNCATE TABLE tag;
                SET FOREIGN_KEY_CHECKS = 1; -- Enable foreign key checking.
                """
            cursor.execute(sql)

def get_lyric_by_musicDB(musicid,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            sql = """SELECT lyric FROM music WHERE id=%s"""
            cursor.execute(sql,(musicid))
            lyric = cursor.fetchone()[0]
    return lyric
    
def get_all_music_id_list(host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8')
    sql = "SELECT id FROM music"
    with db:
        with db.cursor() as cursor:
            cursor.execute(sql)
            all_music_id_list = [music_id[0] for music_id in cursor.fetchall()]
    return all_music_id_list

def save_tag_list_in_db(tag_list,musicid,host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            delete_prev_tag_sql = """DELETE FROM tag_has_music WHERE music_id=%s"""
            cursor.execute(delete_prev_tag_sql,(musicid))
            
            tag_has_music_insert_sql = """INSERT INTO tag_has_music(tag_id,music_id,tag_rank)
                                                VALUES((SELECT id FROM tag WHERE name=%s),%s,%s)"""
            tag_insert_sql = """INSERT IGNORE INTO tag(name) VALUES(%s)"""
            for rank,tag in enumerate(tag_list):
                cursor.execute(tag_insert_sql,(tag))
                cursor.execute(tag_has_music_insert_sql,(tag,musicid,rank+1))
        db.commit()

def is_in_korean(input_s):
  for c in input_s:
      if ord('가') <= ord(c) <= ord('힣'):
          return 1
  return 0