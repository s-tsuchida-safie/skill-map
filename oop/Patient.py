from Human import Human


class Patient(Human):
    def __init__(self, name, patiend_id, symptom):
        super().__init__(name)
        # 症状
        self.patient_id = patiend_id
        # 診察番号
        self.symptom = symptom
