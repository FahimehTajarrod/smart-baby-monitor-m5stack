# Smart Baby Monitor — وضعیت نهایی پروژه
**فهیمه تجرد | Prof. Oakes | IoT Course**
**آخرین آپدیت: جلسه نهایی**

---

## مشخصات پروژه
- دستگاه: M5Stack Core (Basic/Gray)
- محیط برنامه‌نویسی: UIFlow 1.15.3 (Blockly + Python execute)
- دو نسخه: با میکروفون و بدون میکروفون

---

## اتصال سخت‌افزار (نسخه بدون میکروفون)
- **Port A** — ENV III
- **Port B** — Angle sensor
- **Port C + Hub** — RGB Unit + PIR

## اتصال سخت‌افزار (نسخه با میکروفون)
- **Port A** — ENV III
- **Port B** — Microphone
- **Port C + Hub** — RGB Unit + PIR
- ⚠️ Angle sensor حذف شده

---

## ساختار حالت‌ها
| دکمه | حالت | عملکرد |
|---|---|---|
| A | Good Morning | حالت پایه — مانیتورینگ فعال |
| B | Good Night | Brahms lullaby + LED dance → بعد برمیگرده به Morning |
| C | Standby | همه labelها hide میشن |

---

## متغیرها
| نام | کاربرد | مقدار اولیه |
|---|---|---|
| `CurrentMode` | حالت فعلی | `"Morning"` |
| `Volume` | صدای speaker | `5` |
| `LastSyncTime` | زمان آخرین EZ-data sync | `0` |
| `LastAngle` | مقدار قبلی Angle sensor | `0` |
| `Temperature` | دمای فعلی | `'*C'` |
| `Humidity` | رطوبت فعلی | `'%'` |
| `Motion` | وضعیت motion | `'None'` |
| `IMU` | وضعیت IMU | `'Safe'` |
| `MotionFlag` | flag حرکت | `False` |

---

## UI — المان‌های نامگذاری شده (M5Stack)
| اسم | کاربرد |
|---|---|
| `lbl_status` | STATUS: SAFE/WARNING/ALERT |
| `circle_status` | دایره RGB وضعیت |
| `lbl_mode` | نام حالت فعلی |
| `lbl_temp` | مقدار دما |
| `lbl_humidity` | مقدار رطوبت |
| `lbl_motion` | وضعیت motion |
| `lbl_imu_tilt` | مقدار tilt |
| `lbl_imu_status` | STABLE / !! FALLEN !! |
| `lbl_sd` | SD: OK / ERR |
| `lbl_wifi` | WiFi: OK / ERR |
| `lbl_sync` | Last sync: زمان |

---

## Mobile Dashboard — Remote+ Widget ها
| اسم | نوع | کاربرد |
|---|---|---|
| `r_status` | Label | وضعیت (IMU متغیر) |
| `r_temp` | Label | دما |
| `r_humidity` | Label | رطوبت |
| `r_motion` | Label | motion |
| `r_imu` | Label | IMU tilt |
| `r_mode` | Label | حالت فعلی |
| `r_sync` | Label | زمان آخرین sync |
| `r_btn_morning` | Button | Morning mode |
| `r_btn_night` | Button | Night mode |
| `r_btn_standby` | Button | Standby mode |
| `r_volume` | Slider | volume |

---

## ساختار کد

### Setup:
1. WiFiInit
2. SDInit
3. Initialization
4. Safe()
5. EZsync()

### Loop:
```
if Angle تغییر کرد → Volume آپدیت
Speaker.volume = Volume
if ticks - LastSyncTime > 30000 → EZsync() + LogTelemetry()
if Standby → Standby()
else if Night → Night()
else → Morning()
wait 500ms
```

### EZsync فوری:
- Motion تشخیص داده شد
- دستگاه افتاد
- Mode عوض شد (button callbacks)

---

## RGB Logic
| وضعیت | رنگ | lbl_status |
|---|---|---|
| Safe | R:0 G:255 B:0 | STATUS: SAFE |
| Warning (دما>36 یا رطوبت>50) | R:255 G:165 B:0 | STATUS: WARNING!! |
| Alert (motion یا fallen) | R:255 G:0 B:0 | STATUS: ALERT! |

---

## Lullaby — Brahms (با LED dance)
12 نت با رنگ‌های آبی/بنفش متناسب — بعد LED خاموش

---

## وضعیت پیاده‌سازی ✅ همه موارد انجام شده:
- UI کامل با آیکون بچه
- WiFi + SD Card init و چک
- ENV III (دما و رطوبت)
- PIR (motion detection)
- IMU (tilt و fall detection)
- RGB status (Safe/Warning/Alert)
- Speaker (آلارم + Brahms lullaby)
- LED Bar (رقص نور Good Night)
- Angle sensor (volume — نسخه بدون میکروفون)
- EZ-data sync (30 ثانیه + فوری برای alert)
- SD Card logging (JSON + LOGS)
- Mobile Dashboard کامل
- Standby mode با hide/show

---

## مشکلات باز (جزئی)
1. خطاهای پراکنده WiFi — با try/except مدیریت میشه
2. WorldTimeAPI کار نکرد — ساعت --:-- مونده
3. Microphone — با Port B مستقیم کار نمیکنه (floating pin noise)

---

## پیام به استاد
- Microphone Unit در کیت استاندارد نبود و نسخه موجود با UIFlow سازگار نبود
- Angle sensor فقط مستقیم به Port B کار میکنه
- دو نسخه پروژه آماده شده: با و بدون میکروفون
