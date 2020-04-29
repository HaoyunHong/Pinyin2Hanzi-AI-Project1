import pickle
from os.path import join

SINANEWS_DIR = "./sina_news_gbk/"
THUNEWS_DIR = "./thu_news/"
PURECORPUS_DIR = "./pure_corpus/"
COUNT_DIR = "./counts/"
WORDS_DIR = "./n_gram_words/"
HANZI_DIR = "./hanzi_pinyin/hanzi.txt"
PINYIN_TO_HANZI_DIR = "./hanzi_pinyin/pinyin2hanzi.txt"
PINYIN_HANZI_DIR = "./hanzi_pinyin/"
DATA_DIR = "./data/"
EVALUATION = "./evaluation/"
BAIKE_DIR = "./baike_qa/"
WEB_DIR = "./webtext2019zh/"

# 用tuple会更加安全

# 处理文本
stop_list = (',', '，', '。', ".", "‘", "’", '“', '”', "：", "；", "（", "）", "、", "！", "？", "……",
             "《", "》", "——", "【", "】", "[", "]", "{", "}", "#", "￥", "%", "&", "*", "-", "+", "=", "·", "~", "|", "/")
number_list = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
number_dict = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}

# 题给语料序号
index_list = ('02', '04', '05', '06', '07', '08', '09', '10', '11')

# 全体语料类别
corpus_name_list = tuple("sinanews_{}".format(index) for index in index_list) + ("thunews",)
baike_name_list = ("baike_qa_valid",)
web_name_list = ("web_text_zh_test", "web_text_zh_valid")
more_corpus_name_list = ("more_1", "more_2", "more_3")


# 以二进制保存对象
def store_obj(dir, fname, obj):
    f = open(join(dir, fname), 'wb')
    pickle.dump(obj, f)
    f.close()


# 以读取存储的对象
def load_obj(dir, fname):
    f = open(join(dir, fname), 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
