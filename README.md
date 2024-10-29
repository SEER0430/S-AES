# S-AES
# 作业任务：根据"信息安全导论"课程第8-9次课讲述的AES算法，在课外认真阅读教科书附录D的内容，学习了解S-AES算法，使用Python+QT来编程实现加、解密程序。
# 组内成员 20220602肖浩然 20221751徐雷鸣 20221733常子昕
3.1 第1关：基本测试       根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文。
![89036de14d6d19a27796d183d149205f_](https://github.com/user-attachments/assets/fc49dbc0-8fbe-40b1-a7dd-effe1875cfcb)
![9f249ec08872433ca63e783824581ccd_](https://github.com/user-attachments/assets/e90426c1-a6ac-4ef6-ad70-b1c773ff0328)

3.2 第2关：交叉测试考虑到是"算法标准"，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行。设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。
他组案例：
![b9a66f154237b681c9ac5dfd2cbf15c](https://github.com/user-attachments/assets/6e0c814c-60c4-42ce-8170-fe535211bd81)
我组项目效果：
![18e771b4e73c8679cc83bc6f6c1f2d4](https://github.com/user-attachments/assets/ade7c5ea-79b2-4458-8e1e-9c750197bc05)
![ce6c83e25521094b13d6318c551287e](https://github.com/user-attachments/assets/a57ce123-99fd-4dc4-b616-a63722cc1b8a)

3.3 第3关：扩展功能考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。
![29384c84f532e71a085ddf676f978184_](https://github.com/user-attachments/assets/981c3489-3fac-4f5a-8d51-566d6d039845)
![7f60c5a28128cc8b31c57e6a276210a5_](https://github.com/user-attachments/assets/1605b880-a495-45c6-b699-35bb267b1966)

3.4 第4关：多重加密
3.4.1 双重加密将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits。
![555b66aea3b1ae4a3aa01c8a6b255dfb_](https://github.com/user-attachments/assets/2517c6b0-f858-4ea2-9d86-12834ab414be)
![13123de3628187d2f5f2b745461fcfc8_](https://github.com/user-attachments/assets/f7e5cd36-0676-4034-a560-872347c6c6db)

3.4.2 中间相遇攻击假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥Key(K1+K2)。
![f1e9d11f9df48a3080ac2eac214a8f75_](https://github.com/user-attachments/assets/53d1f0f9-9566-4313-a96e-7e4bcb9c5d10)
![6e8ba6dc6be5e8a491e63fb4f96f76e7_](https://github.com/user-attachments/assets/52460d2c-8477-46c0-8423-8b3f36af8252)

3.4.3 三重加密将S-AES算法通过三重加密进行扩展，下面两种模式选择一种完成：(1)按照32 bits密钥Key(K1+K2)的模式进行三重加密解密，(2)使用48bits(K1+K2+K3)的模式进行三重加解密。
![1fb813307afe131e1e8150173ee9ffb0_](https://github.com/user-attachments/assets/c947c28f-9861-45cd-be8f-45b8abd40ff7)
![1c4b4dcfd0cf856ac8f1b01d9a512fce_](https://github.com/user-attachments/assets/113472c9-96f8-46eb-aad8-f5b28cf3b14b)

3.5 第5关：工作模式基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果。
![35c365eaafa59127cdf453cd633ce0fa_](https://github.com/user-attachments/assets/7006fd3b-7c5f-4f24-a652-a1199e30f8bb)
![1702da2cba9201bfee6201c7cd744667_](https://github.com/user-attachments/assets/58cdf153-4274-4569-be9d-ec6e91a6bbe3)
![a592f1fdf6b0108103c4289a1c55959](https://github.com/user-attachments/assets/9607bfaa-b730-4ea8-bdf2-c4c9ba3da5d0)
