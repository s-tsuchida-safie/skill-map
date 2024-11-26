from Clinic import Clinic
from Patient import Patient


clinic = Clinic()
clinic.reserve(Patient('佐藤', '111', '咳'))
clinic.reserve(Patient('田中', '222', '腹痛'))
clinic.reserve(Patient('鈴木', '333', '鼻水'))
clinic.reserve(Patient('山田', '444', '倦怠感'))
clinic.reserve(Patient('土田', '555', '発熱'))
clinic.show_waiting_count()
clinic.reserve(Patient('鈴木', '333', '鼻水'))
clinic.diagnosis()
clinic.show_waiting_count()
clinic.diagnosis('555')
clinic.show_waiting_count()