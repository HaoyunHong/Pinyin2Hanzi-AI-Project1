import sys
from model_2_3_4_gram import Model234Gram

if __name__ == "__main__":
    # 调用2+3+4元字模型进行转换
    model = Model234Gram(sys.argv[1], sys.argv[2])
    model.translate()