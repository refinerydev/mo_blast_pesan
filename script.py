from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep, time
from datetime import datetime
from urllib.parse import quote

def save_to_file(status, data):
    with open(f'{status}_dikirim_{datetime.now()}.txt', 'w') as f:
        for i in data:
            f.write(f'{i}\n')
        print('done')

start = time()

f = open('message.txt', 'r')
message = f.read()
f.close()

contacts = []
f = open('phone_number.txt', 'r')
for line in f.read().splitlines():
	if line != '':
		contacts.append(line)
f.close()

count = 0
success = 0
fail = 0
parsed_text = quote(message)

msg_sent = []
msg_not_sent = []

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://web.whatsapp.com')
input('Tekan ENTER setelah berhasil login')
for index, number in enumerate(contacts):
    try:
        url = 'https://web.whatsapp.com/send?phone=' + str(number) + '&text=' + parsed_text 
        sent = False

        driver.get(url)
        try:
            sleep(2)
            click_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'epia9gcq')))
            success += 1
            msg_sent.append(number)
        except Exception as e:
            print(str(index+1) + ' Tidak dapat mengirim pesan ke no: ' + str(number))
            fail += 1
            msg_not_sent.append(number)
        else:
            sleep(2)
            click_btn.click()
            sent = True
            sleep(2)
            print(str(index+1) + ' Pesan terkirim ke: ' + str(number))
        count += 1
    except Exception as e:
        print(str(index+1) + ' Gagal dikirim ke no: ' + str(number) + str(e))
        fail += 1
        msg_not_sent.append(number)
driver.quit()

print('Selesai!')
print('terkirim: ', success)
print('gagal: ', fail)
end = time()

print('waktu eksekusi:', end-start)

save_to_file('berhasil', msg_sent)
save_to_file('gagal', msg_not_sent)