import random
from sklearn.ensemble import RandomForestClassifier


def train_parking_model():

    X = []
    y = []

    # Generate demo training data
    for _ in range(500):

        hour = random.randint(8, 20)
        day = random.randint(0, 6)
        visitors = random.randint(0, 80)
        employees = random.randint(10, 200)
        previous_occupancy = random.randint(0, 100)

        occupancy = (
            visitors * 0.5
            + employees * 0.2
            + previous_occupancy * 0.4
            + (10 if 9 <= hour <= 11 else 0)
            + (15 if 17 <= hour <= 19 else 0)
        )

        busy = 1 if occupancy > 70 else 0

        X.append([
            hour,
            day,
            visitors,
            employees,
            previous_occupancy
        ])

        y.append(busy)

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_parking(
    hour,
    day,
    visitors,
    employees,
    previous_occupancy
):

    model = train_parking_model()

    prediction = model.predict([[
        hour,
        day,
        visitors,
        employees,
        previous_occupancy
    ]])[0]

    probability = model.predict_proba([[
        hour,
        day,
        visitors,
        employees,
        previous_occupancy
    ]])[0][1]

    if prediction == 1:
        status = "High Parking Demand"
        recommendation = "Parking demand is expected to be high. Consider arriving earlier."
    else:
        status = "Normal Parking Demand"
        recommendation = "Parking availability is expected to be normal."

    return {
        "status": status,
        "probability": round(probability * 100, 2),
        "recommendation": recommendation
    }