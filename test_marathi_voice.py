import asyncio
import edge_tts

async def main():
    text = (
        "चेरी पावडर मिल्ड्यू. "
        "रोगाची लक्षणे तपासा. "
        "प्रभावित पाने काढून टाका. "
        "पिकाचे नियमित निरीक्षण करा."
    )
    voice = "mr-IN-AarohiNeural"
    await edge_tts.Communicate(text, voice).save("marathi_voice_test.mp3")
    print("Created marathi_voice_test.mp3")

asyncio.run(main())
