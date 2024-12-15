- ไม่ได้ทำหลายๆเคสหรือพวกเคสประชดแล้ว ต้องเอาออกจากรีพอรตด้วย บอกแค่ทำ sequence result syncing พอ แล้วอาจจะเอาไปใช้ในอนาคตสำหรับอย่างอื่นที่ไม่ใช่เอไอได้เต็มเลย
    - ลองหารีพอร์ตเกี่ยวกับ sequence syncing แทน ว่ามีใครเคยทำมั้ย แล้วเราทำดีกว่าเค้าหรือแตกต่างมั้ย อาจจะแบบไม่ใครมีใครทำสำหรับอารมณ์ หรือแบบเอไอ
    - อย่างที่สองที่ต้องกังวลคือ sequence จาก AI มันไม่เท่ากันแต่ละรอบใช่มั้ย จะทำไงให้ dynamically adaptive ตาม


- การที่เราขยายอะไรมากขึ้นไป ให้ความรู้มากขึ้นก็คิดว่่มากพอสำหรับโปรเจคหนึ่งเทอมแล้วครับ

---

## TODO:
@krypiix 
มึงลองทำ thesis ก่อนได้เลยนะ  

เดะ กุทำ cv ดีเทคทีละเฟรมได้แน่ๆ ละเดะลองทำให้มันอ่าน predict ทีบะเฟรมจนจบคลิป

ส่วนพาร์ทโทนเสียง มึงลองหาโมเดลแล้วทำโค้ดเลยก็ได้

สักวันศุกร์มาทำ integration กัน คือจะเอาสอง result มา sync กัน
1. ดีไซน์ว่าจะใข้ attribute อะไร sync กันมั่ง คำนวนยังไง sync กี่รอบ ใช้ time stamp เป็นตัวเชื่อมมั้ย แล้งถ้า result image มันมีเป็นร้อยเฟรม แล้งจะsync กับ voice tone ทีมีน้อยกว่ายังไง ละคือแค่syncกันโง่ๆมันพอแล้วมั้ย หรือต้องเพิ่มอะไรมาแอดเช่น condition base ของแต่ละรอลที่ sync เช่น โทนเสียง conflict กับ สีหน้า แล้วtranscript เราควรหั่นๆมาใช้predictย่อยๆ ตามจำนวน โทนเสียงมั้ย เพื่อเอามา sync ด้วยกับ สีหน้า และ โทนเสียง -> ละตอนท้ายค่อยเอามา sync รวมๆอีกที ว่าcontextรวมๆเค้าพูดบวกหรือลบ
2. โค้ด ไม่ต้องเชื่อม เอาresult ของแต่ละ channel มาแปะในconfig ละลองเอามาsyncกันเลย จะโหวตเล็กๆกี่รอบ แล้ว จำนวนเฟรม(result)ที่ไม่เท่ากัน ของแต่ละรอบจะ sync ยังไงให้ dynamic ตามจำนวนเฟรม แบบต้องใช้ syntax โค้ดอะไรมารองรับสมการ พวก len(facial_results) เอามาเทียบกับ len(voicetone_results) ละคำนวนยังไง floor มั้ยถ้าไม่พอดี มีต่องคิดเยอะ กูก็คิดเองคนเดียวไม่ได้ อยากให้มึงช่วยดีไซน์ด้วยแหละว่าจะออกแบบยังไง 

เพราะงั้นหลักๆก็แยกกันเขียนโค้ดของแต่ละ channel ทิ้งไว้ก่อนก็ได้ ละวันศุกร์มาเอาสอง result นี้ sync กัน ออกแบบทั้งสมการละโค้ดเลย ต้องการความคิดสร้างสรรค์


---

my current idea: [PDF: Syncing](./Syncing.pdf)

NOTE:
พาร์ทหั่นสคริปต์อะเตอร์ ก็แค่หั่นวิดีโอก่อน แล้วค่อยเอาวิดีโอไป extract  transcript from that trimmed video แค่นั้นเลย
ไอ้ condition ยังมีแค่ ประชด เพราะยังไม่ได้คิดเพิ่ม ยังไม่เข้าใจอารมณ์มนุษย์เพียงพอ ยังไม่บรรลุ

---
## TODO:
1. syncing on 2 or 3 channels partitioned by transcript chunk with weight on confident score
2. if conflict(+/- or +/neutral or bla bla bla, use creative) emotion, reach threshold > 3 consecutive timestamps: count as it's really conflict and reset the threshold -> use ChatGPT to help
3. 

---

## The Universal Format:
```
[
    {
        "partition": "0-6s",
        "transcript": {
            "text": "Mitch was in his final semester at a college in Louisiana when he met another senior, a wonderful",
            "emotion": "Happy",
            "confidence": 0.9222
        },
        "facial_expression": [
            {"frame": "0000.jpg", "emotion": "Neutral", "confidence": 0.87},
            {"frame": "0001.jpg", "emotion": "Angry", "confidence": 0.78},
            {"frame": "0002.jpg", "emotion": "Neutral", "confidence": 0.85},
            {"frame": "0003.jpg", "emotion": "Sad", "confidence": 0.72},
            {"frame": "0004.jpg", "emotion": "Happy", "confidence": 0.81},
            {"frame": "0005.jpg", "emotion": "Neutral", "confidence": 0.89}
        ],
        "voice_tone": [
            {"time": 0.0, "emotion": "Calm", "confidence": 0.88},
            {"time": 2.0, "emotion": "Happy", "confidence": 0.91},
            {"time": 4.0, "emotion": "Neutral", "confidence": 0.80}
        ]
    },
    {
        "partition": "7-12s",
        "transcript": {
            "text": "young lady named Kayla.",
            "emotion": "Neutral",
            "confidence": 0.85
        },
        "facial_expression": [
            {"frame": "0007.jpg", "emotion": "Neutral", "confidence": 0.84},
            {"frame": "0008.jpg", "emotion": "Angry", "confidence": 0.76},
            {"frame": "0009.jpg", "emotion": "Neutral", "confidence": 0.81},
            {"frame": "0010.jpg", "emotion": "Sad", "confidence": 0.73},
            {"frame": "0011.jpg", "emotion": "Happy", "confidence": 0.79},
            {"frame": "0012.jpg", "emotion": "Neutral", "confidence": 0.90}
        ],
        "voice_tone": [
            {"time": 7.0, "emotion": "Calm", "confidence": 0.88},
            {"time": 9.0, "emotion": "Happy", "confidence": 0.91},
            {"time": 11.0, "emotion": "Neutral", "confidence": 0.80}
        ]
    }
]
```