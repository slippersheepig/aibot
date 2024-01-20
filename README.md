搭配[Hugging Face](https://huggingface.co/models)使用的AI机器人  
> [!TIP]
> 需注册Hugging Face账号，在个人信息profile处点击settings-access tokens生成api复制备用

> [!NOTE]
> 该代码仅兼容有限模型使用（或者说官方免费api限制太多导致的，未测试付费api该代码是否可用），并且免费api基本不支持自然语言对话，回复都是答非所问，只能根据模型的功能针对性提出任务

`.env`
```bash
HUGGINGFACEHUB_API_TOKEN=hf_ABCDEFGHIJKLMNOPQRSTUVWXYZ
TOKEN=123456789:abcdefghijklmnopqrstuvwxyz
BOT_USERNAME=@tg_bot_name
TEMPERATURE=0.5
MAX_LENGTH=10000
MODEL_REPO_ID=openchat/openchat-3.5-0106
```
（必填）HUGGINGFACEHUB_API_TOKEN：填入tip提到的api  
（必填）TOKEN：电报机器人token  
（必填）BOT_USERNAME：机器人名称（@不要漏）  
（选填，默认0.7，可删除）TEMPERATURE：取值范围0-1，越小回答越固定，越大越发散  
（选填，默认500，可删除）MAX_LENGTH：回复最大长度  
（必填）MODEL_REPO_ID：模型名称，自行选择填入  
`docker-compose.yml`
```bash
services:
  chatgpt:
    image: sheepgreen/aibot
    container_name: aibot
    volumes:
      - ./.env:/app/.env
    restart: always
```
以上两个文件放同一目录，然后运行`docker-compose up -d`命令即可  
> [!IMPORTANT]
> 部分模型回复极慢，如果日志没报错（不含警告）请耐心等待，若报错请自行解决，各种情形太多了  
> 查日志`docker logs aibot`
