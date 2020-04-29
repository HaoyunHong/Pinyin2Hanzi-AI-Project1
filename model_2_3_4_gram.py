import settings


class Model234Gram(object):
    def __init__(self, input_dir, output_dir):
        # 对模型中的权重赋值，权重是根据调参文件得到的
        # 因为浮点数精度问题所以有的数值有很多位
        self.num = 8
        self.a = 0.0001
        self.b = 1
        self.c = 1.5
        self.d = 1.5
        self.e = 1.5

        # 导入矩阵

        # 单个拼音转汉字的概率
        self.pinyin2hanzi_matrix = settings.load_obj(settings.PINYIN_HANZI_DIR, "new_pinyin2hanzi_freq.dat")

        # 连续文本中单个汉字转汉字的概率
        self.two_gram_continuous_matrix = settings.load_obj(settings.COUNT_DIR, "new_2_gram_continuous_freq_matrix.dat")

        # 2元词语中单个汉字转汉字的概率
        self.two_gram_matrix = settings.load_obj(settings.COUNT_DIR, "new_2_gram_freq_matrix.dat")

        # 3元词语中前两个汉字转移到第三个汉字的概率
        self.three_gram_matrix = settings.load_obj(settings.COUNT_DIR, "new_3_gram_freq_matrix.dat")

        # 4元词语中前三个汉字转移到第四个汉字的概率
        self.four_gram_matrix = settings.load_obj(settings.COUNT_DIR, "new_4_gram_freq_matrix.dat")

        # 输入文件文件夹
        self.__input_dir = input_dir
        # 输出文件文件夹
        self.__output_dir = output_dir

        # 记录全句概率，初始化
        self.prob = {}
        for i in range(self.num):
            self.prob[i] = 1
        # 记录选择的汉字，初始化
        self.seq = {}
        for i in range(self.num):
            self.seq[i] = ''

    # 把前(n-1)元的字符串项更新
    def __update_results(self, value_list, pair_list):
        # 更新概率和汉字序列
        for index in range(self.num):
            try:
                self.prob[index] = value_list[index]
                length = len(self.seq[index])
                # 先抛弃末尾字符
                self.seq[index] = self.seq[index][:length - 3]
                self.seq[index] += pair_list[index]
            except IndexError:
                continue

    # 2+3+4元字模型
    def __two_three_four_gram_translator(self, phones):
        for i, phone in enumerate(phones):
            # 为首音节时，选取候选的num个汉字
            if i == 0:
                candidates = self.pinyin2hanzi_matrix[phone]
                top_candidates_char = sorted(candidates.keys(), key=lambda x: candidates[x], reverse=True)[:self.num]
                top_candidates_value = sorted(candidates.values(), key=lambda x: x, reverse=True)[:self.num]
                for index in range(self.num):
                    try:
                        self.prob[index] = top_candidates_value[index]
                        self.seq[index] = top_candidates_char[index]
                    except IndexError:
                        continue
            elif i == 1:
                # 由拼音转移到汉字的概率
                candidates = self.pinyin2hanzi_matrix[phone]
                pair_prob = {}
                for index in range(self.num):
                    # 计算每个候选汉字的概率
                    for k, v in candidates.items():
                        pair = self.seq[index][i - 1] + k
                        pair_prob[pair] = self.prob[index] * (
                                self.a * v + self.b * self.two_gram_continuous_matrix[self.seq[index][i - 1]][k]
                                + self.c * self.two_gram_matrix[self.seq[index][i - 1]][k])
                # 文本的连续两字间转移的概率
                top_candidates_char = sorted(pair_prob.keys(), key=lambda x: pair_prob[x], reverse=True)[:self.num]
                top_candidates_value = sorted(pair_prob.values(), key=lambda x: x, reverse=True)[:self.num]
                # 更新概率和汉字序列
                for index in range(self.num):
                    try:
                        self.prob[index] = top_candidates_value[index]
                        length = len(self.seq[index])
                        # 先抛弃末尾字符
                        self.seq[index] = self.seq[index][:length - 1]
                        self.seq[index] += top_candidates_char[index]
                    except IndexError:
                        continue
            elif i == 2:
                # 由拼音转移到汉字的概率
                candidates = self.pinyin2hanzi_matrix[phone]
                pair_prob = {}
                for index in range(self.num):
                    try:
                        # 计算每个候选汉字的概率
                        for k, v in candidates.items():
                            pair = self.seq[index][i - 2] + self.seq[index][i - 1] + k
                            pair_prob[pair] = self.prob[index] * (
                                    self.a * v + self.b * self.two_gram_continuous_matrix[self.seq[index][i - 1]][k]
                                    + self.c * self.two_gram_matrix[self.seq[index][i - 1]][k]
                                    + self.d *
                                    self.three_gram_matrix[self.seq[index][i - 2] + self.seq[index][i - 1]][k])
                    except IndexError:
                        continue
                # 文本的连续两字间转移的概率
                top_candidates_char = sorted(pair_prob.keys(), key=lambda x: pair_prob[x], reverse=True)[:self.num]
                top_candidates_value = sorted(pair_prob.values(), key=lambda x: x, reverse=True)[:self.num]
                # 更新概率和汉字序列
                # 更新概率和汉字序列
                for index in range(self.num):
                    try:
                        self.prob[index] = top_candidates_value[index]
                        length = len(self.seq[index])
                        # 先抛弃末尾字符
                        self.seq[index] = self.seq[index][:length - 2]
                        self.seq[index] += top_candidates_char[index]
                    except IndexError:
                        continue
            else:
                # 由拼音转移到汉字的概率
                candidates = self.pinyin2hanzi_matrix[phone]
                pair_prob = {}
                for index in range(self.num):
                    try:
                        # 计算每个候选汉字的概率
                        for k, v in candidates.items():
                            pair = self.seq[index][i - 3] + self.seq[index][i - 2] + self.seq[index][i - 1] + k
                            pair_prob[pair] = self.prob[index] * (
                                    self.a * v + self.b * self.two_gram_continuous_matrix[self.seq[index][i - 1]][k]
                                    + self.c * self.two_gram_matrix[self.seq[index][i - 1]][k]
                                    + self.d *
                                    self.three_gram_matrix[self.seq[index][i - 2] + self.seq[index][i - 1]][
                                        k]
                                    + self.e * self.four_gram_matrix[
                                        self.seq[index][i - 3] + self.seq[index][i - 2] + self.seq[index][i - 1]][
                                        k])
                    except IndexError:
                        continue
                # 文本的连续两字间转移的概率
                top_candidates_char = sorted(pair_prob.keys(), key=lambda x: pair_prob[x], reverse=True)[:self.num]
                top_candidates_value = sorted(pair_prob.values(), key=lambda x: x, reverse=True)[:self.num]
                # 更新概率和汉字序列
                self.__update_results(top_candidates_value, top_candidates_char)
        # 这是num个候选句子，选前5个输出
        # 这是最终概率最大的句子
        self.__store_output(self.seq[0])
        return self.seq

    def translate(self):
        f = open(self.__input_dir, 'r')
        input_list = f.read().split('\n')
        f.close()

        for i, line in enumerate(input_list):
            line = line.strip()
            line = line.lower()
            phones = line.split()
            # 只对一个字及以上的拼音转换有效
            if len(phones) < 1:
                continue
            # 用模型获得的概率最大的句子作为答案
            output_seq = self.__two_three_four_gram_translator(phones)
            print(phones)
            print(output_seq[0])

    def __store_output(self, line):
        with open(self.__output_dir, 'a') as f:
            f.write(line + '\n')
