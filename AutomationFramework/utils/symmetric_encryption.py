from jose import jwe


class SymmetricEncryption:
    """
    用于数据加解密，使用"python-jose[cryptography]"进行处理
    """
    def __init__(self):
        # 固定的对称密钥，转为byte类型
        self.key = b"f49e1029549bac0b4f1d9ed7b9de5135"

    def encrypt(self, text, alg="A256KW", enc="A256CBC-HS512"):
        """
        数据加密
        :param text:str类型字符串，处理过程中会处理为byte
        :param alg: 加密密钥算法
        :param enc:加密模式
        :return:已加密的数据
        """
        return jwe.encrypt(text.encode(), self.key, algorithm=alg, encryption=enc)

    def decrypt(self, encrypted_text):
        """
        数据解密
        :param encrypted_text: 加密后的字符串
        :return: 解密后的字符串
        """
        decrypted_text = jwe.decrypt(encrypted_text, self.key)
        return decrypted_text.decode()

