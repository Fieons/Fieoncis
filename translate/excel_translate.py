import pandas as pd
from googletrans import Translator

# 加载Excel文件
df = pd.read_excel('/Users/smart_boy/Desktop/Ozon_Product_20230830221217.xlsx')
print('have load excel!')
# 定义翻译器
translator = Translator()

# 定义要翻译的列和目标列
translate_column = '产品名称-ru'  # 要翻译的列名
target_column = '产品名称-CN'  # 存放翻译结果的目标列名

print('translating...')
# 使用翻译器翻译每一行的英文数据，并将结果保存到新列中
df[target_column] = df[translate_column].apply(lambda x: translator.translate(x, dest='zh-CN').text)

# 保存修改后的DataFrame到新的Excel文件
df.to_excel('/Users/smart_boy/Desktop/Ozon_Product_20230830221217_translated.xlsx', index=False)
print("finish!")