import asyncio
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import holidays

KR_HOLIDAYS = holidays.KR(years=[2025])

NOTIFY_SCHEDULE = [
    ((8, 50),  "🕗 수업 시작 10분 전이에요! 준비물 챙기셨나요? 😊"),
    ((9, 50),  "🕘 9시 50분입니다! 다음 강의 시작 곧이니 자리 잡아보세요!"),
    ((10, 50), "🕙 10시 50분이에요! 잠깐 스트레칭 어떠세요?"),
    ((11, 50), "🕚 11시 50분, 점심 시간입니다! 맛있게 드세요! 🍱"),
    ((12, 55), "🕛 오후 수업 시작 5분 전입니다! 에너지 충전하세요!"),
    ((13, 50), "🕜 13시 50분! 오후 첫 강의 준비해볼까요?"),
    ((14, 20), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 25), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 30), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 35), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 40), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 35), "🕑 쉬는시간 알림 테스트 중이니까 신경끄고 11시까지 잠이나 처 자셈!"),
    ((14, 50), "🕑 14시 50분이에요! 집중 모드 ON!"),
    ((15, 50), "🕒 15시 50분, 잠깐 휴식하셔도 좋아요!"),
    ((16, 50), "🕓 16시 50분, 오늘 배운 것 정리할 시간입니다!"),
    ((17, 50), "🕔 17시 50분, 오늘 수업 마무리할 시간이에요! 수고하셨습니다! 🎉"),
]

def setup_scheduler(bot, channel_id: int):
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
    for (hour, minute), message in NOTIFY_SCHEDULE:
        trigger = CronTrigger(
            hour=hour,
            minute=minute,
            day_of_week="mon-fri",
        )

        scheduler.add_job(
            lambda msg=message: asyncio.create_task(_notify(bot, channel_id, msg)),
            trigger=trigger,
            id=f"notify_{hour:02d}{minute:02d}"
        )
    scheduler.start()

async def _notify(bot, channel_id: int, message: str):
    today = datetime.date.today()

    # if today.weekday() >= 5 or today in KR_HOLIDAYS:
    #     return

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
