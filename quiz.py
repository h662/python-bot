import json
import re
from discord.ext import commands

class QuizCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_queue: list[dict] = []
        self.current_quiz: dict | None = None
        self.master_id: int | None = 943335596162691093
        self.scoreboard = {i: 0 for i in range(1, 11)}

    @commands.command(name="퀴즈")
    async def quiz(self, ctx):
        if self.master_id is not None and ctx.author.id != self.master_id:
            return

        try:
            with open("quiz.json", encoding="utf-8") as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("퀴즈 JSON은 반드시 배열([{}, ...]) 형태여야 합니다.")

            self.quiz_queue = data.copy()
            self.current_quiz = self.quiz_queue.pop(0)
            q = self.current_quiz
            await ctx.send(f"**퀴즈 {q['number']}번**\n{q['quiz']}")
        except Exception as e:
            await ctx.send(f"⚠️ 퀴즈 로드 실패: {e}")

    @commands.command(name="다음")
    async def next_quiz(self, ctx):
        if self.master_id is None or ctx.author.id != self.master_id:
            return

        if not self.quiz_queue:
            await ctx.send("😢 더 풀 문제가 없습니다. `!퀴즈` 로 새로 로드하세요.")
            return
        self.current_quiz = self.quiz_queue.pop(0)
        q = self.current_quiz
        await ctx.send(f"**퀴즈 {q['number']}번**\n{q['quiz']}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.content.startswith("!"):
            return
        
        await self.bot.process_commands(message)

        if not self.current_quiz:
            return

        m = re.match(r"^(\d+)팀\s+(.+)$", message.content)
        if not m:
            return

        team = int(m.group(1))
        answer = m.group(2).strip()
        correct = self.current_quiz.get("answer", "")
        if answer.lower() == correct.lower():
            pts = self.current_quiz.get("score", 1)
            self.scoreboard[team] += pts
            await message.channel.send(f"✅ **{team}팀** 정답! +{pts}점")

            desc = self.current_quiz.get("description", "")
            if desc:
                await message.channel.send(f"💡 해설: {desc}")

            scores = self.scoreboard
            max_score = max(scores.values())
            lines = []
            for t in sorted(scores):
                line = f"{t}팀: {scores[t]}점"
                if max_score > 0 and scores[t] == max_score:
                    line = f"**🎉 {line} 🎉**"
                lines.append(line)
            await message.channel.send("=== 현재 점수 ===\n" + "\n".join(lines))

            await message.channel.send("다음 문제는 `!다음` 으로 시작하세요.")

            self.current_quiz = None

    @commands.command(name="점수")
    async def show_score(self, ctx):
        scores = self.scoreboard
        max_score = max(scores.values())
        lines = []
        for t in sorted(scores):
            line = f"{t}팀: {scores[t]}점"
            if max_score > 0 and scores[t] == max_score:
                line = f"**🎉 {line} 🎉**"
            lines.append(line)
        await ctx.send("=== 현재 점수 ===\n" + "\n".join(lines))
