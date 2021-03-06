from dotenv import load_dotenv

load_dotenv()

from obschart import ObschartClient, ProgramTrackActionResponse
from .body_mass_index import get_info_text
import os
import matplotlib.pyplot as plt

token = os.environ["OBSCHART_APP_TOKEN"]
client = ObschartClient(token)

print("App server running...")


async def on_response(response: ProgramTrackActionResponse):
    unit = response._data["response"]["steps"][0]["fields"][1]

    if unit == "1":
        feedback = await response.set_feedback(
            "BMI Calculator",
            client.build_feedback_data()
            .add_number_field("Age", required=True, min=0, max=100)
            .add_number_field("Height (feet)", required=True, min=0, max=100, id="height_feet")
            .add_number_field("Height (inches)", required=True, min=0, max=100, id="height_inches")
            .add_number_field("Weight (pounds)", required=True, min=0, max=100, id="weight_pounds"),
        )

        feedback_response = await feedback.wait_for_response()
        values = feedback_response.values

        bmi = 703 * (
            float(values["weight_pounds"])
            / (float(values["height_feet"]) * 12 + float(values["height_inches"])) ** 2
        )
    else:
        feedback = await response.set_feedback_with_data(
            '{"type":"multiStep","steps":[{"name":"","action":{"type":"blocks","blocks":[{"type":"numberField","title":"Age","min":-9007199254740991,"max":9007199254740991,"step":1,"required":true},{"type":"multipleChoiceField","title":"Gender","choices":[{"title":"Male "},{"title":"Female"}],"required":true},{"type":"numberField","title":"Height in cm","min":-9007199254740991,"max":9007199254740991,"step":1,"required":true},{"type":"numberField","title":"Weight in kg","min":-9007199254740991,"max":9007199254740991,"step":1,"required":true}]}}]}'
        )

        feedback_response = await feedback.wait_for_response()

        response_fields = feedback_response.data["steps"][0]["fields"]

        bmi = float(response_fields[3]) / (float(response_fields[2]) / 100) ** 2

    bmi_rounded = round(bmi, 1)
    # REPLACE THIS WITH A BETTER CHART
    plt.plot(bmi_rounded, marker="o")
    figure = plt.gcf()
    image = await client.create_image(figure)

    bmi_info = get_info_text(bmi)
    feedback2 = await feedback_response.set_feedback(
        "BMI Calculator",
        client.build_feedback_data().add_text(
            "Your BMI is: " + str(bmi_rounded) + bmi_info + "\n![](" + image.url + ")"
        ),
    )

    response2 = await feedback2.wait_for_response()
    await response2.set_no_feedback()


client.on_response(on_response)
