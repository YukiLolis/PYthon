#pip install pyttsx3
import speech_recognition as sr
import json
import os

scheduled_event_file = "scheduled_events.json"

def load_scheduled_events():
    if os.path.exists(scheduled_event_file):
        try:
            with open(scheduled_event_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                events = []
                for item in data:
                    event_time = datetime.strptime(item["event_time"], "%Y-%m-%d %H:%M:%S")
                    event_description = item["event_description"]
                    events.append((event_time, event_description))
                return events
        except Exception as e:
            print(f"Lỗi khi tải lịch sự kiện: {e}")
            return []
    else:
        return []

def save_scheduled_events():
    try:
        data = []
        for event_time, event_description in scheduled_event:
            data.append({
                "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                "event_description": event_description
            })
        with open(scheduled_event_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu lịch sự kiện: {e}")

scheduled_event = load_scheduled_events()

import pyttsx3
import serial
import requests
from datetime import datetime
import threading
import time

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def configure_voice():
    try:
        voices = engine.getProperty('voices')
        vietnamese_voice_found = False
        print("Available voices:")
        for voice in voices:
            print(f"Voice ID: {voice.id}, Name: {voice.name}, Languages: {voice.languages}")
            # Try to find Vietnamese voice by name or id or languages
            if ('vietnamese' in voice.name.lower() or 'vi' in voice.name.lower() or 'vn' in voice.name.lower()) or \
               any('vi' in lang.decode('utf-8').lower() if isinstance(lang, bytes) else 'vi' in lang.lower() for lang in voice.languages):
                engine.setProperty('voice', voice.id)
                vietnamese_voice_found = True
                print(f"Vietnamese voice selected: {voice.name}")
                break
        
        if not vietnamese_voice_found:
            print("Vietnamese voice not found, using default voice.")
        
        # Set rate and volume
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 0.9)
        
    except Exception as e:
        print(f"Lỗi cấu hình giọng đọc: {e}")

# Gọi hàm cấu hình khi khởi động
configure_voice()

def speak_text(text):
    """Hàm đọc tiếng Việt"""
    try:
        if not isinstance(text, str):
            text = str(text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Lỗi phát âm: {str(e)}")

def setup_serial_connection(port='COM3', baudrate=9600):
    """Set up serial connection with Arduino."""
    try:
        ser = serial.Serial(port, baudrate)
        time.sleep(2)
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to serial port: {e}")
        return None

def get_weather_by_voice(source):
    """Get weather for city from voice input"""
    speak_text("Bạn muốn xem thời tiết ở thành phố nào?")
    
    
    try:
        print("Đang nghe tên thành phố...")
        city_audio = recognizer.listen(source, timeout=10)
        city = recognizer.recognize_google(city_audio, language="vi-VN")
        print(f"Đã nhận diện thành phố: {city}")
        return get_weather(city)
    except sr.UnknownValueError:
        return "Xin lỗi, tôi không nghe rõ tên thành phố"
    except sr.RequestError as e:
        return f"Lỗi kết nối dịch vụ nhận diện giọng nói: {e}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

def get_weather(city):
    """Fetch the current weather from OpenWeatherMap API."""
    api_key = "a3e670ab8298b8320c68c28054cae417"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=vi"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind = data['wind']['speed']
            
            return (f"Thời tiết tại {city}:\n"
                    f"- Trạng thái: {description}\n"
                    f"- Nhiệt độ: {temp}°C\n"
                    f"- Độ ẩm: {humidity}%\n"
                    f"- Gió: {wind} m/s")
        else:
            return f"Không tìm thấy thông tin thời tiết cho {city}"
    except Exception as e:
        return f"Lỗi khi lấy thông tin thời tiết: {str(e)}"

def schedule_event(event_time, event_description):
    """Schedule an event."""
    scheduled_event.append((event_time, event_description))
    save_scheduled_events()
    print(f"Scheduled event: {event_description} at {event_time}")
    return f"Đã lên lịch sự kiện {event_description} vào {event_time.strftime('%d/%m %H:%M')}"

def month_to_number(month_name):
    """Convert month name to its corresponding number."""
    months = {
         "tháng 1": 1, "tháng một": 1, "tháng 01": 1,
        "tháng 2": 2, "tháng hai": 2, "tháng 02": 2,
        "tháng 3": 3, "tháng ba": 3, "tháng 03": 3,
        "tháng 4": 4, "tháng tư": 4, "tháng 04": 4,
        "tháng 5": 5, "tháng năm": 5, "tháng 05": 5,
        "tháng 6": 6, "tháng sáu": 6, "tháng 06": 6,
        "tháng 7": 7, "tháng bảy": 7, "tháng 07": 7,
        "tháng 8": 8, "tháng tám": 8, "tháng 08": 8,
        "tháng 9": 9, "tháng chín": 9, "tháng 09": 9,
        "tháng 10": 10, "tháng mười": 10,
        "tháng 11": 11, "tháng mười một": 11,
        "tháng 12": 12, "tháng mười hai": 12
    }
    return months.get(month_name.lower().strip(), None)

def notify_events():
    """Check for upcoming scheduled events and notify the user."""
    while True:
        current_time = datetime.now()
        for event in scheduled_event[:]:
            event_time, event_description = event
            if current_time >= event_time:
                # Alarm notification
                speak_text(f"Chuông báo: Sự kiện {event_description} đã đến giờ.")
                print(f"Sự kiện: {event_description} đã đến giờ.")
                scheduled_event.remove(event)
                save_scheduled_events()
        time.sleep(30)

def process_schedule_command(text, source):
    """Handle the scheduling process."""
    try:
        speak_text("Vui lòng cho biết tên sự kiện.")
        
        print("Vui lòng cho biết tên sự kiện.")
        event_audio = recognizer.listen(source, timeout=15)
        event_description = recognizer.recognize_google(event_audio, language="vi-VN")
        
        speak_text("Vui lòng cho biết ngày, tháng, giờ và phút của sự kiện theo định dạng 'ngày 25 tháng 12 lúc 14 giờ 30 phút'.")
        
        print("Vui lòng cho biết ngày, tháng, giờ và phút của sự kiện theo ví dụ 'ngày 25 tháng 12 lúc 14 giờ 30 phút'.")
        date_audio = recognizer.listen(source, timeout=15, phrase_time_limit=20)
        event_date_str = recognizer.recognize_google(date_audio, language="vi-VN")
        print(event_date_str)
        
        event_date_str_lower = event_date_str.lower()
        
        # Retry if input incomplete or missing keywords
        if "ngày" not in event_date_str_lower or "tháng" not in event_date_str_lower or "lúc" not in event_date_str_lower:
            speak_text("Vui lòng nói lại theo định dạng 'ngày X tháng Y lúc H giờ M phút'")
            print("Vui lòng nói lại theo định dạng 'ngày X tháng Y lúc H giờ M phút'")
            date_audio = recognizer.listen(source, timeout=30, phrase_time_limit=30)
            event_date_str = recognizer.recognize_google(date_audio, language="vi-VN")
            print(event_date_str)
            event_date_str_lower = event_date_str.lower()
            if "ngày" not in event_date_str_lower or "tháng" not in event_date_str_lower or "lúc" not in event_date_str_lower:
                return "Lỗi: Vui lòng nói theo định dạng 'ngày X tháng Y lúc H giờ M phút'"
        
        # Parse day
        try:
            day_part = event_date_str_lower.split("ngày")[1].split("tháng")[0].strip()
            day = int(day_part)
        except Exception:
            return "Lỗi: Không nhận diện được ngày"
        
        # Parse month
        try:
            month_part = event_date_str_lower.split("tháng")[1].split("lúc")[0].strip()
            month_number = month_to_number("tháng " + month_part)
            if not month_number:
                return "Lỗi: Không nhận diện được tháng"
        except Exception:
            return "Lỗi: Không nhận diện được tháng"
        
        # Parse hour and minute
        try:
            time_part = event_date_str_lower.split("lúc")[1].strip()
            if "giờ" in time_part:
                hour = int(time_part.split("giờ")[0].strip())
                if "phút" in time_part:
                    minute = int(time_part.split("giờ")[1].split("phút")[0].strip())
                else:
                    minute = 0
            else:
                # Try to parse hour as first number in time_part if "giờ" missing
                import re
                numbers = re.findall(r'\d+', time_part)
                if numbers:
                    hour = int(numbers[0])
                    minute = int(numbers[1]) if len(numbers) > 1 else 0
                else:
                    return "Lỗi: Vui lòng nói giờ theo định dạng 'lúc H giờ' hoặc 'lúc H giờ M phút'"
        except Exception:
            return "Lỗi: Không nhận diện được giờ và phút"
        
        current_year = datetime.now().year
        event_time = datetime.strptime(f"{day}/{month_number}/{current_year} {hour}:{minute}", "%d/%m/%Y %H:%M")
        
        response = schedule_event(event_time, event_description)
        return response
        
    except Exception as e:
        return f"Lỗi khi lập lịch: {str(e)}"

def listen_and_recognize(ser):
    while True:
        with sr.Microphone() as source:
            print("Hãy nói gì đó...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                try:
                    text = recognizer.recognize_google(audio, language="vi-VN")
                    print("Bạn đã nói: " + text)
                    
                    # Process commands
                    if any(cmd in text.lower() for cmd in ["bật đèn phòng khách", "mở đèn phòng khách", "cho đèn phòng khách sáng lên"]):
                        response = "Đèn phòng khách đã được bật."
                        if ser: ser.write(b'1')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn phòng khách", "đèn phòng khách tắt đi", "cho đèn phòng khách tắt"]):
                        response = "Đèn phòng khách đã được tắt."
                        if ser: ser.write(b'0')

                    # Thêm các lệnh mới cho đèn
                    elif any(cmd in text.lower() for cmd in ["bật đèn phòng tắm", "mở đèn phòng tắm"]):
                        response = "Đèn phòng tắm đã được bật."
                        if ser: ser.write(b'2')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn phòng tắm", "đèn phòng tắm tắt đi"]):
                        response = "Đèn phòng tắm đã được tắt."
                        if ser: ser.write(b'3')

                    elif any(cmd in text.lower() for cmd in ["bật đèn phòng ăn", "mở đèn phòng ăn"]):
                        response = "Đèn phòng ăn đã được bật."
                        if ser: ser.write(b'4')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn phòng ăn", "đèn phòng ăn tắt đi"]):
                        response = "Đèn phòng ăn đã được tắt."
                        if ser: ser.write(b'5')

                    elif any(cmd in text.lower() for cmd in ["bật đèn gác máy", "mở đèn gác máy"]):
                        response = "Đèn gác máy đã được bật."
                        if ser: ser.write(b'6')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn gác máy", "đèn gác máy tắt đi"]):
                        response = "Đèn gác máy đã được tắt."
                        if ser: ser.write(b'7')

                    elif any(cmd in text.lower() for cmd in ["bật đèn phòng ngủ 1", "mở đèn phòng ngủ 1"]):
                        response = "Đèn phòng ngủ 1 đã được bật."
                        if ser: ser.write(b'8')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn phòng ngủ 1", "đèn phòng ngủ 1 tắt đi"]):
                        response = "Đèn phòng ngủ 1 đã được tắt."
                        if ser: ser.write(b'9')

                    elif any(cmd in text.lower() for cmd in ["bật đèn phòng ngủ 2", "mở đèn phòng ngủ 2"]):
                        response = "Đèn phòng ngủ 2 đã được bật."
                        if ser: ser.write(b'a')
                    elif any(cmd in text.lower() for cmd in ["tắt đèn phòng ngủ 2", "đèn phòng ngủ 2 tắt đi"]):
                        response = "Đèn phòng ngủ 2 đã được tắt."
                        if ser: ser.write(b'b')

                    # Điều khiển quạt
                    elif any(cmd in text.lower() for cmd in ["bật quạt phòng khách", "mở quạt phòng khách"]):
                        response = "Quạt phòng khách đã được bật."
                        if ser: ser.write(b'c')
                    elif any(cmd in text.lower() for cmd in ["tắt quạt phòng khách", "quạt phòng khách tắt đi"]):
                        response = "Quạt phòng khách đã được tắt."
                        if ser: ser.write(b'd')

                    elif any(cmd in text.lower() for cmd in ["bật quạt phòng ngủ 1", "mở quạt phòng ngủ 1"]):
                        response = "Quạt phòng ngủ 1 đã được bật."
                        if ser: ser.write(b'e')
                    elif any(cmd in text.lower() for cmd in ["tắt quạt phòng ngủ 1", "quạt phòng ngủ 1 tắt đi"]):
                        response = "Quạt phòng ngủ 1 đã được tắt."
                        if ser: ser.write(b'f')

                    elif any(cmd in text.lower() for cmd in ["bật quạt phòng ngủ 2", "mở quạt phòng ngủ 2"]):
                        response = "Quạt phòng ngủ 2 đã được bật."
                        if ser: ser.write(b'g')
                    elif any(cmd in text.lower() for cmd in ["tắt quạt phòng ngủ 2", "quạt phòng ngủ 2 tắt đi"]):
                        response = "Quạt phòng ngủ 2 đã được tắt."
                        if ser: ser.write(b'h')
                    
                    
                    elif "bây giờ là mấy giờ" in text.lower():
                        current_time = datetime.now().strftime("%H:%M")
                        response = f"Bây giờ là {current_time}."
                        
                    elif "thời tiết" in text.lower():
                        if "ở" in text.lower():
                            city = text.lower().split("ở")[-1].strip()
                            response = get_weather(city)
                        else:
                            response = get_weather_by_voice(source)
                            
                    elif "lập lịch" in text.lower() or "schedule" in text.lower():
                        response = process_schedule_command(text, source)

                    elif "bye" in text.lower() or "chào tạm biệt" in text.lower() or "tạm biệt" in text.lower():
                        response = "Tạm biệt!"
                        print(response)
                        break
                    else:
                        response = "Tôi không hiểu yêu cầu của bạn"
                       
                    print(response)
                    speak_text(response)
                    
                    
                except sr.UnknownValueError:
                    print("Không thể nhận diện giọng nói")
                except sr.RequestError as e:
                    print(f"Lỗi kết nối đến dịch vụ nhận diện giọng nói; {e}")
                    
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    ser = setup_serial_connection()
    threading.Thread(target=notify_events, daemon=True).start()
    listen_and_recognize(ser)
