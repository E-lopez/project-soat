from datetime import date

def calculate_days_between(start_date: date, end_date: date) -> int:
    return (end_date - start_date).days

def calculate_days_late(due_date: date, current_date: date = None) -> int:
    if current_date is None:
        current_date = date.today()
    days = calculate_days_between(due_date, current_date)
    return max(0, days)

def calculate_days_until(target_date: date, current_date: date = None) -> int:
    if current_date is None:
        current_date = date.today()
    return calculate_days_between(current_date, target_date)

def get_current_date_legal_format():
    days_es = {
        1: "primero", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
        6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
        11: "once", 12: "doce", 13: "trece", 14: "catorce", 15: "quince",
        16: "dieciséis", 17: "diecisiete", 18: "dieciocho", 19: "diecinueve", 20: "veinte",
        21: "veintiuno", 22: "veintidós", 23: "veintitrés", 24: "veinticuatro", 25: "veinticuyo",
        26: "veintiséis", 27: "veintisiete", 28: "veintiocho", 29: "veintinueve", 30: "treinta",
        31: "treinta y uno"
    }
    
    months_es = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
        7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    
    now = date.today()
    
    day_literal = days_es[now.day]
    month_literal = months_es[now.month]
    year = now.year
    
    return f"{day_literal} de {month_literal} de {year}"