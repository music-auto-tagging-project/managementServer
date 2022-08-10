import pymysql
from pymysql.constants import CLIENT

def get_tag_has_music_in_db(host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    with db:
        with db.cursor() as cursor:
            sql = """
                select * from tag_has_music;
                """
            cursor.execute(sql)

            tag_has_music_list = cursor.fetchall()

    return tag_has_music_list


def get_music_tag_list(host,user,db,password):
    db = pymysql.connect(host=host,user=user,db=db,password=password,charset='utf8',client_flag=CLIENT.MULTI_STATEMENTS)
    music_tag_list={}
    get_tag_id_sql = "select id from tag"
    get_music_id_by_tag_id_sql = "select music_id,tag_rank from tag_has_music where tag_id=%s"
    with db:
        with db.cursor() as cursor:
            cursor.execute(get_tag_id_sql)
            tag_id_list = [tag_id[0] for tag_id in cursor.fetchall()]

            for tag_id in tag_id_list:
                cursor.execute(get_music_id_by_tag_id_sql,(tag_id))
                music_id_list = [(music_id,rank) for music_id,rank in cursor.fetchall()]

                music_tag_list[tag_id] = music_id_list

    return music_tag_list