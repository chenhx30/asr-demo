import random
from http import HTTPStatus
from dashscope import Generation

# 设置您的API密钥
API_KEY = 'sk-16aa6d09b6ba46699e842d5dbc89ba50'

def multi_round_conversation():
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #
    #     {"role": "user", "content": "明天是张三的生日，他打算去购物。"},
    #     {"role": "assistant", "content": "{'input': '明天是张三的生日，他打算去购物。', 'tag': '[明天/noun 是/verb 张三/noun 的/particle 生日/noun ，/punctuation 他/pron 打算/verb 去/verb 购物/noun 。/punctuation]', 'output': '明天是张三的生日，张三打算去购物。'}"},
    #
    #     {"role": "user", "content": "这本书很有趣，我买给了李四。"},
    #     {"role": "assistant", "content": "{'input': '这本书很有趣，我买给了李四。', 'tag': '[这/det 本/m classifier 书/noun 很/adv 有趣/adj ，/punctuation 我/pron 买给/verb 了/aux 李四/noun 。/punctuation]', 'output': '这本书很有趣，我买给了李四。'}"},
    #
    #     {"role": "user", "content": "我们计划在周末去野餐，你们想要带什么？"},
    #     {"role": "assistant", "content": "{'input': '我们计划在周末去野餐，你们想要带什么？', 'tag': '[我们/pron 计划/verb 在/p rep 周末/noun 去/verb 野餐/noun ，/p 我们/pron 想要/verb 带/verb 什么/pron ？/p]', 'output': '我们计划在周末去野餐，我们想要带什么？'}"},
    #
    #     {"role": "user", "content": "这篇论文写得很好，我推荐给了王五。"},
    #     {"role": "assistant", "content": "{'input': '这篇论文写得很好，我推荐给了王五。', 'tag': '[这/det 篇/m classifier 论文/noun 写/verb 得/aux 很/adv 好/adj ，/p 我/pron 推荐/verb 给/verb 了/aux 王五/noun 。/p]', 'output': '这篇论文写得很好，我推荐给了王五。'}"},
    #
    #     {"role": "user", "content": "这个项目需要张三和李四的协助，他们会提供帮助。"},
    #     {"role": "assistant", "content": "{'input': '这个项目需要张三和李四的协助，他们会提供帮助。', 'tag': '[这/det 个/q classifier 项目/noun 需要/verb 张三/noun 和/c 李四/noun 的/particle 协助/noun ，/p 他们/pron 会/verb 提供/verb 帮助/noun 。/p]', 'output': '这个项目需要张三和李四的协助，张三和李四会提供帮助。'}"}
    # ]

    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #
    #     {"role": "user", "content": "昨天我去了动物园，看到了一只可爱的大熊猫。"},
    #     {"role": "assistant", "content": "{\"input\": \"昨天我去了动物园，看到了一只可爱的大熊猫。\", \"tag\": \"[昨天/time 我/pron 去/verb 了/aux 动物园/noun ，/punctuation 看到/verb 了/aux 一/m classifier 只/q classifier 可爱/adj 的/particle 大熊猫/noun 。/punctuation]\", \"output\": \"昨天我去了动物园，看到了一只可爱的大熊猫。\"}"},
    #
    #     {"role": "user", "content": "它在阳光下悠闲地吃着竹子，是一种非常温柔的动物。"},
    #     {"role": "assistant", "content": "{\"input\": \"它在阳光下悠闲地吃着竹子，是一种非常温柔的动物。\", \"tag\": \"[它/pron 在/p 阳光/noun 下/f 悠闲/adj 地/p 吃/verb 着/aux 竹子/noun ，/punctuation 是/verb 一种/m classifier 非常/adv 温柔/adj 的/particle 动物/noun 。/punctuation]\", \"output\": \"大熊猫在阳光下悠闲地吃着竹子，是一种非常温柔的动物。\"}"},
    #
    #     {"role": "user", "content": "我听说它们非常擅长攀爬树木和游泳。"},
    #     {"role": "assistant", "content": "{\"input\": \"我听说它们非常擅长攀爬树木和游泳。\", \"tag\": \"[我/pron 听说/verb 它们/pron 非常/adv 擅长/verb 攀爬/verb 树木/noun 和/c 游泳/verb 。/punctuation]\", \"output\": \"我听说大熊猫非常擅长攀爬树木和游泳。\"}"},
    #
    #     {"role": "user", "content": "它们是我最喜欢的动物之一，我希望有一天能够亲眼见到它们。"},
    #     {"role": "assistant", "content": "{\"input\": \"它们是我最喜欢的动物之一，我希望有一天能够亲眼见到它们。\", \"tag\": \"[它们/pron 是/verb 我/pron 最/adv 喜欢/verb 的/particle 动物/noun 之一/measure ，/p 我/pron 希望/verb 有/verb 一天/m classifier 能够/aux 亲眼/adv 见到/verb 它们/pron 。/punctuation]\", \"output\": \"大熊猫是我最喜欢的动物之一，我希望有一天能够亲眼见到大熊猫。\"}"}
    # ]

    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are a helpful assistant."
    #     },
    #
    #     {
    #         "role": "user",
    #         "content": "张三去了哪里？他去买菜了。他要买什么？他要买西红柿、黄瓜和土豆。"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": """
    #         {
    #             '输入': '张三去了哪里？他去买菜了。他要买什么？他要买西红柿、黄瓜和土豆。',
    #             '分词和词性标注': '[张三] [去] [了] [哪里] ？[他] [去] [买菜] [了] 。[他] [要] [买] [什么] ？[他] [要] [买] [西红柿]、[黄瓜] [和] [土豆] 。',
    #             '命名实体': '[张三]去了哪里？[他]去买菜了。[他]要买什么？[他]要买[西红柿]、[黄瓜]和[土豆]。',
    #             '分析依存句法，找出代词与其先行词之间的关系': '代词[他]与先行词[张三]之间存在着动作关系',
    #             '输出': '张三去了哪里？张三去买菜了。张三要买什么？张三要买西红柿、黄瓜和土豆。'
    #         }
    #         """
    #     }
    # ]

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },

        {
            "role": "user",
            "content": "我的同学张三，他养了两只大金毛波妞和花花，它们经常跟着一起去食堂，食堂的阿姨也很喜欢它们，所以他常常以此为豪，时不时地就对食堂的阿姨们说：你们真老登"
        },
        {
            "role": "assistant",
            "content": """
		{
            '输入': '我的同学张三，他养了两只大金毛波妞和花花，它们经常跟着一起去食堂，食堂的阿姨也很喜欢它们，所以他常常以此为豪，时不时地就对食堂的阿姨们说：你们真老登',
            '分词和词性标注': '[我的/r] [同学/n] [张三/nr] [，/w] [他/r] [养/v] [了/u] [两只/m] [大/a] [金毛/nz] [波妞/nz] [和/c] [花花/nz] [，/w] [它们/r] [经常/d] [跟着/p] [一起/d] [去/v] [食堂/n] [，/w] [食堂/n] [的/u] [阿姨/n] [也/d] [很/d] [喜欢/v] [它们/r] [，/w] [所以/c] [他/r] [常常/d] [以/p] [此/r] [为/p] [豪/n] [，/w] [时不时/d] [地/uv] [就/d] [对/p] [食堂/n] [的/u] [阿姨们/n] [说/v] [：/w] [你们/rr] [真/d] [老登/a] [。/w]',
            '命名实体': '[我的/O] [同学/O] [张三/person] [，/O] [他/O] [养/O] [了/O] [两只/O] [大金毛波妞/animal] [和/O] [花花/animal] [，/O] [它们/O] [经常/O] [跟着/O] [一起/O] [去/O] [食堂/O] [，/O] [食堂/O] [的/O] [阿姨/O] [也/O] [很/O] [喜欢/O] [它们/O] [，/O] [所以/O] [他/O] [常常/O] [以此/O] [为/O] [豪/O] [，/O] [时不时/O] [地/O] [就/O] [对/O] [食堂/O] [的/O] [阿姨/O] [们/O] [说/O] [：/O] [你们/O] [真/O] [老登/O] [。/O]',
            '依存句法分析': '代词[他]与先行词[张三]之间存在着指代关系,代词[它们]与先行词[大金毛波妞]、[花花]之间存在着指代关系,代词[你们]与先行词[阿姨]之间存在着指代关系',
            '代词识别': '人称代词[他]、[它们]、[你们]',
            '先行词识别': '先行词[张三]、[大金毛波妞]、[花花]、[阿姨们]',
            '指代消解': '替换人称代词[他]为先行词[张三]，替换人称代词[它们]为先行词[大金毛波妞]、[花花]，替换人称代词[你们]为先行词[阿姨们]',
            '输出': '我的同学张三，张三养了两只大金毛波妞和花花，大金毛波妞、花花经常跟着一起去食堂，食堂的阿姨也很喜欢大金毛波妞、花花，所以张三常常以此为豪，时不时地就对食堂的阿姨们说：阿姨们真老登'
        }
		"""
        },

        {
            "role": "user",
            "content": "我和我的好朋友小明经常一起在操场踢足球，他总是射门很准，因此我们的队伍常常赢得比赛。"
        },
        {
            "role": "assistant",
            "content": """
		{
			'输入': '我和我的好朋友小明经常一起在操场踢足球，他总是射门很准，因此我们的队伍常常赢得比赛。',
			'分词和词性标注': '[我/r] [和/c] [我/r] [的/u] [好/a] [朋友/n] [小明/nr] [经常/d] [一起/d] [在/p] [操场/n] [踢/v] [足球/n] [，/w] [他/r] [总是/d] [射门/n] [很/d] [准/a] [，/w] [因此/c] [我们/r] [的/u] [队伍/n] [常常/d] [赢得/v] [比赛/v] [。/w]',
			'命名实体': '[我/O] [和/O] [我/O] [的/O] [好/O] [朋友/O] [小明/person] [经常/O] [一起/O] [在/O] [操场/O] [踢足球/O] [，/O] [他/O] [总是/O] [射门/O] [很/O] [准/O] [，/O] [因此/O] [我们/O] [的/O] [队伍/O] [常常/O] [赢得/O] [比赛/O] [。/O]',
			'依存句法分析': '代词[他]与先行词[小明]之间存在着指代关系',
			'代词识别': '人称代词[他]',
			'先行词识别': '先行词[小明]',
			'指代消解': '替换人称代词[他]为先行词[小明]',
			'输出': '我和我的好朋友小明经常一起在操场踢足球，小明总是射门很准，因此我们的队伍常常赢得比赛。'
		}
		"""
        },

        {
            "role": "user",
            "content": "校园里有一个小卖部，我每天都会去那里买饮料，老板娘很热情，她总是微笑着为我服务。"
        },
        {
            "role": "assistant",
            "content": """
		{
            '输入': '校园里有一个小卖部，我每天都会去那里买饮料，老板娘很热情，她总是微笑着为我服务。',
            '分词和词性标注': '[校园/n] [里/f] [有/v] [一个/m] [小卖部/n] [，/w] [我/r] [每天/r] [都/d] [会/v] [去/v] [那里/r] [买/v] [饮料/n] [，/w] [老板娘/n] [很/d] [热情/a] [，/w] [她/r] [总是/d] [微笑/v] [着/u] [为/p] [我/r] [服务/v] [。/w]',
            '命名实体': '[校园/O] [里/O] [有/O] [一个/O] [小卖部/O] [，/O] [我/O] [每天/O] [都/O] [会/O] [去/O] [那里/O] [买/O] [饮料/O] [，/O] [老板娘/O] [很/O] [热情/O] [，/O] [她/O] [总是/O] [微笑/O] [着/O] [为/O] [我/O] [服务/O] [。/O]',
            '依存句法分析': '代词[她]与先行词[老板娘]之间存在着指代关系',
            '代词识别': '人称代词[她]',
            '先行词识别': '先行词[老板娘]',
            '指代消解': '替换人称代词[她]为先行词[老板娘]',
            '输出': '校园里有一个小卖部，我每天都会去那里买饮料，小卖部的老板娘很热情，老板娘总是微笑着为我服务。'
        }
		"""
        }
    ]


    while True:
        user_content = input("用户输入：").strip()
        if user_content:
            messages.append({"role": "user", "content": user_content})

            response = Generation.call(
                # 'qwen-14b-chat',
                'qwen-plus',
                api_key=API_KEY,
                messages=messages,
                seed=random.randint(1, 10000),
                result_format='message'
            )

            if response.status_code == HTTPStatus.OK:
                #print(response)
                # 获取 content 的值
                content_value = response['output']['choices'][0]['message']['content']
                print("模型输出：" + content_value)

                messages.append({'role': response.output.choices[0]['message']['role'],
                                 'content': response.output.choices[0]['message']['content']})
            else:
                print('请求ID：%s，状态码：%s，错误码：%s，错误消息：%s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))

if __name__ == '__main__':
    multi_round_conversation()
