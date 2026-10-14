
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    name = request.form.get("name", "")
    age = request.form.get("age", "")
    gender = request.form.get("gender", "")
    temperature = request.form.get("temperature", "")
    heart_rate = request.form.get("heartRate", "")
    blood_pressure = request.form.get("bloodPressure", "")
    symptoms = request.form.get("symptoms", "")

    messages = []
    recommendations = []
        # Check that required fields are filled in
    if not name.strip() or not age.strip() or not gender.strip():
        messages.append("Please enter your name, age, and gender.")

    if not temperature.strip() or not heart_rate.strip() or not blood_pressure.strip():
        messages.append("Please enter your temperature, heart rate, and blood pressure.")

    if not symptoms.strip():
        messages.append("Please describe your symptoms.")

    # Stop assessment if required information is missing
    if messages:
        return render_template(
            "index.html",
            messages=messages,
            recommendations=recommendations
        )

    # 1. Temperature assessment
    try:
        temp = float(temperature)

        if temp >= 38:
            messages.append("Your temperature is elevated.")
            recommendations.append(
                "Rest, drink fluids if you can, and recheck your "
                "temperature. Seek medical advice if the fever persists "
                "or you feel worse."
            )
        elif temp < 35:
            messages.append("Your temperature is unusually low.")
            recommendations.append(
                "Recheck your temperature. If it remains low or you "
                "feel unwell, seek prompt medical advice."
            )
        else:
            messages.append(
                "Your temperature is within a typical range."
            )
            recommendations.append(
                "Continue your usual healthy habits and stay hydrated."
            )

    except (ValueError, TypeError):
        messages.append(
            "Temperature was not provided as a valid number."
        )
        recommendations.append(
            "Enter your temperature in degrees Celsius to assess it."
        )

    # 2. Heart-rate assessment
    try:
        heart = int(heart_rate)

        if heart <= 0:
            messages.append("Please check the heart-rate value entered.")
            recommendations.append(
                "Enter a valid heart rate in beats per minute."
            )
        elif heart > 100:
            messages.append(
                "Your heart rate is above the typical adult resting range."
            )
            recommendations.append(
                "Rest quietly and recheck your pulse. If it remains "
                "unusually high or you have concerning symptoms, contact "
                "a healthcare professional."
            )
        elif heart < 60:
            messages.append(
                "Your heart rate is below the typical adult resting range."
            )
            recommendations.append(
                "A low pulse can be normal for some people, including "
                "trained athletes. If this is unusual for you or you "
                "feel unwell, seek medical advice."
            )
        else:
            messages.append(
                "Your heart rate is within the typical adult resting range."
            )
            recommendations.append(
                "Measure your pulse while resting for a more meaningful "
                "comparison."
            )

    except (ValueError, TypeError):
        messages.append(
            "Heart rate was not provided as a valid number."
        )
        recommendations.append(
            "Enter your heart rate in beats per minute if available."
        )

    # 3. Symptom recommendations
    if symptoms.strip():
        recommendations.append(
            f"You reported these symptoms: {symptoms.strip()}. "
            "Monitor how you feel and consult a healthcare professional "
            "if symptoms persist, worsen, or concern you."
        )
    else:
        recommendations.append(
            "If you have symptoms, enter them in the symptoms field."
        )

    # 4. Blood-pressure reminder
    if blood_pressure.strip():
        recommendations.append(
            f"Your blood pressure entry is {blood_pressure.strip()}. "
            "This version does not automatically interpret blood pressure. "
            "Repeat unusual readings after resting and seek appropriate "
            "medical advice."
        )
    else:
        recommendations.append(
            "If available, enter blood pressure in the format used by "
            "your form, such as 120/80."
        )

    # 5. General safety reminder
    recommendations.append(
        "This tool provides general health information, not a diagnosis. "
        "Seek emergency help for severe breathing difficulty, chest pain, "
        "fainting, confusion, or other severe or sudden symptoms."
    )

    # Display results on the existing HTML page
    return render_template(
        "index.html",
        result=True,
        name=name,
        age=age,
        gender=gender,
        temperature=temperature,
        heart_rate=heart_rate,
        blood_pressure=blood_pressure,
        symptoms=symptoms,
        messages=messages,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
