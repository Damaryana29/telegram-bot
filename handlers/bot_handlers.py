import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config.config import BOT_TOKEN
from utils.sheets_handler import get_sheet, update_spreadsheet_id, SPREADSHEET_ID
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)

def send_welcome(message):
    chat_id = message.chat.id
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Mulai Input Data"), KeyboardButton("📝 Ubah Spreadsheet ID"))
    markup.add(KeyboardButton("📊 Lihat Data Terakhir"))
    bot.send_message(chat_id, "Halo! Pilih opsi di bawah:", reply_markup=markup)
    if not SPREADSHEET_ID:
        bot.send_message(chat_id, "⚠️ ID Spreadsheet belum diset. Kirimkan ID sekarang:")
        bot.register_next_step_handler(message, change_spreadsheet_id)

@bot.message_handler(commands=['start'])
def start_command(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text == "📝 Ubah Spreadsheet ID")
def ask_for_spreadsheet_id(message):
    bot.send_message(message.chat.id, "Kirimkan ID Spreadsheet yang baru:")
    bot.register_next_step_handler(message, change_spreadsheet_id)

def change_spreadsheet_id(message):
    global SPREADSHEET_ID
    try:
        new_id = message.text.strip()
        SPREADSHEET_ID = new_id
        update_spreadsheet_id(new_id)
        bot.send_message(message.chat.id, "✅ Spreadsheet ID berhasil diperbarui!")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Gagal mengubah Spreadsheet ID: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "🚀 Mulai Input Data")
def ask_for_data(message):
    if not SPREADSHEET_ID:
        bot.send_message(message.chat.id, "⚠️ ID Spreadsheet belum diset. Kirimkan ID dulu!")
        return
    bot.send_message(message.chat.id, "Kirim data dalam format: Colagold, Colagold Closing, Flamora, Flamora Closing\nContoh: 10,5,7,3")

def handle_message(message):
    if not SPREADSHEET_ID:
        bot.send_message(message.chat.id, "⚠️ ID Spreadsheet belum diset. Kirimkan ID dulu!")
        return
    try:
        sheet = get_sheet()
        data = message.text.split(',')
        if len(data) != 4:
            bot.reply_to(message, "⚠️ Format salah! Gunakan format: 10,5,7,3")
            return
        tanggal = datetime.now().strftime("%Y-%m-%d")
        colagold, colagold_closing, flamora, flamora_closing = map(int, map(str.strip, data))
        existing_data = sheet.get("A12:E12")
        if existing_data and existing_data[0]:
            old_data = existing_data[0]
            old_tanggal = old_data[0] if len(old_data) > 0 else ""
            old_values = list(map(lambda x: int(x) if x else 0, old_data[1:]))
            if old_tanggal == tanggal:
                new_values = [old_values[i] + [colagold, colagold_closing, flamora, flamora_closing][i] for i in range(4)]
            else:
                new_values = [colagold, colagold_closing, flamora, flamora_closing]
        else:
            new_values = [colagold, colagold_closing, flamora, flamora_closing]
        sheet.update("A12:E12", [[tanggal] + new_values])
        bot.reply_to(message, "✅ Data berhasil disimpan!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Terjadi kesalahan: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "📊 Lihat Data Terakhir")
def lihat_data_terakhir(message):
    try:
        sheet = get_sheet()
        data = sheet.get("A12:E12")
        if data and data[0]:
            tanggal, colagold, colagold_closing, flamora, flamora_closing = data[0]
            response = (f"📅 Tanggal: {tanggal}\n"
                        f"🥤 Colagold: {colagold}\n"
                        f"🔻 Colagold Closing: {colagold_closing}\n"
                        f"🍷 Flamora: {flamora}\n"
                        f"🔻 Flamora Closing: {flamora_closing}")
        else:
            response = "⚠️ Belum ada data yang tersimpan."
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Gagal mengambil data: {str(e)}")

@bot.message_handler(func=lambda message: True)
def general_handler(message):
    handle_message(message)
