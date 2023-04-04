import discord
import re
import MeCab

# Bot Tokenをここに入力してください
TOKEN = ""

# クライアントの作成
client = discord.Client(intents=discord.Intents.all())


# 禁止ワードとそれに対応するメッセージの辞書
banned_words = {
    "えろい": "今の発言は何が問題だと思いますか？そうですか。でも、実は「えろい」という言葉には、問題があるとされています。まず、「えろい」という言葉は、本来は「エロチックな」という意味で使われます。つまり、性的な意味合いを持つ言葉なのです。そのため、「えろい」という言葉を使うことで、相手に不快感を与えたり、誤解を招いたりすることがあるため、控えることが望ましいです。また、このような言葉を使うことで、周囲の人たちに悪影響を与える可能性があります。学校や職場などで、「えろい」という言葉を平気で使っている人がいると、周囲の人たちも同じように使うようになるかもしれません。これが続くと、周囲の人たちに不快感を与えるだけでなく、社会的にもマナー違反とされることがあります。さらに、このような言葉を使うことで、相手を傷つけたり、差別的な表現になることがあります。例えば、女性を指して「えろい」という言葉を使うことで、その人を性的対象としてしか見ていないように受け取られる可能性があります。これは、相手を不快にさせるだけでなく、性差別的な表現としても問題視されることがあります。以上のように、「えろい」という言葉を使うことには、何かしらの問題があると言えます。このような表現は、相手に不快感を与えたり、周囲の人たちに悪影響を与えたりすることがあるため、控えることが望ましいです。",
    "吹いた": "今の発言は何が問題だと思いますか？そうですか。でも、実は「吹いた」という言葉には、問題があるとされています。まず、「吹いた」という言葉は、通常は「笑った」という意味で使われますが、それ以外にも、薬物を吸ったことを隠すために使われることがあります。つまり、「吹いた」という言葉を聞いた場合、その人が薬物を使用した可能性があると疑われることがあります。これは、一般的には望ましくないことです。また、「吹いた」という言葉は、単語自体には問題がなくても、その言い方や文脈によっては失礼な表現になってしまうことがあります。例えば、誰かが努力している様子を見て「あの人、吹いたな」と言われた場合、それはその人を軽んじているように受け取られる可能性があります。さらに、このような表現を使うことで、相手を不快にさせることがあることも考えられます。例えば、友達が何かを話している時に、突然「吹いた」と言われたら、相手はどう思うでしょうか？「笑った」と言えば、相手も一緒に笑ってくれることができますが、「吹いた」と言われたら、相手は自分の話を聞いてくれていないと感じるかもしれません。つまり、「吹いた」という言葉を使うことには、何かしらの問題があると言えます。このような表現は、相手に不快感を与えたり、誤解を招いたりすることがあるため、控えることが望ましいです。以上のように、生徒さんが「吹いた」という言葉を使うことには問題があることが説明できました。今後は、適切な表現を使うように心がけてください。",
    "くさ": "今の発言は何が問題だと思いますか？そうですか。でも、実は「くさ」という言葉には、問題があるとされています。まず、この言葉は「臭い」という意味で使われます。相手が汗をかいているなどの理由で、体臭が気になる場合に使うことが多いですが、これは相手を傷つけることに繋がります。相手に対して「臭い」と言うことは、自分自身が優位に立っているかのような意味合いを持ち、相手を軽蔑しているように受け取られることがあります。特に、相手が自分ではコントロールできないようなもの（体臭など）について指摘することは、その人を傷つけることに繋がる可能性が高いです。また、このような言葉を使うことで、周囲の人たちに悪影響を与える可能性があります。学校や職場などで、「くさ」という言葉を平気で使っている人がいると、周囲の人たちも同じように使うようになるかもしれません。これが続くと、周囲の人たちに不快感を与えるだけでなく、社会的にもマナー違反とされることがあります。さらに、このような言葉を使うことで、相手を傷つけたり、差別的な表現になることがあります。例えば、アジア人を指して「くさい」という言葉を使うことで、その人たちを差別的に見るような印象を与えることがあります。これは、相手を不快にさせるだけでなく、人種差別的な表現としても問題視されることがあります。以上のように、「くさ」という言葉を使うことには、何かしらの問題があると言えます。このような表現は、相手を傷つけたり、周囲の人たちに悪影響を与えたりすることがあるため、控えることが望ましいです。" ,
    "キレそう": "今の発言は何が問題だと思いますか？そうですか。でも、実は「キレそう」という言葉には、問題があるとされています。まず、「キレそう」という言葉は、人を攻撃的にする言葉ではありませんが、使用することが不適切である理由があります。これは、この言葉が感情的に不安定な状態を示唆するため、周囲の人々に不安を与える可能性があるからです。まず第一に、この言葉は「怒る」という行動を暗示することがあります。このような言葉は、怒りや暴力行為が起こる可能性があることを示唆しています。このような言葉を使用すると、周囲の人々が不安や緊張を感じ、恐怖感を抱くことがあります。また、使用者自身が実際に怒りを感じているわけではない場合でも、周囲の人々が不安や恐怖を感じる可能性があるため、この言葉の使用は好ましくありません。第二に、この言葉は暴力や攻撃性を示唆する可能性があります。たとえば、人が「キレそうだ」と言った場合、その人が自分自身や他の人に対して暴力を振るう可能性があると誤解されるかもしれません。このような状況は非常に危険であり、周囲の人々に不安や恐怖を与える可能性があります。第三に、この言葉は解決策を提供しません。感情的に不安定な状態にある場合、自分の感情をコントロールするための方法を模索する必要があります。このような状況では、「キレそうだ」と言うことは、解決策を提供せず、むしろ問題を悪化させることがあります。代わりに、冷静になり、自分自身や他の人々に対して危険を回避する方法を探す必要があります。以上の理由から、先生たちは生徒に対して「キレそう」という言葉を使うことが不適切であることを教える必要があります。",
    "くっさ": "生徒さん、今回の発言で何が問題なのか、理解していますか？そうですか。実は「くっさ」という言葉にも、問題があるとされています。「くっさ」という言葉は、「臭い」という意味の「くさ」と同じように使われますが、より強い意味合いを持ちます。この言葉は、相手の臭いを厳しく非難する表現であり、相手を傷つけたり、人格を否定するような意味合いを持っている場合があります。例えば、自分が「くっさ」と感じる相手を公然と批判することで、その人を恥ずかしくさせたり、周囲の人たちから嫌われたりすることがあります。これは、その人の自尊心を傷つけることに繋がる可能性があり、相手との良好な関係を築くことが難しくなります。また、このような表現は相手に対して攻撃的で、人間関係を悪化させる原因になることがあります。さらに、「くっさ」という言葉は、周囲の人たちに不快感を与えることがあります。学校や職場などで、周囲の人たちが「くっさ」という言葉を使うと、その空間全体が嫌な雰囲気になってしまいます。このような状況になると、人々の協力やコミュニケーションが損なわれる可能性があります。さらに、このような言葉を使うことで、相手を傷つけたり、差別的な表現になることがあります。例えば、アジア人を指して「くっさい」という言葉を使うことで、その人たちを差別的に見るような印象を与えることがあります。これは、相手を不快にさせるだけでなく、人種差別的な表現としても問題視されることがあります。以上のように、「くっさ」という言葉を使うことには、何かしらの問題があると言えます。このような表現は、相手を傷つけたり、周囲の人たちに悪影響を",
    "えろ": "「生徒さん、今の発言は何が問題だと思いますか？そうですか。でも、実は「えろ」という言葉には、問題があるとされています。まず、この言葉は「エロティック（性的）」という意味で使われます。相手の外見や行動がセクシーであると感じた時に使うことが多いですが、これは相手を性的な対象として見ているような印象を与えることがあります。特に、相手が自分自身がそのように見られたくない場合には、相手を傷つけることに繋がる可能性が高いです。また、このような言葉を使うことで、周囲の人たちに悪影響を与える可能性があります。学校や職場などで、「えろ」という言葉を平気で使っている人がいると、周囲の人たちも同じように使うようになるかもしれません。これが続くと、周囲の人たちに不快感を与えるだけでなく、社会的にもマナー違反とされることがあります。さらに、このような言葉を使うことで、相手を傷つけたり、セクシャルハラスメントになることがあります。例えば、女性を指して「えろい」という言葉を使うことで、その女性を性的な対象として見るような印象を与え、不快感を与えることがあります。これは、相手を傷つけたり、性的な迷惑行為になることがあるため、決して許される行為ではありません。以上のように、「えろ」という言葉を使うことには、何かしらの問題があると言えます。このような表現は、相手を傷つけたり、周囲の人たちに悪影響を与えたりすることがあるため、控えることが望ましいです。また、このような言葉を使うことで、性的な迷惑行為に繋がることがあるため、避けることが大切です。",
    "だんごねろ": "「だんごねろ」という言葉は、差別的で人を傷つける言葉です。この言葉には、人種や国籍、文化的背景に基づく差別的な意味が含まれているため、使用することは許容できません。「だんごねろ」という言葉は、一部の人々が日本人を侮辱するために使用することがある言葉です。このような言葉を使用することは、日本人や日本文化に対する偏見や差別を助長することになります。また、「だんごねろ」という言葉は、相手を侮辱する意図を持って使用されることが多いため、相手を傷つけることがあります。このような言葉を使用することは、相手を尊重するという基本的なマナーを無視することになります。さらに、「だんごねろ」という言葉は、場の雰囲気を悪化させる可能性があります。特に、使用者や聞き手によっては、この言葉が非常に不快なものに感じられることがあります。そのため、この言葉を使用することで、人間関係を悪化させることがあることに注意する必要があります。総合すると、「だんごねろ」という言葉を使用することは、人種差別や文化差別を助長し、相手を傷つけることがあり、場の雰囲気を悪化させることがあるため、許容できるものではありません。",
}


# MeCabの初期化
m = MeCab.Tagger("-Owakati")

# 禁止ワードが含まれているかどうかを確認する関数
def contains_banned_word(message):
    for word in banned_words.keys():
        # 禁止ワードを形態素解析してリストにする
        banned_word_tokens = m.parse(word).strip().split()
        # メッセージを形態素解析してリストにする
        message_tokens = m.parse(message.content).strip().split()
        # 禁止ワードのトークンがメッセージのトークンに完全一致する場合、禁止ワードが含まれていると判定する
        if all(token in message_tokens for token in banned_word_tokens):
            return word
    return None

# Botが起動した時に呼び出されるイベント
@client.event
async def on_ready():
    print("Botが起動しました。")

# メッセージが送信された時に呼び出されるイベント
@client.event
async def on_message(message):
    # メッセージを送信したユーザーがBotである場合、無視する
    if message.author == client.user:
        return

    # 禁止ワードが含まれている場合、メッセージを削除し、注意のメッセージを送信する
    banned_word = contains_banned_word(message)
    if banned_word:
        await message.delete()
        await message.channel.send(f"{message.author.mention} さん、{banned_words[banned_word]}")

# Botを起動する
client.run(TOKEN)