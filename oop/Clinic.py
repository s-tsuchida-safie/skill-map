from Patient import Patient


class Clinic:
    def __init__(self):
        # 患者リスト
        self.patients_list: list[Patient] = []

    # 待ち人数表示
    def show_waiting_count(self):
        print(f"待ち人数は{len(self.patients_list)}人です。")

    # 予約
    def reserve(self, patient: Patient):
        if self._check_reserved(patient):
            print(f"{patient.name}さんはすでに予約済みです。")
        else:
            print(f"{patient.name}さん予約完了")
            # 患者リストpatients_listにpatientを追加
            self.patients_list.append(patient)

    def diagnosis(self, patient_id=None):
        # 患者指定なしの場合順番に
        patient: Patient | None = None
        if patient_id == None:
            if len(self.patients_list) > 0:
                patient = self.patients_list[0]
        else:
            for p in self.patients_list:
                if p.patient_id == patient_id:
                    patient = p
        if patient is None:
            print("診察する患者さんがいません")
        else:
            print(f"{patient.name}さん、{patient.symptom}ですね。")
            print(f"診察終わりました。お大事に。")
            for i, patient_item in enumerate(self.patients_list):
                if patient_item.patient_id == patient.patient_id:
                    self.patients_list.pop(i)
                    break

    def _check_reserved(self, patient: Patient) -> bool:
        for patient_item in self.patients_list:
            if patient_item.patient_id == patient.patient_id:
                return True
        return False
