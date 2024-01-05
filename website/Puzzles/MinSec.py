def Calcu(val):
    try:
        seconds = int(val)
    except:
        return "Invalid"
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"