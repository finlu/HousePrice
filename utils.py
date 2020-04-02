import base64
from io import BytesIO
from fontTools.ttLib import TTFont


def decrypt_text(getText, bs64_str):
    '''
    :param getText: 要转码的字符串
    :param bs64_str:  转码格式
    :return: 转码后的字符串
    '''
    font = TTFont(BytesIO(base64.decodebytes(bs64_str.encode())))
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap
    ret_list = []
    for char in getText:
        decode_num = ord(char)
        if decode_num in c:
            num = c[decode_num]
            num = int(num[-2:]) - 1
            ret_list.append(num)
        else:
            ret_list.append(char)
    ret_str_show = ''
    for num in ret_list:
        ret_str_show += str(num)
    return ret_str_show


if __name__ == '__main__':
    print(decrypt_text('麣餼'))

    # 加密    解密     实际
    # 龒閏 ->  04  ->  15
    # 鑶龒 ->  70  ->  40
    # 麣麣 ->  11  ->  22
    # 麣餼 ->  13  ->  13
