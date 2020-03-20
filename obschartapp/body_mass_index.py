def get_info_text(bmi: float):
    standard_string = " According to the World Health Organisation (WHO) BMI values for adults indicates that you are within the following range: "
    category = ""
    if bmi < 16:
        category = "Severe Thinness < 16"
    elif bmi < 17:
        category = "Moderate Thinness 16 - 17"
    elif bmi < 18.5:
        category = "Mild Thinness 17 - 18.5"
    elif bmi < 25:
        category = "Normal 18.5 - 25"
    elif bmi < 30:
        category = "Overweight 25 - 30"
    elif bmi < 35:
        category = "Obese Class I 30 - 35"
    elif bmi < 40:
        category = "Obese Class II 35 - 40"
    else:
        category = "Obese Class III > 40"

    return standard_string + category
