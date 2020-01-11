import base64
from Crypto.Cipher import AES
import binascii
import random

#用来得到一个混乱的密码表
def get_table():
    table=[]
    for x in range(256):
        table.append(x)
    print(table)
    random.shuffle(table)
    print(table)

#将一个0x01的16进制的list转为十六进制的bytes
def hex2bytes(list):
    list_no_ox=[]
    for x in list:
        y=x.replace('0x','')
        if len(y)==1:
            y='0'+y
        list_no_ox.append(y)
    a_str=''
    for x in list_no_ox:
        a_str+=x
    return binascii.a2b_hex(a_str.encode())

#256个的密码表得到的加密字典
def get_en_table():
    en_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    en_list_ramdom = [206, 91, 7, 200, 220, 169, 55, 198, 246, 111, 79, 101, 9, 240, 40, 243, 6, 226, 52, 157, 250, 68, 13, 128, 0, 249, 89, 25, 37, 164, 99, 39, 201, 81, 242, 5, 195, 69, 135, 112, 131, 14, 160, 19, 116, 219, 33, 147, 223, 209, 238, 241, 122, 62, 152, 54, 190, 236, 108, 137, 254, 82, 212, 115, 251, 167, 80, 232, 16, 47, 60, 10, 124, 214, 149, 182, 32, 189, 12, 196, 35, 248, 183, 144, 15, 133, 177, 121, 31, 166, 151, 3, 119, 8, 255, 58, 129, 93, 230, 210, 227, 222, 162, 72, 41, 215, 86, 87, 56, 67, 88, 44, 233, 103, 213, 90, 140, 77, 185, 132, 70, 134, 106, 95, 98, 205, 11, 117, 172, 105, 75, 21, 153, 104, 216, 228, 163, 26, 92, 202, 126, 178, 102, 211, 207, 114, 118, 59, 84, 154, 43, 123, 17, 150, 244, 109, 138, 45, 218, 145, 96, 221, 74, 97, 107, 224, 148, 83, 194, 27, 66, 30, 239, 85, 125, 76, 38, 179, 191, 139, 94, 22, 142, 42, 110, 170, 48, 63, 53, 71, 113, 176, 165, 4, 245, 247, 175, 50, 34, 168, 143, 193, 141, 199, 73, 18, 155, 217, 180, 188, 225, 158, 252, 51, 127, 24, 171, 36, 100, 174, 156, 234, 20, 208, 159, 23, 2, 181, 28, 253, 229, 61, 161, 231, 136, 57, 187, 120, 204, 65, 237, 203, 146, 78, 173, 49, 235, 46, 184, 197, 29, 130, 1, 192, 64, 186]
    en_table = {}
    for k, v in enumerate(en_list):
        en_table[v] = en_list_ramdom[k]
    #print(en_table)
    return en_table

#256个的密码表得到的解密字典
def get_de_table():
    en_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    en_list_ramdom =[206, 91, 7, 200, 220, 169, 55, 198, 246, 111, 79, 101, 9, 240, 40, 243, 6, 226, 52, 157, 250, 68, 13, 128, 0, 249, 89, 25, 37, 164, 99, 39, 201, 81, 242, 5, 195, 69, 135, 112, 131, 14, 160, 19, 116, 219, 33, 147, 223, 209, 238, 241, 122, 62, 152, 54, 190, 236, 108, 137, 254, 82, 212, 115, 251, 167, 80, 232, 16, 47, 60, 10, 124, 214, 149, 182, 32, 189, 12, 196, 35, 248, 183, 144, 15, 133, 177, 121, 31, 166, 151, 3, 119, 8, 255, 58, 129, 93, 230, 210, 227, 222, 162, 72, 41, 215, 86, 87, 56, 67, 88, 44, 233, 103, 213, 90, 140, 77, 185, 132, 70, 134, 106, 95, 98, 205, 11, 117, 172, 105, 75, 21, 153, 104, 216, 228, 163, 26, 92, 202, 126, 178, 102, 211, 207, 114, 118, 59, 84, 154, 43, 123, 17, 150, 244, 109, 138, 45, 218, 145, 96, 221, 74, 97, 107, 224, 148, 83, 194, 27, 66, 30, 239, 85, 125, 76, 38, 179, 191, 139, 94, 22, 142, 42, 110, 170, 48, 63, 53, 71, 113, 176, 165, 4, 245, 247, 175, 50, 34, 168, 143, 193, 141, 199, 73, 18, 155, 217, 180, 188, 225, 158, 252, 51, 127, 24, 171, 36, 100, 174, 156, 234, 20, 208, 159, 23, 2, 181, 28, 253, 229, 61, 161, 231, 136, 57, 187, 120, 204, 65, 237, 203, 146, 78, 173, 49, 235, 46, 184, 197, 29, 130, 1, 192, 64, 186]
    de_table = {}
    for k, v in enumerate(en_list_ramdom):
        de_table[v] = en_list[k]
    #print(de_table)
    return de_table

#15个的密码表得到的加密字典
def get_en_table15():
    en_list = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    en_list_ramdom = ['d', 'f', '1', '0', '7', '4', '8', 'b', '3', 'c', 'e', '2', '5', '6', '9', 'a']
    en_table = {}
    for k, v in enumerate(en_list):
        en_table[v] = en_list_ramdom[k]
    #print(en_table)
    return en_table

#15个的密码表得到的解密字典
def get_de_table15():
    en_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    en_list_ramdom = ['d', 'f', '1', '0', '7', '4', '8', 'b', '3', 'c', 'e', '2', '5', '6', '9', 'a']
    de_table = {}
    for k, v in enumerate(en_list_ramdom):
        de_table[v] = en_list[k]
    #print(de_table)
    return de_table

# 加密方法，15位的加密
#十六进制bytes-》ascii-》字符串-》ascii
def encrypt_message(text_b,en_table):
    h=binascii.b2a_hex(text_b).decode()#将十六进制的bytes转为ascii的bytes，然后转为字符串
    #print(h)
    en_h=''
    #根据加密表替换
    for v in h:
        #print(k,v)
        en_h+=en_table[v]
    #print(en_h)
    #print(en_h)
    en_h_bytes=binascii.a2b_hex(en_h.encode())
    return en_h_bytes

# 解密方法，15位的解密
#ascii——》字符串-》ascii-》十六进制bytes
def decrypt_message(text,de_table):
    de_h=''
    #根据解密表替换
    for k,v in enumerate(binascii.b2a_hex(text).decode()):
        #print(k,v)
        de_h+=(de_table[v])
    h=de_h.encode()
    return binascii.a2b_hex(h)

#255位的加密
#十六进制bytes——》ascii->10进制字符串（替换）》ascii-》十六进制bytes
def encrypt_message_addr(text,en_table):
    list_dec=[]
    h=binascii.b2a_hex(text)#将十六进制的bytes转为ascii的bytes，然后转为字符串
    #print(h)
    x=2
    while x<=len(h.decode()):
        list_dec.append(int(h[x-2:x],16))
        x+=2
    en_list_dec=[]
    #根据加密表替换
    for v in list_dec:
        #print(k,v)
        en_list_dec.append(en_table[v])
    list_hex=[]
    for x in en_list_dec:
        list_hex.append(hex(x))
    h_bytes=hex2bytes(list_hex)
    return h_bytes

# 解密方法，255位的解密
#十六进制bytes——》ascii->10进制字符串(替换)》ascii-》十六进制bytes
def decrypt_message_addr(text,de_table):
    h_list=[]
    h_str=binascii.b2a_hex(text).decode()
    x=2
    while x<=len(h_str):
        h_list.append(h_str[x-2:x])
        x+=2
    d_list=[]
    for i in h_list:
        d_list.append(int(i,16))
    de_d_list=[]
    for v in d_list:
        de_d_list.append(de_table[v])
    h_str_list=[]
    for i in de_d_list:
        h_str_list.append(hex(i))
    h_bytes=hex2bytes(h_str_list)
    return h_bytes


glo_en_table=get_en_table()
glo_de_table=get_de_table()
glo_en_table15=get_en_table15()
glo_de_table15=get_de_table15()

if __name__ == '__main__':

    encrypt_message( b'\x15\x03\x03\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x08\xff,\xf0\x940\x14\x0c\xe2\xda*w78\x95\x82\xeb\x0c\x17',glo_en_table15)
    decrypt_message(b'\xf4\xd0\xd0\xdd\xfe\xdd\xdd\xdd\xdd\xdd\xdd\xdd\xd3\xaa\x15\xad\xc7\r\xf7\xd5\x91n\x1e\xbb\x0b\x03\xc41\x92\xd5\xfb',glo_de_table15)
    #
    encrypt_message_addr( b'\x15\x03\x03\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x08\xff,\xf0\x940\x14\x0c\xe2\xda*w78\x95\x82\xeb\x0c\x17',glo_en_table)
    decrypt_message_addr(b'D\xc8\xc8\xceY\xce\xce\xce\xce\xce\xce\xce\xf6\xbat\xedT\xdf\xfa\t\x02d\xa0\x846\xbe\x9aK9\t\x80',glo_de_table)
