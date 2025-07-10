import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import holidays
import logging

KR_HOLIDAYS = holidays.KR(years=[2025])

NOTIFY_SCHEDULE = [
    ((8, 50),  "🕗 곧 수업 시작 10분 전이에요! QR 체크 준비하셨나요? 😊"),
    ((9, 0),   "📸 9시 정각입니다! 스크린샷 찍을게요~ 얼굴이 잘 보이게 해주세요!"),
    ((9, 50),  "🕘 9시 50분입니다. 잠깐 눈을 쉬면서 휴식해볼까요?"),
    ((10, 50), "🕙 10시 50분이에요! 자리에서 일어나 스트레칭 한번 해보는 건 어떨까요?"),
    ((11, 50), "🕚 11시 50분, 점심 시간이에요! 맛있게 드시고 재충전하세요! 🍱"),
    ((12, 55), "🕛 오후 수업 5분 전이에요! 기지개 한번 쭉~ 켜고 준비해볼까요? ⚡️"),
    ((13, 0),  "📸 13시 정각입니다! 오후 수업 스크린샷 찍습니다. 얼굴 보여주세요 😊"),
    ((13, 50), "🕜 13시 50분, 짧은 휴식 시간입니다. 잠깐 숨 고르고 다시 집중해요!"),
    ((14, 50), "🕑 14시 50분입니다! 눈도 쉬고, 잠시 머리도 식혀주세요."),
    ((15, 50), "🕒 15시 50분이에요. 휴식 후 오늘 하루를 돌아보는 시간 가져보세요 🦁"),
    ((16, 0),  "📝 지금은 회고 시간입니다! 오늘 배운 내용을 TIL로 정리해볼까요?"),
    ((16, 50), "🕓 16시 50분입니다. 오늘 배운 내용을 마지막으로 한번 더 정리해보세요."),
    ((17, 50), "🕔 17시 50분이에요! 회고 마무리하고 하루를 깔끔하게 정리해봐요."),
    ((18, 0),  "📸 18시가 되었습니다! 수업 종료 스크린샷 촬영합니다. QR 체크도 잊지 마세요! 오늘 하루 정말 고생 많으셨어요 🎉"),
]

def setup_scheduler(bot, channel_id: int):
    if hasattr(bot, "scheduler") and bot.scheduler.running:
        logging.warning("⏰ Scheduler is already running. Skipping duplicate setup.")
        return

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
