import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import holidays
import logging

KR_HOLIDAYS = holidays.KR(years=[2025])

NOTIFY_SCHEDULE = [
    ((8, 50),  "🕗 곧 수업 시작 10분 전이에요! QR 코드 준비되셨나요? 😊"),
    ((9, 0),   "📸 9시 정각입니다! 수업 중 스크린샷 찍으니 얼굴 보여주세요."),
    ((9, 50),  "🕘 9시 50분, 잠깐 휴식하고 눈을 쉬어주세요."),
    ((10, 50), "🕙 10시 50분입니다! 스트레칭으로 몸을 풀어보세요."),
    ((11, 50), "🕚 11시 50분, 점심 시간이에요! 맛점하세요! 🍱"),
    ((12, 55), "🕛 오후 수업 5분 전입니다! 에너지 충전하세요. ⚡️"),
    ((13, 0),  "📸 13시 정각, 오후 수업 스크린샷 촬영합니다. 얼굴 보여주기! 😊"),
    ((13, 50), "🕜 13시 50분, 짧은 휴식 후 다시 집중해요."),
    ((14, 50), "🕑 14시 50분입니다! 잠시 휴식 후 진행하도록 하겠습니다."),
    ((15, 50), "🕒 15시 50분, 휴식 후 회고할 시간을 가져보세요. 🦁"),
    ((16, 00), "📝 지금부터 회고 시간! 오늘 배운 내용 TIL 작성 잊지 말기!"),
    ((16, 50), "🕓 16시 50분, 잠시 쉬었다 오늘 배운 내용을 마무리 정리해보세요."),
    ((17, 50), "🕔 17시 50분입니다! 슬슬 회고 정리 마무리해주세요."),
    ((18, 0),  "📸 18시가 되었습니다! 수업 종료 스크린샷 촬영합니다. 'QR' 잊지 마세요! 오늘도 수고 많으셨어요! 🎉"),
]

def setup_scheduler(bot, channel_id: int):
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")

    for (hour, minute), message in NOTIFY_SCHEDULE:
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            day_of_week="mon-fri",
            timezone="Asia/Seoul"
        )

        scheduler.add_job(
            lambda msg=message: bot.loop.create_task(_notify(bot, channel_id, msg)),
            trigger=trigger,
            id=f"notify_{hour:02d}{minute:02d}"
        )
        
    bot.scheduler = scheduler 
    scheduler.start()

    for job in scheduler.get_jobs():
        logging.info(f"Scheduled {job.id} next run at {job.next_run_time}")

async def _notify(bot, channel_id: int, message: str):
    today = datetime.date.today()

    if today.weekday() >= 5 or today in KR_HOLIDAYS:
        return

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
