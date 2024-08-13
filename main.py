import socket
import telebot

def scan_ports(domain, ports=[22, 80, 443, 137, 139, 445, 3389, 20, 21, 23, 25]):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((domain, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


API_TOKEN = 'YOUR_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['scan'])
def scan_command(message):
    domain = message.text.split()[1]
    bot.send_message(message.chat.id, f'Scanning domain: {domain}...')
    
    try:
        open_ports = scan_ports(domain)
        if open_ports:
            bot.send_message(message.chat.id, f'Open ports on {domain}: {", ".join(map(str, open_ports))}')
        else:
            bot.send_message(message.chat.id, f'No open ports found on {domain}.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Port Scan Bot!\nUse /scan <domain> to scan ports.")

bot.polling()



