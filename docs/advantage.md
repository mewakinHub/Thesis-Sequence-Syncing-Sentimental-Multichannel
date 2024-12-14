
// ถ้าจะทำต่อต้อง หาข้อดี ที่จะชนะ multimodal จริงจัง
// หาว่าทำไม โปรเจคเราถึงจำเป็น แล้วเคสไหนที่จะเป็นต้องใช้ของเรา

### Advantages of the Voting Mechanism Approach
Using a post-processing approach like a voting mechanism instead of traditional multimodal techniques for multi-channel sentiment analysis offers several advantages:

**ADVANTAGE 1**: The Face Sentimental/Emotional analysis is commonly use multi-modal already
So, I think further making multimodal on for multi-channel(more model use on each channel) gonna be very hard, and not will be made in soon the end.
SUM: feasible
more: ละก็บอกจารเพิ่มว่าพวก multi-modal resrarch paper ที่มีตอนนี้ในเว็ปหลักอย่าง paper w code ก็ส่วนใหญ่จะมีแค่สอง channel ละก็จะมีแค่ Conversation talk จะไม่ค่อยมี general purpose คนเดียวแบบนี้ 
- การเริ่มต้นทำตรงนี้อาจจะช่วยเปิดเส้นทางการทำ multi-channel มากขึ้น

**ADVANTAGE 2**: Mostly good/steady developed model are black block, which is not the open-source model, so it’ll be very hard to do multi-modal on something because we need to ask for permission to access that whole model. That’s why just use the result for syncing as a post process is the best choice for now!
SUM: Normal people can’t access to those model that's not open-source to build multi-modal. For example, some model on-line via api, might only be able to use it as black box service, but no access to source code!


**ADVANTAGE3**: Multi-modal’s not flexible to change model for each channel if the state-of-art model change. We use Post processing like voting mechanism, so even if we change those model form each channel to match the situation, we still be able to keep process.
CONTEXT: sentimental analysis industry is unstable, so the state-of-art change very often. Some model also has very specific advantage too!
Translated: ข้อดีของโปรเจคเราจริงๆคือ multimodal มันเปลี่ยนโมเดลละลำบากเพราะมันเชื่อมข้างในตัวโมเดลเลย แต่ของเราถึงจะเปลี้ยนโมเดลก็แค่ปรับ result ให้ metric คล้ายๆกัน ก็เอามา sync ได้ละ แค่นี้ก็พร้อมสำหรับทุกโมเดลที่สร้างขึ้นมาเรื่อยๆ (อาจจะบอกจารว่า สำหรับ emotion detection พวกstate-of-artยังไม่ค่อยคงที่ มีโมเดลใหม่ๆขึ้นมาแย่งที่หนึ่งเรื่อยๆ
***SHOWCASE***: [FacialExpression](./FacialExpression.md)
KEYWORD: modularlity(loosely couple), flexibility, adaptability to future

**ADVANTAGE4**:


**PROMTPS**: understand this proiject and help me think the advantage of using post processing lieki Voting mechanism instead of Multimodal for multi channel sentimental analysis
---