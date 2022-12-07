from aiogram import *
import requests
from bs4 import BeautifulSoup as BS
import time

TOKEN = "5860412338:AAEHjJjTdnCVDDiCP45j1JOeo2OvnNtVQAM"
bot =  Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

channel_id = '-1001816777856'


old_link = '12'
new_link = ''
def check_new_post():
    global old_link, new_link
    r = requests.get('https://kun.uz/uz/news/list')
    soup = BS(r.text, 'html.parser')
    img = soup.find('a', {'class': 'daily-block l-item'})
    new_link = str(img['href'])
    if new_link != old_link:
        old_link = new_link
        get_content(new_link)
        return True
    else:
        return False

title = ''
imgg = ''
text = ''
def get_content(link):
    global title, imgg, text
    r = requests.get('https://kun.uz'+link)
    soup = BS(r.text, 'html.parser')

    #-------------------get_title---------
    t = str(soup.find('div', {'class': 'single-header__title'}))
    title = str(t[34:len(t)-7])+'.'

    #-------------------get_image----------
    t = soup.find('div', {'class': 'main-img'})
    if t != None:
        imgg = str(t.find('img')['src'])
    else:
        t = soup.find('figure', {'class': 'image'})
        if t != None:
            imgg = str(t.find('img')['src'])
        else:
            t = str(soup.find('iframe').attrs.get('src'))
            if 'youtube' in t:
                if 'start' in t:
                    ii = t[30:len(t)-8]
                else:
                    ii = t[30:]
                imgg = f'https://img.youtube.com/vi/{ii}/maxresdefault.jpg'
            else:
                imgg = 'https://storage.kun.uz/source/thumbnails/_medium/4/o0LdxtGQj8e0r21Y1bZ9_DQ3Zui8-0aa_medium.jpg'
    
    #----------------get_text---------------
    t = soup.find_all('p')
    text = ''
    for i in range(2):
        y = str(t[i])
        if not'dir="auto"' in y:
            y = y[3:len(y)-4]
        else:
            y = y[14:len(y)-4]
        if not('<' in y):
            text+=y
        else:
            l=''
            p = True
            for j in range(len(y)):
                if y[j]=='<':
                    p = False
                    continue
                elif y[j]=='>':
                    p = True
                    continue
                if p:
                    l+=y[j]
            text+=l
            
        text+=' '
            

# ---------------------------------Asosiy bot uchun codlar-------------------------------------------------------
@dp.message_handler(commands='start')
async def start(message: types.Message):
    if message.from_user.username == 'Feruzbek_Sapayev':
        await message.answer("<a href='https://kun.uz/uz/news/list'>Batafsil...</a>", parse_mode='html')
        while True:
            if check_new_post():
                msg = f"<b>{title}</b>\n\n{text}\n\n<a href='https://kun.uz{new_link}'>Batafsil...</a>\n\n<b>👇Telegram kanal👇 Eng so'ngi yangiliklar</b> https://t.me/YangiliklarJahonXabarlari"
                await bot.send_photo(channel_id, photo=imgg, caption=msg, parse_mode='html')
            time.sleep(60)
    else:
        await message.answer('Siz admin emasssiz!')

@dp.message_handler()
async def msg(message: types.Message):
    await message.delete()

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
