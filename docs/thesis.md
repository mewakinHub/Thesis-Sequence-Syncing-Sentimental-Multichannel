### ถ้าจะทำต่อต้อง หาข้อดี ที่จะชนะ multimodal จริงจัง
// หาว่าทำไม โปรเจคเราถึงจำเป็น แล้วเคสไหนที่จะเป็นต้องใช้ของเรา

ADVANTAGE 1: The Face Sentimental/Emotional analysis is commonly use multi-modal already
So, I think further making multimodal on for multi-channel(more model use on each channel) gonna be very hard, and not will be made in soon the end.

ADVANTAGE 2: Mostly good/steady developed model are black block, which is not the open-source model, so it’ll be very hard to do multi-modal on something because we need to ask for permission to access that whole model. That’s why just use the result for syncing as a post process is the best choice for now!
SUM: normal people can’t afford to do it!

ADVANTAGE3: Multi-modal’s not flexible to change model for each channel if the state-of-art model change. We use Post processing like voting mechanism, so even if we change those model form each channel to match the situation, we still be able to keep process.
CONTEXT: sentimental analysis industry is unstable, so the state-of-art change very often. Some model also has very specific advantage too!

ADVANTAGE4:



---


- ไม่ได้ทำหลายๆเคสหรือพวกเคสประชดแล้ว ต้องเอาออกจากรีพอรตด้วย บอกแค่ทำ sequence result syncing พอ แล้วอาจจะเอาไปใช้ในอนาคตสำหรับอย่างอื่นที่ไม่ใช่เอไอได้เต็มเลย
    - ลองหารีพอร์ตเกี่ยวกับ sequence syncing แทน ว่ามีใครเคยทำมั้ย แล้วเราทำดีกว่าเค้าหรือแตกต่างมั้ย อาจจะแบบไม่ใครมีใครทำสำหรับอารมณ์ หรือแบบเอไอ
    - อย่างที่สองที่ต้องกังวลคือ sequence จาก AI มันไม่เท่ากันแต่ละรอบใช่มั้ย จะทำไงให้ dynamically adaptive ตาม


- การที่เราขยายอะไรมากขึ้นไป ให้ความรู้มากขึ้นก็คิดว่่มากพอสำหรับโปรเจคหนึ่งเทอมแล้วครับ